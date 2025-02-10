# from fabric import Connection

# # 서버 정보
# HOST = "101.79.11.121"
# USER = "root"
# KEY_FILE = "/home/ubuntu/.ssh/github_actions_key"  # SSH 키 파일 경로

# def deploy():
#     conn = Connection(host=HOST, user=USER, connect_kwargs={"key_filename": KEY_FILE})
    
#     with conn.cd("/home/ubuntu/geol-eum-geol-i"):
#         conn.run("git pull origin main")  # 최신 코드 가져오기
#         conn.run("source venv/bin/activate && pip install -r requirements.txt")  # 패키지 업데이트
#         conn.run("source venv/bin/activate && python manage.py migrate")  # DB 마이그레이션
#         # 기존 collectstatic 파일 삭제 후 다시 생성
#         conn.run("rm -rf staticfiles/")  # 기존 collectstatic 파일 삭제
#         conn.run("source venv/bin/activate && python manage.py collectstatic --noinput")

#         # 정적 파일 권한 설정 (서버가 접근 가능하도록 변경)
#         conn.run("sudo chmod -R 755 /home/ubuntu/geol-eum-geol-i/staticfiles/")
#         conn.run("sudo chown -R www-data:www-data /home/ubuntu/geol-eum-geol-i/staticfiles/")
#         conn.run("sudo systemctl restart gunicorn")  # Gunicorn 재시작
#         conn.run("sudo systemctl restart nginx")  # Nginx 재시작
#         conn.run("sudo systemctl reload nginx")  # Nginx 설정 다시 로드
#     print("🚀 자동 배포 완료!")
