from dotenv import load_dotenv
load_dotenv()

import os, traceback, requests
from flask import Flask, render_template, request, current_app

# shared/database.py 에서 current_app.instance_path 기반으로 DATA_FILE을 가져오도록 수정 필요
from .shared.database import save_user_info, get_users, get_google_sheet
from .shared.spreadsheet import update_spreadsheet

# ① instance_relative_config=True 로 플라스크 인스턴스 폴더 사용
app = Flask(__name__, template_folder="templates", instance_relative_config=True)

# ② 인스턴스 폴더(instance/)가 없다면 생성
os.makedirs(app.instance_path, exist_ok=True)

@app.route("/")
def index():
    return "서버가 실행 중입니다."

@app.route("/consent")
def consent():
    return render_template("consent.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        discord_id = request.form["discord_id"]
        username   = request.form["username"]
        joined_at  = request.form["joined_at"]

        # shared/database.py 의 save_user_info() 가 current_app.instance_path/user_data.json에 씁니다
        save_user_info(discord_id, username, joined_at)
        return render_template("success.html")

    except Exception as e:
        # 로그에 전체 스택트레이스 찍어 줍니다
        traceback.print_exc()
        return f"에러 발생 ({e.__class__.__name__}): {repr(e)}", 500
        
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

# 개발 환경에서만 실행
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

    # 구글 시트 테스트
    try:
        sheet = get_google_sheet()
        print("첫 번째 행:", sheet.row_values(1))
        update_spreadsheet()
    except Exception as e:
        print(f"[ERROR] Google Sheet 처리 중 문제 발생: {e}")
