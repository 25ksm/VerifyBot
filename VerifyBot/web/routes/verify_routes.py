# web/routes/verify_routes.py
from flask import Blueprint, request, redirect
import requests
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