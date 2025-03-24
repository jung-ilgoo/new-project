from flask import Blueprint, render_template, request, redirect, url_for
import psycopg2
import os

record_bp = Blueprint("record_bp", __name__)

def get_db_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])

@record_bp.route("/record", methods=["GET", "POST"])
def record():
    conn = get_db_connection()
    cur = conn.cursor()
    success_message = None  # 이 줄을 추가하여 변수 초기화
    form_data = {}  # 폼 데이터를 저장할 딕셔너리

    if request.method == "POST":
        # 1) 폼에서 넘어온 데이터 받기
        match_date = request.form.get("match_date")
        form_data["match_date"] = match_date

        # 블루팀 TOP
        blue_top = request.form.get("blue_top")
        blue_top_champion = request.form.get("blue_top_champion")
        blue_top_kills = int(request.form.get("blue_top_kills", 0))
        blue_top_deaths = int(request.form.get("blue_top_deaths", 0))
        blue_top_assists = int(request.form.get("blue_top_assists", 0))

        form_data["blue_top"] = blue_top
        # 챔피언과 KDA는 초기화할 것이므로 저장하지 않음

        # 블루팀 JUNGLE
        blue_jungle = request.form.get("blue_jungle")
        blue_jungle_champion = request.form.get("blue_jungle_champion")
        blue_jungle_kills = int(request.form.get("blue_jungle_kills", 0))
        blue_jungle_deaths = int(request.form.get("blue_jungle_deaths", 0))
        blue_jungle_assists = int(request.form.get("blue_jungle_assists", 0))

        form_data["blue_jungle"] = blue_jungle

        # 블루팀 MID
        blue_mid = request.form.get("blue_mid")
        blue_mid_champion = request.form.get("blue_mid_champion")
        blue_mid_kills = int(request.form.get("blue_mid_kills", 0))
        blue_mid_deaths = int(request.form.get("blue_mid_deaths", 0))
        blue_mid_assists = int(request.form.get("blue_mid_assists", 0))

        form_data["blue_mid"] = blue_mid

        # 블루팀 ADC
        blue_adc = request.form.get("blue_adc")
        blue_adc_champion = request.form.get("blue_adc_champion")
        blue_adc_kills = int(request.form.get("blue_adc_kills", 0))
        blue_adc_deaths = int(request.form.get("blue_adc_deaths", 0))
        blue_adc_assists = int(request.form.get("blue_adc_assists", 0))

        form_data["blue_adc"] = blue_adc

        # 블루팀 SUPPORT
        blue_support = request.form.get("blue_support")
        blue_support_champion = request.form.get("blue_support_champion")
        blue_support_kills = int(request.form.get("blue_support_kills", 0))
        blue_support_deaths = int(request.form.get("blue_support_deaths", 0))
        blue_support_assists = int(request.form.get("blue_support_assists", 0))

        form_data["blue_support"] = blue_support

        # 레드팀 TOP
        red_top = request.form.get("red_top")
        red_top_champion = request.form.get("red_top_champion")
        red_top_kills = int(request.form.get("red_top_kills", 0))
        red_top_deaths = int(request.form.get("red_top_deaths", 0))
        red_top_assists = int(request.form.get("red_top_assists", 0))

        form_data["red_top"] = red_top

        # 레드팀 JUNGLE
        red_jungle = request.form.get("red_jungle")
        red_jungle_champion = request.form.get("red_jungle_champion")
        red_jungle_kills = int(request.form.get("red_jungle_kills", 0))
        red_jungle_deaths = int(request.form.get("red_jungle_deaths", 0))
        red_jungle_assists = int(request.form.get("red_jungle_assists", 0))

        form_data["red_jungle"] = red_jungle

        # 레드팀 MID
        red_mid = request.form.get("red_mid")
        red_mid_champion = request.form.get("red_mid_champion")
        red_mid_kills = int(request.form.get("red_mid_kills", 0))
        red_mid_deaths = int(request.form.get("red_mid_deaths", 0))
        red_mid_assists = int(request.form.get("red_mid_assists", 0))

        form_data["red_mid"] = red_mid

        # 레드팀 ADC
        red_adc = request.form.get("red_adc")
        red_adc_champion = request.form.get("red_adc_champion")
        red_adc_kills = int(request.form.get("red_adc_kills", 0))
        red_adc_deaths = int(request.form.get("red_adc_deaths", 0))
        red_adc_assists = int(request.form.get("red_adc_assists", 0))

        form_data["red_adc"] = red_adc

        # 레드팀 SUPPORT
        red_support = request.form.get("red_support")
        red_support_champion = request.form.get("red_support_champion")
        red_support_kills = int(request.form.get("red_support_kills", 0))
        red_support_deaths = int(request.form.get("red_support_deaths", 0))
        red_support_assists = int(request.form.get("red_support_assists", 0))

        form_data["red_support"] = red_support

        # 승리 팀
        winner = request.form.get("winner")

        # 2) INSERT 쿼리 실행
        insert_sql = """
            INSERT INTO matches (
                match_date,

                blue_top, blue_top_champion, blue_top_kills, blue_top_deaths, blue_top_assists,
                blue_jungle, blue_jungle_champion, blue_jungle_kills, blue_jungle_deaths, blue_jungle_assists,
                blue_mid, blue_mid_champion, blue_mid_kills, blue_mid_deaths, blue_mid_assists,
                blue_adc, blue_adc_champion, blue_adc_kills, blue_adc_deaths, blue_adc_assists,
                blue_support, blue_support_champion, blue_support_kills, blue_support_deaths, blue_support_assists,

                red_top, red_top_champion, red_top_kills, red_top_deaths, red_top_assists,
                red_jungle, red_jungle_champion, red_jungle_kills, red_jungle_deaths, red_jungle_assists,
                red_mid, red_mid_champion, red_mid_kills, red_mid_deaths, red_mid_assists,
                red_adc, red_adc_champion, red_adc_kills, red_adc_deaths, red_adc_assists,
                red_support, red_support_champion, red_support_kills, red_support_deaths, red_support_assists,

                winner
            )
            VALUES (
                %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,

                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s
            )
        """

        values = (
            match_date,

            blue_top, blue_top_champion, blue_top_kills, blue_top_deaths, blue_top_assists,
            blue_jungle, blue_jungle_champion, blue_jungle_kills, blue_jungle_deaths, blue_jungle_assists,
            blue_mid, blue_mid_champion, blue_mid_kills, blue_mid_deaths, blue_mid_assists,
            blue_adc, blue_adc_champion, blue_adc_kills, blue_adc_deaths, blue_adc_assists,
            blue_support, blue_support_champion, blue_support_kills, blue_support_deaths, blue_support_assists,

            red_top, red_top_champion, red_top_kills, red_top_deaths, red_top_assists,
            red_jungle, red_jungle_champion, red_jungle_kills, red_jungle_deaths, red_jungle_assists,
            red_mid, red_mid_champion, red_mid_kills, red_mid_deaths, red_mid_assists,
            red_adc, red_adc_champion, red_adc_kills, red_adc_deaths, red_adc_assists,
            red_support, red_support_champion, red_support_kills, red_support_deaths, red_support_assists,

            winner
        )

        # === 여기서 디버그 출력 ===
        placeholder_count = insert_sql.count('%s')
        print("DEBUG placeholder_count:", placeholder_count, flush=True)
        print("DEBUG len(values):", len(values), flush=True)

        cur.execute(insert_sql, values)
        conn.commit()

        # 성공 메시지 설정
        success_message = "경기 기록이 성공적으로 저장되었습니다!"

    # GET 요청 및 POST 요청 후 모두 실행
    cur.execute("SELECT player_name FROM players")
    players = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT champion_name FROM champions")
    champions = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return render_template("record.html", players=players, champions=champions, success_message=success_message, form_data=form_data)

# 이 코드를 record.py에 있는 history 함수를 대체하는데 사용하세요

@record_bp.route("/history")
def history():
    # 현재 페이지 번호 (URL 파라미터에서 가져옴, 기본값은 1)
    page = request.args.get('page', 1, type=int)
    
    # 페이지당 표시할 항목 수
    per_page = 10
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 전체 매치 수 조회
    cur.execute("SELECT COUNT(*) FROM matches")
    total_matches = cur.fetchone()[0]
    
    # 전체 페이지 수 계산
    total_pages = (total_matches + per_page - 1) // per_page
    
    # 현재 페이지가 유효한 범위 내에 있는지 확인
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages
    
    # 페이지에 해당하는 매치 조회 (LIMIT와 OFFSET 사용)
    offset = (page - 1) * per_page
    cur.execute(
        "SELECT * FROM matches ORDER BY match_date DESC LIMIT %s OFFSET %s", 
        (per_page, offset)
    )
    matches = cur.fetchall()
    
    cur.close()
    conn.close()
    
    # 페이지네이션을 위한 표시할 페이지 번호 범위 계산
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)
    
    # 표시할 페이지 번호 리스트
    page_numbers = list(range(start_page, end_page + 1))
    
    # 첫 페이지와 마지막 페이지 표시를 위한 처리
    if start_page > 1:
        page_numbers = [1, '...'] + page_numbers
    if end_page < total_pages:
        page_numbers = page_numbers + ['...', total_pages]

    return render_template("history.html", 
                           matches=matches, 
                           current_page=page, 
                           total_pages=total_pages,
                           page_numbers=page_numbers)

# record.py 파일에 아래 함수들을 추가하세요

@record_bp.route("/edit_match/<int:match_id>")
def edit_match(match_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 해당 ID의 경기 정보 조회
    cur.execute("SELECT * FROM matches WHERE id = %s", (match_id,))
    match = cur.fetchone()
    
    if not match:
        cur.close()
        conn.close()
        return "경기 정보를 찾을 수 없습니다.", 404
    
    # 플레이어 목록 조회
    cur.execute("SELECT player_name FROM players")
    players = [row[0] for row in cur.fetchall()]
    
    # 챔피언 목록 조회
    cur.execute("SELECT champion_name FROM champions")
    champions = [row[0] for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return render_template("edit_match.html", match=match, players=players, champions=champions)

@record_bp.route("/update_match/<int:match_id>", methods=["POST"])
def update_match(match_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 폼에서 데이터 가져오기
    match_date = request.form.get("match_date")

    # 블루팀 TOP
    blue_top = request.form.get("blue_top")
    blue_top_champion = request.form.get("blue_top_champion")
    blue_top_kills = int(request.form.get("blue_top_kills", 0))
    blue_top_deaths = int(request.form.get("blue_top_deaths", 0))
    blue_top_assists = int(request.form.get("blue_top_assists", 0))

    # 블루팀 JUNGLE
    blue_jungle = request.form.get("blue_jungle")
    blue_jungle_champion = request.form.get("blue_jungle_champion")
    blue_jungle_kills = int(request.form.get("blue_jungle_kills", 0))
    blue_jungle_deaths = int(request.form.get("blue_jungle_deaths", 0))
    blue_jungle_assists = int(request.form.get("blue_jungle_assists", 0))

    # 블루팀 MID
    blue_mid = request.form.get("blue_mid")
    blue_mid_champion = request.form.get("blue_mid_champion")
    blue_mid_kills = int(request.form.get("blue_mid_kills", 0))
    blue_mid_deaths = int(request.form.get("blue_mid_deaths", 0))
    blue_mid_assists = int(request.form.get("blue_mid_assists", 0))

    # 블루팀 ADC
    blue_adc = request.form.get("blue_adc")
    blue_adc_champion = request.form.get("blue_adc_champion")
    blue_adc_kills = int(request.form.get("blue_adc_kills", 0))
    blue_adc_deaths = int(request.form.get("blue_adc_deaths", 0))
    blue_adc_assists = int(request.form.get("blue_adc_assists", 0))

    # 블루팀 SUPPORT
    blue_support = request.form.get("blue_support")
    blue_support_champion = request.form.get("blue_support_champion")
    blue_support_kills = int(request.form.get("blue_support_kills", 0))
    blue_support_deaths = int(request.form.get("blue_support_deaths", 0))
    blue_support_assists = int(request.form.get("blue_support_assists", 0))

    # 레드팀 TOP
    red_top = request.form.get("red_top")
    red_top_champion = request.form.get("red_top_champion")
    red_top_kills = int(request.form.get("red_top_kills", 0))
    red_top_deaths = int(request.form.get("red_top_deaths", 0))
    red_top_assists = int(request.form.get("red_top_assists", 0))

    # 레드팀 JUNGLE
    red_jungle = request.form.get("red_jungle")
    red_jungle_champion = request.form.get("red_jungle_champion")
    red_jungle_kills = int(request.form.get("red_jungle_kills", 0))
    red_jungle_deaths = int(request.form.get("red_jungle_deaths", 0))
    red_jungle_assists = int(request.form.get("red_jungle_assists", 0))

    # 레드팀 MID
    red_mid = request.form.get("red_mid")
    red_mid_champion = request.form.get("red_mid_champion")
    red_mid_kills = int(request.form.get("red_mid_kills", 0))
    red_mid_deaths = int(request.form.get("red_mid_deaths", 0))
    red_mid_assists = int(request.form.get("red_mid_assists", 0))

    # 레드팀 ADC
    red_adc = request.form.get("red_adc")
    red_adc_champion = request.form.get("red_adc_champion")
    red_adc_kills = int(request.form.get("red_adc_kills", 0))
    red_adc_deaths = int(request.form.get("red_adc_deaths", 0))
    red_adc_assists = int(request.form.get("red_adc_assists", 0))

    # 레드팀 SUPPORT
    red_support = request.form.get("red_support")
    red_support_champion = request.form.get("red_support_champion")
    red_support_kills = int(request.form.get("red_support_kills", 0))
    red_support_deaths = int(request.form.get("red_support_deaths", 0))
    red_support_assists = int(request.form.get("red_support_assists", 0))

    # 승리 팀
    winner = request.form.get("winner")

    # UPDATE 쿼리 실행
    update_sql = """
        UPDATE matches SET
            match_date = %s,

            blue_top = %s, blue_top_champion = %s, blue_top_kills = %s, blue_top_deaths = %s, blue_top_assists = %s,
            blue_jungle = %s, blue_jungle_champion = %s, blue_jungle_kills = %s, blue_jungle_deaths = %s, blue_jungle_assists = %s,
            blue_mid = %s, blue_mid_champion = %s, blue_mid_kills = %s, blue_mid_deaths = %s, blue_mid_assists = %s,
            blue_adc = %s, blue_adc_champion = %s, blue_adc_kills = %s, blue_adc_deaths = %s, blue_adc_assists = %s,
            blue_support = %s, blue_support_champion = %s, blue_support_kills = %s, blue_support_deaths = %s, blue_support_assists = %s,

            red_top = %s, red_top_champion = %s, red_top_kills = %s, red_top_deaths = %s, red_top_assists = %s,
            red_jungle = %s, red_jungle_champion = %s, red_jungle_kills = %s, red_jungle_deaths = %s, red_jungle_assists = %s,
            red_mid = %s, red_mid_champion = %s, red_mid_kills = %s, red_mid_deaths = %s, red_mid_assists = %s,
            red_adc = %s, red_adc_champion = %s, red_adc_kills = %s, red_adc_deaths = %s, red_adc_assists = %s,
            red_support = %s, red_support_champion = %s, red_support_kills = %s, red_support_deaths = %s, red_support_assists = %s,

            winner = %s
        WHERE id = %s
    """

    values = (
        match_date,

        blue_top, blue_top_champion, blue_top_kills, blue_top_deaths, blue_top_assists,
        blue_jungle, blue_jungle_champion, blue_jungle_kills, blue_jungle_deaths, blue_jungle_assists,
        blue_mid, blue_mid_champion, blue_mid_kills, blue_mid_deaths, blue_mid_assists,
        blue_adc, blue_adc_champion, blue_adc_kills, blue_adc_deaths, blue_adc_assists,
        blue_support, blue_support_champion, blue_support_kills, blue_support_deaths, blue_support_assists,

        red_top, red_top_champion, red_top_kills, red_top_deaths, red_top_assists,
        red_jungle, red_jungle_champion, red_jungle_kills, red_jungle_deaths, red_jungle_assists,
        red_mid, red_mid_champion, red_mid_kills, red_mid_deaths, red_mid_assists,
        red_adc, red_adc_champion, red_adc_kills, red_adc_deaths, red_adc_assists,
        red_support, red_support_champion, red_support_kills, red_support_deaths, red_support_assists,

        winner,
        match_id
    )

    cur.execute(update_sql, values)
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("record_bp.history"))

# 경기 삭제 기능 추가
@record_bp.route("/delete_match/<int:match_id>", methods=["POST"])
def delete_match(match_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM matches WHERE id = %s", (match_id,))
    conn.commit()
    
    cur.close()
    conn.close()
    
    return redirect(url_for("record_bp.history"))