import logging
from backend.app.tasks.celery_app import celery_app
from backend.app.core.database import SessionLocal
from backend.app.models.item import Item
from backend.app.models.classification import Classification
from backend.app.models.pipeline_error import PipelineError
from backend.app.ml.features import CATEGORY_TO_DOMAIN, DOMAIN_LABELS

logger = logging.getLogger(__name__)

DOMAIN_KEYWORDS = {
    "Natural Language Processing": ["nlp", "language model", "llm", "text", "translation", "bert", "gpt", "transformer", "token", "sentiment", "tokenizer", "rag"],
    "Computer Vision": ["vision", "image", "video", "segmentation", "detection", "yolo", "diffusion", "diffusion model", "pixel", "depth", "optical", "3d mesh"],
    "Reinforcement Learning": ["reinforcement learning", "rl", "policy gradient", "mdp", "reward", "q-learning", "actor-critic", "agent", "environment", "atari"],
    "IoT and Embedded Systems": ["iot", "embedded", "microcontroller", "edge", "tinyml", "arduino", "raspberry", "sensor", "fpga", "low-power", "ble"],
    "Systems and Infrastructure": ["distributed", "kubernetes", "cloud", "cache", "serverless", "runtime", "latency", "cuda", "compiler", "acceleration", "gpu"],
    "Robotics": ["robot", "robotics", "manipulation", "drone", "autonomous vehicle", "slam", "kinematics", "lidar", "actuator", "locomotion"],
    "Security and Privacy": ["security", "privacy", "cryptography", "adversarial", "vulnerability", "malware", "federated learning", "differential privacy", "exploit"],
    "Data Engineering and Pipelines": ["pipeline", "etl", "database", "data engineering", "spark", "streaming", "data warehouse", "lakehouse", "parquet", "kafka"],
    "Multimodal and Foundation Models": ["multimodal", "vlm", "clip", "vision-language", "audio-visual", "foundation model", "omni", "cross-modal"],
    "General Machine Learning": ["classification", "regression", "optimization", "clustering", "loss function", "gradient descent", "neural network", "deep learning"],
}


def classify_text_to_domains(title: str, description: str, category_hint: str = None) -> tuple[str, list[str], dict[str, float]]:
    """
    Evaluates text relevance across the 10 ATIP domains, returning primary domain,
    secondary domains, and normalized confidence scores.
    """
    text = f"{title.lower()} {description.lower()}"
    scores = {d: 0.05 for d in DOMAIN_LABELS}

    # 1. Apply category hint if available (from arXiv category or GitHub topic)
    if category_hint and category_hint in CATEGORY_TO_DOMAIN:
        hint_domain = CATEGORY_TO_DOMAIN[category_hint]
        scores[hint_domain] += 0.50

    # 2. Score keyword matches
    for domain, kw_list in DOMAIN_KEYWORDS.items():
        match_count = sum(1 for kw in kw_list if kw in text)
        if match_count > 0:
            scores[domain] += min(0.40, match_count * 0.12)

    # Normalize scores so highest score is dominant
    total = sum(scores.values())
    norm_scores = {d: round(s / total, 3) for d, s in scores.items()}

    sorted_domains = sorted(norm_scores.items(), key=lambda x: x[1], reverse=True)
    primary_domain = sorted_domains[0][0]
    primary_score = sorted_domains[0][1]

    # Secondary domains with confidence > 0.15
    secondary = [d for d, s in sorted_domains[1:3] if s >= 0.15]

    return primary_domain, secondary, norm_scores


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def classify_batch_task(self, item_ids: list[str]):
    """
    Stage 3: Classifies unclassified items into the 10 ATIP domain taxonomy.
    """
    if not item_ids:
        return {"status": "skipped", "classified_count": 0}

    logger.info("Executing classification batch for %d items...", len(item_ids))
    db = SessionLocal()
    classified_count = 0

    try:
        items = db.query(Item).filter(Item.id.in_(item_ids)).all()
        for item in items:
            existing = db.query(Classification).filter(Classification.item_id == item.id).first()
            if existing:
                continue

            # Extract category hint if arXiv paper
            cat_hint = None
            meta = item.metadata_json or {}
            if item.source == "arxiv" and "categories" in meta:
                cats = meta["categories"]
                if cats and isinstance(cats, list):
                    cat_hint = cats[0]

            primary_domain, secondary_domains, conf_scores = classify_text_to_domains(
                item.title, item.description or "", cat_hint
            )

            primary_score = conf_scores.get(primary_domain, 0.5)
            low_conf = primary_score < 0.35

            # Check if item exhibits viral / rising velocity
            is_rising = False
            if item.source == "github":
                stars = meta.get("stargazers_count", 0)
                if stars > 500:
                    is_rising = True
            elif item.source == "hn":
                points = meta.get("points", 0)
                if points > 100:
                    is_rising = True
            
            if is_rising:
                meta["is_rising"] = True
                item.metadata_json = meta

            cls = Classification(
                item_id=item.id,
                primary_domain=primary_domain,
                secondary_domains=secondary_domains,
                confidence_scores=conf_scores,
                low_confidence=low_conf,
                model_version="domain_classifier_v1.0",
            )
            db.add(cls)
            classified_count += 1

        db.commit()
        logger.info("Successfully classified %d items across ATIP taxonomy", classified_count)
        return {"status": "success", "classified_count": classified_count}
    except Exception as e:
        db.rollback()
        logger.error("Classification batch failed: %s", e)
        error_log = PipelineError(task_name="classify_batch_task", error_msg=str(e))
        db.add(error_log)
        if hasattr(self, "request") and self.request.id:
            raise self.retry(exc=e)
        raise e
    finally:
        db.close()
