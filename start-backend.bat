@echo off
REM Script para iniciar el backend en Windows

cd api

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Iniciar servidor FastAPI
echo 🚀 Iniciando servidor backend...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause

