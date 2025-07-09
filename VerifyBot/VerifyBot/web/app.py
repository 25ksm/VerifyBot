from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request
from . import init_user_data

from .shared.database import save_user_info, get_users, get_google_sheet
from .shared.spreadsheet import update_spreadsheet

import requests
import os

# ① instance_relative_config=True 로 플라스크 인스턴스 폴더 사용
app = Flask(__name__, template_folder="templates", instance_relative_config=True)

# ② 인스턴스 폴더(instance/)가 없다면 생성
os.makedirs(app.instance_path, exist_ok=True)

@app.route("/") 
def index():
    return render_template("consent.html")

@app.route("/consent")
def consent():
    return render_template("consent.html")

@app.route("/submit", methods=["POST"])
def submit():
    discord_id = request.form.get("discord_id")
    username = request.form.get("username")
    joined_at = request.form.get("joined_at")
    save_user_info(discord_id, username, joined_at)
    return render_template("success.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/admin")
def admin():
    users = get_users()
    return {"users": users}

@app.route("/callback")
def callback():
    error = request.args.get("error")
    if error:
        return f"Error: {error}", 400

    code = request.args.get("code")
    if not code:
        return "No code received."

    # Discord OAuth2 토큰 요청
    data = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("DISCORD_REDIRECT_URI"),
        "scope": "identify guilds.join"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    if resp.status_code != 200:
        return f"Discord 인증 실패: {resp.text}", 500
    return resp.json()

    data = {
        "client_id": os.getenv("DISCORD_CLIENT_ID"),
        "client_secret": os.getenv("DISCORD_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("DISCORD_REDIRECT_URI"),
        "scope": "identify guilds.join"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)

    if response.status_code != 200:
        return f"Discord 인증 실패: {response.text}", 500

    return response.json()

# 테스트용 실행
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

    try:
        sheet = get_google_sheet()
        print("첫 번째 행:", sheet.row_values(1))
        update_spreadsheet()
    except Exception as e:
        print(f"[ERROR] Google Sheet 처리 중 문제 발생: {e}")
