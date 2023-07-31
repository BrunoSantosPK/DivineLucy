from uuid import uuid4
from datetime import datetime
from src.models._base import Base
from src.models.record import Record
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Float


class RecordDetail(Base):
    __tablename__ = "record_details"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    record_id = Column(UUID(as_uuid=True), ForeignKey(Record.id), nullable=False)
    description = Column(String(200), nullable=False)
    value = Column(Float, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow())
