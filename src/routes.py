import os
from dotenv import load_dotenv
from flask import Flask, request
from src.utils.execution import Execution
from src.validations.item import ItemValidator
from src.controllers.page import PageController
from src.controllers.user import UserController
from src.validations.user import UserValidation
from src.validations.budget import BudgetValidator
from src.validations.record import RecordValidator
from src.validations.wallet import WalletValidator
from src.controllers.wallet import WalletController
from src.controllers.budget import BudgetController
from src.controllers.record import RecordController
from src.controllers.classification_item import ClassificationItemController


BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(f"{BASE_PATH}/config/.env")
app = Flask(__name__)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return Execution.run(UserValidation.post_login, UserController.login)
    elif request.method == "GET":
        return Execution.run(PageController.to_login)
    

@app.route("/user", methods=["POST"])
def manager_user():
    return Execution.run(UserValidation.post_new, UserController.new)


@app.route("/recover", methods=["POST", "PUT"])
def request_recover():
    if request.method == "POST":
        return Execution.run(UserValidation.post_recover, UserController.recover_password)
    elif request.method == "PUT":
        return Execution.run(UserValidation.put_change_password_by_recover, UserController.change_password_by_recover)


@app.route("/recover/<recover_id>", methods=["GET"])
def page_recover(recover_id: str):
    return Execution.run(UserController.access_page_recover_password)


@app.route("/auth", methods=["GET"])
def verify_auth():
    return Execution.run(UserController.auth)


@app.route("/", methods=["GET"])
def page_home():
    return Execution.run(UserController.auth_redirect_login, PageController.to_home)


@app.route("/login", methods=["GET"])
def page_login():
    return Execution.run(PageController.to_login)


@app.route("/budget", methods=["GET"])
def page_budget():
    return Execution.run(UserController.auth_redirect_login, PageController.to_budget)


@app.route("/transaction", methods=["GET"])
def page_action():
    return Execution.run(UserController.auth_redirect_login, PageController.to_transactions)


@app.route("/wallets", methods=["POST"])
def create_wallet():
    return Execution.run(UserController.auth, WalletValidator.post_new, WalletController.new)


@app.route("/wallets/<user_id>", methods=["GET"])
def get_wallets(user_id: str):
    return Execution.run(UserController.auth, WalletController.get_all)


@app.route("/budget", methods=["POST", "PUT", "DELETE"])
def manage_budget():
    if request.method == "POST":
        return Execution.run(UserController.auth, BudgetValidator.post_new, BudgetController.new)
    elif request.method == "PUT":
        return Execution.run(UserController.auth, BudgetValidator.put_edit, BudgetController.edit)
    elif request.method == "DELETE":
        return Execution.run(UserController.auth, BudgetValidator.delete_remove, BudgetController.delete)


@app.route("/budget/<user_id>", methods=["GET"])
def get_budgets(user_id: str):
    return Execution.run(UserController.auth, BudgetController.get_all)


@app.route("/item/<user_id>", methods=["GET"])
def get_items(user_id: str):
    return Execution.run(UserController.auth, ClassificationItemController.get_all)


@app.route("/item", methods=["POST", "DELETE"])
def manage_items():
    if request.method == "POST":
        return Execution.run(UserController.auth, ItemValidator.post_new, ClassificationItemController.new)
    elif request.method == "DELETE":
        return Execution.run(UserController.auth, ItemValidator.delete_remove, ClassificationItemController.delete)


@app.route("/record", methods=["POST", "PUT", "DELETE"])
def get_records():
    if request.method == "POST":
        return Execution.run(UserController.auth, RecordValidator.post_new, RecordController.new)
    elif request.method == "PUT":
        return Execution.run(UserController.auth, RecordValidator.put_edit, RecordController.edit)
    elif request.method == "DELETE":
        return Execution.run(UserController.auth, RecordValidator.delete_remove, RecordController.delete)


@app.route("/record/<user_id>", methods=["GET"])
def manage_records(user_id: str):
    return Execution.run(UserController.auth, RecordController.get_all)
