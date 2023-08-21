import hashlib
import binascii
from uuid import uuid4
from datetime import datetime
from src.models._base import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID


class UserData:
    def __init__(self, user_id:str=None, name:str=None, email:str=None,\
    start_date:str=None) -> None:
        self.user_id = user_id
        self.name = name
        self.email = email
        self.start_date = start_date


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow())

    @staticmethod
    def encrypt_password(pw: str, token: str) -> str:
        pw = (pw + token).encode("utf-8")
        hash = hashlib.pbkdf2_hmac("sha256", pw, token.encode("utf-8"), 100000)
        hash = binascii.hexlify(hash).decode("ascii")
        return hash
    
    def export(self) -> UserData:
        return UserData(
            user_id=str(self.id),
            name=self.name,
            email=self.email,
            start_date=self.start_date.isoformat()
        )
