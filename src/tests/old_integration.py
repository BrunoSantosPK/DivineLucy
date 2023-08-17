import os
from datetime import date
from src.routes import app
from dotenv import load_dotenv
from src.services.record import RecordService
from src.services.wallet import WalletService
from src.services.budget import BudgetService


BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(f"{BASE_PATH}/config/.env")
track_test_data = {
    "user_id": "49fe6c42-b940-4122-906b-e95c7316e349",
    "item_id": "fb0b8338-63ab-4ccf-8ebf-8e4b2798b08a",
    "target_id": "24d3bbbc-20a2-4350-bf96-408501af4a4b",
    "records": [],
    "budgets": []
}

def test_calc_records():
    res = RecordService.new(
        track_test_data["user_id"],
        track_test_data["item_id"],
        track_test_data["target_id"],
        date(2022, 1, 1),
        "Depósito 1",
        100
    )
    track_test_data["records"].append(res.record_id)

    res = RecordService.new(
        track_test_data["user_id"],
        track_test_data["item_id"],
        track_test_data["target_id"],
        date(2022, 1, 1),
        "Depósito 1",
        150
    )
    track_test_data["records"].append(res.record_id)

    res = RecordService.new(
        track_test_data["user_id"],
        track_test_data["item_id"],
        track_test_data["target_id"],
        date(2022, 2, 1),
        "Saque 1",
        -30
    )
    track_test_data["records"].append(res.record_id)

    data, _ = WalletService.get_all(track_test_data["user_id"])
    comp = None
    for d in data:
        if d["id"] == track_test_data["target_id"]:
            comp = d

    assert comp["total_income"] == 250
    assert comp["total_outcome"] == -30
    assert comp["current_value"] == 220


def test_calc_budgets():
    budget_id, _ = BudgetService.new(track_test_data["user_id"], 2022, 1, track_test_data["item_id"], 100)
    track_test_data["budgets"].append(budget_id)

    budget_id, _ = BudgetService.new(track_test_data["user_id"], 2022, 2, track_test_data["item_id"], 50)
    track_test_data["budgets"].append(budget_id)

    data, _ = BudgetService.get_all(track_test_data["user_id"], 2022, 1)
    assert data[0]["real"] == 250
    assert data[0]["real"] > 100

    data, _ = BudgetService.get_all(track_test_data["user_id"], 2022, 2)
    assert data[0]["real"] == 30
    assert data[0]["real"] < 50


def test_remove_records_and_budgets():
    for record_id in track_test_data["records"]:
        RecordService.delete(record_id, track_test_data["user_id"])

    for budget_id in track_test_data["budgets"]:
        BudgetService.delete(budget_id)
