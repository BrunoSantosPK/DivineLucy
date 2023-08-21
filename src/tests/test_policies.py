from uuid import uuid4
from src.policies.auth import AuthPolicy


config_policy = {
    "user_id": str(uuid4()),
    "jwt": "",
    "old_jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiMDcxNjQzNzEtNzRhZC00NDlmLWJjM2MtNGQxMzExM2M5NDI4IiwiZXhwIjoxNjkyMzc1NjMxfQ.hgSS0KJCsKwW4bFLEoyGhk90ygFHxlMRkbUThrBQqa8"
}


def test_valid_crypt():
    pw, cpw = "lambari", "8jQ615Sg$sVElkDR260*!cx^Fuf687c!6mJ000caqK4q22%%39Ry9j^gz90k5Xy7"
    result = AuthPolicy.crypt_pass(pw)
    assert result.get_status_code() == 200
    assert result.get_data() == cpw
    assert result.get_data() != pw


def test_generate_jwt():
    user_id = str(uuid4())
    result = AuthPolicy.generate_jwt(config_policy["user_id"])
    config_policy["jwt"] = result.get_data()

    assert result.get_status_code() == 200
    assert result.get_message() == ""
    assert AuthPolicy.is_jwt(config_policy["jwt"]).get_status_code() == 200


def test_decode_jwt():
    result = AuthPolicy.decode_jwt(config_policy["jwt"])
    assert result.get_data() == config_policy["user_id"]
    assert result.get_status_code() == 200
    assert result.get_message() == ""


def test_decode_invalid_jwt():
    result = AuthPolicy.decode_jwt("lambari")
    assert result.get_status_code() == 500
    assert result.get_message() == "O token de autenticação não é válido"


def test_decode_expired_jwt():
    result = AuthPolicy.decode_jwt(config_policy["old_jwt"])
    assert result.get_status_code() == 500
    assert result.get_message() == "Sua sessão expirou"


class TestPassword:
    def test_short_password(self):
        result = AuthPolicy.valid_password("lambari")
        assert result.get_status_code() == 500
        assert result.get_message() == "A senha deve ter ao menos 8 caracteres"

    def test_password_without_upper(self):
        result = AuthPolicy.valid_password("lambaroso")
        assert result.get_status_code() == 500
        assert result.get_message() == "A senha deve ter ao menos 1 caractere maiúsculo"

    def test_password_without_lower(self):
        result = AuthPolicy.valid_password("LAMBAROSO")
        assert result.get_status_code() == 500
        assert result.get_message() == "A senha deve ter ao menos 1 caractere minúsculo"

    def test_password_without_number(self):
        result = AuthPolicy.valid_password("Lambaroso")
        assert result.get_status_code() == 500
        assert result.get_message() == "A senha deve ter ao menos 1 número"

    def test_valid_password(self):
        result = AuthPolicy.valid_password("Lambaroso1")
        assert result.get_status_code() == 200
        assert result.get_message() == ""