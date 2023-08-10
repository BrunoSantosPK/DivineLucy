from datetime import datetime
from typing import Tuple, List
from sqlalchemy.sql import func
from src.models.wallet import Wallet
from src.models.record import Record
from src.database.connect import get_session


class WalletService:

    @staticmethod
    def new(name: str, user_id: str) -> Tuple[str, str]:
        session = get_session()
        message = ""

        try:
            # Verifica se o nome já existe
            exist = session.query(Wallet).filter(Wallet.name == name, Wallet.user_id == user_id).all()
            if len(exist) > 0:
                raise Exception("Você já tem uma conta com este nome")
            
            wallet = Wallet(name=name, user_id=user_id, create_at=datetime.utcnow())
            session.add(wallet)
            session.commit()
            wallet_id = str(wallet.id)

        except BaseException as e:
            wallet_id = ""
            message = str(e)
            session.rollback()

        finally:
            session.close()
            return wallet_id, message
        
    @staticmethod
    def delete(id: str) -> Tuple[bool, str]:
        session = get_session()
        message = ""

        try:
            session.query(Wallet).filter(Wallet.id == id).delete()
            session.commit()
            result = True

        except BaseException as e:
            result = False
            message = str(e)
            session.rollback()

        finally:
            session.close()
            return result, message
    
    @staticmethod
    def get_all(user_id: str) -> Tuple[List[dict], str]:
        session = get_session()
        data, message = [], ""

        try:
            result: List[Wallet] = session.query(Wallet).filter(Wallet.user_id == user_id).order_by(Wallet.create_at.desc()).all()
            for wallet in result:
                q = session.query(func.sum(Record.value).label("result_value"))
                r_income = q.filter(Record.user_id == user_id, Record.target_wallet == wallet.id, Record.value > 0).all()
                r_outcome = q.filter(Record.user_id == user_id, Record.target_wallet == wallet.id, Record.value < 0).all()
                income = sum([v.result_value for v in r_income if v.result_value is not None])
                outcome = sum([v.result_value for v in r_outcome if v.result_value is not None])

                data.append({
                    "id": str(wallet.id),
                    "name": wallet.name,
                    "create_at": wallet.create_at.isoformat(),
                    "total_income": income,
                    "total_outcome": outcome,
                    "current_value": income + outcome
                })
            
        except BaseException as e:
            message = str(e)

        finally:
            session.close()
            return data, message
