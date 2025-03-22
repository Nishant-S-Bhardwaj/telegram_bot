# telegram_bot

This is an AI-powered Telegram bot with administrative controls and OpenAI integration for automated responses.

Features

Admin Commands:

/setadmin <your_id> - Claim admin rights.

/announce <message> - Send an admin announcement.

/kick - Kick a user (reply to their message).

/ban - Ban a user (reply to their message).

/mute - Mute a user (reply to their message).

General Commands:

/start - Welcome message with user ID.

/myid - Show your Telegram ID.

AI Chat Functionality:

The bot responds to text messages using OpenAI's GPT-3.5 Turbo.

Setup

Install dependencies:

pip install python-telegram-bot openai

Set up environment variables or update the script:

TELEGRAM_TOKEN: Your Telegram bot token.

OPENAI_API_KEY: Your OpenAI API key.

Run the bot:

python bot.py

Notes

Only the admin can use moderation commands.

The first user to run /setadmin <your_id> will claim admin rights.

The bot runs using polling; switch to webhook mode for production.

License

This project is open-source. Modify and use it as needed!
