import pytest, json
from uuid import UUID
from src.routes import app
from datetime import datetime
from flask.testing import FlaskClient
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


class TestUserController:
    @pytest.fixture(scope="class", autouse=True)
    def client(self):
        with app.test_client() as client:
            yield client

    @pytest.fixture(scope="class")
    def params(self):
        return {"token": None, "user_id": None}

    def test_login_without_body(self, client: FlaskClient):
        res = client.post("/login")
        data = json.loads(res.get_data(as_text=True))
        assert res.status_code == 400
        assert data["message"] == "O corpo informado não é um json válido"

    def test_login_body_without_email(self, client: FlaskClient):
        res = client.post("/login", json={})
        data = json.loads(res.get_data(as_text=True))
        assert res.status_code == 400
        assert data["message"] == "O campo obrigatório 'email' não foi encontrado"

    def test_login_body_without_password(self, client: FlaskClient):
        res = client.post("/login", json={"email": "root@root.com"})
        data = json.loads(res.get_data(as_text=True))
        assert res.status_code == 400
        assert data["message"] == "O campo obrigatório 'password' não foi encontrado"

    def test_login_invalid_credentials(self, client: FlaskClient):
        res = client.post("/login", json={"email": "root@root.com", "password": "root"})
        data = json.loads(res.get_data(as_text=True))
        assert res.status_code == 500
        assert data["message"] == "Usuário ou senha inválidos"

    def test_not_auth(self, client: FlaskClient):
        res = client.get("/auth")
        data = json.loads(res.get_data(as_text=True))
        assert res.status_code == 401
        assert data["message"] == "Você não está logado no sistema"

    def test_success_login(self, client: FlaskClient, params: dict):
        res = client.post("/login", json={"email": "bruno.19ls@gmail.com", "password": "Lambaroso1"})
        data = json.loads(res.get_data(as_text=True))
        params["token"] = data["data"]["token"]
        params["user_id"] = data["data"]["user_data"]["user_id"]
        assert res.status_code == 200
        assert data["message"] == ""

    def test_is_auth(self, client: FlaskClient, params: dict):
        client.set_cookie("token", params["token"])
        client.set_cookie("user_id", params["user_id"])
        res = client.get("/auth")
        data = json.loads(res.get_data(as_text=True))
        assert res.status_code == 200
        assert data["message"] == ""

    def test_request_recover_invalid_email(self, client: FlaskClient):
        res = client.post("/recover", json={"email": "bruno19ls@gmail.com"})
        data = json.loads(res.get_data(as_text=True))
        assert res.status_code == 500
        assert data["message"] == "O usuário não foi encontrado"

    def test_request_recover(self, client: FlaskClient):
        res = client.post("/recover", json={"email": "bruno.19ls@gmail.com"})
        data = json.loads(res.get_data(as_text=True))
        assert res.status_code == 200
        assert data["message"] == ""

    def test_change_password_by_request_invalid_body(self, client: FlaskClient):
        res = client.put("/recover", json={})
        data = json.loads(res.get_data(as_text=True))
        assert res.status_code == 400
        assert data["message"] == "O campo obrigatório 'password' não foi encontrado"

        res = client.put("/recover", json={"password": "lambari"})
        data = json.loads(res.get_data(as_text=True))
        assert res.status_code == 400
        assert data["message"] == "O campo obrigatório 'repeat_password' não foi encontrado"

        res = client.put("/recover", json={"password": "lambari", "repeat_password": "lambaroso"})
        data = json.loads(res.get_data(as_text=True))
        assert res.status_code == 400
        assert data["message"] == "O campo obrigatório 'recover_id' não foi encontrado"

    def test_change_password_by_request_invalid_password(self, client: FlaskClient):
        recover_id = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
        body = {"password": "lambari", "repeat_password": "lambaroso", "recover_id": recover_id}

        res = client.put("/recover", json=body)
        data = json.loads(res.get_data(as_text=True))
        assert res.status_code == 400
        assert data["message"] == "As senhas não são iguais"

        body["repeat_password"] = body["password"]
        res = client.put("/recover", json=body)
        data = json.loads(res.get_data(as_text=True))
        assert res.status_code == 400
        assert data["message"] == "A senha deve ter ao menos 8 caracteres"

        body["password"] = "lambaroso"
        body["repeat_password"] = body["password"]
        res = client.put("/recover", json=body)
        data = json.loads(res.get_data(as_text=True))
        assert res.status_code == 400
        assert data["message"] == "A senha deve ter ao menos 1 caractere maiúsculo"

        body["password"] = "Lambaroso"
        body["repeat_password"] = body["password"]
        res = client.put("/recover", json=body)
        data = json.loads(res.get_data(as_text=True))
        assert res.status_code == 400
        assert data["message"] == "A senha deve ter ao menos 1 número"
