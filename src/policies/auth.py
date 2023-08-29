import jwt, os, hashlib, binascii
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
    def decode_jwt(token: str) -> Transfer:
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

        except jwt.DecodeError:
            res.set_status_code(500)
            res.set_message("O token de autenticação não é válido")

        finally:
            return res
        
    @staticmethod
    def crypt_pass(pw: str) -> Transfer:
        res = Transfer()
        try:
            token = os.getenv("SECRET_PASS")
            pw = (pw + token).encode("utf-8")
            hash = hashlib.pbkdf2_hmac("sha256", pw, token.encode("utf-8"), 100000)
            hash = binascii.hexlify(hash).decode("ascii")
            res.set_data(hash)
        except BaseException as e:
            res.set_status_code(500)
            res.set_message(str(e))
        finally:
            return res
        
    @staticmethod
    def valid_password(pw: str) -> Transfer:
        res = Transfer()
        chars = "abcdefghijklmnopqrstuvwxyz"
        nums = "0123456789"

        try:
            if len(pw) < 8:
                raise Exception("A senha deve ter ao menos 8 caracteres")
            
            def valid(chain: str, obj: str) -> bool:
                is_valid = False
                for c in chain:
                    if c in obj:
                        is_valid = True
                        break
                return is_valid
            
            if not valid(chars, pw):
                raise Exception("A senha deve ter ao menos 1 caractere minúsculo")
            
            if not valid(chars.upper(), pw):
                raise Exception("A senha deve ter ao menos 1 caractere maiúsculo")
            
            if not valid(nums, pw):
                raise Exception("A senha deve ter ao menos 1 número")
            
        except BaseException as e:
            res.set_status_code(500)
            res.set_message(str(e))
        finally:
            return res
