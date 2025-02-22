# 🚀 Pornrips.to Telegram Bot

A Telegram bot for searching and managing torrent links from Pornrips.to

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features
- Search torrents via Telegram
- Generate formatted Telegraph pages
- Export torrent links as text files
- 24/7 background service operation

## 📥 Installation

### Clone Repository
```bash
git clone https://github.com/yourusername/pornrips-bot.git
cd pornrips-bot

### Install Dependencies
sudo apt update && sudo apt install python3-pip -y
pip3 install -r requirements.txt


2. Install Dependencies
Install the required Python packages by running the following commands:

bash
Copy
sudo apt update && sudo apt install python3-pip -y  # Update package list and install pip
pip3 install -r requirements.txt  # Install dependencies from requirements.txt
3. Configure Your Telegram Bot Token
Get your Telegram bot token from @BotFather.

Open the pornrips_bot.py file and find the following line:

python
Copy
Application.builder().token('YOUR_TELEGRAM_BOT_TOKEN').build()
Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token.

4. Set Up the Systemd Service
To ensure the bot runs as a background service, follow these steps:

4.1 Create the Service File
Create a new systemd service file to manage the bot as a background service:

bash
Copy
sudo nano /etc/systemd/system/pornrips-bot.service
4.2 Add the Following Configuration
Replace /path/to/pornrips-bot.py with the actual path to your Python script (pornrips_bot.py) and set the correct working directory. For example:

ini
Copy
[Unit]
Description=Pornrips.to Telegram Bot
After=network.target

[Service]
User=root
WorkingDirectory=/root/prt-rips-sites-scarape  # Replace with your project directory
ExecStart=/usr/bin/python3 /root/prt-rips-sites-scarape/pornrips_bot.py  # Path to your Python file
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
4.3 Reload Systemd and Enable the Service
Reload systemd to apply the new service, enable it to start at boot, and start it immediately:

bash
Copy
sudo systemctl daemon-reload  # Reload systemd manager
sudo systemctl enable pornrips-bot  # Enable service to start on boot
sudo systemctl start pornrips-bot  # Start the bot service
5. Manage the Service
You can control the bot's service using the following systemd commands:

To check the status of the service:

bash
Copy
sudo systemctl status pornrips-bot
To view the live logs of the service:

bash
Copy
journalctl -u pornrips-bot -f
To restart the service:

bash
Copy
sudo systemctl restart pornrips-bot
To stop the service:

bash
Copy
sudo systemctl stop pornrips-bot
The bot will now run continuously in the background and restart automatically if it fails or if the VPS reboots.

Remember to replace placeholders like yourusername in the GitHub URL, /path/to/pornrips-bot with the actual path, and YOUR_TELEGRAM_BOT_TOKEN with your real token.

css
Copy

This updated guide should be clearer for users and provide all necessary instructions to install and run the bot on a VPS.
