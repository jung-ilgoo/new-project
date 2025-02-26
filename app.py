from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Fly.io! 🚀 자동 배포 테스트 완료!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
