import gspread
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from gspread_formatting import format_cell_range, cellFormat, textFormat, Color
import json

# 환경변수 불러오기
load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME", "인증리스트")  # 기본값 지정
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Google Sheets 인증
def authenticate_google_sheets():
    info = json.loads(os.getenv("GOOGLE_CREDENTIALS_JSON"))
    credentials = service_account.Credentials.from_service_account_info(
        info,
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(credentials)
    return client

# 스프레드시트 열기
def open_spreadsheet():
    try:
        client = authenticate_google_sheets()
        sheet = client.open(SPREADSHEET_NAME).sheet1
        return sheet
    except Exception as e:
        print(f"[ERROR] 스프레드시트를 열 수 없습니다: {e}")
        return None

# 스타일 적용 (헤더 스타일 등)
def apply_styles(sheet):
    try:
        # A1 셀: 회색 배경 + 흰 글씨 + 볼드
        format_cell_range(sheet, 'A1', cellFormat(
            backgroundColor=Color(0.5, 0.5, 0.5),  # 회색 배경
            textFormat=textFormat(bold=True, foregroundColor=Color(1, 1, 1))  # 흰색 글씨
        ))

        # B1:D1 셀: 초록색 배경 + 흰 글씨 + 볼드
        format_cell_range(sheet, 'B1:C1', cellFormat(
            backgroundColor=Color(0, 0.5, 0),  # 초록색 배경
            textFormat=textFormat(bold=True, foregroundColor=Color(1, 1, 1))  # 흰색 글씨, 볼드
        ))

        # A2 셀: 가운데 정렬
        format_cell_range(sheet, 'A2', cellFormat(
            horizontalAlignment='CENTER',
            verticalAlignment='MIDDLE'
        ))
    except Exception as e:
        print(f"[ERROR] 셀 스타일 적용 중 오류 발생: {e}")

# 전체 적용 함수
def update_spreadsheet():
    sheet = open_spreadsheet()
    if sheet:
        apply_styles(sheet)
