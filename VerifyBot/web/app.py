from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request
from . import init_user_data

from .shared.database import save_user_info, get_users, get_google_sheet
from .shared.spreadsheet import update_spreadsheet

import requests
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config

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
    try:
        discord_id = request.form.get("discord_id")
        username = request.form.get("username")
        joined_at = request.form.get("joined_at")
        save_user_info(username, discord_id, joined_at)
        guild = discord.utils.get(bot.guilds)
        member = guild.get_member(int(discord_id))
        role = discord.utils.get(guild.roles, name=auth_role_name)
        if not member:
            return "서버에서 사용자를 찾을 수 없습니다."
        if not role:
            return "인증 역할을 찾을 수 없습니다."
        if not guild:
            return "봇이 서버에 없습니다."
        return render_template("success.html")
    except Exception as e:
        return f"에러 발생: {str(e)}", 500

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

    # OAuth2 토큰 요청
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

    tokens = response.json()
    access_token = tokens["access_token"]
    token_type = tokens["token_type"]  # 보통 "Bearer"

    # 유저 정보 요청
    user_response = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"{token_type} {access_token}"}
    )
    if user_response.status_code != 200:
        return f"유저 정보 가져오기 실패: {user_response.text}", 500

    user = user_response.json()
    user_id = user["id"]

    # 서버에 유저 추가 + 역할 부여
    guild_id = os.getenv("DISCORD_GUILD_ID")         # 서버 ID
    role_id = os.getenv("DISCORD_ROLE_ID")           # 인증 시 부여할 역할 ID
    bot_token = os.getenv("DISCORD_BOT_TOKEN")       # 봇 토큰

    # 서버에 유저 추가
    assign_role_url = f"https://discord.com/api/guilds/{guild_id}/members/{user_id}/roles/{role_id}"
    add_member_data = {
        "access_token": access_token
    }

    add_member_headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }

    member_response = requests.put(add_member_url, json=add_member_data, headers=add_member_headers)

    if member_response.status_code not in [200, 201, 204]:
        return f"서버 초대 실패: {member_response.text}", 500

    # 역할 부여
    role_url = f"https://discord.com/api/guilds/{guild_id}/members/{user_id}/roles/{role_id}"

    role_response = requests.put(role_url, headers={
        "Authorization": f"Bot {bot_token}"
    })

    if role_response.status_code != 204:
        return f"역할 부여 실패: {role_response.text}", 500

    # 완료 후 성공 페이지 렌더
    return render_template("success.html")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)

    if response.status_code != 200:
        return f"Discord 인증 실패: {response.text}", 500

    return response.json()

@app.route("/assign-role", methods=["POST"])
def assign_role():
    discord_id = request.form.get("discord_id")
    
    # 디스코드 봇 서버에 역할 요청
    response = requests.post("http://your-discord-bot-server.com/api/assign-role", json={
        "discord_id": discord_id
    })

    return redirect("https://discord.com/channels/@me")  # 혹은 인증 서버 주소

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

# 테스트용 실행
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

    try:
        sheet = get_google_sheet()
        print("첫 번째 행:", sheet.row_values(1))
        update_spreadsheet()
    except Exception as e:
        print(f"[ERROR] Google Sheet 처리 중 문제 발생: {e}")
