import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, Boolean, Date, DateTime, Index
from backend.app.core.database import Base


class DomainTrend(Base):
    __tablename__ = "domain_trends"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    domain = Column(String(100), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    item_count = Column(Integer, default=0)
    avg_impact = Column(Float, default=0.0)
    trend_score = Column(Float, default=0.0)
    wow_delta = Column(Float, default=0.0)
    is_trending = Column(Boolean, default=False)
    hype_adoption_ratio = Column(Float, default=1.0)
    aggregated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_trend_domain_date", "domain", "date", unique=True),
    )
