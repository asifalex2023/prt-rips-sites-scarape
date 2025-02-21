# Pornrips.to Telegram Bot 🤖

A Telegram bot that scrapes and delivers torrent links from Pornrips.to

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Features ✨
- Search torrents via Telegram
- Generate Telegraph pages with results
- Export torrent links as text files
- Background service operation

## Installation 📦

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/pornrips-bot.git
cd pornrips-bot

2. Install Dependencies
sudo apt update
sudo apt install python3-pip -y
pip3 install -r requirements.txt

Configuration ⚙️
Get your Telegram bot token from @BotFather

Edit main.py:
Application.builder().token('YOUR_TELEGRAM_BOT_TOKEN').build()

Commands 🤖
/start - Show welcome message

/search <query> - Search for torrents

/links <telegraph-url> - Export torrent links as TXT

Deployment on VPS 🚀
1. Create Systemd Service
sudo nano /etc/systemd/system/pornrips-bot.service
Add this configuration:

[Unit]
Description=Pornrips.to Telegram Bot
After=network.target

[Service]
User=root
WorkingDirectory=/path/to/pornrips-bot
ExecStart=/usr/bin/python3 /path/to/pornrips-bot/main.py
Restart=always

[Install]
WantedBy=multi-user.target

2. Enable and Start Service
sudo systemctl daemon-reload
sudo systemctl enable pornrips-bot
sudo systemctl start pornrips-bot

Management 🔧
Check status: sudo systemctl status pornrips-bot

View logs: journalctl -u pornrips-bot -f

Restart: sudo systemctl restart pornrips-bot

Stop: sudo systemctl stop pornrips-bot

Contributing 🤝
Pull requests welcome! Please ensure:

Python code follows PEP8 guidelines

Test your changes thoroughly

Update documentation accordingly

License 📄

### To Run as Background Service:
1. Follow the deployment section in README
2. Essential commands:
```bash
# Reload service files
sudo systemctl daemon-reload

# Enable auto-start on boot
sudo systemctl enable pornrips-bot

# Start service
sudo systemctl start pornrips-bot

# Check logs in real-time
journalctl -u pornrips-bot -f

python-telegram-bot==20.3
requests==2.31.0
telegraph-python==1.4.0
beautifulsoup4==4.12.2
html5lib==1.1Requirements File (requirements.txt):


This setup will:

Run 24/7 in background ✅

Auto-restart on failure 🔄

Survive server reboots 🔌

Easy log monitoring 📄

Remember to:

Replace /path/to/pornrips-bot with actual path

Set proper permissions for files

Keep your bot token secure 🔒

Regularly check logs for errors 🐛
