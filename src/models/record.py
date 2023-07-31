from uuid import uuid4
from datetime import datetime
from src.models.user import User
from src.models._base import Base
from src.models.wallet import Wallet
from sqlalchemy.dialects.postgresql import UUID
from src.models.classification_item import ClassificationItem
from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Float


class Record(Base):
    __tablename__ = "records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey(ClassificationItem.id), nullable=True)
    target_wallet = Column(UUID(as_uuid=True), ForeignKey(Wallet.id), nullable=False)
    origin_wallet = Column(UUID(as_uuid=True), nullable=True)
    moviment_date = Column(Date, nullable=False)
    description = Column(String(200), nullable=False)
    value = Column(Float, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow())
    modified_at = Column(DateTime, nullable=True)
