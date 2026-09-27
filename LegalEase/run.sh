#!/usr/bin/env bash
# LegalEase Launcher for Linux / macOS

echo "==================================================="
echo "    LegalEase: AI Legal Document Generator"
echo "==================================================="

# Check python virtualenv or system python
if [ -d ".venv" ]; then
    PYTHON_EXEC=".venv/bin/python"
else
    PYTHON_EXEC="python3"
fi

echo "[1/3] Installing dependencies..."
$PYTHON_EXEC -m pip install -r requirements.txt

echo "[2/3] Starting FastAPI Backend on http://localhost:8000..."
$PYTHON_EXEC -m uvicorn legalEaseAPI.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

sleep 2

echo "[3/3] Starting Streamlit Frontend on http://localhost:8501..."
$PYTHON_EXEC -m streamlit run frontend/app.py --server.port 8501

# Cleanup backend when frontend exits
kill $BACKEND_PID
