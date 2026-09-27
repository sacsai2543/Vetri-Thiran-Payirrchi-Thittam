import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory of LegalEase
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Google Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEFAULT_MODEL = os.getenv("DEFAULT_GEMINI_MODEL", "gemini-1.5-pro")

# FastAPI Backend Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Asset Paths
IMAGE_DIR = BASE_DIR / "image"
DOCS_DIR = BASE_DIR / "docs"

DOC_LOGO_PATH = IMAGE_DIR / "Logo.png"
WEB_LOGO_PATH = IMAGE_DIR / "inverseLogo.png"

# Ensure directories exist
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Auto-provision logo assets if needed
def ensure_assets():
    import shutil
    brain_dir = Path(r"C:\Users\acer\.gemini\antigravity-ide\brain\6be1a216-7cf9-452e-8ef7-e565c05d7fd0")
    source_white = brain_dir / "legalease_white_bg_1790435106281.jpg"
    source_inverse = brain_dir / "legalease_inverse_1790435085253.jpg"

    if not DOC_LOGO_PATH.exists() and source_white.exists():
        shutil.copy2(source_white, DOC_LOGO_PATH)
    if not WEB_LOGO_PATH.exists() and source_inverse.exists():
        shutil.copy2(source_inverse, WEB_LOGO_PATH)

ensure_assets()

