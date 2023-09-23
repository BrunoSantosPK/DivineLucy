import json
from flask import request
from src.utils.transfer import Transfer
from src.validations.base_validator import BaseValidator


class WalletValidator:
    @staticmethod
    def post_new() -> Transfer:
        result = Transfer()
        try:
            # Verifica integridade do corpo da requisição
            body = request.data
            validate = BaseValidator.validate_body(body)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
            # Verifica campos obrigatórios da requisição
            body = json.loads(body)
            fields = [("user_id", str), ("name", str)]
            validate = BaseValidator.validate_required_fields(body, fields)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
        except BaseException as e:
            result.set_status_code(400)
            result.set_message(str(e))
        finally:
            return result
