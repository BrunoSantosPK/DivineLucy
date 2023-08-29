import os
from dotenv import load_dotenv
from src.utils.execution import Execution
from src.controllers.user import UserController
from src.validations.user import UserValidation
from src.controllers.wallet import WalletController
from src.controllers.budget import BudgetController
from src.controllers.record import RecordController
from flask import Flask, render_template, Response, request
from src.controllers.classification_item import ClassificationItemController


BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(f"{BASE_PATH}/config/.env")
app = Flask(__name__)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return Execution.run(UserValidation.post_login, UserController.login)
    elif request.method == "GET":
        return render_template("login.html")
    

@app.route("/user", methods=["POST"])
def manager_user():
    return Execution.run(UserValidation.post_new, UserController.new)


@app.route("/recover", methods=["POST"])
def request_recover():
    return Execution.run(UserValidation.post_recover, UserController.recover_password)


@app.route("/", methods=["GET"])
def page_home():
    return render_template("index.html")


@app.route("/login", methods=["GET"])
def page_login():
    return render_template("login.html")


@app.route("/budget", methods=["GET"])
def page_budget():
    return render_template("budget.html")


@app.route("/transaction", methods=["GET"])
def page_action():
    return render_template("transaction.html")


@app.route("/wallets", methods=["POST"])
def create_wallet():
    result = WalletController.new()
    return Response(result.to_json(), result.get_status_code())


@app.route("/wallets/<user_id>", methods=["GET"])
def get_wallets(user_id: str):
    result = WalletController.get_all()
    return Response(result.to_json(), result.get_status_code())


@app.route("/budget", methods=["POST", "PUT", "DELETE"])
def manage_budget():
    result = None
    if request.method == "POST":
        result = BudgetController.new()
    elif request.method == "PUT":
        result = BudgetController.edit()
    elif request.method == "DELETE":
        result = BudgetController.delete()
    return Response(result.to_json(), result.get_status_code())


@app.route("/budget/<user_id>", methods=["GET"])
def get_budgets(user_id: str):
    result = BudgetController.get_all()
    return Response(result.to_json(), result.get_status_code())


@app.route("/item/<user_id>", methods=["GET"])
def get_items(user_id: str):
    result = ClassificationItemController.get_all()
    return Response(result.to_json(), result.get_status_code())


@app.route("/item", methods=["POST", "DELETE"])
def manage_items():
    result = None
    if request.method == "POST":
        result = ClassificationItemController.new()
    elif request.method == "DELETE":
        result = ClassificationItemController.delete()
    return Response(result.to_json(), result.get_status_code())


@app.route("/record", methods=["POST", "PUT", "DELETE"])
def get_records():
    result = None
    if request.method == "POST":
        result = RecordController.new()
    elif request.method == "PUT":
        result = RecordController.edit()
    elif request.method == "DELETE":
        result = RecordController.delete()
    return Response(result.to_json(), result.get_status_code())


@app.route("/record/<user_id>", methods=["GET"])
def manage_records(user_id: str):
    result = RecordController.get_all()
    return Response(result.to_json(), result.get_status_code())
