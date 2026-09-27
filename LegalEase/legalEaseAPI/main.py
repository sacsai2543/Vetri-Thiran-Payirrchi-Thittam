import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import API_HOST, API_PORT
from legalEaseAPI.routes import router

app = FastAPI(
    title="LegalEase - AI Legal Document Generator",
    description="Backend API powering AI-driven legal document generation and formatting",
    version="1.0.0"
)

# Enable CORS for flexible integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


# Root endpoint
@app.get("/")
def home():
    """Health and status root endpoint."""
    return {
        "message": "Welcome to LegalEase AI Legal Document Generator API",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """Service health check endpoint."""
    return {"status": "healthy", "service": "LegalEase API"}


# Run FastAPI if executed directly
if __name__ == "__main__":
    uvicorn.run("legalEaseAPI.main:app", host=API_HOST, port=API_PORT, reload=True)
