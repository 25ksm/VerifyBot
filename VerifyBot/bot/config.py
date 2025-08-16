import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
AUTH_WEB_URL = os.getenv("AUTH_WEB_URL", "http://localhost:5000")
PORT = int(os.getenv("PORT", 5000))