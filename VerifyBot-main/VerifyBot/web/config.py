import os
from dotenv import load_dotenv

auth_role_name = "인증된 유저"

# 사용 예:
role_name = get_auth_role_name()
role = discord.utils.get(guild.roles, name=role_name)

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
AUTH_WEB_URL = os.getenv("AUTH_WEB_URL", "http://localhost:5000")
PORT = int(os.getenv("PORT", 5000))