import os
import json
import pytest
from src.routes import app
from dotenv import load_dotenv
from flask.testing import FlaskClient
from src.services.wallet import WalletService


BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(f"{BASE_PATH}/config/.env")
track_test_data = {
    "user_id": "49fe6c42-b940-4122-906b-e95c7316e349"
}


@pytest.fixture(scope="session", autouse=True)
def client():
    with app.test_client() as client:
        yield client


def test_service_create_wallet():
    wallet_id, message = WalletService.new("Carteira de Bolso", track_test_data["user_id"])
    track_test_data["wallet_id"] = wallet_id
    assert wallet_id != ""
    assert message == ""


def test_service_create_wallet_same_name():
    wallet_id, message = WalletService.new("Carteira de Bolso", track_test_data["user_id"])
    assert wallet_id == ""
    assert message == "Você já tem uma conta com este nome"


def test_controller_create_wallet_same_name(client: FlaskClient):
    body = {"name": "Carteira de Bolso", "user_id": track_test_data["user_id"]}
    res = client.post("/wallets", json=body)
    data = json.loads(res.get_data(as_text=True))
    assert data["status_code"] == 500
    assert data["message"] == "Você já tem uma conta com este nome"


def test_service_get_wallets():
    data, message = WalletService.get_all(track_test_data["user_id"])
    assert len(data) == 1
    assert message == ""


def test_controller_get_wallets(client: FlaskClient):
    res = client.get(f"/wallets/{track_test_data['user_id']}")
    data = json.loads(res.get_data(as_text=True))
    assert data["message"] == ""
    assert data["status_code"] == 200
    assert len(data["data"]) == 1


def test_service_delete_wallet():
    result, message = WalletService.delete(track_test_data["wallet_id"])
    assert result
    assert message == ""


def test_service_get_null_wallets():
    data, message = WalletService.get_all(track_test_data["user_id"])
    assert len(data) == 0
    assert message == ""
