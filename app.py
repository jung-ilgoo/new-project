import os
import psycopg2
from flask import Flask, render_template, Blueprint

# Blueprint import
from routes.main import main_bp
from routes.players import players_bp

app = Flask(__name__)

app.register_blueprint(main_bp)
app.register_blueprint(players_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
