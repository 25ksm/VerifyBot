import os
import json
from dotenv import load_dotenv

load_dotenv()  # .env 파일도 로드

def check_credentials():
    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

    if not credentials_json:
        print("❌ 환경변수 GOOGLE_CREDENTIALS_JSON이 없습니다.")
        return

    try:
        info = json.loads(credentials_json)
        print("✅ JSON 파싱 성공!")
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 실패: {e}")
        return

    if "private_key" not in info:
        print("❌ private_key 항목이 없습니다.")
        return

    private_key = info["private_key"]
    print("\n🔑 복원 전 private_key 일부:")
    print(private_key[:100])

    # 줄바꿈 복원
    private_key_fixed = private_key.replace("\\n", "\n")
    print("\n🔑 복원 후 private_key 일부:")
    print(private_key_fixed[:100])

    # PEM 헤더 확인
    if "BEGIN PRIVATE KEY" in private_key_fixed and "END PRIVATE KEY" in private_key_fixed:
        print("\n✅ private_key 줄바꿈 복원 완료 (정상)")
    else:
        print("\n❌ private_key 복원 실패 (PEM 포맷 이상)")

if __name__ == "__main__":
    check_credentials()