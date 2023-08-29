import json, os
import ssl, smtplib
from flask import request
from email.mime.text import MIMEText
from src.utils.transfer import Transfer
from src.policies.auth import AuthPolicy
from src.services.user import UserService
from email.mime.multipart import MIMEMultipart


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
                raise Exception(result.message)
            
            email = result.user_data.email
            result = UserService.request_recover(body["email"])
            if result.recover_id is None:
                raise Exception(result.message)
            
            # Envia link para recuperação de senha para o e-mail
            context = ssl.create_default_context()
            port = os.getenv("EMAIL_PORT")

            body = MIMEMultipart("alternative")
            body["Subject"] = "Recuperação de senha Lucy"
            body["From"] = os.getenv("EMAIL_FROM")
            body["To"] = email

            link = f"{os.getenv('LUCY_DOMAIN')}/recover/{result.recover_id}"
            message = f"Você solicitou a recuperação de senha para o sistema Lucy.\nSe não foi você, desconsidere a mensagem.\nCaso contrário, acesse {link}."
            body.attach(MIMEText(message, "plain"))

            with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
                server.starttls(context=context)
                server.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_PASS"))
                server.sendmail(os.getenv("EMAIL_FROM"), email, body.as_string())
            
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
        pass

    @staticmethod
    def access_page_recover_password() -> Transfer:
        pass
