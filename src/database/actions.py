from src.models._base import Base
from src.models.user import User
from src.models.budget import Budget
from src.models.record import Record
from src.models.wallet import Wallet
from src.models.record_detail import RecordDetail
from src.database.connect import get_engine, get_session
from src.models.classification_item import ClassificationItem


def create_tables() -> None:
    try:
        Base.metadata.create_all(get_engine())
        print("Tabelas criadas com sucesso.")
    except BaseException as e:
        print(str(e))


def create_root_user() -> None:
    try:
        session = get_session()
        root = User(
            id="49fe6c42-b940-4122-906b-e95c7316e349",
            name="Root",
            email="root@root.com.br",
            password=User.encrypt_password("lambari", "token")
        )
        session.add(root)
        session.commit()
        print(f"Usuário padrão criado com sucesso, id: {root.id}")
    except BaseException as e:
        print(str(e))
    finally:
        session.close()


def create_default_items() -> None:
    try:
        session = get_session()
        session.add_all([
            ClassificationItem(name="Supermercado", id="fb0b8338-63ab-4ccf-8ebf-8e4b2798b08a"),
            ClassificationItem(name="Lazer", id="404c3daa-5759-454c-81fc-39cc644b13d2"),
            ClassificationItem(name="Saúde"),
            ClassificationItem(name="Transporte"),
            ClassificationItem(name="Casa"),
            ClassificationItem(name="Manutenção"),
            ClassificationItem(name="Emergência"),
            ClassificationItem(name="Renda"),
            ClassificationItem(name="Recorrente"),
            ClassificationItem(name="Supermercado"),
            ClassificationItem(name="Investimento")
        ])
        session.commit()
        print("Itens de classificação padrão criados com sucesso")
    except BaseException as e:
        print(str(e))
    finally:
        session.close()


def delete_tables() -> None:
    try:
        Base.metadata.drop_all(get_engine())
        print("Tabelas removidas com sucesso!")
    except BaseException as e:
        print(str(e))
