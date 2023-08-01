import calendar
from typing import Tuple
from datetime import date, datetime
from src.models.budget import Budget
from src.database.connect import get_session


class BudgetService:

    @staticmethod
    def new(user_id: str, year: int, month: int, item_id: str, value: float) -> Tuple[str, str]:
        session = get_session()
        message = ""

        try:
            # Recupera datas de início da, de finalização da meta e de criação
            start_date = date(year, month, 1)
            end_date = date(year, month, calendar.monthrange(year, month)[1])
            create = datetime.utcnow()

            # Cria classe e insere no banco de dados
            budget = Budget(
                user_id=user_id,
                item_id=item_id,
                start_date=start_date,
                end_date=end_date,
                value=value,
                create_at=create
            )
            session.add(budget)
            session.commit()
            budget_id = str(budget.id)

        except BaseException as e:
            budget_id = ""
            message = str(e)
            session.rollback()

        finally:
            session.close()
            return budget_id, message

    @staticmethod
    def delete(budget_id: str) -> Tuple[bool, str]:
        session = get_session()
        message = ""

        try:
            session.query(Budget).filter(Budget.id == budget_id).delete()
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
    def edit(budget_id: str, item_id: str, value: float) -> str:
        session = get_session()
        message = ""

        try:
            session.query(Budget).filter(Budget.id == budget_id).update({
                Budget.item_id: item_id,
                Budget.value: value,
                Budget.modified_at: datetime.utcnow()
            })
            session.commit()

        except BaseException as e:
            message = str(e)
            session.rollback()

        finally:
            session.close()
            return message

    @staticmethod
    def get_all():
        pass
