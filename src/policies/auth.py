import jwt, os
from src.utils.transfer import Transfer
from datetime import datetime, timedelta


class AuthPolicy:
    @staticmethod
    def generate_jwt(uuid: str) -> Transfer:
        res = Transfer()
        try:
            exp = datetime.utcnow() + timedelta(hours=24)
            token = jwt.encode({"uuid": uuid, "exp": exp}, os.getenv("SECRET_AUTH"), algorithm="HS256")
            res.set_status_code(200)
            res.set_data(token)

        except BaseException as e:
            res.set_status_code(500)
            res.set_message(str(e))

        finally:
            return res

    @staticmethod
    def decode(token: str) -> Transfer:
        res = Transfer()
        try:
            payload = jwt.decode(token.encode("utf-8"), os.getenv("SECRET_AUTH"), algorithms=["HS256"])
            res.set_data(payload["uuid"])
            res.set_status_code(200)

        except jwt.ExpiredSignatureError:
            res.set_status_code(500)
            res.set_message("Sua sessão expirou")

        except jwt.InvalidTokenError:
            res.set_status_code(500)
            res.set_message("O token de autenticação não é válido")

        except BaseException as e:
            res.set_status_code(500)
            res.set_message(str(e))

        finally:
            return res
        
    @staticmethod
    def is_jwt(token: str) -> Transfer:
        res = Transfer()
        try:
            jwt.decode(token.encode("utf-8"), os.getenv("SECRET_AUTH"), algorithms=["HS256"])
            res.set_status_code(200)

        except jwt.InvalidTokenError:
            res.set_status_code(500)
            res.set_message("O token de autenticação não é válido")

        finally:
            return res
