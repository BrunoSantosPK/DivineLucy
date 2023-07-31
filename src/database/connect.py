import os
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine


def get_engine() -> Engine:
    user = os.getenv("DB_USER")
    pw = os.getenv("DB_PASS")
    db = os.getenv("DB_NAME")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    return create_engine(f"postgresql://{user}:{pw}@{host}:{port}/{db}")


def get_session() -> Session:
    engine = get_engine()
    return Session(engine)
