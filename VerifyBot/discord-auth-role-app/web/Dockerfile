FROM python:3.10
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]

# Flask 실행을 위한 포트 열기
EXPOSE 10000

CMD ["./start.sh"]