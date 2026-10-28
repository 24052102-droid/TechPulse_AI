"""
Master Pipeline Orchestrator for ATIP (TechPulse AI)
Executes the 6-stage autonomous processing workflow:
  Stage 1: Multi-Source Ingestion (arXiv, GitHub, HN)
  Stage 2: Metadata Enrichment (Semantic Scholar citations & author h-index)
  Stage 3: Domain Classification (Zero-shot domain taxonomy)
  Stage 4: Supervised ML Prediction (XGBoost regression + TreeSHAP drivers)
  Stage 5: LLM Insight Synthesis (Structured AI intelligence cards + Redis caching)
  Stage 6: Domain Trend & Technology Radar Aggregation (Rolling 7d stats & WoW deltas)
"""

import sys
import logging
import time
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.core.database import SessionLocal, init_db
from backend.app.models.item import Item
from backend.app.tasks.ingest import ingest_arxiv_task, ingest_github_task, ingest_hn_task
from backend.app.tasks.enrich import enrich_arxiv_batch_task
from backend.app.tasks.classify import classify_batch_task
from backend.app.tasks.predict import predict_batch_task
from backend.app.tasks.insights import generate_insights_batch_task
from backend.app.tasks.trends import aggregate_trends_task

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("atip.pipeline")


def run_autonomous_pipeline(max_per_source: int = 15) -> dict:
    """
    Executes all 6 stages of the autonomous technical intelligence pipeline.
    Can be executed via Celery Beat or run directly via CLI.
    """
    start_time = time.time()
    logger.info("======================================================================")
    logger.info("🚀 STARTING ATIP 6-STAGE AUTONOMOUS PROCESSING PIPELINE")
    logger.info("======================================================================")

    init_db()
    stats = {
        "start_time": datetime.now(timezone.utc).isoformat(),
        "stages": {},
    }

    # -------------------------------------------------------------------------
    # STAGE 1: MULTI-SOURCE INGESTION
    # -------------------------------------------------------------------------
    logger.info("\n--- [STAGE 1/6] Ingesting from arXiv, GitHub & Hacker News ---")
    s1_start = time.time()
    
    arxiv_res = ingest_arxiv_task(max_results=max_per_source)
    github_res = ingest_github_task(max_results=max_per_source)
    hn_res = ingest_hn_task(max_results=max_per_source)

    new_arxiv_ids = arxiv_res.get("new_item_ids", [])
    new_github_ids = github_res.get("new_item_ids", [])
    new_hn_ids = hn_res.get("new_item_ids", [])
    all_new_ids = new_arxiv_ids + new_github_ids + new_hn_ids

    logger.info("Stage 1 complete in %.2fs: %d new arXiv, %d new GitHub, %d new HN (Total new: %d)",
                time.time() - s1_start, len(new_arxiv_ids), len(new_github_ids), len(new_hn_ids), len(all_new_ids))

    stats["stages"]["stage_1_ingestion"] = {
        "arxiv_new": len(new_arxiv_ids),
        "github_new": len(new_github_ids),
        "hn_new": len(new_hn_ids),
        "total_new": len(all_new_ids),
        "duration_seconds": round(time.time() - s1_start, 2),
    }

    # If no net-new items were found (all already in DB), pick unprocessed items from DB
    if not all_new_ids:
        db = SessionLocal()
        try:
            unclassified = db.query(Item.id).filter(
                ~Item.id.in_(db.query(Item.id).join(Item.classification))
            ).limit(20).all()
            all_new_ids = [u[0] for u in unclassified]
            logger.info("Using %d previously unclassified items from database", len(all_new_ids))
        finally:
            db.close()

    # -------------------------------------------------------------------------
    # STAGE 2: METADATA ENRICHMENT & REPO MATCHING
    # -------------------------------------------------------------------------
    logger.info("\n--- [STAGE 2/6] Enriching arXiv papers via Semantic Scholar ---")
    s2_start = time.time()
    enrich_res = enrich_arxiv_batch_task(new_arxiv_ids or all_new_ids[:10])
    stats["stages"]["stage_2_enrichment"] = {
        "enriched_count": enrich_res.get("enriched_count", 0),
        "duration_seconds": round(time.time() - s2_start, 2),
    }

    # -------------------------------------------------------------------------
    # STAGE 3: DOMAIN CLASSIFICATION
    # -------------------------------------------------------------------------
    logger.info("\n--- [STAGE 3/6] Classifying items into 10 ATIP domain taxonomy ---")
    s3_start = time.time()
    classify_res = classify_batch_task(all_new_ids)
    stats["stages"]["stage_3_classification"] = {
        "classified_count": classify_res.get("classified_count", 0),
        "duration_seconds": round(time.time() - s3_start, 2),
    }

    # -------------------------------------------------------------------------
    # STAGE 4: SUPERVISED ML PREDICTION & TREESHAP DRIVERS
    # -------------------------------------------------------------------------
    logger.info("\n--- [STAGE 4/6] Running XGBoost impact models & TreeSHAP attributions ---")
    s4_start = time.time()
    predict_res = predict_batch_task(all_new_ids)
    stats["stages"]["stage_4_prediction"] = {
        "scored_count": predict_res.get("scored_count", 0),
        "duration_seconds": round(time.time() - s4_start, 2),
    }

    # -------------------------------------------------------------------------
    # STAGE 5: LLM INSIGHT SYNTHESIS & REDIS CACHING
    # -------------------------------------------------------------------------
    logger.info("\n--- [STAGE 5/6] Synthesizing AI insight cards with Redis cache guardrail ---")
    s5_start = time.time()
    insight_res = generate_insights_batch_task(all_new_ids)
    stats["stages"]["stage_5_insights"] = {
        "generated_count": insight_res.get("generated_count", 0),
        "duration_seconds": round(time.time() - s5_start, 2),
    }

    # -------------------------------------------------------------------------
    # STAGE 6: DAILY DOMAIN TREND & RADAR AGGREGATION
    # -------------------------------------------------------------------------
    logger.info("\n--- [STAGE 6/6] Aggregating daily domain trends & Technology Radar ---")
    s6_start = time.time()
    trend_res = aggregate_trends_task()
    stats["stages"]["stage_6_trends"] = {
        "status": trend_res.get("status"),
        "domains_updated": trend_res.get("domains_updated", 10),
        "duration_seconds": round(time.time() - s6_start, 2),
    }

    total_duration = time.time() - start_time
    stats["total_duration_seconds"] = round(total_duration, 2)
    stats["end_time"] = datetime.now(timezone.utc).isoformat()
    stats["status"] = "success"

    logger.info("======================================================================")
    logger.info("✅ ATIP 6-STAGE PIPELINE COMPLETED IN %.2f SECONDS", total_duration)
    logger.info("======================================================================")

    return stats


if __name__ == "__main__":
    max_items = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    results = run_autonomous_pipeline(max_per_source=max_items)
    print("\nPipeline Summary:")
    import json
    print(json.dumps(results, indent=2))
