from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request
import logging
import traceback

from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.db.init_db import init_admin

from app.api import auth, users, issues, stats, deps
from app.metrics import prometheus as metrics
from app.utils.websocket import manager
from app.workers.stats_worker import start as start_scheduler

# ─────────────────────────────────────────────────────
# Logging setup for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────
# Create DB Tables and Initialize Admin User
try:
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created.")
    
    # Initialize admin user
    db = SessionLocal()
    try:
        init_admin(db)
        logger.info("✅ Admin user initialized.")
    except Exception as e:
        logger.error(f"❌ Failed to initialize admin user: {e}")
    finally:
        db.close()
        
except Exception as e:
    logger.error(f"❌ Failed to create tables: {e}")

# ─────────────────────────────────────────────────────
# Initialize FastAPI app
app = FastAPI(
    title="Issues & Insights Tracker",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# ─────────────────────────────────────────────────────
# Global error handler (to log 500 errors)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    logger.error(f"❌ Internal Server Error: {exc}\nTraceback:\n{tb}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},  # Show the real error in the response for debugging
    )

# ─────────────────────────────────────────────────────
# CORS Setup (Allow all for dev; restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────
# API Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(issues.router, prefix="/api/issues", tags=["Issues"])
app.include_router(stats.router, prefix="/api/stats", tags=["Stats"])
app.include_router(metrics.router, tags=["Metrics"])  # exposes /metrics

# ─────────────────────────────────────────────────────
# WebSocket Endpoint
@app.websocket("/ws/issues")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep connection alive
    except Exception:
        manager.disconnect(websocket)

# ─────────────────────────────────────────────────────
# Start APScheduler background job (for daily stats)
try:
    start_scheduler()
    logger.info("✅ Scheduler started.")
except Exception as e:
    logger.error(f"❌ Failed to start scheduler: {e}")
