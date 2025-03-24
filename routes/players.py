# routes/players.py
from flask import Blueprint, render_template, request, redirect, url_for
import psycopg2
import os

players_bp = Blueprint("players_bp", __name__)

def get_db_connection():
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

@players_bp.route("/edit_player/<int:player_id>")
def edit_player(player_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, player_name FROM players WHERE id = %s", (player_id,))
    player = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("edit_player.html", player=player)

# players.py 파일의 update_player 함수를 아래 코드로 대체하세요

@players_bp.route("/update_player/<int:player_id>", methods=["POST"])
def update_player(player_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 기존 플레이어 이름 조회
    cur.execute("SELECT player_name FROM players WHERE id = %s", (player_id,))
    old_player_name = cur.fetchone()[0]
    
    # 새 플레이어 이름
    new_player_name = request.form.get("player_name")
    
    # 플레이어 이름이 실제로 변경됐는지 확인
    if old_player_name != new_player_name:
        # 1. players 테이블에서 플레이어 이름 업데이트
        cur.execute("UPDATE players SET player_name = %s WHERE id = %s", (new_player_name, player_id))
        
        # 2. matches 테이블에서 해당 플레이어가 출전한 모든 경기 기록 업데이트
        
        # 블루팀 TOP
        cur.execute("UPDATE matches SET blue_top = %s WHERE blue_top = %s", (new_player_name, old_player_name))
        
        # 블루팀 JUNGLE
        cur.execute("UPDATE matches SET blue_jungle = %s WHERE blue_jungle = %s", (new_player_name, old_player_name))
        
        # 블루팀 MID
        cur.execute("UPDATE matches SET blue_mid = %s WHERE blue_mid = %s", (new_player_name, old_player_name))
        
        # 블루팀 ADC
        cur.execute("UPDATE matches SET blue_adc = %s WHERE blue_adc = %s", (new_player_name, old_player_name))
        
        # 블루팀 SUPPORT
        cur.execute("UPDATE matches SET blue_support = %s WHERE blue_support = %s", (new_player_name, old_player_name))
        
        # 레드팀 TOP
        cur.execute("UPDATE matches SET red_top = %s WHERE red_top = %s", (new_player_name, old_player_name))
        
        # 레드팀 JUNGLE
        cur.execute("UPDATE matches SET red_jungle = %s WHERE red_jungle = %s", (new_player_name, old_player_name))
        
        # 레드팀 MID
        cur.execute("UPDATE matches SET red_mid = %s WHERE red_mid = %s", (new_player_name, old_player_name))
        
        # 레드팀 ADC
        cur.execute("UPDATE matches SET red_adc = %s WHERE red_adc = %s", (new_player_name, old_player_name))
        
        # 레드팀 SUPPORT
        cur.execute("UPDATE matches SET red_support = %s WHERE red_support = %s", (new_player_name, old_player_name))
    
    # 변경사항 저장
    conn.commit()
    cur.close()
    conn.close()
    
    # 플레이어 목록 페이지로 리다이렉트
    return redirect(url_for("players_bp.add_player"))