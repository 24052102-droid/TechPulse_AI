import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

# Handle SQLite vs PostgreSQL engine arguments
connect_args = {}
engine_kwargs = {"pool_pre_ping": True}

if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
    engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
else:
    engine_kwargs.update({"pool_size": 10, "max_overflow": 20})
    engine = create_engine(settings.DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a SQLAlchemy database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize all tables defined in Base metadata."""
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    # If running PostgreSQL, ensure full text search vector & GIN index exist
    if "postgresql" in settings.DATABASE_URL:
        try:
            with engine.connect() as conn:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto;"))
                conn.execute(text("""
                    ALTER TABLE items ADD COLUMN IF NOT EXISTS search_vector tsvector
                    GENERATED ALWAYS AS (
                        setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
                        setweight(to_tsvector('english', coalesce(description, '')), 'B')
                    ) STORED;
                """))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_items_search_vector ON items USING GIN (search_vector);"))
                conn.commit()
                logger.info("PostgreSQL tsvector & GIN index verified.")
        except Exception as e:
            logger.warning(f"Could not initialize PostgreSQL tsvector: {e}")
