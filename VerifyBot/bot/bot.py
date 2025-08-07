import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot import commands as bot_commands # commands.py 에 정의된 명령어 등록

# 환경 변수 로드
load_dotenv()

# 인텐트 설정
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True  # 슬래시 명령 시 사용자 정보 확인용

# 봇 인스턴스 (commands.py 에서 가져옴)
bot = bot_commands.bot

GUILD_ID = int(os.getenv("GUILD_ID", "0"))

# 봇 준비 완료 시 실행
@bot.event
async def on_ready():
    await bot.tree.sync()  # 슬래시 명령어 동기화
    print(f"✅ 봇 로그인됨: {bot.user} (슬래시 커맨드 동기화 완료)")

# 봇 실행
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ DISCORD_TOKEN 환경 변수가 설정되지 않았습니다.")
    else:
        bot.run(token)
