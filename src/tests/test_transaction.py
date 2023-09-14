import pytest
from datetime import date
from uuid import UUID, uuid4
from src.services.record import RecordDetails, RecordService


def is_uuid(value: str):
    try:
        UUID(value)
        return True
    except:
        return False


class TestTransactionService:
    user_id = "b334d4ee-b95a-462e-bc7a-b19ec2e242dd"
    item_id = "fb0b8338-63ab-4ccf-8ebf-8e4b2798b08a"
    target_id = "24d3bbbc-20a2-4350-bf96-408501af4a4b"
    origin_id = "7961fd02-ac54-458a-a9ae-e3d57241aa70"

    @pytest.fixture(scope="class")
    def track_data(self) -> dict:
        return {"record_id_simple": None, "record_id_detail": None}

    def test_new_record_withoud_details(self, track_data):
        moviment_date = date(2023, 9, 14)
        description = "Registro de teste"
        value = 250
        result = RecordService.new(self.user_id, self.item_id, self.target_id, moviment_date, description, value, origin_id=None, details=[])
        track_data["record_id_simple"] = result.record_id

        assert result.success
        assert is_uuid(result.record_id)

    def test_new_record_with_details_and_origin(self, track_data):
        record_date = date(2023, 9, 13)
        description = "Registro de teste"
        value = 250
        details = [RecordDetails("Item 1", 200), RecordDetails("Item 2", 50)]
        result = RecordService.new(self.user_id, self.item_id, self.target_id, record_date, description, value, origin_id=self.origin_id, details=details)
        track_data["record_id_detail"] = result.record_id
        assert result.success
        assert is_uuid(result.record_id)

    def test_get_records_page_1(self):
        result = RecordService.get_all(self.user_id, page=1)
        assert result.success
        assert len(result.records) == 2
        assert len(result.records[0]["details"]) == 0
        assert len(result.records[1]["details"]) == 2

    def test_get_records_page_2(self):
        result = RecordService.get_all(self.user_id, page=2)
        assert result.success
        assert len(result.records) == 0

    def test_edit_record_add_details(self, track_data):
        record_date = date(2023, 9, 14)
        description = "Registro de teste"
        value = 250
        details = [RecordDetails("Item 1", 250)]
        result = RecordService.edit(
            track_data["record_id_simple"], self.user_id, self.item_id, self.target_id,
            record_date, description, value, origin_id=None, details=details
        )
        assert result.success
        assert result.message == ""

        result = RecordService.get_all(self.user_id, page=1)
        assert len(result.records) == 2
        assert len(result.records[0]["details"]) == 1

    def test_edit_record_remove_details(self, track_data):
        record_date = date(2023, 9, 14)
        description = "Registro de teste"
        value = 250
        result = RecordService.edit(
            track_data["record_id_simple"], self.user_id, self.item_id, self.target_id,
            record_date, description, value, origin_id=None, details=[]
        )
        assert result.success
        assert result.message == ""

        result = RecordService.get_all(self.user_id, page=1)
        assert len(result.records) == 2
        assert len(result.records[0]["details"]) == 0

    def test_delete_transaction_invalid_user(self, track_data):
        result = RecordService.delete(track_data["record_id_simple"], str(uuid4()))
        assert not result.success
        assert result.message == "Registro não encontrado"

    def test_delete_transaction_invalid_record(self, track_data):
        result = RecordService.delete(str(uuid4()), self.user_id)
        assert not result.success
        assert result.message == "Registro não encontrado"

    def test_delete_transaction(self, track_data):
        result = RecordService.delete(track_data["record_id_simple"], self.user_id)
        assert result.success
        assert result.message == ""

    def test_delete_record_with_details(self, track_data):
        result = RecordService.delete(track_data["record_id_detail"], self.user_id)
        assert result.success
        assert result.message == ""


class TestTransactionController:
    pass
