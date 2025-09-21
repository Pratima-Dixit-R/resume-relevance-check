import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import router

# Create FastAPI application with metadata
app = FastAPI(
    title="Resume Relevance Check API",
    description="AI-powered resume relevance analysis with Hugging Face transformers",
    version="1.0.0",
    contact={
        "name": "Pratima Dixit R",
        "email": "pratimadixit2305@gmail.com",
    }
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Resume Relevance Check API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "resume-relevance-check"}