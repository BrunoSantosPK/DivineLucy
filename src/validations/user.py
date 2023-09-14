import json
from flask import request
from src.utils.transfer import Transfer
from src.policies.auth import AuthPolicy
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
        result = Transfer()
        try:
            body = request.data
            validate = BaseValidator.validate_body(body)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
            body = json.loads(body)
            fields = [("email", str), ("password", str), ("repeat_password", str), ("name", str)]
            validate = BaseValidator.validate_required_fields(body, fields)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
            validate = BaseValidator.validate_email(body["email"])
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
            if body["password"] != body["repeat_password"]:
                raise Exception("As senhas não são iguais")
            
            validate = AuthPolicy.valid_password(body["password"])
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
            validate = BaseValidator.validate_string_len(body["name"], lmin=3, lmax=200)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
        except BaseException as e:
            result.set_status_code(400)
            result.set_message(str(e))
        finally:
            return result

    @staticmethod
    def post_recover():
        result = Transfer()
        try:
            body = request.data
            validate = BaseValidator.validate_body(body)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
            body = json.loads(body)
            fields = [("email", str)]
            validate = BaseValidator.validate_required_fields(body, fields)
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
    def put_change_password():
        result = Transfer()
        try:
            body = request.data
            validate = BaseValidator.validate_body(body)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
        except BaseException as e:
            result.set_status_code(400)
            result.set_message(str(e))
        finally:
            return result

    @staticmethod
    def put_change_password_by_recover():
        result = Transfer()
        try:
            body = request.data
            validate = BaseValidator.validate_body(body)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
            body = json.loads(body)
            fields = [("password", str), ("repeat_password", str), ("recover_id", str)]
            validate = BaseValidator.validate_required_fields(body, fields)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
            if body["password"] != body["repeat_password"]:
                raise Exception("As senhas não são iguais")
            
            validate = AuthPolicy.valid_password(body["password"])
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
        except BaseException as e:
            result.set_status_code(400)
            result.set_message(str(e))
        finally:
            return result
