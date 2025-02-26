import os
import psycopg2
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    # Fly.io에서 자동 설정된 환경 변수 사용 (DATABASE_URL)
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    with conn.cursor() as cur:
        cur.execute("SELECT 'Hello from PostgreSQL!'")
        row = cur.fetchone()
    conn.close()
    return row[0]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
