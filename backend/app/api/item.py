from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.item import Item
from backend.app.models.classification import Classification
from backend.app.models.prediction import Prediction
from backend.app.models.insight import Insight
from backend.app.schemas.item import ItemDetailResponse, DriverFeature
from backend.app.schemas.insight import InsightResponse, InsightStatusResponse

router = APIRouter(prefix="/item", tags=["Item"])


@router.get("/{item_id}", response_model=ItemDetailResponse)
def get_item_detail(item_id: str, db: Session = Depends(get_db)):
    """Retrieve detailed item information including all predictions and metadata."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    cls = item.classification
    pred = db.query(Prediction).filter(Prediction.item_id == item_id).order_by(Prediction.predicted_at.desc()).first()
    ins = item.insight

    top_drivers = []
    if pred and pred.features_used and isinstance(pred.features_used, dict):
        for d in pred.features_used.get("top_drivers", []):
            top_drivers.append(DriverFeature(
                feature=str(d.get("feature", "")),
                value=d.get("value", 0),
                impact=float(d.get("impact", 0.0)),
            ))

    insight_dict = None
    if ins:
        insight_dict = {
            "summary": ins.summary,
            "key_takeaways": ins.key_takeaways or [],
            "why_it_matters": ins.why_it_matters,
            "technical_depth": ins.technical_depth,
            "estimated_read_time": ins.estimated_read_time,
            "related_topics": ins.related_topics or [],
            "llm_model": ins.llm_model,
            "generated_at": ins.generated_at.isoformat() if ins.generated_at else None,
        }

    all_preds = []
    for p in item.predictions:
        all_preds.append({
            "prediction_type": p.prediction_type,
            "score": p.score,
            "score_display": p.score_display,
            "model_version": p.model_version,
            "predicted_at": p.predicted_at.isoformat() if p.predicted_at else None,
        })

    return ItemDetailResponse(
        id=item.id,
        source=item.source,
        source_id=item.source_id,
        title=item.title,
        description=item.description,
        url=item.url,
        primary_domain=cls.primary_domain if cls else "General Machine Learning",
        secondary_domains=cls.secondary_domains if cls and cls.secondary_domains else [],
        domain_confidence=cls.confidence_scores.get(cls.primary_domain, 0.8) if cls and cls.confidence_scores else 0.8,
        impact_score=pred.score_display if pred else 5.0,
        top_drivers=top_drivers,
        is_rising=bool(item.metadata_json.get("is_rising", False)) if item.metadata_json else False,
        has_insights=ins is not None,
        created_at=item.created_at or item.ingested_at,
        metadata=item.metadata_json or {},
        insight=insight_dict,
        all_predictions=all_preds,
    )


@router.get("/{item_id}/insights", response_model=InsightStatusResponse)
def get_item_insights(item_id: str, db: Session = Depends(get_db)):
    """
    Lazy-loaded AI insight endpoint.
    Returns 200 with structured insight if available, or 202 Accepted if queued.
    """
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    ins = item.insight
    if ins:
        return InsightStatusResponse(
            status="ready",
            item_id=item_id,
            insight=InsightResponse(
                item_id=item_id,
                summary=ins.summary,
                key_takeaways=ins.key_takeaways or [],
                why_it_matters=ins.why_it_matters,
                technical_depth=ins.technical_depth,
                estimated_read_time=ins.estimated_read_time,
                related_topics=ins.related_topics or [],
                llm_model=ins.llm_model,
                generated_at=ins.generated_at,
            ),
        )

    # If not yet generated, return processing status (would trigger celery task in full queue)
    return InsightStatusResponse(
        status="processing",
        item_id=item_id,
        insight=None,
    )
