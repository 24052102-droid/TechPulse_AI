import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship
from backend.app.core.database import Base


class Classification(Base):
    __tablename__ = "classifications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(String(36), ForeignKey("items.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    primary_domain = Column(String(100), nullable=False, index=True)
    secondary_domains = Column(JSON, nullable=True)  # List of secondary domain strings
    confidence_scores = Column(JSON, nullable=True)  # Dict: {"NLP": 0.85, ...}
    low_confidence = Column(Boolean, default=False)
    model_version = Column(String(50), nullable=False)
    classified_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    item = relationship("Item", back_populates="classification")

    __table_args__ = (
        Index("idx_cls_domain_date", "primary_domain", "classified_at"),
    )
