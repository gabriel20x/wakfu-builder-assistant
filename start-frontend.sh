#!/bin/bash

# Script para iniciar el frontend
cd frontend

# Instalar dependencias si node_modules no existe
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias..."
    npm install
fi

# Iniciar servidor de desarrollo
echo "🚀 Iniciando servidor de desarrollo..."
npm run dev

