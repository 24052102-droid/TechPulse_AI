import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base


class Insight(Base):
    __tablename__ = "insights"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(String(36), ForeignKey("items.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    summary = Column(Text, nullable=False)
    key_takeaways = Column(JSON, nullable=False)           # List of 3 strings
    why_it_matters = Column(Text, nullable=False)
    technical_depth = Column(String(20), default="intermediate") # "beginner", "intermediate", "advanced"
    estimated_read_time = Column(Integer, default=5)       # Minutes
    related_topics = Column(JSON, nullable=True)           # List of 3 topic tags
    llm_model = Column(String(100), default="claude-3-5-sonnet")
    generated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    item = relationship("Item", back_populates="insight")
