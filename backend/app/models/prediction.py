import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship
from backend.app.core.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(String(36), ForeignKey("items.id", ondelete="CASCADE"), nullable=False, index=True)
    prediction_type = Column(String(50), nullable=False)  # "paper_impact", "repo_growth", "hn_velocity"
    score = Column(Float, nullable=False)                 # Normalized 0.0 to 1.0
    score_display = Column(Float, nullable=False, index=True) # 0.0 to 10.0 for UI display
    confidence = Column(Float, default=1.0)
    features_used = Column(JSON, nullable=True)           # Features and TreeSHAP top drivers
    model_version = Column(String(50), nullable=False)
    predicted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    item = relationship("Item", back_populates="predictions")

    __table_args__ = (
        Index("idx_pred_type_score", "prediction_type", "score_display"),
    )
