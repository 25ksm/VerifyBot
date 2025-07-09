import os
import json
import gspread
from google.oauth2 import service_account
from dotenv import load_dotenv
from flask import current_app

import os
import json
import gspread
from google.oauth2 import service_account
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 경로 설정
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_FILE = os.path.join(BASE_DIR, "user_data.json")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", os.path.join(BASE_DIR, "credentials.json"))
CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME", "Sheet1")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
info = json.loads(credentials_json)
info["private_key"] = info["private_key"].replace("\\n", "\n")

# credentials.json 파일 생성
if CREDENTIALS_JSON and not os.path.exists(SERVICE_ACCOUNT_FILE):
    try:
        info = json.loads(CREDENTIALS_JSON)
        if "private_key" in info:
            info["private_key"] = info["private_key"].replace("\\n", "\n")
        with open(SERVICE_ACCOUNT_FILE, "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
        print("✅ credentials.json 파일 생성 완료")
    except Exception as e:
        print(f"❌ GOOGLE_CREDENTIALS_JSON 파싱 실패: {e}")

# Google Sheets 인증
def authenticate_google_sheets():
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES
        )
        return gspread.authorize(creds)
    raise ValueError("❌ 인증 실패: SERVICE_ACCOUNT_FILE이 없습니다.")

# 구글 시트 객체 반환
def get_google_sheet():
    client = authenticate_google_sheets()
    return client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# 유저 정보 로컬 저장 + 구글 시트 저장
def save_user_info(discord_id, username, joined_at):
    # 1) 로컬 파일 처리
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []

    entry = {
        'discord_id': discord_id,
        'username': username,
        'joined_at': joined_at,
    }
    data.append(entry)

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # 2) 구글 시트에도 저장
    save_user_info_to_sheets(discord_id, username, joined_at)

def save_user_info_to_sheets(discord_id, username, joined_at):
    sheet = get_google_sheet()
    row = [discord_id, username, joined_at]
    sheet.append_row(row)

# 로컬 JSON에서 유저 목록 불러오기
def get_users():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


# 구글 시트에 유저 정보 저장

def save_user_info_to_sheets(discord_id, username, joined_at):
    client = authenticate_google_sheets()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    row = [discord_id, username, joined_at]
    sheet.append_row(row)

def _data_file():
    return os.path.join(current_app.instance_path, "user_data.json")
