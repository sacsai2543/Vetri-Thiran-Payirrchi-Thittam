@echo off
TITLE LegalEase - AI Legal Document Generator

echo ===================================================
echo     LegalEase: AI Legal Document Generator
echo ===================================================
echo.

SET PYTHON_EXEC=.venv\python.exe
IF NOT EXIST "%PYTHON_EXEC%" (
    SET PYTHON_EXEC=python
)

echo [1/3] Checking dependencies...
"%PYTHON_EXEC%" -m pip install -r requirements.txt --quiet

echo [2/3] Starting FastAPI Backend on http://localhost:8000...
start /B "" "%PYTHON_EXEC%" -m uvicorn legalEaseAPI.main:app --host 0.0.0.0 --port 8000

timeout /t 2 /nobreak >nul

echo [3/3] Starting Streamlit Frontend on http://localhost:8501...
"%PYTHON_EXEC%" -m streamlit run frontend\app.py --server.port 8501 --server.headless false

pause
