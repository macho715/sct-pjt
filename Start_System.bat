@echo off
TITLE ADNOC Logistics AI System Launcher
CLS

ECHO ==========================================================
ECHO   PROJECT SCHEDULER AI - ADNOC HVDC
ECHO   (Anti-Gravity Engine v2.0 - Native Mode)
ECHO ==========================================================
ECHO.

:: ------------------------------------------------------------
:: 1. Backend Server Launch (Python/FastAPI)
:: ------------------------------------------------------------
ECHO [1/3] Starting AI Engine (Backend Port: 8000)...
:: 새 창을 열고 가상환경 진입 후 서버 실행
START "AI_Backend_Server" cmd /k "cd backend && venv\Scripts\activate && uvicorn main_api:app --reload --port 8000"

:: ------------------------------------------------------------
:: 2. Frontend Server Launch (Next.js/Tremor)
:: ------------------------------------------------------------
ECHO [2/3] Starting Dashboard UI (Frontend Port: 3000)...
:: 서버 로딩 대기 (3초)
TIMEOUT /T 3 /NOBREAK >NUL
:: 새 창을 열고 Next.js 실행
START "Web_Dashboard_Client" cmd /k "cd frontend && npm run dev"

:: ------------------------------------------------------------
:: 3. Launch Browser
:: ------------------------------------------------------------
ECHO [3/3] Opening Dashboard in Browser...
:: UI 서버 로딩 대기 (5초)
TIMEOUT /T 5 /NOBREAK >NUL
START http://localhost:3000

ECHO.
ECHO ==========================================================
ECHO   SYSTEM IS LIVE!
ECHO   - Terminal 1: Backend Logs (API Calls)
ECHO   - Terminal 2: Frontend Logs (Rendering)
ECHO   - Browser: Control Center
ECHO ==========================================================
PAUSE
