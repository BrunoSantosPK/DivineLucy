from uuid import uuid4
from src.models.user import User
from src.models._base import Base
from datetime import datetime, timedelta
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, ForeignKey, Boolean


class UserRecoverData:
    def __init__(self, recover_id:str=None, user_id:str=None, create_at:str=None, \
    expire_at:str=None, used:bool=None) -> None:
        self.recover_id = recover_id
        self.user_id = user_id
        self.create_at = create_at
        self.expire_at = expire_at
        self.used = used


class UserRecover(Base):
    __tablename__ = "user_recovers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow())
    expire_at = Column(DateTime, default=(datetime.utcnow() + timedelta(hours=3)))
    used = Column(Boolean, default=False)

    def export(self) -> UserRecoverData:
        return UserRecoverData(
            recover_id=str(self.id),
            user_id=str(self.user_id),
            create_at=self.create_at.isoformat(),
            expire_at=self.expire_at.isoformat(),
            used=self.used
        )
