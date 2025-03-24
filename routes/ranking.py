from flask import Blueprint, render_template
import psycopg2
import os
from collections import defaultdict

ranking_bp = Blueprint("ranking_bp", __name__)

def get_db_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])

@ranking_bp.route("/ranking")
def ranking():
    conn = get_db_connection()
    cur = conn.cursor()
    # 모든 매치 정보 조회
    cur.execute("SELECT * FROM matches")
    all_matches = cur.fetchall()
    cur.close()
    conn.close()

    # 플레이어별 통계를 저장할 딕셔너리
    # 예: stats_map[player_name] = {
    #   'games': 0,
    #   'wins': 0,
    #   'kills': 0,
    #   'deaths': 0,
    #   'assists': 0,
    #   'champion_count': defaultdict(int),
    #   'position_count': defaultdict(int)
    # }
    stats_map = defaultdict(lambda: {
        'games': 0,
        'wins': 0,
        'kills': 0,
        'deaths': 0,
        'assists': 0,
        'champion_count': defaultdict(int),
        'position_count': defaultdict(int)
    })

    for match in all_matches:
        # match 테이블 구조 예시 (id, match_date, blue_top, blue_top_champion, ...)
        # 인덱스는 실제 DB 컬럼 순서에 맞춰 조정해야 합니다.
        # 예) match[1] = match_date
        #     match[2] = blue_top, match[3] = blue_jungle, ...
        #     match[?] = winner

        # 아래는 가정(예: match[12] = winner). 실제 인덱스는 DB 컬럼 순서와 일치시켜야 함.
        winner = match[52]  # 예: 'blue' or 'red' (인덱스는 예시)

        # 예를 들어, blue_top = match[2], blue_top_champion = match[3], kills = match[4], ...
        # 실제 인덱스를 match 테이블 구조와 맞춰 주세요.

        # -- 블루팀 5명 --
        # (포지션명, (플레이어, 챔피언, kills, deaths, assists)) 형태로 묶어서 반복
        blue_positions = [
            ("TOP",    (match[2], match[3], match[4], match[5], match[6])),
            ("JUNGLE", (match[7], match[8], match[9], match[10], match[11])),
            ("MID",    (match[12], match[13], match[14], match[15], match[16])),
            ("ADC",    (match[17], match[18], match[19], match[20], match[21])),
            ("SUPPORT",(match[22], match[23], match[24], match[25], match[26]))
        ]

        # -- 레드팀 5명 --
        red_positions = [
            ("TOP",    (match[27], match[28], match[29], match[30], match[31])),
            ("JUNGLE", (match[32], match[33], match[34], match[35], match[36])),
            ("MID",    (match[37], match[38], match[39], match[40], match[41])),
            ("ADC",    (match[42], match[43], match[44], match[45], match[46])),
            ("SUPPORT",(match[47], match[48], match[49], match[50], match[51]))
        ]

        # 블루팀 처리
        for pos, (player, champion, kills, deaths, assists) in blue_positions:
            stats_map[player]['games'] += 1
            stats_map[player]['kills'] += kills
            stats_map[player]['deaths'] += deaths
            stats_map[player]['assists'] += assists
            stats_map[player]['champion_count'][champion] += 1
            stats_map[player]['position_count'][pos] += 1

            # 승리 판단
            if winner == 'blue':
                stats_map[player]['wins'] += 1

        # 레드팀 처리
        for pos, (player, champion, kills, deaths, assists) in red_positions:
            stats_map[player]['games'] += 1
            stats_map[player]['kills'] += kills
            stats_map[player]['deaths'] += deaths
            stats_map[player]['assists'] += assists
            stats_map[player]['champion_count'][champion] += 1
            stats_map[player]['position_count'][pos] += 1

            if winner == 'red':
                stats_map[player]['wins'] += 1

    # 이제 stats_map을 기반으로 최종 승률, 최다 챔피언, 주 포지션, 평균 KDA 등을 계산
    ranking_data = []
    for player, stats in stats_map.items():
        games = stats['games']
        wins = stats['wins']
        kills = stats['kills']
        deaths = stats['deaths']
        assists = stats['assists']

        if games > 0:
            win_rate = 100.0 * wins / games
        else:
            win_rate = 0.0

        if deaths == 0:
            avg_kda = kills + assists  # deaths가 0이면 kda를 kills+assists로 처리
        else:
            avg_kda = (kills + assists) / deaths

        # 최다 챔피언
        if stats['champion_count']:
            favorite_champion = max(stats['champion_count'], key=stats['champion_count'].get)
        else:
            favorite_champion = None

        # 주 포지션
        if stats['position_count']:
            favorite_position = max(stats['position_count'], key=stats['position_count'].get)
        else:
            favorite_position = None

        ranking_data.append((
            player,
            games,
            wins,
            win_rate,
            favorite_champion,
            favorite_position,
            avg_kda
        ))

    # 승률 기준으로 내림차순 정렬
    ranking_data.sort(key=lambda x: x[3], reverse=True)

    return render_template("ranking.html", rankings=ranking_data)
