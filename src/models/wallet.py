from uuid import uuid4
from datetime import datetime
from src.models.user import User
from src.models._base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, ForeignKey


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    name = Column(String(100), nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow())
