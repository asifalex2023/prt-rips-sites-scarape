# 🔞 PRT Telegram Bot 🚀

A feature-rich Telegram bot for searching and managing torrent links from Pornrips

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features
- 🔍 Search torrents directly through Telegram
- 📄 Generate formatted Telegraph pages
- 📤 Export torrent links as text files
- 🕒 24/7 background service operation

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/pornrips-bot.git
cd pornrips-bot
```

### 2. Install Dependencies
```bash
sudo apt update && sudo apt install python3-pip -y
pip3 install -r requirements.txt
```

### 3. Configure Bot Token
1. Get your Telegram bot token from [@BotFather](https://t.me/BotFather)
2. Edit `pornrips_bot.py`:
```python
# Replace with your actual token
Application.builder().token('YOUR_TELEGRAM_BOT_TOKEN').build()
```

## 🖥️ Systemd Service Setup

### 1. Create Service File
```bash
sudo nano /etc/systemd/system/pornrips-bot.service
```

### 2. Service Configuration
```ini
[Unit]
Description=Pornrips.to Telegram Bot
After=network.target

[Service]
User=root
WorkingDirectory=/path/to/pornrips-bot
ExecStart=/usr/bin/python3 /path/to/pornrips-bot/pornrips_bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 3. Enable & Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable pornrips-bot
sudo systemctl start pornrips-bot
```

## 🎮 Service Management
```bash
# Check status
sudo systemctl status pornrips-bot

# View logs
journalctl -u pornrips-bot -f

# Restart service
sudo systemctl restart pornrips-bot

# Stop service
sudo systemctl stop pornrips-bot
```

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---

**Note:** Replace all placeholders (`yourusername`, `YOUR_TELEGRAM_BOT_TOKEN`, `/path/to/`) with your actual values before use.

**Telegram** - @asifalex
