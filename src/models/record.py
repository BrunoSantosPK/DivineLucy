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

    def to_json(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "item_id": str(self.item_id) if self.item_id is not None else None,
            "target_wallet": str(self.target_wallet),
            "origin_wallet": str(self.origin_wallet) if self.origin_wallet is not None else None,
            "moviment_date": self.modified_at.isoformat(),
            "description": self.description,
            "value": self.value,
            "create_at": self.create_at.isoformat(),
            "modified_at": self.modified_at.isoformat() if self.modified_at is not None else None
        }
