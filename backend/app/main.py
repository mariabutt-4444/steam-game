from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import health, stats, games, pipeline, predict

app = FastAPI(
    title=settings.app_name,
    description="Steam Game Popularity Predictor - Stage 1 (ETL + EDA) REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS dynamically from comma-separated environment variable
origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
if not origins:
    origins = ["*"]

allow_all = "*" in origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all else origins,
    allow_credentials=not allow_all,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers under /api
app.include_router(health.router, prefix="/api")
app.include_router(stats.router, prefix="/api")
app.include_router(games.router, prefix="/api")
app.include_router(pipeline.router, prefix="/api")
app.include_router(predict.router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "Welcome to Steam Game Popularity Predictor API",
        "docs": "/docs",
        "health": "/api/health",
        "stats": "/api/stats",
        "games": "/api/games",
    }