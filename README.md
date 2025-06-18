# 🛎️ The Concierge — A John Wick-Inspired Discord Bot

Welcome to **The Concierge**, an elegant and modular Discord bot designed in the style of the *John Wick* universe. This bot brings the luxurious atmosphere of The Continental and the deadly efficiency of The High Table to your server with immersive leveling, currency, roles, and inventory systems.

---

## ✨ Features

- 🎯 **XP & Leveling** — Earn XP by messaging, level up automatically, and unlock exclusive ranks.
- 🖼️ **XP Cards** — Beautiful rank cards showing user progress with server nicknames and avatars.
- 💰 **Currency System** — Earn Coins and Markers to use in shops and contracts.
- 🛍️ **Shop & Inventory** — Buy and store custom items with a clean inventory interface.
- 🎭 **Auto Roles by Level** — Become an Operator, Assassin, Cleaner, or ascend to the High Table.
- 📅 **Daily Rewards** — Claim daily Coins and Markers to grow your reputation.
- 🧩 **Modular Cogs** — Clean structure and easy to expand or customize.
- 🔒 **Secure Config** — Uses `.env` for token safety. `.gitignore` excludes sensitive files.

---

## 🧱 Folder Structure

The Concierge/
├── bot.py # Entry point
├── config.py # Bot config (token loaded from .env)
├── cogs/ # Modular bot features
│ ├── xp.py
│ ├── shop.py
│ ├── inventory.py
│ ├── visuals.py
│ ├── daily.py
│ └── roles.py
├── assets/ # Fonts & images for visuals
│ └── OpenSans.ttf
├── data/ # Local database storage
│ └── currency.db
├── .env # Environment variables (not tracked)
├── .gitignore # Ignore token, db, and cache
├── requirements.txt # Python dependencies
└── README.md # You're here!


---

## 🚀 Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/the-concierge-bot.git
   cd the-concierge-bot
2. **Install requirements**
   pip install -r requirements.txt
3. **Add your bot token**
   - Create a file named .env
    DISCORD_TOKEN=your_bot_token_here
4. **Run the bot**
   python bot.py

## 📜 Role Auto-Assignment Logic
The bot automatically manages promotion/demotion based on user level:

| Level | Role       |
| ----- | ---------- |
| 1+    | Operator   |
| 5+    | Assassin   |
| 10+   | Cleaner    |
| 20+   | High Table |

Users get promoted as they gain XP. Lower roles are removed automatically.

## 🎯 Commands Overview
| Command       | Description                        |
| ------------- | ---------------------------------- |
| `!level`      | View your current XP and level     |
| `!levelcard`  | Display your styled XP card        |
| `!daily`      | Claim your daily Coins and Markers |
| `!shop`       | Browse available items             |
| `!buy <item>` | Purchase an item from the shop     |
| `!inventory`  | View your current owned items      |

## 📦 Example .gitignore
.env
__pycache__/
*.db
assets/


## 📦 Example requirements.txt
discord.py
python-dotenv
aiosqlite
Pillow
aiohttp

Generate yours with:
pip freeze > requirements.txt

## 🛠️ Contributing
Pull requests are welcome! If you have an idea for a new feature or enhancement, feel free to fork the project and submit a PR. All contributions must maintain the elegant tone and purpose of the bot.

## ⚖️ License
This project is licensed under the MIT License.

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy...

## ⭐ Support & Promotion
If you enjoy this project or find it useful:
- 🌟 Star the repo
- 🍴 Fork it
- 💬 Share with the community

Help us expand the High Table’s influence — one server at a time.


  
