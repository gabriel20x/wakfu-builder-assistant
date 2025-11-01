@echo off
REM Script para iniciar el frontend en Windows

cd frontend

REM Instalar dependencias si node_modules no existe
if not exist "node_modules" (
    echo 📦 Instalando dependencias...
    call npm install
)

REM Iniciar servidor de desarrollo
echo 🚀 Iniciando servidor de desarrollo...
call npm run dev

pause

