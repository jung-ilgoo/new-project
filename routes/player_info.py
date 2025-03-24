# routes/player_info.py
from flask import Blueprint, render_template, request
import psycopg2
import os
from collections import defaultdict

player_info_bp = Blueprint("player_info_bp", __name__)

def get_db_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])

@player_info_bp.route("/player_stats", methods=["GET", "POST"])
def player_stats():
    conn = get_db_connection()
    cur = conn.cursor()

    # 1) 모든 플레이어 목록 불러오기 (드롭다운용)
    cur.execute("SELECT player_name FROM players ORDER BY player_name")
    all_players = [row[0] for row in cur.fetchall()]

    # 사용자가 선택한 플레이어 (드롭다운에서 넘어온 값)
    selected_player = None
    if request.method == "POST":
        selected_player = request.form.get("selected_player")
    else:
        selected_player = request.args.get("player", None)

    # 초기화
    position_data = None
    champion_data = None
    teammate_data = None

    if selected_player:
        # 2) matches 테이블에서 모든 매치를 가져와서, 해당 플레이어의 전적을 분석
        cur.execute("SELECT * FROM matches")
        all_matches = cur.fetchall()

        # 포지션별 경기수 카운팅
        position_count_map = defaultdict(int)

        # 챔피언별 통계를 저장할 딕셔너리
        champion_stats = defaultdict(lambda: {
            "games": 0,
            "wins": 0,
            "losses": 0,
            "kills": 0,
            "deaths": 0,
            "assists": 0
        })

        # 팀메이트 정보를 저장할 딕셔너리
        teammate_stats = defaultdict(lambda: {
            "total_matches": 0,
            "wins": 0
        })

        for match in all_matches:
            winner = match[52]  # 'blue' or 'red' (가정)

            # 블루팀 5명 (포지션, (플레이어, 챔피언, kills, deaths, assists))
            blue_positions = [
                ("TOP",    (match[2],  match[3],  match[4],  match[5],  match[6])),
                ("JUNGLE", (match[7],  match[8],  match[9],  match[10], match[11])),
                ("MID",    (match[12], match[13], match[14], match[15], match[16])),
                ("ADC",    (match[17], match[18], match[19], match[20], match[21])),
                ("SUPPORT",(match[22], match[23], match[24], match[25], match[26]))
            ]
            # 레드팀 5명
            red_positions = [
                ("TOP",    (match[27], match[28], match[29], match[30], match[31])),
                ("JUNGLE", (match[32], match[33], match[34], match[35], match[36])),
                ("MID",    (match[37], match[38], match[39], match[40], match[41])),
                ("ADC",    (match[42], match[43], match[44], match[45], match[46])),
                ("SUPPORT",(match[47], match[48], match[49], match[50], match[51]))
            ]

            # 선택된 플레이어의 팀 찾기
            selected_player_team = None
            selected_player_teammates = []

            # 블루팀 분석
            if any(player_name == selected_player for _, (player_name, _, _, _, _) in blue_positions):
                selected_player_team = "blue"
                selected_player_teammates = [
                    player_name for _, (player_name, _, _, _, _) in blue_positions if player_name != selected_player
                ]
            # 레드팀 분석
            elif any(player_name == selected_player for _, (player_name, _, _, _, _) in red_positions):
                selected_player_team = "red"
                selected_player_teammates = [
                    player_name for _, (player_name, _, _, _, _) in red_positions if player_name != selected_player
                ]

            # 선수의 포지션과 챔피언 스탯 분석
            for team_positions in [blue_positions, red_positions]:
                for pos, (player_name, champion_name, kills, deaths, assists) in team_positions:
                    if player_name == selected_player:
                        # 포지션 카운트
                        position_count_map[pos] += 1
                        # 챔피언별 스탯
                        champion_stats[champion_name]["games"] += 1
                        champion_stats[champion_name]["kills"] += kills
                        champion_stats[champion_name]["deaths"] += deaths
                        champion_stats[champion_name]["assists"] += assists
                        # 승/패
                        if (selected_player_team == "blue" and winner == "blue") or \
                           (selected_player_team == "red" and winner == "red"):
                            champion_stats[champion_name]["wins"] += 1
                        else:
                            champion_stats[champion_name]["losses"] += 1

            # 팀메이트 승률 계산
            if selected_player_team:
                for teammate in selected_player_teammates:
                    teammate_stats[teammate]["total_matches"] += 1
                    if (selected_player_team == "blue" and winner == "blue") or \
                       (selected_player_team == "red" and winner == "red"):
                        teammate_stats[teammate]["wins"] += 1

        # 포지션 데이터
        position_data = dict(position_count_map)

        # 챔피언 데이터 준비
        champion_data_list = []
        for champ, st in champion_stats.items():
            games = st["games"]
            wins = st["wins"]
            losses = st["losses"]
            kills = st["kills"]
            deaths = st["deaths"]
            assists = st["assists"]

            # KDA 계산
            if deaths == 0:
                kda = kills + assists
            else:
                kda = round((kills + assists) / deaths, 2)

            champion_data_list.append({
                "champion": champ,
                "games": games,
                "wins": wins,
                "losses": losses,
                "kda": kda
            })

        # 게임 수 내림차순 정렬
        champion_data_list.sort(key=lambda x: x["games"], reverse=True)
        champion_data = champion_data_list

        # 팀메이트 데이터 준비
        teammate_data_list = []
        for teammate, stats in teammate_stats.items():
            if teammate != selected_player:
                win_rate = round((stats["wins"] / stats["total_matches"]) * 100, 2) if stats["total_matches"] > 0 else 0
                teammate_data_list.append({
                    "name": teammate,
                    "total_matches": stats["total_matches"],
                    "wins": stats["wins"],
                    "win_rate": win_rate
                })

        # 함께한 게임 수 내림차순 정렬
        teammate_data_list.sort(key=lambda x: x["total_matches"], reverse=True)
        teammate_data = teammate_data_list

    cur.close()
    conn.close()

    # 템플릿 렌더링
    return render_template(
        "player_stats.html",
        all_players=all_players,
        selected_player=selected_player,
        position_data=position_data,
        champion_data=champion_data,
        teammate_data=teammate_data
    )