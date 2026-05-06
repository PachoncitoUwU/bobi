@echo off
REM ══════════════════════════════════════════════════════════════
REM  BOBI - Iniciar Interfaz Web
REM ══════════════════════════════════════════════════════════════

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              INICIANDO BOBI - INTERFAZ WEB                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Verificar Flask
python -c "import flask" 2>nul
if errorlevel 1 (
    echo 📦 Instalando Flask...
    pip install flask flask-cors
    if errorlevel 1 (
        echo ❌ Error instalando Flask
        pause
        exit /b 1
    )
    echo ✅ Flask instalado
    echo.
)

REM Iniciar servidor
echo 🚀 Iniciando servidor web...
echo.
python bobi_web.py

pause
