from datetime import datetime, timedelta
from src.models.user import User, UserData
from src.database.connect import get_session
from src.models.user_recover import UserRecover, UserRecoverData


class UserResponse:
    def __init__(self) -> None:
        self.message = ""
        self.success = True
        self.user_id: str = None
        self.user_data: UserData = None
        self.recover_id: str = None
        self.recover_data: UserRecoverData = None


class UserService:
    @staticmethod
    def create(name: str, email: str, pw: str) -> UserResponse:
        session = get_session()
        res = UserResponse()

        try:
            # Verifica se o e-mail já está cadastrado
            search = UserService.find_by_email(email)
            if search.user_id is not None:
                raise Exception("O e-mail já está cadastrado")

            # Faz a inclusão de novo registro
            user = User(name=name, email=email, password=pw, start_date=datetime.utcnow())
            session.add(user)
            session.commit()

            res.user_id = str(user.id)
            res.user_data = user.export()

        except BaseException as e:
            res.success = False
            res.message = str(e)
        finally:
            session.close()
            return res

    @staticmethod
    def delete(user_id: str) -> UserResponse:
        session = get_session()
        res = UserResponse()

        try:
            session.query(UserRecover).filter(UserRecover.user_id == user_id).delete()
            quantity = session.query(User).filter(User.id == user_id).delete()
            if quantity == 0:
                raise Exception(f"O {user_id} não foi encontrado")
            session.commit()
        except BaseException as e:
            res.success = False
            res.message = str(e)
        finally:
            session.close()
            return res

    @staticmethod
    def find_by_email(email: str) -> UserResponse:
        session = get_session()
        res = UserResponse()

        try:
            q = session.query(User).filter(User.email == email).first()
            if q is not None:
                res.user_id = str(q.id)
                res.user_data = q.export()
            
        except BaseException as e:
            res.success = False
            res.message = str(e)
        finally:
            session.close()
            return res
        
    @staticmethod
    def find_by_email_and_password(email: str, pw: str) -> UserResponse:
        session = get_session()
        res = UserResponse()

        try:
            q = session.query(User).filter(User.email == email, User.password == pw).first()
            if q is not None:
                res.user_id = str(q.id)
                res.user_data = q.export()
            
        except BaseException as e:
            res.success = False
            res.message = str(e)
        finally:
            session.close()
            return res
        
    @staticmethod
    def request_recover(email: str):
        session = get_session()
        res = UserResponse()

        try:
            # Verifica se o e-mail informado existe
            search = UserService.find_by_email(email)
            if search.user_id is None:
                raise Exception("O e-mail não foi encontrado")
            
            # Cria o registro de recuperação e retorna o id dele
            recover = UserRecover(
                user_id=search.user_id,
                create_at=datetime.utcnow(),
                expire_at=(datetime.utcnow() + timedelta(hours=3))
            )
            session.add(recover)
            session.commit()
            res.recover_id = str(recover.id)

        except BaseException as e:
            res.success = False
            res.message = str(e)
        finally:
            session.close()
            return res
        
    @staticmethod
    def find_recover_by_id(uuid: str) -> UserResponse:
        session = get_session()
        res = UserResponse()

        try:
            q = session.query(UserRecover).filter(UserRecover.id == uuid).first()
            if q is not None:
                res.recover_id = str(q.id)
                res.recover_data = q.export()

        except BaseException as e:
            res.success = False
            res.message = str(e)
        finally:
            session.close()
            return res
        
    @staticmethod
    def change_password_by_recover(recover_id: str, new_pw: str):
        session = get_session()
        res = UserResponse()

        try:
            # Busca solicitação de recuperação de senha
            result = UserService.find_recover_by_id(recover_id)
            if result.recover_id is None:
                raise Exception("Não foi encontrada a solicitação de recuperação de senha")
            
            # Verifica se a solicitação ainda está válida
            if datetime.utcnow() > datetime.fromisoformat(result.recover_data.expire_at):
                raise Exception("A solicitação de recuperação já expirou")
            
            if result.recover_data.used:
                raise Exception("Esta solicitação de recuperação já foi executada")
            
            session.query(User).filter(User.id == result.recover_data.user_id)\
                .update({User.password: new_pw})
            session.query(UserRecover).filter(UserRecover.id == recover_id)\
                .update({UserRecover.used: True})
            session.commit()
            
        except BaseException as e:
            res.success = False
            res.message = str(e)
        finally:
            session.close()
            return res

    @staticmethod
    def change_password(email: str, old_pw: str, new_pw):
        session = get_session()
        res = UserResponse()

        try:
            result = UserService.find_by_email_and_password(email, old_pw)
            if result.user_id is None:
                raise Exception("O e-mail e senha atuais não estão corretos")
            
            session.query(User).filter(User.id == result.user_id).update({User.password: new_pw})
            session.commit()

        except BaseException as e:
            res.success = False
            res.message = str(e)
        finally:
            session.close()
            return res
