# routes/team_balance.py
from flask import Blueprint, render_template, request, jsonify
import psycopg2
import os
from collections import defaultdict
import itertools

team_balance_bp = Blueprint("team_balance_bp", __name__)

def get_db_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])

def calculate_player_stats():
    """플레이어의 승률, KDA, 포지션 기록을 계산"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 모든 경기 기록 가져오기
    cur.execute("SELECT * FROM matches")
    all_matches = cur.fetchall()
    
    # 플레이어별 통계 정보를 저장할 딕셔너리
    player_stats = defaultdict(lambda: {
        'games': 0,
        'wins': 0,
        'kills': 0,
        'deaths': 0,
        'assists': 0,
        'positions': defaultdict(int)
    })
    
    # 경기 기록을 순회하며 통계 정보 수집
    for match in all_matches:
        winner = match[52]  # 승리 팀 정보
        
        # 블루팀 처리
        blue_positions = [
            ("TOP", (match[2], match[4], match[5], match[6])),  # player, kills, deaths, assists
            ("JUNGLE", (match[7], match[9], match[10], match[11])),
            ("MID", (match[12], match[14], match[15], match[16])),
            ("ADC", (match[17], match[19], match[20], match[21])),
            ("SUPPORT", (match[22], match[24], match[25], match[26]))
        ]
        
        # 레드팀 처리
        red_positions = [
            ("TOP", (match[27], match[29], match[30], match[31])),
            ("JUNGLE", (match[32], match[34], match[35], match[36])),
            ("MID", (match[37], match[39], match[40], match[41])),
            ("ADC", (match[42], match[44], match[45], match[46])),
            ("SUPPORT", (match[47], match[49], match[50], match[51]))
        ]
        
        # 블루팀 플레이어 통계 업데이트
        for position, (player, kills, deaths, assists) in blue_positions:
            player_stats[player]['games'] += 1
            player_stats[player]['kills'] += kills
            player_stats[player]['deaths'] += deaths
            player_stats[player]['assists'] += assists
            player_stats[player]['positions'][position] += 1
            
            if winner == 'blue':
                player_stats[player]['wins'] += 1
        
        # 레드팀 플레이어 통계 업데이트
        for position, (player, kills, deaths, assists) in red_positions:
            player_stats[player]['games'] += 1
            player_stats[player]['kills'] += kills
            player_stats[player]['deaths'] += deaths
            player_stats[player]['assists'] += assists
            player_stats[player]['positions'][position] += 1
            
            if winner == 'red':
                player_stats[player]['wins'] += 1
    
    # 승률 및 KDA 계산하여 최종 통계 정보 생성
    final_stats = {}
    for player, stats in player_stats.items():
        win_rate = (stats['wins'] / stats['games'] * 100) if stats['games'] > 0 else 0
        kda = ((stats['kills'] + stats['assists']) / stats['deaths']) if stats['deaths'] > 0 else (stats['kills'] + stats['assists'])
        
        # 포지션 정보 정리
        positions = dict(stats['positions'])
        main_positions = sorted(positions.items(), key=lambda x: x[1], reverse=True)
        
        final_stats[player] = {
            'games': stats['games'],
            'wins': stats['wins'],
            'win_rate': round(win_rate, 2),
            'kda': round(kda, 2),
            'positions': positions,
            'main_positions': [pos for pos, count in main_positions if count > 0]
        }
    
    cur.close()
    conn.close()
    
    return final_stats

@team_balance_bp.route("/team_balance", methods=["GET"])
def team_balance():
    # 플레이어 통계 정보 계산
    player_stats = calculate_player_stats()
    
    # 승률 기준으로 플레이어 정렬
    sorted_players = sorted(player_stats.items(), key=lambda x: x[1]['win_rate'], reverse=True)
    
    return render_template(
        "team_balance.html", 
        players=sorted_players,
        player_stats=player_stats
    )

def get_zigzag_teams(selected_players, player_stats):
    """지그재그 방식으로 팀 구성"""
    # 선택된 플레이어만 필터링
    selected_stats = {player: player_stats[player] for player in selected_players if player in player_stats}
    
    # 승률 기준으로 정렬
    sorted_players = sorted(selected_stats.items(), key=lambda x: x[1]['win_rate'], reverse=True)
    sorted_players = [player for player, _ in sorted_players]
    
    # 팀 A와 팀 B 구성 (지그재그 방식)
    team_a = []
    team_b = []
    
    for i, player in enumerate(sorted_players):
        # 지그재그 패턴에 따라 팀 분배
        # 1, 4, 5, 8, 9... -> 팀 A
        # 2, 3, 6, 7, 10... -> 팀 B
        if i % 4 == 0 or i % 4 == 3:
            team_a.append(player)
        else:
            team_b.append(player)
    
    # 각 팀의 평균 승률 계산
    team_a_win_rate = sum(player_stats[player]['win_rate'] for player in team_a) / len(team_a) if team_a else 0
    team_b_win_rate = sum(player_stats[player]['win_rate'] for player in team_b) / len(team_b) if team_b else 0
    
    # 팀 정보 반환
    return {
        "team_a": {
            "players": team_a,
            "avg_win_rate": round(team_a_win_rate, 2)
        },
        "team_b": {
            "players": team_b,
            "avg_win_rate": round(team_b_win_rate, 2)
        },
        "win_rate_diff": round(abs(team_a_win_rate - team_b_win_rate), 2)
    }

@team_balance_bp.route("/api/balanced_teams", methods=["POST"])
def balanced_teams():
    """10명의 플레이어로 두 가지 방식의 팀 구성 결과 제공"""
    selected_players = request.json.get('players', [])
    
    if len(selected_players) != 10:
        return jsonify({"error": "정확히 10명의 플레이어를 선택해야 합니다."}), 400
    
    # 플레이어 통계 정보 계산
    player_stats = calculate_player_stats()
    
    # 1. 지그재그 방식 팀 구성
    zigzag_result = get_zigzag_teams(selected_players, player_stats)

def get_min_diff_teams(selected_players, player_stats):
    """승률 차이를 최소화하는 팀 구성"""
    # 선택된 플레이어만 필터링
    selected_stats = {player: player_stats[player] for player in selected_players if player in player_stats}
    
    # 팀 수가 홀수면 빈 결과 반환
    if len(selected_stats) % 2 != 0:
        return None
    
    # 최적의 팀 구성 찾기
    team_size = len(selected_stats) // 2
    min_diff = float('inf')
    best_teams = ([], [])
    
    # 모든 가능한 팀 조합 탐색
    for team_a_players in itertools.combinations(selected_stats.keys(), team_size):
        team_a = list(team_a_players)
        team_b = [p for p in selected_stats if p not in team_a]
        
        # 각 팀의 평균 승률 계산
        team_a_win_rate = sum(selected_stats[p]['win_rate'] for p in team_a) / team_size
        team_b_win_rate = sum(selected_stats[p]['win_rate'] for p in team_b) / team_size
        
        # 승률 차이 계산
        diff = abs(team_a_win_rate - team_b_win_rate)
        
        # 최소 차이 업데이트
        if diff < min_diff:
            min_diff = diff
            best_teams = (team_a, team_b)
    
    team_a, team_b = best_teams
    team_a_win_rate = sum(selected_stats[p]['win_rate'] for p in team_a) / team_size
    team_b_win_rate = sum(selected_stats[p]['win_rate'] for p in team_b) / team_size
    
    # 팀 정보 반환
    return {
        "team_a": {
            "players": team_a,
            "avg_win_rate": round(team_a_win_rate, 2)
        },
        "team_b": {
            "players": team_b,
            "avg_win_rate": round(team_b_win_rate, 2)
        },
        "win_rate_diff": round(min_diff, 2)
    }

@team_balance_bp.route("/api/balanced_teams", methods=["POST"])
def balanced_teams():
    """10명의 플레이어로 두 가지 방식의 팀 구성 결과 제공"""
    selected_players = request.json.get('players', [])
    
    if len(selected_players) != 10:
        return jsonify({"error": "정확히 10명의 플레이어를 선택해야 합니다."}), 400
    
    # 플레이어 통계 정보 계산
    player_stats = calculate_player_stats()
    
    # 1. 지그재그 방식 팀 구성
    zigzag_result = get_zigzag_teams(selected_players, player_stats)
    
    # 2. 승률 차이 최소화 방식
    min_diff_result = get_min_diff_teams(selected_players, player_stats)
    
    # 두 방식의 결과를 모두 반환
    return jsonify({
        "zigzag": zigzag_result,
        "min_diff": min_diff_result
    })