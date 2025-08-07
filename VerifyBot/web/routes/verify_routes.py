# web/routes/verify_routes.py
from flask import Blueprint, request, redirect, jsonify
import requests
from bot.bot import bot, GUILD_ID
import discord

verify_bp = Blueprint("verify_bp", __name__)

BOT_API_URL = os.getenv("BOT_API_URL", "http://localhost:5000")

@verify_bp.route("/assign-role", methods=["POST"])
def assign_role():
    data = request.get_json() or request.form
    discord_id = data.get("discord_id")

    if not discord_id:
        return jsonify({"status": "fail", "reason": "discord_id not provided"}), 400

    response = requests.post(f"{BOT_API_URL}/api/assign-role", json={
        "discord_id": discord_id
    })

    if response.ok:
        return redirect("https://discord.com/channels/@me")
    else:
        return jsonify({"status": "fail", "reason": "Bot API error"}), 500


@verify_bp.route("/verify", methods=["POST"])
def verify_user():
    data = request.get_json()
    if not data or "discord_id" not in data:
        return jsonify({"status": "fail", "reason": "discord_id required"}), 400

    try:
        discord_id = int(data["discord_id"])
    except ValueError:
        return jsonify({"status": "fail", "reason": "Invalid discord_id"}), 400

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return jsonify({"status": "fail", "reason": "Guild not found"}), 404

    member = guild.get_member(discord_id)
    role = discord.utils.get(guild.roles, name="인증됨")

    if member and role:
        try:
            # Flask는 비동기 처리 루프가 없음 -> Discord 봇 쪽에서 처리하도록 하세요!
            # 또는 Celery나 Background Thread로 처리 필요
            return jsonify({"status": "fail", "reason": "Cannot assign role from Flask"}), 500
        except Exception as e:
            return jsonify({"status": "fail", "reason": str(e)}), 500

    return jsonify({"status": "fail", "reason": "Member or Role not found"}), 404