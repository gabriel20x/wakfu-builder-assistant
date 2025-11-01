#!/bin/bash

# Script para iniciar el backend
cd api

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Iniciar servidor FastAPI
echo "🚀 Iniciando servidor backend..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

