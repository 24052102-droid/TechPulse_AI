import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.core.database import init_db
from backend.app.api import api_router
from backend.app.ml.inference import ml_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("atip.backend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist and ML models are loaded
    logger.info("Starting up TechPulse AI backend (ATIP)...")
    init_db()
    if not ml_engine.is_loaded:
        ml_engine.load_models()
    logger.info("Backend startup complete. ML models loaded: %s", ml_engine.is_loaded)
    yield
    logger.info("Shutting down TechPulse AI backend...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Autonomous Technical Intelligence & Prediction Platform (ATIP / TechPulse AI) API",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Timing middleware to log latency and append X-Process-Time header (verifying NFR-02).
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000.0
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    return response


# Mount API routers under /api
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    return {
        "platform": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "docs": "/docs",
        "endpoints": {
            "feed": f"{settings.API_V1_PREFIX}/feed",
            "trends": f"{settings.API_V1_PREFIX}/trends",
            "search": f"{settings.API_V1_PREFIX}/search",
            "health": f"{settings.API_V1_PREFIX}/health",
            "evaluation": f"{settings.API_V1_PREFIX}/evaluation",
        },
    }
