import os
from dotenv import load_dotenv
from flask import Flask, render_template


BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(f"{BASE_PATH}/config/.env")
app = Flask(__name__)


@app.route("/", methods=["GET"])
def page_home():
    return render_template("index.html")


@app.route("/login", methods=["GET"])
def page_login():
    return render_template("login.html")


@app.route("/budget", methods=["GET"])
def page_budget():
    return render_template("budget.html")


@app.route("/action", methods=["GET"])
def page_action():
    return render_template("action.html")
