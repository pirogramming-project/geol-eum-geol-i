from fabric import Connection

# 서버 정보
HOST = "http://101.79.11.121/"
USER = "root"
KEY_FILE = "/home/ubuntu/.ssh/github_actions_key"  # SSH 키 파일 경로

def deploy():
    conn = Connection(host=HOST, user=USER, connect_kwargs={"key_filename": KEY_FILE})
    
    with conn.cd("/home/ubuntu/geol-eum-geol-i"):
        conn.run("git pull origin main")  # 최신 코드 가져오기
        conn.run("source venv/bin/activate && pip install -r requirements.txt")  # 패키지 업데이트
        conn.run("source venv/bin/activate && python manage.py migrate")  # DB 마이그레이션
        conn.run("source venv/bin/activate && python manage.py collectstatic --noinput")  # 정적 파일 적용
        conn.run("sudo systemctl restart gunicorn")  # 서버 재시작
	conn.run("sudo systemctl restart nginx")

    print("🚀 자동 배포 완료!")
