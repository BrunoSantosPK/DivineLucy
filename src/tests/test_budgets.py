import os
import json
import pytest
from src.routes import app
from dotenv import load_dotenv
from flask.testing import FlaskClient
from src.services.budget import BudgetService


BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(f"{BASE_PATH}/config/.env")
track_test_data = {
    "user_id": "49fe6c42-b940-4122-906b-e95c7316e349",
    "item_id": "fb0b8338-63ab-4ccf-8ebf-8e4b2798b08a",
    "budget_id_service": "",
    "budget_id_controller": ""
}


@pytest.fixture(scope="session", autouse=True)
def client():
    with app.test_client() as client:
        yield client


def test_service_create_budget():
    budget_id, message = BudgetService.new(
        track_test_data["user_id"], 2023, 8,
        track_test_data["item_id"], 450
    )
    track_test_data["budget_id_service"] = budget_id
    assert message == ""
    assert budget_id != ""


def test_service_edit_budget():
    message = BudgetService.edit(
        track_test_data["budget_id_service"],
        track_test_data["item_id"], 400
    )
    assert message == ""


def test_service_delete_budget():
    result, message = BudgetService.delete(track_test_data["budget_id_service"])
    assert message == ""
    assert result


def test_controller_create_budget(client: FlaskClient):
    body = {
        "user_id": track_test_data["user_id"],
        "year": 2023,
        "month": 8,
        "item_id": track_test_data["item_id"],
        "value": 450
    }
    res = client.post("/budget", json=body)
    data = json.loads(res.get_data(as_text=True))
    track_test_data["budget_id_controller"] = data["data"]["budget_id"]

    assert data["message"] == ""
    assert data["status_code"] == 200
    assert data["data"]["budget_id"] != ""


def test_controller_edit_budget(client: FlaskClient):
    body = {
        "budget_id": track_test_data["budget_id_controller"],
        "item_id": track_test_data["item_id"],
        "value": 350
    }
    res = client.put("/budget", json=body)
    data = json.loads(res.get_data(as_text=True))

    assert data["message"] == ""
    assert data["status_code"] == 200
    assert data["data"] == None


def test_controller_delete_budget(client: FlaskClient):
    body = {"budget_id": track_test_data["budget_id_controller"]}
    res = client.delete("/budget", json=body)
    data = json.loads(res.get_data(as_text=True))

    assert data["message"] == ""
    assert data["status_code"] == 200
    assert data["data"] == None
