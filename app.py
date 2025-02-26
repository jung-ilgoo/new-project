import os
import psycopg2
from flask import Flask, render_template, Blueprint

app = Flask(__name__)

main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/")
def home():
    return render_template("index.html")

app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
