# web/routes/verify_routes.py
from flask import Blueprint, request, redirect
import requests
import os
from bot.bot import bot, GUILD_ID
import discord

verify_bp = Blueprint("verify_bp", __name__)

BOT_API_URL = os.getenv("BOT_API_URL", "http://localhost:5000")

@verify_bp.route("/verify", methods=["POST"])
def verify_user():
    data = request.get_json()
    if not data or "discord_id" not in data:
        return jsonify({"status": "fail", "reason": "discord_id required"}), 400

    discord_id = data["discord_id"]

    response = requests.post(f"{BOT_API_URL}/api/assign-role", json={
        "discord_id": discord_id
    })

    if response.ok:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "fail", "reason": "Bot API error"}), 500


@verify_bp.route("/submit", methods=["POST"])
def submit():
    try:
        discord_id = request.form.get("discord_id")
        username = request.form.get("username")
        joined_at = request.form.get("joined_at")

        # 유저 정보 저장
        save_user_info(username, discord_id, joined_at)

        guild = discord.utils.get(bot.guilds, id=int(os.getenv("GUILD_ID")))
        if not guild:
            return "봇이 서버에 없습니다."

        member = guild.get_member(int(discord_id))
        if not member:
            return "서버에서 사용자를 찾을 수 없습니다."

        role = discord.utils.get(guild.roles, name=auth_role_name)
        if not role:
            return "인증 역할을 찾을 수 없습니다."

        # 역할 부여
        import asyncio
        asyncio.run_coroutine_threadsafe(member.add_roles(role), bot.loop)

        return render_template("success.html")

    except Exception as e:
        return f"에러 발생: {str(e)}", 500