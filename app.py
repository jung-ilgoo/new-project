import os
import psycopg2
from flask import Flask, render_template, Blueprint

# Blueprint import
from routes.main import main_bp
from routes.players import players_bp
from routes.champion import champion_bp
from routes.record import record_bp
from routes.ranking import ranking_bp
from routes.player_info import player_info_bp
from routes.team_balance import team_balance_bp

app = Flask(__name__)

app.register_blueprint(main_bp)
app.register_blueprint(players_bp)
app.register_blueprint(champion_bp)
app.register_blueprint(record_bp)
app.register_blueprint(ranking_bp)
app.register_blueprint(player_info_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
