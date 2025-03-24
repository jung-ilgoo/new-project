# routes/champion.py
from flask import Blueprint, render_template, request, redirect, url_for
import psycopg2
import os

champion_bp = Blueprint("champion_bp", __name__)

def get_db_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])

@champion_bp.route("/add_champion", methods=["GET", "POST"])
def add_champion():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == "POST":
        champion_name = request.form.get("champion_name")
        cur.execute("INSERT INTO champions (champion_name) VALUES (%s)", (champion_name,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("champion_bp.add_champion"))
    else:
        cur.execute("SELECT id, champion_name FROM champions")
        champions = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("add_champion.html", champions=champions)
