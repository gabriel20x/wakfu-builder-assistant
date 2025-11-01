from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import engine, Base
from app.routers import solver, items, gamedata

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Wakfu Builder Crafter API",
    description="API for generating Wakfu equipment builds",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(solver.router, prefix="/build", tags=["solver"])
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(gamedata.router, prefix="/gamedata", tags=["gamedata"])

@app.get("/")
async def root():
    return {
        "message": "Wakfu Builder Crafter API",
        "version": "0.1.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

