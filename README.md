# 📰 Daily Briefing Discord Bot

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Discord](https://img.shields.io/badge/discord-bot-5865F2)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![Contributions](https://img.shields.io/badge/contributions-welcome-orange)

A **production-ready Discord bot** that delivers **daily news and weather briefings** with rich embeds, smart scheduling, and dynamic weather visuals—optimized for Indian audiences 🇮🇳.

---

## ✨ Features

### 🗞️ News Updates
- 🇮🇳 National headlines (India)
- 🌸 Local news (Kolkata & West Bengal)
- Clean, clickable Discord embeds
- Powered by **GNews API**

### 🌦️ Weather Briefing
- Current temperature & “feels like”
- Humidity, wind speed, visibility
- Year-on-year comparison
- Powered by **OpenWeather** & **Visual Crossing**

### 🖼️ Dynamic Weather Images
- Context-aware visuals based on:
  - Weather condition
  - Day/Night
  - Season (Summer, Monsoon, Winter)
- Powered by **Pexels API**

### ⏰ Auto Posting
- Scheduled updates at:
  - **07:00**
  - **13:00**
  - **18:00**
  - **22:00** (IST)
- Fully timezone-aware

---

## 🛠️ Tech Stack

| Category | Tools |
|-------|------|
| Language | Python 3.10+ |
| Discord | discord.py |
| HTTP | aiohttp |
| Config | python-dotenv |
| APIs | GNews, OpenWeather, Visual Crossing, Pexels |

---

## 📁 Project Structure

├── main.py # Discord bot source code
├── .env # Environment variables (not committed)
├── README.md # Documentation


---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token
GNEWS_API_KEY=your_gnews_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
VISUALCROSSING_API_KEY=your_visualcrossing_api_key
PEXELS_API_KEY=your_pexels_api_key
AUTO_CHANNEL_ID=your_channel_id   # Optional (for auto-posting)
⚠️ The bot will not start if required environment variables are missing.

🚀 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/yourusername/daily-briefing-discord-bot.git
cd daily-briefing-discord-bot

2️⃣ Install Dependencies
pip install discord.py aiohttp python-dotenv

3️⃣ Run the Bot
python main.py

🤖 Bot Commands
Command	Description
!dailynews	Sends news & weather briefing
!test	Test command
🌍 Default Settings

City: Kolkata

Timezone: Asia/Kolkata (IST)

You can modify these values in the CONFIG section of main.py.

🔐 Security Notes

Never commit your .env file

Rotate API keys regularly

Limit Discord bot permissions

Use environment variables in production

📜 License

This project is licensed under the MIT License.

🙌 Acknowledgements

Discord.py

OpenWeather

Visual Crossing

GNews

Pexels

🤝 Contributing

Contributions, issues, and feature requests are welcome!
Fork the repo and submit a pull request 🚀


---

If you want, I can:
- Add **dynamic repo badges** (stars, forks, issues)
- Create a **`requirements.txt`**
- Add **screenshots / demo GIFs**
- Customize it with **your GitHub username**

Just say the word 👍
