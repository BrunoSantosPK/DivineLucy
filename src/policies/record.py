from src.utils.transfer import Transfer
from src.validations.base_validator import BaseValidator


class RecordPolicy:
    @staticmethod
    def record_data(body: dict):
        '''
        Este método avalia os campos: moviment_date, description, value e details
        (com os campos description e value). Como políticas de registro saudável,
        adota padrões de tamanho e valores.
        '''
        result = Transfer()
        try:
            validations = [
                BaseValidator.validate_date_string(body["moviment_date"]),
                BaseValidator.validate_string_len(body["description"], lmin=5, lmax=200)
            ]
            validations.extend([BaseValidator.validate_string_len(b["description"], lmin=5, lmax=100) for b in body["details"]])
            success = True
            for validate in validations:
                if validate.get_status_code() != 200:
                    success = False
                    break

            if not success:
                raise Exception(validate.get_message())
            
        except BaseException as e:
            result.set_status_code(400)
            result.set_message(str(e))
        finally:
            return result
