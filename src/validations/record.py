import json
from flask import request
from src.utils.transfer import Transfer
from src.policies.record import RecordPolicy
from src.validations.base_validator import BaseValidator


class RecordValidator:
    @staticmethod
    def post_new() -> Transfer:
        result = Transfer()
        try:
            # Sequência de validação do envio de campos necessários para processamento
            body = request.data
            validate = BaseValidator.validate_body(body)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
            body = json.loads(body)
            required_fields = [("user_id", str), ("item_id", str), ("target_id", str), ("moviment_date", str), ("description", str)]
            optional_fields = [("details", list, []), ("origin_id", str, None)]
            list_fields = [("description", str)]
            seq = [
                (BaseValidator.validate_required_fields, (body, required_fields)),
                (BaseValidator.validate_optional_field, (body, optional_fields)),
                (BaseValidator.validate_list_of_dict, (body["details"], list_fields))
            ]

            success = True
            for func, args in seq:
                validade: Transfer = func(args[0], args[1])
                if validade.get_status_code() != 200:
                    success = False
                    break
            if not success:
                raise Exception(validade.get_message())
            
            # Verifica integridade dos IDs enviados
            for field in ["user_id", "item_id", "target_id", "origin_id"]:
                if body[field] is None:
                    continue

                validate = BaseValidator.validate_uuid(body[field])
                if validate.get_status_code() != 200:
                    validate.set_message(f"{field}: {validate.get_message()}")
                    break

            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
            # Aplica a política de tamanho de dados
            validate = RecordPolicy.record_data(body)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
        except BaseException as e:
            result.set_status_code(400)
            result.set_message(str(e))
        finally:
            return result

    @staticmethod
    def put_edit() -> Transfer:
        result = Transfer()
        try:
            # Sequência de validação do envio de campos necessários para processamento
            body = request.data
            validate = BaseValidator.validate_body(body)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
            body = json.loads(body)
            required_fields = [("record_id", str), ("user_id", str), ("item_id", str), ("target_id", str), ("moviment_date", str), ("description", str)]
            optional_fields = [("details", list, []), ("origin_id", str, None)]
            list_fields = [("description", str)]
            seq = [
                (BaseValidator.validate_required_fields, (body, required_fields)),
                (BaseValidator.validate_optional_field, (body, optional_fields)),
                (BaseValidator.validate_list_of_dict, (body["details"], list_fields))
            ]

            success = True
            for func, args in seq:
                validade: Transfer = func(args[0], args[1])
                if validade.get_status_code() != 200:
                    success = False
                    break
            if not success:
                raise Exception(validade.get_message())
            
            # Verifica integridade dos IDs enviados
            for field in ["user_id", "item_id", "target_id", "origin_id"]:
                if body[field] is None:
                    continue

                validate = BaseValidator.validate_uuid(body[field])
                if validate.get_status_code() != 200:
                    break

            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
            # Aplica a política de tamanho de dados
            validate = RecordPolicy.record_data(body)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
        except BaseException as e:
            result.set_status_code(400)
            result.set_message(str(e))
        finally:
            return result

    @staticmethod
    def delete_remove() -> Transfer:
        result = Transfer()
        try:
            # Sequência de validação do envio de campos necessários para processamento
            body = request.data
            validate = BaseValidator.validate_body(body)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())
            
            body = json.loads(body)
            required_fields = [("user_id", str), ("record_id", str)]
            validate = BaseValidator.validate_required_fields(body, required_fields)
            if validate.get_status_code() != 200:
                raise Exception(validate.get_message())

        except BaseException as e:
            result.set_status_code(400)
            result.set_message(str(e))
        finally:
            return result
