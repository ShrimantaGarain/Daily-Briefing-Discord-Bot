import discord
from discord.ext import commands
import aiohttp
import os
import logging
from datetime import datetime, timezone, timedelta, time
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import asyncio

# --- INITIAL SETUP ---
load_dotenv()
logging.basicConfig(level=logging.INFO)

REQUIRED_KEYS = [
    "DISCORD_BOT_TOKEN",
    "GNEWS_API_KEY",
    "OPENWEATHER_API_KEY",
    "VISUALCROSSING_API_KEY",
    "PEXELS_API_KEY",
]

for key in REQUIRED_KEYS:
    if not os.getenv(key):
        raise RuntimeError(f"❌ Missing required environment variable: {key}")

CONFIG = {
    "DISCORD_TOKEN": os.getenv("DISCORD_BOT_TOKEN"),
    "GNEWS_KEY": os.getenv("GNEWS_API_KEY"),
    "OPENWEATHER_KEY": os.getenv("OPENWEATHER_API_KEY"),
    "VISUAL_KEY": os.getenv("VISUALCROSSING_API_KEY"),
    "PEXELS_KEY": os.getenv("PEXELS_API_KEY"),
    "AUTO_CHANNEL_ID": os.getenv("AUTO_CHANNEL_ID"),  # Optional: Set this env var to the channel ID for auto-posts
    "LOCATION": {"lat": 22.5726, "lon": 88.3639, "city": "Kolkata"},
    "THEME_COLOR": 0x2F3136,
    "TIMEZONE": ZoneInfo("Asia/Kolkata"),
}

intents = discord.Intents.default()
intents.message_content = True


class DailyBriefingBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents, help_command=None)
        self.session = None

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        await self.add_cog(Briefing(self))

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
            await super().close()

    async def on_ready(self):
        logging.info(f"✅ Logged in as {self.user}")


class Briefing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = None
        self._image_cache = {}
        self.scheduled_hours = [7, 13, 18, 22]  # 7am, 1pm, 6pm, 10pm
        self.timezone = CONFIG["TIMEZONE"]
        self.scheduler_started = False
        self.bg_task = None

    # ---------- HELPERS ----------

    async def fetch_json(self, url, headers=None):
        async with self.bot.session.get(url, headers=headers, timeout=15) as resp:
            if resp.status != 200:
                logging.warning(f"API error {resp.status}: {url}")
                return None
            return await resp.json()

    def trim_embed_value(self, text: str, limit: int = 1024) -> str:
        if len(text) <= limit:
            return text
        return text[: limit - 4] + " …"

    # ---------- NEWS ----------

    async def get_news(self, query, limit=4):
        url = (
            "https://gnews.io/api/v4/search"
            f"?q={query}&lang=en&country=in&max={limit}&apikey={CONFIG['GNEWS_KEY']}"
        )
        data = await self.fetch_json(url)
        return data.get("articles", []) if data else []

    # ---------- WEATHER ----------

    async def get_current_weather(self):
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?lat={CONFIG['LOCATION']['lat']}"
            f"&lon={CONFIG['LOCATION']['lon']}"
            f"&appid={CONFIG['OPENWEATHER_KEY']}&units=metric"
        )
        return await self.fetch_json(url)

    async def get_historical_weather(self):
        today = datetime.now(CONFIG["TIMEZONE"])
        last_year = today.replace(year=today.year - 1).strftime("%Y-%m-%d")
        url = (
            "https://weather.visualcrossing.com/VisualCrossingWebServices/"
            f"rest/services/timeline/{CONFIG['LOCATION']['city']}/"
            f"{last_year}/{last_year}"
            f"?unitGroup=metric&key={CONFIG['VISUAL_KEY']}&contentType=json"
        )
        data = await self.fetch_json(url)
        return data["days"][0] if data and data.get("days") else None

    # ---------- WEATHER IMAGE LOGIC ----------

    def get_season(self):
        month = datetime.now(CONFIG["TIMEZONE"]).month
        if month in (3, 4, 5):
            return "summer"
        if month in (6, 7, 8, 9):
            return "monsoon"
        if month in (10, 11):
            return "autumn"
        return "winter"

    def map_weather_to_image_query(self, weather_id: int, is_night: bool):
        time = "night city" if is_night else "day city"
        season = self.get_season()

        if 200 <= weather_id < 300:
            return f"thunderstorm {time} dramatic clouds"
        if 300 <= weather_id < 600:
            return f"rainy {time} street monsoon"
        if 600 <= weather_id < 700:
            return f"snow {time}"
        if 700 <= weather_id < 800:
            return f"foggy {time} morning"
        if weather_id == 800:
            return f"clear sky {time} skyline"
        if 801 <= weather_id <= 804:
            return f"cloudy {time} skyline"
        return f"{season} {time}"

    async def get_pexels_image(self, query):
        if query in self._image_cache:
            return self._image_cache[query]

        headers = {"Authorization": CONFIG["PEXELS_KEY"]}
        url = (
            "https://api.pexels.com/v1/search"
            f"?query=Kolkata {query}&per_page=1&orientation=landscape"
        )
        data = await self.fetch_json(url, headers=headers)
        image = (
            data["photos"][0]["src"]["large2x"]
            if data and data.get("photos")
            else "https://images.unsplash.com/photo-1558431382-27e3031422e6"
        )
        self._image_cache[query] = image
        return image

    # ---------- EMBEDS ----------

    async def build_news_embed(self):
        now = datetime.now(CONFIG["TIMEZONE"])
        embed = discord.Embed(
            title=f"📰 The NSG Chronicle • {now:%d %B %Y}",
            description="*Top headlines*",
            color=CONFIG["THEME_COLOR"],
        )

        national = await self.get_news("India", 4)
        local = await self.get_news('Kolkata OR "West Bengal"', 4)

        def format_articles(articles):
            if not articles:
                return "_No articles available._"
            lines = []
            for art in articles:
                title = art.get("title", "Untitled")
                url = art.get("url", "#")
                lines.append(f"[:newspaper2:]({url}) {title}")
            combined = "\n".join(lines)
            return self.trim_embed_value(combined)

        embed.add_field(
            name="🇮🇳 National Updates",
            value="\n" + format_articles(national),
            inline=False,
        )

        embed.add_field(
            name="🌸 Bengal & Kolkata",
            value="\n" + format_articles(local),
            inline=False,
        )

        thumb = (
            (local[0].get("image") if local else None)
            or (national[0].get("image") if national else None)
        )
        if thumb:
            embed.set_thumbnail(url=thumb)

        return embed

    async def build_weather_embed(self):
        curr = await self.get_current_weather()
        past = await self.get_historical_weather()
        if not curr:
            return None

        weather = curr["weather"][0]
        temp = round(curr["main"]["temp"])
        feels = round(curr["main"]["feels_like"])
        humid = curr["main"]["humidity"]
        wind = curr["wind"]["speed"]
        vis = curr.get("visibility")
        visibility = f"{vis // 1000} km" if vis else "N/A"

        is_night = weather["icon"].endswith("n")
        image_query = self.map_weather_to_image_query(weather["id"], is_night)

        color = 0x3498DB if temp < 20 else 0xE67E22 if temp < 30 else 0xE74C3C

        embed = discord.Embed(
            title=f"🌤️ Weather in {CONFIG['LOCATION']['city']}",
            description=f"**{weather['description'].capitalize()}**",
            color=color,
            timestamp=datetime.now(timezone.utc),
        )

        embed.add_field(name="🌡️ Temp", value=f"{temp}°C", inline=True)
        embed.add_field(name="🤔 Feels", value=f"{feels}°C", inline=True)
        embed.add_field(name="💧 Humidity", value=f"{humid}%", inline=True)
        embed.add_field(name="💨 Wind", value=f"{wind} m/s", inline=True)
        embed.add_field(name="👁️ Visibility", value=visibility, inline=True)
        embed.add_field(name="📍 Location", value="Kolkata", inline=True)

        if past:
            p_temp = round(past.get("temp", temp))
            diff = temp - p_temp
            trend = "warmer 📈" if diff > 0 else "cooler 📉"
            embed.add_field(
                name="📅 Year-on-Year",
                value=f"Last year: {p_temp}°C • Today {abs(diff)}°C {trend}",
                inline=False,
            )

        embed.set_thumbnail(
            url=f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
        )
        embed.set_image(url=await self.get_pexels_image(image_query))
        embed.set_footer(text="Dynamic weather visuals • OpenWeather • Pexels")

        return embed

    # ---------- SCHEDULER ----------

    async def auto_post_loop(self):
        channel_id = CONFIG.get("AUTO_CHANNEL_ID")
        if not channel_id:
            logging.warning("AUTO_CHANNEL_ID not set in environment variables. Auto-posting disabled.")
            return

        channel = self.bot.get_channel(int(channel_id))
        if not channel:
            logging.warning(f"Could not find channel with ID {channel_id}. Auto-posting disabled.")
            return

        await self.bot.wait_until_ready()
        logging.info("Starting auto-post scheduler.")

        while not self.bot.is_closed():
            now = datetime.now(self.timezone)
            today = now.date()
            next_time = None

            for h in self.scheduled_hours:
                dt = datetime.combine(today, time(hour=h, minute=0, second=0), tzinfo=self.timezone)
                if dt > now:
                    next_time = dt
                    break

            if next_time is None:
                next_day = today + timedelta(days=1)
                next_time = datetime.combine(next_day, time(hour=self.scheduled_hours[0], minute=0, second=0), tzinfo=self.timezone)

            sleep_duration = (next_time - now).total_seconds()
            await asyncio.sleep(sleep_duration)

            # Post the briefing
            try:
                async with channel.typing():
                    news_embed = await self.build_news_embed()
                    await channel.send(embed=news_embed)
                    weather_embed = await self.build_weather_embed()
                    if weather_embed:
                        await channel.send(embed=weather_embed)
                logging.info(f"Auto-posted daily briefing at {next_time}")
            except Exception as e:
                logging.error(f"Error during auto-post: {e}")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.scheduler_started:
            self.scheduler_started = True
            self.bg_task = self.bot.loop.create_task(self.auto_post_loop())

    def cog_unload(self):
        if self.bg_task:
            self.bg_task.cancel()

    # ---------- COMMANDS ----------

    @commands.command(name="dailynews")
    async def dailynews(self, ctx):
        async with ctx.typing():
            await ctx.send(embed=await self.build_news_embed())
            weather = await self.build_weather_embed()
            if weather:
                await ctx.send(embed=weather)

    @commands.command(name="test")
    async def test(self, ctx):
        await ctx.message.add_reaction("🧪")
        await self.dailynews(ctx)


# ---------- START ----------
bot = DailyBriefingBot()
bot.run(CONFIG["DISCORD_TOKEN"])