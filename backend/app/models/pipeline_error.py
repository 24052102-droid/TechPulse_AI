import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime
from backend.app.core.database import Base


class PipelineError(Base):
    __tablename__ = "pipeline_errors"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_name = Column(String(100), nullable=False, index=True)
    item_id = Column(String(36), nullable=True)
    error_msg = Column(Text, nullable=False)
    occurred_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
