from uuid import uuid4
from datetime import datetime
from src.models.user import User
from src.models._base import Base
from sqlalchemy.dialects.postgresql import UUID
from src.models.classification_item import ClassificationItem
from sqlalchemy import Column, DateTime, Date, ForeignKey, Float


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey(ClassificationItem.id), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow())
    modified_at = Column(DateTime, nullable=True)
