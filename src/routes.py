import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template


BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(f"{BASE_PATH}/config/.env")
app = Flask(__name__)


@app.route("/", methods=["GET"])
def page_home():
    return render_template("index.html")
