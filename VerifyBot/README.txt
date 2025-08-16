# discord.bot.Verify.Showker

프로젝트 설명

디스코드(discord)라는 메신저를 활용하여, ID 및 PASSWORD 입력하여 로그인하고, 이를 시트에 시각화하는 인증 프로그램을 제작.

A. 목표

	> 1. 디스코드 봇(discord bot)를 이용하여, 로그인 메세지 출력 O

	> 2. 로그인 메세지의 링크를 통하여, 웹 링크 이동 O 

	> 3. 로그인HTML로 이동 후 로그인 진행 (ID/PW입력) (디스코드 ID = PW / 유저 닉네임 = ID) O

	> 4. 작성된 정보들은 구글 스프레드 시트에 출력(신규) X

	> 5. 작성 후 성공HTML 출력 O -> X

	> 6. 재작성시 관리자 권한이 있다면, 시트 뷰어 ( 없는 경우 권한 없다고 출력 )(신규) X
 
B. 작업 환경
	> 파이썬 3.13

C. 작성시 필요한 것

	> CMD 명령 프롬포트 활용하여 설치
	flask
	fastapi
	uvicorn
	jinja2
	geoip2
	python-multipart
	requests
	gspread
	python-dotenv
	google-auth 버전2.28.1
	gspread_formatting
	discord.py

	> Render -- 대학교 1학년때 알게됨.
	- 깃허브를 통해서, 웹 및 봇 구동 진행
	- 환경 변수 및 중요 정보가 담긴 파일(env 암호화 파일)은 Render에서 따로 작성할 것. 
	
	> Github -- 대학교 1학년때 알게됨.
	- Render 과 연동하며, 업로드 진행
	- 필수 정도 env 파일 및 중요 정보가 담긴 파일은 작성하지 말 것.

	> Docker -- 대학교 1학년때 알게됨.
	- 활용해봤으나, 중간에 보류됨.
	- 포트 설정 및 pip 다운로드

	