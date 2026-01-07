📰 Daily Briefing Discord Bot

A production-ready Discord bot that delivers daily news headlines and weather briefings with rich embeds, auto-scheduling, and dynamic weather visuals—optimized for Indian audiences 🇮🇳.

🚀 Features
🗞️ News Briefing

🇮🇳 National headlines (India)

🌸 Local news (Kolkata & West Bengal)

Clean, clickable embeds

Powered by GNews API

🌦️ Weather Intelligence

Current temperature & “feels like”

Humidity, wind speed, visibility

Year-on-year weather comparison

Powered by OpenWeather & Visual Crossing

🖼️ Smart Weather Visuals

Context-aware images based on:

Weather conditions

Day/Night

Seasonal logic (Summer, Monsoon, Winter)

Powered by Pexels API

⏰ Automation

Auto-posts at:

07:00

13:00

18:00

22:00 (IST)

Timezone-aware scheduling

🛠️ Tech Stack
Category	Tools
Language	Python 3.10+
Discord	discord.py
Networking	aiohttp
Config	python-dotenv
APIs	GNews, OpenWeather, Visual Crossing, Pexels
📁 Project Structure
.
├── main.py          # Discord bot entry point
├── .env             # Environment variables (ignored)
├── README.md        # Documentation

⚙️ Environment Variables

Create a .env file in the root directory:

DISCORD_BOT_TOKEN=your_discord_bot_token
GNEWS_API_KEY=your_gnews_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
VISUALCROSSING_API_KEY=your_visualcrossing_api_key
PEXELS_API_KEY=your_pexels_api_key
AUTO_CHANNEL_ID=your_channel_id   # Optional (auto-posting)


❗ The bot will fail fast if required variables are missing.

📦 Installation
1️⃣ Clone the Repository
git clone https://github.com/yourusername/daily-briefing-discord-bot.git
cd daily-briefing-discord-bot

2️⃣ Install Dependencies
pip install discord.py aiohttp python-dotenv

3️⃣ Run the Bot
python main.py

🤖 Bot Commands
Command	Description
!dailynews	Sends latest news & weather
!test	Runs a test briefing
🌍 Default Configuration

City: Kolkata

Timezone: Asia/Kolkata (IST)

These values can be modified in the CONFIG section of main.py.

🔐 Security Best Practices

Never commit .env

Rotate API keys periodically

Use environment variables in production

Restrict Discord bot permissions

📜 License

This project is licensed under the MIT License.

🌟 Acknowledgements

Discord.py

OpenWeather

Visual Crossing

GNews

Pexels

🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to fork and submit a PR 🚀
