import os
import json
import pytest
from datetime import date
from src.routes import app
from dotenv import load_dotenv
from flask.testing import FlaskClient
from src.services.record import RecordDetails, RecordService


BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(f"{BASE_PATH}/config/.env")
track_test_data = {
    "user_id": "49fe6c42-b940-4122-906b-e95c7316e349",
    "item_id": "fb0b8338-63ab-4ccf-8ebf-8e4b2798b08a",
    "target_id": "24d3bbbc-20a2-4350-bf96-408501af4a4b",
    "origin_id": "7961fd02-ac54-458a-a9ae-e3d57241aa70",
    "record_id_service": "",
    "record_id_controller": ""
}


@pytest.fixture(scope="session", autouse=True)
def client():
    with app.test_client() as client:
        yield client


def test_service_new_record_with_details():
    details = [
        RecordDetails(description="Item A", value=56.69),
        RecordDetails(description="Item B", value=400)
    ]
    res = RecordService.new(
        track_test_data["user_id"],
        track_test_data["item_id"],
        track_test_data["target_id"],
        date(2022, 8, 3),
        "Movimentação de teste",
        456.69,
        details=details
    )
    track_test_data["record_id_service"] = res.record_id
    assert res.message == ""
    assert res.success


def test_service_get_records_with_details():
    res = RecordService.get_all(track_test_data["user_id"], page=1)
    assert res.message == ""
    assert len(res.records) == 1
    assert res.records[0]["id"] == track_test_data["record_id_service"]
    assert len(res.records[0]["details"]) == 2


def test_service_delete_record_with_detail():
    res = RecordService.delete(track_test_data["record_id_service"], track_test_data["user_id"])
    assert res.message == ""
    assert res.success


def test_service_new_record_without_details():
    res = RecordService.new(
        track_test_data["user_id"],
        track_test_data["item_id"],
        track_test_data["target_id"],
        date(2022, 8, 3),
        "Movimentação de teste",
        456.69
    )
    track_test_data["record_id_service"] = res.record_id
    assert res.message == ""
    assert res.success


def test_service_delete_record_without_detail():
    res = RecordService.delete(track_test_data["record_id_service"], track_test_data["user_id"])
    assert res.message == ""
    assert res.success


def test_service_new_record_with_origin():
    res = RecordService.new(
        track_test_data["user_id"],
        track_test_data["item_id"],
        track_test_data["target_id"],
        date(2022, 8, 3),
        "Movimentação de teste",
        456.69,
        origin_id=track_test_data["origin_id"]
    )
    track_test_data["record_id_service"] = res.record_id
    assert res.message == ""
    assert res.success


def test_service_update_record_remove_origin_alter_value():
    res = RecordService.edit(
        track_test_data["record_id_service"],
        track_test_data["user_id"],
        track_test_data["item_id"],
        track_test_data["target_id"],
        date(2022, 8, 3),
        "Movimentação de teste",
        123.45
    )
    assert res.message == ""
    assert res.success


def test_service_get_records_without_details():
    res = RecordService.get_all(track_test_data["user_id"], page=1)
    assert res.message == ""
    assert len(res.records) == 1
    assert res.records[0]["id"] == track_test_data["record_id_service"]
    assert len(res.records[0]["details"]) == 0


def test_service_get_records_next_page():
    res = RecordService.get_all(track_test_data["user_id"], page=2)
    assert res.message == ""
    assert len(res.records) == 0


def test_service_delete_record_with_origin():
    res = RecordService.delete(track_test_data["record_id_service"], track_test_data["user_id"])
    assert res.message == ""
    assert res.success


def test_controller_new_record_without_origin_and_with_details(client: FlaskClient):
    body = {
        "user_id": track_test_data["user_id"],
        "item_id": track_test_data["item_id"],
        "target_id": track_test_data["target_id"],
        "moviment_date": "2023-08-03",
        "description": "Movimentação de teste",
        "value": 456.69,
        "details": [
            {"description": "Item A", "value": 56.69},
            {"description": "Item B", "value": 400}
        ]
    }
    res = client.post("/record", json=body)
    data = json.loads(res.get_data(as_text=True))
    track_test_data["record_id_controller"] = data["data"]["record_id"]

    assert data["message"] == ""
    assert data["status_code"] == 200
    assert data["data"]["record_id"] != ""


def test_controller_edit_record_remove_details_and_add_origin(client: FlaskClient):
    body = {
        "record_id": track_test_data["record_id_controller"],
        "user_id": track_test_data["user_id"],
        "item_id": track_test_data["item_id"],
        "target_id": track_test_data["target_id"],
        "moviment_date": "2023-08-03",
        "description": "Movimentação de teste",
        "origin_id": track_test_data["origin_id"],
        "value": 300,
    }
    res = client.put("/record", json=body)
    data = json.loads(res.get_data(as_text=True))

    assert data["message"] == ""
    assert data["status_code"] == 200


def test_controller_delete_record_with_details(client: FlaskClient):
    body = {
        "user_id": track_test_data["user_id"],
        "record_id": track_test_data["record_id_controller"]
    }
    res = client.delete("/record", json=body)
    data = json.loads(res.get_data(as_text=True))

    assert data["message"] == ""
    assert data["status_code"] == 200


def test_controller_new_record_with_origin_and_without_details(client: FlaskClient):
    body = {
        "user_id": track_test_data["user_id"],
        "item_id": track_test_data["item_id"],
        "target_id": track_test_data["target_id"],
        "moviment_date": "2023-08-03",
        "description": "Movimentação de teste",
        "value": 456.69,
        "origin_id": track_test_data["origin_id"]
    }
    res = client.post("/record", json=body)
    data = json.loads(res.get_data(as_text=True))
    track_test_data["record_id_controller"] = data["data"]["record_id"]

    assert data["message"] == ""
    assert data["status_code"] == 200
    assert data["data"]["record_id"] != ""


def test_controller_edit_record_add_details_remove_origin(client: FlaskClient):
    body = {
        "record_id": track_test_data["record_id_controller"],
        "user_id": track_test_data["user_id"],
        "item_id": track_test_data["item_id"],
        "target_id": track_test_data["target_id"],
        "moviment_date": "2023-08-03",
        "description": "Movimentação de teste",
        "value": 300,
        "details": [
            {"description": "Item A", "value": 56.69},
            {"description": "Item B", "value": 400}
        ]
    }
    res = client.put("/record", json=body)
    data = json.loads(res.get_data(as_text=True))

    assert data["message"] == ""
    assert data["status_code"] == 200


def test_controller_delete_record_witout_details(client: FlaskClient):
    body = {
        "user_id": track_test_data["user_id"],
        "record_id": track_test_data["record_id_controller"]
    }
    res = client.delete("/record", json=body)
    data = json.loads(res.get_data(as_text=True))

    assert data["message"] == ""
    assert data["status_code"] == 200
