import os
import psycopg2
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    # DB 연결
    conn = psycopg2.connect(os.environ["postgres://new_fly_project:ZdDBUehGzo0AUpQ@new-fly-postgres.flycast:5432/new_fly_project?sslmode=disable"])
    # 쿼리 실행 예시
    with conn.cursor() as cur:
        cur.execute("SELECT 'Hello from PostgreSQL!'")
        row = cur.fetchone()
    conn.close()
    return row[0]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
