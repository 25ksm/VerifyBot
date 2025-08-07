import os
import discord
import config
from discord.ext import commands
from discord import Embed, ButtonStyle
from discord.ui import View, Button
from fastapi import FastAPI, Request



bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
# 봇 인텐트 설정
tokens = discord.Intents.default()
tokens.guilds = True
tokens.messages = True
tokens.message_content = True

# 봇 인스턴스 생성
bot = commands.Bot(command_prefix="!", intents=tokens)

# ----- PREFIX COMMANDS (! 접두사) -----

@bot.command(name="인증채널")
async def set_auth_channel(ctx, channel_name: str):
    global auth_channel_id
    for ch in ctx.guild.text_channels:
        if ch.name == channel_name:
            auth_channel_id = ch.id
            await ctx.send(f"✅ 인증 채널이 `{channel_name}`(으)로 설정되었습니다.")
            return
    await ctx.send("❌ 해당 채널을 찾을 수 없습니다.")

@bot.command(name="인증역할")
async def set_auth_role(ctx, role_name: str):
    global auth_role_name
    auth_role_name = role_name
    await ctx.send(f"✅ 인증 역할이 `{role_name}`(으)로 설정되었습니다.")

@bot.command(name="인증메시지")
async def send_auth_message(ctx):
    if auth_channel_id is None:
        return await ctx.send("❗ 먼저 `!인증채널 (채널명)`을 입력해주세요.")
    
    embed = Embed(
        title="✅ 디스코드 인증 시스템",
        description="아래 버튼을 눌러 인증을 시작하세요.",
        color=0x00ff00
    )
    auth_url = os.getenv("AUTH_WEB_URL", "http://localhost:5000") + "/consent"
    button = Button(label="인증하기", style=ButtonStyle.link, url=auth_url)
    view = View()
    view.add_item(button)

    channel = bot.get_channel(auth_channel_id)
    if channel:
        await channel.send(embed=embed, view=view)
        await ctx.send("✅ 인증 메시지를 전송했습니다.")
    else:
        await ctx.send("❌ 설정된 인증 채널을 찾을 수 없습니다.")

@bot.command(name="인증")
async def auth_help(ctx):
    await ctx.send("🛠 먼저 `!인증채널 (채널명)` 및 `!인증역할 (역할명)`을 설정한 후 `!인증메시지`를 사용하세요.")

# ----- SLASH COMMANDS (/ 접두사) -----

@bot.tree.command(name="인증채널", description="인증 메시지를 보낼 채널을 설정합니다.")
async def slash_set_channel(interaction: discord.Interaction, channel_name: str):
    global auth_channel_id
    for ch in interaction.guild.text_channels:
        if ch.name == channel_name:
            auth_channel_id = ch.id
            await interaction.response.send_message(f"✅ 인증 채널이 `{channel_name}`(으)로 설정되었습니다.", ephemeral=True)
            return
    await interaction.response.send_message("❌ 해당 채널을 찾을 수 없습니다.", ephemeral=True)

@bot.tree.command(name="인증역할", description="인증된 유저에게 부여할 역할을 설정합니다.")
async def slash_set_role(interaction: discord.Interaction, role_name: str):
    global auth_role_name
    auth_role_name = role_name
    await interaction.response.send_message(f"✅ 인증 역할이 `{role_name}`(으)로 설정되었습니다.", ephemeral=True)

@bot.tree.command(name="인증메시지", description="설정된 채널에 인증 임베드와 버튼을 보냅니다.")
async def slash_send_message(interaction: discord.Interaction):
    if auth_channel_id is None:
        return await interaction.response.send_message("❗ 먼저 `/인증채널` 명령으로 채널을 설정해주세요.", ephemeral=True)
    embed = Embed(
        title="✅ 디스코드 인증 시스템",
        description="아래 버튼을 눌러 인증을 시작하세요.",
        color=0x00ff00
    )
    auth_url = config.AUTH_WEB_URL.rstrip("/") + "/consent"
    button = Button(label="인증하기", style=ButtonStyle.link, url=auth_url)
    view = View()
    view.add_item(button)

    channel = bot.get_channel(auth_channel_id)
    if channel:
        await channel.send(embed=embed, view=view)
        await interaction.response.send_message("✅ 인증 메시지를 전송했습니다.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ 설정된 인증 채널을 찾을 수 없습니다.", ephemeral=True)

@bot.tree.command(name="인증도움", description="인증 명령어 사용법을 안내합니다.")
async def slash_help(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🛠 먼저 `/인증채널 (채널명)`, `/인증역할 (역할명)`을 설정한 후 `/인증메시지`를 사용하세요.",
        ephemeral=True
    )
