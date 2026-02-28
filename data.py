import os
from dotenv import load_dotenv

load_dotenv()

botToken = os.getenv("botToken")

if not botToken or "YOUR_BOT_TOKEN" in botToken:
    raise ValueError("Error: 'botToken' is missing in .env or is a placeholder. Please set a valid Telegram bot token from @BotFather.")