import json, os
from flask import request
from datetime import datetime
from src.utils.transfer import Transfer
from src.policies.auth import AuthPolicy
from src.services.user import UserService
from src.services.email import EmailService
from src.controllers.page import PageController


class UserController:
    @staticmethod
    def login() -> Transfer:
        res = Transfer()
        try:
            # Aplica criptografia de senha e busca usuário
            body = json.loads(request.data)
            password = AuthPolicy.crypt_pass(body["password"]).get_data()
            process = UserService.find_by_email_and_password(body["email"], password)
            if process.user_id is None:
                raise Exception("Usuário ou senha inválidos")
            
            # Gera um token de autenticação
            token = AuthPolicy.generate_jwt(process.user_id).get_data()
            res.set_cookie("token", token)
            res.set_cookie("user_id", process.user_id)
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
    def new() -> Transfer:
        res = Transfer()
        try:
            # Aplica criptografia de senha e envia para o serviço
            body = json.loads(request.data)
            password = AuthPolicy.crypt_pass(body["password"]).get_data()
            result = UserService.create(body["name"], body["email"], password)
            if not result.success:
                raise Exception(result.message)
            
            res.set_data({"new_user": result.user_id})
            
        except BaseException as e:
            res.set_status_code(500)
            res.set_message(str(e))
        finally:
            return res

    @staticmethod
    def recover_password() -> Transfer:
        res = Transfer()
        try:
            # Recupera dados da requisição e verifica e-mail
            body = json.loads(request.data)
            result = UserService.find_by_email(body["email"])
            if result.user_id is None:
                raise Exception("O usuário não foi encontrado")
            
            email = result.user_data.email
            result = UserService.request_recover(body["email"])
            if result.recover_id is None:
                raise Exception(result.message)
            
            # Envia link para recuperação de senha para o e-mail
            link = f"{os.getenv('LUCY_DOMAIN')}/recover/{result.recover_id}"
            message = f"Você solicitou a recuperação de senha para o sistema Lucy.\nSe não foi você, desconsidere a mensagem.\nCaso contrário, acesse {link}."
            result = EmailService.send_mail(email, message)
            if result.get_status_code() != 200:
                raise Exception(result.get_message())
            
        except BaseException as e:
            res.set_status_code(500)
            res.set_message(str(e))
        finally:
            return res

    @staticmethod
    def change_password() -> Transfer:
        pass

    @staticmethod
    def change_password_by_recover() -> Transfer:
        res = Transfer()
        try:
            body = json.loads(request.data)
            password = AuthPolicy.crypt_pass(body["password"]).get_data()
            result = UserService.change_password_by_recover(body["recover_id"], password)
            if not result.success:
                raise Exception(result.message)
            
        except BaseException as e:
            res.set_status_code(500)
            res.set_message(str(e))
        finally:
            return res

    @staticmethod
    def access_page_recover_password() -> Transfer:
        try:
            recover_id = request.view_args["recover_id"]
            result = UserService.find_recover_by_id(recover_id)
            if result.recover_id is None:
                raise Exception("A solicitação não foi encontrada no banco de dados")
            
            if datetime.utcnow() > datetime.fromisoformat(result.recover_data.expire_at):
                raise Exception("A solicitação de recuperação já expirou")
            
            if result.recover_data.used:
                raise Exception("Esta solicitação de recuperação já foi executada")
            
            return PageController.to_recover(recover_id)
            
        except BaseException as e:
            return PageController.to_404(str(e))

    @staticmethod
    def auth() -> Transfer:
        res = Transfer()
        try:
            auth_token = request.cookies.get("token")
            user_id = request.cookies.get("user_id")
            if auth_token is None or user_id is None:
                raise Exception("Você não está logado no sistema")
            
            result = AuthPolicy.decode_jwt(auth_token)
            if result.get_status_code() != 200:
                raise Exception(result.get_message())
            
        except BaseException as e:
            res.set_status_code(401)
            res.set_message(str(e))
        finally:
            return res
        
    @staticmethod
    def auth_redirect_login() -> Transfer():
        res = Transfer()
        try:
            result = UserController.auth()
            if result.get_status_code() != 200:
                raise Exception(result.get_message())
            return res
            
        except BaseException as e:
            return PageController.to_login(401)
