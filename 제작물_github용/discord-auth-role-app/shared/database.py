import json
import os
import gspread
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

# .env 파일의 값을 환경 변수로 로드
load_dotenv()

# .env 에 설정해둔 값을 가져오기
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# 절대 경로 기준으로 DATA_FILE 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "user_data.json")
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')


def save_user_info(discord_id, username, joined_at, ip, country, region):
    # 파일이 없으면 빈 리스트로 초기화
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

    # 기존 데이터 로드 (JSON 깨짐 방지 처리)
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []

    # 새 정보 추가
    data.append({
        "discord_id": discord_id,
        "username": username,
        "joined_at": joined_at,
        "ip": ip,
        "country": country,
        "region": region
    })

    # 파일에 저장
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_users():
    # 파일이 없으면 빈 리스트 반환
    if not os.path.exists(DATA_FILE):
        return []

    # 데이터 읽기 (깨진 JSON 방지 처리)
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


# Google Sheets API 인증 정보
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'path/to/your/credentials.json'  # 다운로드 받은 JSON 파일 경로

# 스프레드시트 ID와 시트 이름
SPREADSHEET_ID = 'your_spreadsheet_id'  # Google Sheets의 스프레드시트 ID
SHEET_NAME = 'Sheet1'  # 데이터를 추가할 시트 이름

# Google Sheets 인증
def authenticate_google_sheets():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return gspread.authorize(creds)

# 사용자 정보 저장 함수 (Google Sheets로 저장)
def save_user_info_to_sheets(discord_id, username, joined_at, ip, country, region):
    client = authenticate_google_sheets()

    # 구글 시트 열기
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    
    # 새로운 데이터를 시트에 추가
    row = [discord_id, username, joined_at, ip, country, region]
    sheet.append_row(row)

# 사용자 정보 저장 함수
def save_user_info(discord_id, username, joined_at, ip, country, region):
    # 기존 save_user_info 코드도 실행할 수 있음 (로컬 JSON 파일에 저장)
    # 기존 코드: 
    # ...
    
    # 구글 시트에도 저장
    save_user_info_to_sheets(discord_id, username, joined_at, ip, country, region)
