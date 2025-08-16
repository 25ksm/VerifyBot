import os
import json

# shared 폴더 경로
shared_dir = os.path.join(os.path.dirname(__file__), 'shared')
os.makedirs(shared_dir, exist_ok=True)  # 폴더 없으면 생성

# user_data.json 경로
data_file = os.path.join(shared_dir, 'user_data.json')

# 파일이 없거나 잘못된 경우 초기화
if not os.path.exists(data_file):
    with open(data_file, 'w') as f:
        json.dump([], f)
    print("✅ user_data.json 파일이 생성되었습니다.")
else:
    try:
        with open(data_file, 'r') as f:
            json.load(f)
        print("✔️ user_data.json 파일이 이미 존재하고 정상입니다.")
    except json.JSONDecodeError:
        with open(data_file, 'w') as f:
            json.dump([], f)
        print("⚠️ JSON 형식 오류 발견 — 파일을 초기화했습니다.")