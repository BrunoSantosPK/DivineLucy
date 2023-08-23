import json
from flask import request
from src.utils.transfer import Transfer
from src.policies.auth import AuthPolicy
from src.services.user import UserService


class UserController:
    @staticmethod
    def login():
        res = Transfer()
        try:
            # Aplica criptografia de senha e busca usuário
            body = json.loads(request.data)
            password = AuthPolicy.crypt_pass(body["password"])
            process = UserService.find_by_email_and_password(body["email"], password)
            if process.user_id is None:
                raise Exception("Usuário ou senha inválidos")
            
            # Gera um token de autenticação
            token = AuthPolicy.generate_jwt(process.user_id)
            res.set_data({
                "token": token,
                "user_data": process.user_data.__dict__
            })
            
        except BaseException as e:
            res.set_status_code(500)
            res.set_message(str(e))
        finally:
            return res

    @staticmethod
    def new():
        pass

    @staticmethod
    def recover_password():
        pass

    @staticmethod
    def change_password():
        pass

    @staticmethod
    def change_password_by_recover():
        pass

    @staticmethod
    def access_page_recover_password():
        pass
