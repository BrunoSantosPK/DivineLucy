import json
from uuid import uuid4
from typing import List
from datetime import datetime, date
from src.models.record import Record
from src.database.connect import get_session
from src.models.record_detail import RecordDetail


class RecordResponse:
    def __init__(self) -> None:
        self.message = ""
        self.success = True
        self.record_id: str = None
        self.details_id: List[str] = None
        self.records: List[dict] = None


class RecordDetails:
    def __init__(self, description: str, value: float) -> None:
        self.description = description
        self.value = value


class RecordService:

    @staticmethod
    def new(
        user_id: str, item_id: str, target_id: str, moviment_date: date,
        description: str, value: float, origin_id: str=None, details: List[RecordDetails]=[]
    ) -> RecordResponse:
        res = RecordResponse()
        session = get_session()

        try:
            record_id = uuid4()
            create = datetime.utcnow()
            record = Record(
                id=record_id,
                user_id=user_id,
                item_id=item_id,
                target_wallet=target_id,
                origin_wallet=origin_id,
                description=description,
                moviment_date=moviment_date,
                value=value,
                create_at=create
            )
            record_details = [
                RecordDetail(
                    record_id=record_id,
                    description=d.description,
                    value=d.value,
                    create_at=create
                ) for d in details
            ]

            session.add(record)
            session.add_all(record_details)
            session.commit()
            res.record_id = str(record_id)

        except BaseException as e:
            session.rollback()
            res.message = str(e)
            res.success = False

        finally:
            session.close()
            return res

    @staticmethod
    def delete(record_id: str, user_id: str) -> RecordResponse:
        res = RecordResponse()
        session = get_session()

        try:
            # Verifica se id e usuário existem
            q = session.query(Record).filter(Record.id == record_id, Record.user_id == user_id)
            if len(q.all()) == 0:
                raise Exception("Registro não encontrado")
            
            session.query(RecordDetail).filter(RecordDetail.record_id == record_id).delete()
            q.delete()
            session.commit()

        except BaseException as e:
            session.rollback()
            res.message = str(e)
            res.success = False

        finally:
            session.close()
            return res

    @staticmethod
    def edit(
        record_id: str, user_id: str, item_id: str, target_id: str, moviment_date: date,
        description: str, value: float, origin_id: str=None, details: List[RecordDetails]=[]
    ) -> RecordResponse:
        res = RecordResponse()
        session = get_session()

        try:
            modified = datetime.utcnow()
            session.query(Record).filter(Record.id == record_id, Record.user_id == user_id).update({
                Record.item_id: item_id,
                Record.target_wallet: target_id,
                Record.moviment_date: moviment_date,
                Record.description: description,
                Record.value: value,
                Record.origin_wallet: origin_id,
                Record.modified_at: modified
            })
            record_details = [
                RecordDetail(
                    record_id=record_id,
                    description=d.description,
                    value=d.value,
                    create_at=modified
                ) for d in details
            ]

            session.query(RecordDetail).filter(RecordDetail.record_id == record_id).delete()
            session.add_all(record_details)
            session.commit()
            
        except BaseException as e:
            session.rollback()
            res.message = str(e)
            res.success = False

        finally:
            session.close()
            return res

    @staticmethod
    def get_all(user_id: str, page=1) -> RecordResponse:
        res = RecordResponse()
        session = get_session()

        try:
            per_page = 100
            records: List[Record] = session.query(Record).order_by(Record.moviment_date.desc())\
                .limit(per_page).offset((page - 1) * per_page).all()
            records_id = [str(r.id) for r in records]
            details = session.query(RecordDetail).filter(RecordDetail.record_id in records_id).all()

            # Todo: fazer o merge das informações

            res.records = [r.to_json() for r in records]

        except BaseException as e:
            session.rollback()
            res.message = str(e)
            res.success = False

        finally:
            session.close()
            return res
