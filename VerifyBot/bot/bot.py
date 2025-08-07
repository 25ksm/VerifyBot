import discord
from fastapi import FastAPI, Request
from discord.ext import commands
from discord import Embed, ButtonStyle
from discord.ui import View, Button
import os
import config

auth_channel_id = None
auth_role_name = None

intents = discord.Intents.all()

app = FastAPI()

GUILD_ID = int(os.getenv("GUILD_ID", "123456789012345678"))

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot ready: {bot.user}")

@bot.command(name="인증채널")
async def set_auth_channel(ctx, channel_name: str):
    global auth_channel_id
    for ch in ctx.guild.text_channels:
        if ch.name == channel_name:
            auth_channel_id = ch.id
            await ctx.send(f"인증 채널이 `{channel_name}`로 설정되었습니다.")
            return
    await ctx.send("해당 채널을 찾을 수 없습니다.")

@bot.command(name="인증역할")
async def set_auth_role(ctx, role_name: str):
    global auth_role_name
    auth_role_name = role_name
    await ctx.send(f"인증 역할이 `{role_name}`로 설정되었습니다.")

@bot.command(name="인증메시지")
async def send_auth_message(ctx):
    if auth_channel_id is None:
        return await ctx.send("먼저 `!인증채널 (채널명)`으로 지정해주세요.")
    embed = Embed(title="Discord 인증 시스템", description="버튼을 눌러 인증하세요.", color=0x00ff00)
    auth_url = config.AUTH_WEB_URL.rstrip("/") + "/consent"
    button = Button(label="인증하기", style=ButtonStyle.link, url=auth_url)
    view = View()
    view.add_item(button)
    channel = bot.get_channel(auth_channel_id)
    if channel:
        await channel.send(embed=embed, view=view)
        await ctx.send("인증 메시지를 보냈습니다.")
    else:
        await ctx.send("설정한 인증 채널을 찾을 수 없습니다.")

@app.post("/api/assign-role")
async def assign_role(req: Request):
    data = await req.json()
    discord_id = int(data["discord_id"])

    guild = bot.get_guild(GUILD_ID)
    member = guild.get_member(discord_id)
    role = discord.utils.get(guild.roles, name="인증됨")

    if member and role:
        await member.add_roles(role, reason="웹에서 인증 완료")
        return {"status": "success"}
    return {"status": "fail", "reason": "Member or Role not found"}