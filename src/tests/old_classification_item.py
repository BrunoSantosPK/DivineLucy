import os
import json
import pytest
from src.routes import app
from dotenv import load_dotenv
from flask.testing import FlaskClient
from src.services.classification_item import ClassificationItemService


BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(f"{BASE_PATH}/config/.env")
track_test_data = {
    "user_id": "49fe6c42-b940-4122-906b-e95c7316e349",
    "item_id": "",
    "item_id_controller": ""
}


@pytest.fixture(scope="session", autouse=True)
def client():
    with app.test_client() as client:
        yield client


def test_service_create_item():
    item_id, message = ClassificationItemService.new(track_test_data["user_id"], "Item novo")
    track_test_data["item_id"] = item_id
    assert message == ""
    assert item_id != ""


def test_service_create_item_same_name():
    item_id, message = ClassificationItemService.new(track_test_data["user_id"], "Item novo")
    assert message == "Você já possui um item com este nome"
    assert item_id == ""


def test_service_get_items():
    items, message = ClassificationItemService.get_all(track_test_data["user_id"])
    assert message == ""
    assert len(items) == 12


def test_service_delete_item():
    message = ClassificationItemService.delete(track_test_data["item_id"], track_test_data["user_id"])
    assert message == ""


def test_controller_create_item(client: FlaskClient):
    body = {"user_id": track_test_data["user_id"], "name": "Item novo"}
    res = client.post("/item", json=body)
    data = json.loads(res.get_data(as_text=True))
    track_test_data["item_id_controller"] = data["data"]["item_id"]

    assert data["message"] == ""
    assert data["status_code"] == 200
    assert data["data"]["item_id"] != ""


def test_controller_create_item_same_name(client: FlaskClient):
    body = {"user_id": track_test_data["user_id"], "name": "Item novo"}
    res = client.post("/item", json=body)
    data = json.loads(res.get_data(as_text=True))

    assert data["message"] == "Você já possui um item com este nome"
    assert data["status_code"] == 500
    assert data["data"] == None


def test_controller_get_items(client: FlaskClient):
    res = client.get(f"/item/{track_test_data['user_id']}")
    data = json.loads(res.get_data(as_text=True))

    assert data["message"] == ""
    assert data["status_code"] == 200
    assert len(data["data"]) == 12


def test_controller_delete_item(client: FlaskClient):
    body = {"item_id": track_test_data["item_id_controller"], "user_id": track_test_data["user_id"]}
    res = client.delete("/item", json=body)
    data = json.loads(res.get_data(as_text=True))

    assert data["message"] == ""
    assert data["status_code"] == 200
    assert data["data"] == None
