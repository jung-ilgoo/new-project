# routes/main.py
from flask import Blueprint, render_template

# Blueprint 생성
main_bp = Blueprint("main_bp", __name__)

# 메인 페이지 라우트
@main_bp.route("/")
def home():
    return render_template("index.html")
