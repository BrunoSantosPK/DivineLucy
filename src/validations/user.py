import json
from flask import request
from src.utils.transfer import Transfer
from src.validations.base_validator import BaseValidator


class UserValidation:
    @staticmethod
    def post_login() -> Transfer:
        result = Transfer()
        try:
            body = request.data
            validate = BaseValidator.validate_body(body)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
            body = json.loads(body)
            validate = BaseValidator.validate_required_fields(body, [("email", str), ("password", str)])
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
            validate = BaseValidator.validate_email(body["email"])
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
        except BaseException as e:
            result.set_status_code(400)
            result.set_message(str(e))
        finally:
            return result

    @staticmethod
    def post_new():
        pass

    @staticmethod
    def post_recover():
        pass

    @staticmethod
    def put_change_password():
        pass

    @staticmethod
    def put_change_password_by_recover():
        pass
