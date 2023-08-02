from datetime import datetime
from typing import Tuple, List
from src.database.connect import get_session
from src.models.classification_item import ClassificationItem


class ClassificationItemService:

    @staticmethod
    def new(user_id: str, name: str) -> Tuple[str, str]:
        session = get_session()
        message = ""

        try:
            # Verifica se o nome está disponível
            results = session.query(ClassificationItem).filter(
                ClassificationItem.user_id == user_id,
                ClassificationItem.name == name
            ).all()
            if len(results) != 0:
                raise Exception("Você já possui um item com este nome")

            # Cria o novo item
            create = datetime.utcnow()
            item = ClassificationItem(user_id=user_id, name=name, create_at=create)
            session.add(item)
            session.commit()
            item_id = str(item.id)

        except BaseException as e:
            item_id = ""
            message = str(e)
            session.rollback()

        finally:
            session.close()
            return item_id, message

    @staticmethod
    def get_all(user_id: str) -> Tuple[List[dict], str]:
        session = get_session()
        message, items = "", []

        try:
            results: List[ClassificationItem] = session.query(ClassificationItem).filter(
                (ClassificationItem.user_id == user_id) | (ClassificationItem.user_id == None)
            ).all()
            items = [{"name": r.name, "id": str(r.id)} for r in results]

        except BaseException as e:
            message = str(e)
            session.rollback()

        finally:
            session.close()
            return items, message

    @staticmethod
    def delete(item_id: str, user_id: str) -> str:
        session = get_session()
        message = ""

        try:
            session.query(ClassificationItem).filter(
                ClassificationItem.id == item_id,
                ClassificationItem.user_id == user_id
            ).delete()
            session.commit()

        except BaseException as e:
            message = str(e)
            session.rollback()

        finally:
            session.close()
            return message
