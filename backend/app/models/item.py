import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, JSON, Index
from sqlalchemy.orm import relationship
from backend.app.core.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Item(Base):
    __tablename__ = "items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source = Column(String(50), nullable=False, index=True)  # "arxiv", "github", "hn"
    source_id = Column(String(200), unique=True, nullable=False, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    url = Column(Text, nullable=False)
    metadata_json = Column(JSON, nullable=True)
    ingested_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    created_at = Column(DateTime, nullable=True)

    # Relationships
    classification = relationship("Classification", back_populates="item", uselist=False, cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="item", cascade="all, delete-orphan")
    insight = relationship("Insight", back_populates="item", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_items_source_ingested", "source", "ingested_at"),
    )
