# routes/players.py
from flask import Blueprint, render_template, request, redirect, url_for
import psycopg2
import os

players_bp = Blueprint("players_bp", __name__)

def get_db_connection():
    # Fly.io에서 자동 설정된 DATABASE_URL 사용 (필요 시 수정)
    return psycopg2.connect(os.environ["DATABASE_URL"])

@players_bp.route("/add_player", methods=["GET", "POST"])
def add_player():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        player_name = request.form.get("player_name")
        cur.execute("INSERT INTO players (player_name) VALUES (%s)", (player_name,))
        conn.commit()
        return redirect(url_for("players_bp.add_player"))
    else:
        cur.execute("SELECT id, player_name FROM players")
        players = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("add_player.html", players=players)
