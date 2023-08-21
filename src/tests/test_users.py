import pytest
from uuid import UUID
from datetime import datetime
from src.services.user import UserService


def is_uuid(value: str):
    try:
        UUID(value)
        return True
    except:
        return False


class TestUserService:
    email = "email@email.com"
    pw = "lambaroso"
    new_pw = "novasenha"

    @pytest.fixture(scope="class")
    def track_data(self):
        return {"user_id": None, "recover_id": None}
    
    def test_create_valid_user(self, track_data):
        result = UserService.create("Lambari", self.email, self.pw)
        track_data["user_id"] = result.user_id

        assert result.success
        assert result.user_id != ""
        assert is_uuid(result.user_id)

    def test_registered_email(self):
        email = "email@email.com"
        result = UserService.find_by_email(email)
        assert result.user_id is not None
        assert result.user_data is not None

    def test_create_with_registered_email(self):
        result = UserService.create("Lambari", self.email, self.pw)
        assert not result.success
        assert result.message == "O e-mail já está cadastrado"

    def test_invalid_password(self):
        result = UserService.find_by_email_and_password(self.email, self.pw + "ok")
        assert result.success
        assert result.user_id is None

    def test_invalid_email(self):
        result = UserService.find_by_email_and_password(self.email + "ok", self.pw)
        assert result.success
        assert result.user_id is None

    def test_invalid_email_and_password(self):
        result = UserService.find_by_email_and_password(self.email + "nok", self.pw + "ok")
        assert result.success
        assert result.user_id is None

    def test_valid_email_and_password(self, track_data):
        result = UserService.find_by_email_and_password(self.email, self.pw)
        assert result.success
        assert result.user_id == track_data["user_id"]

    def test_request_recover_token_invalid_email(self):
        result = UserService.request_recover(self.email + "ok")
        assert not result.success
        assert result.message == "O e-mail não foi encontrado"

    def test_request_recover_token_valid_email(self, track_data):
        result = UserService.request_recover(self.email)
        track_data["recover_id"] = result.recover_id
        assert result.success
        assert result.recover_id is not None
        assert is_uuid(result.recover_id)

    def test_not_find_recover_token(self, track_data):
        result = UserService.find_recover_by_id(track_data["user_id"])
        assert result.success
        assert result.recover_id is None

    def test_find_recover_token(self, track_data):
        result = UserService.find_recover_by_id(track_data["recover_id"])
        assert result.success
        assert result.recover_id is not None
        assert datetime.fromisoformat(result.recover_data.expire_at) > datetime.utcnow()

    def test_recover_invalid_token(self, track_data):
        result = UserService.change_password_by_recover(track_data["recover_id"] + "ok", self.new_pw)
        assert not result.success
        assert result.message == "Não foi encontrada a solicitação de recuperação de senha"

    def test_recover_change_password(self, track_data):
        result = UserService.change_password_by_recover(track_data["recover_id"], self.new_pw)
        assert result.success
        assert result.message == ""

    def test_recover_change_password_second_time(self, track_data):
        result = UserService.change_password_by_recover(track_data["recover_id"], self.new_pw)
        assert not result.success
        assert result.message == "Esta solicitação de recuperação já foi executada"

    def test_find_user_new_password_after_recover(self, track_data):
        result = UserService.find_by_email_and_password(self.email, self.new_pw)
        assert result.success
        assert result.user_id == track_data["user_id"]

    def test_change_password(self):
        result = UserService.change_password(self.email, self.new_pw, self.pw)
        assert result.success
        assert result.message == ""

    def test_find_user_old_password_after_change(self, track_data):
        result = UserService.find_by_email_and_password(self.email, self.pw)
        assert result.success
        assert result.user_id == track_data["user_id"]

    def test_delete_user(self, track_data):
        result = UserService.delete(track_data["user_id"])
        assert result.success
        assert result.message == ""
