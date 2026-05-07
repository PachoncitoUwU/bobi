@echo off
chcp 65001 >nul
echo.
echo  ╔══════════════════════════════════╗
echo  ║           BOBI v5                ║
echo  ║   http://localhost:5000          ║
echo  ╚══════════════════════════════════╝
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado. Instalalo desde https://python.org
    pause
    exit /b 1
)

REM Instalar dependencias si faltan
python -c "import flask, flask_cors, edge_tts" 2>nul
if errorlevel 1 (
    echo Instalando dependencias...
    pip install flask flask-cors edge-tts pycaw comtypes psutil google-generativeai
    echo.
)

REM Arrancar servidor
echo Iniciando Bobi...
echo Abre tu navegador en http://localhost:5000
echo Presiona Ctrl+C para detener.
echo.
python bobi_web.py
pause
