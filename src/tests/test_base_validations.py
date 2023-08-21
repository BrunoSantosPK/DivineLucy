from src.validations.base_validator import BaseValidator

def test_null_body():
    body = None
    result = BaseValidator.validate_body(body)
    assert result.get_status_code() == 400
    assert result.get_message() == "O corpo informado não é um json válido"


def test_invalid_json_body():
    body = "um texto qualquer"
    result = BaseValidator.validate_body(body)
    assert result.get_status_code() == 400
    assert result.get_message() == "O corpo informado não é um json válido"


def test_valid_json_body():
    body = b'{"campo": "valor"}'
    result = BaseValidator.validate_body(body)
    assert result.get_status_code() == 200
    assert result.get_message() == ""


def test_without_required_field():
    body = {"campo1": "valor1", "campo2": 2}
    result = BaseValidator.validate_required_fields(body, [("campo1", str), ("campo2", int), ("campo3", str)])
    assert result.get_status_code() == 400
    assert result.get_message() == "O campo obrigatório 'campo3' não foi encontrado"


def test_invalid_type_field():
    body = {"campo1": "valor1", "campo2": "2"}
    result = BaseValidator.validate_required_fields(body, [("campo1", str), ("campo2", int)])
    assert result.get_status_code() == 400
    assert result.get_message() == "O campo 'campo2' deve ser do tipo int"


def test_all_required_field():
    body = {"campo1": "valor1", "campo2": 2}
    result = BaseValidator.validate_required_fields(body, [("campo1", str), ("campo2", int)])
    assert result.get_status_code() == 200
    assert result.get_message() == ""


def test_not_optional_field():
    body = {}
    result = BaseValidator.validate_optional_field(body, [("campo1", str, None)])
    assert body["campo1"] == None
    assert result.get_status_code() == 200
    assert result.get_message() == ""


def test_invalid_type_optional_field():
    body = {"campo1": 0}
    result = BaseValidator.validate_optional_field(body, [("campo1", str, None)])
    body["campo1"] == 0
    assert result.get_status_code() == 400
    assert result.get_message() == "O campo 'campo1' deve ser do tipo str"


def test_invalid_uuid():
    value = "lambari"
    result = BaseValidator.validate_uuid(value)
    assert result.get_status_code() == 400
    assert result.get_message() == "O id informado não é válido"


def test_valid_uuid():
    value = "841a0aa4-26b7-4f8f-8944-7b11054d3447"
    result = BaseValidator.validate_uuid(value)
    assert result.get_status_code() == 200
    assert result.get_message() == ""


def test_invalid_jwt():
    token = "lambari"
    result = BaseValidator.validate_jwt(token)
    assert result.get_status_code() == 500
    assert result.get_message() == "O token de autenticação não é válido"


def test_valid_jwt():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiMDcxNjQzNzEtNzRhZC00NDlmLWJjM2MtNGQxMzExM2M5NDI4IiwiZXhwIjoxNjkyMzc1NjMxfQ.hgSS0KJCsKwW4bFLEoyGhk90ygFHxlMRkbUThrBQqa8"
    result = BaseValidator.validate_jwt(token)
    #assert result.get_status_code() == 200
    assert result.get_message() == ""


def test_invalid_emails():
    result = BaseValidator.validate_email("lambari")
    assert result.get_status_code() == 400 and result.get_message() == "O e-mail informado não é válido"

    result = BaseValidator.validate_email("lambari@.com")
    assert result.get_status_code() == 400 and result.get_message() == "O e-mail informado não é válido"

    result = BaseValidator.validate_email("lambari@lambari")
    assert result.get_status_code() == 400 and result.get_message() == "O e-mail informado não é válido"


def test_valid_email():
    result = BaseValidator.validate_email("lambari@lambari.com")
    assert result.get_status_code() == 200 and result.get_message() == ""

    result = BaseValidator.validate_email("lambari@lambari.com.br")
    assert result.get_status_code() == 200 and result.get_message() == ""


def test_invalid_len_strings():
    result = BaseValidator.validate_string_len("lambari", lmin=10, lmax=None)
    assert result.get_status_code() == 400 and result.get_message() == "O campo precisa ter ao menos 10 caracteres"

    result = BaseValidator.validate_string_len("lambari", lmin=None, lmax=2)
    assert result.get_status_code() == 400 and result.get_message() == "O campo não pode ter mais que 2 caracteres"

    result = BaseValidator.validate_string_len("lambari", lmin=10, lmax=5)
    assert result.get_status_code() == 400 and result.get_message() == "O limite máximo precisar ser maior que o limite mínimo"


def test_valid_len_strings():
    result = BaseValidator.validate_string_len("lambari", lmin=5, lmax=10)
    assert result.get_status_code() == 200 and result.get_message() == ""


def test_invalid_values_interval():
    result = BaseValidator.validate_interval_value(100, lmin=120, lmax=None)
    assert result.get_status_code() == 400 and result.get_message() == "O valor não pode ser menor que 120"

    result = BaseValidator.validate_interval_value(100, lmin=None, lmax=80)
    assert result.get_status_code() == 400 and result.get_message() == "O valor não pode ser maior que 80"

    result = BaseValidator.validate_interval_value(100, lmin=100, lmax=80)
    assert result.get_status_code() == 400 and result.get_message() == "O valor máximo precisar ser maior que o valor mínimo"


def test_valid_value_interval():
    result = BaseValidator.validate_interval_value(100, lmin=80, lmax=120)
    assert result.get_status_code() == 200 and result.get_message() == ""


def test_invalid_dict_list():
    body = {"campo1": 0, "lista": []}
    result = BaseValidator.validate_required_fields(body, [("campo1", int), ("lista", list)])
    assert result.get_status_code() == 200 and result.get_message() == ""

    body["lista"] = [{"campo2": "1", "campo3": 0, "campo4": False}, {"campo3": 0, "campo4": False}]
    result = BaseValidator.validate_list_of_dict(body["lista"], [("campo2", str), ("campo3", int), ("campo4", bool)])
    assert result.get_status_code() == 400
    assert result.get_message() == "O campo 'campo2' não está presente na listagem"

    body["lista"] = [{"campo2": "1", "campo4": False}, {"campo3": 0, "campo4": False}]
    result = BaseValidator.validate_list_of_dict(body["lista"], [("campo2", str), ("campo3", int), ("campo4", bool)])
    assert result.get_status_code() == 400
    assert result.get_message() == "O campo 'campo3' não está presente na listagem"


def test_valid_dict_list():
    body = {
        "campo1": 0,
        "lista": [
            {"campo2": "1", "campo3": 0, "campo4": False},
            {"campo2": "5", "campo3": 5, "campo4": True}
        ]
    }

    result = BaseValidator.validate_required_fields(body, [("campo1", int), ("lista", list)])
    assert result.get_status_code() == 200 and result.get_message() == ""

    result = BaseValidator.validate_list_of_dict(body["lista"], [("campo2", str), ("campo3", int), ("campo4", bool)])
    assert result.get_status_code() == 200
    assert result.get_message() == ""


def test_invalid_date():
    result = BaseValidator.validate_date_string("lambari")
    assert result.get_status_code() == 400
    assert result.get_message() == "Uma data precisa estar no formato yyyy-mm-dd"

    result = BaseValidator.validate_date_string("18/08/2023")
    assert result.get_status_code() == 400
    assert result.get_message() == "Uma data precisa estar no formato yyyy-mm-dd"
