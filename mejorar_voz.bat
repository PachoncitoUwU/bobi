@echo off
REM ══════════════════════════════════════════════════════════════
REM  MEJORAR VOZ DE BOBI - Script de Instalación Rápida
REM ══════════════════════════════════════════════════════════════

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║           MEJORANDO LA VOZ DE BOBI                           ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📦 Instalando pygame para reproducción de audio...
python -m pip install pygame>=2.5.0
if errorlevel 1 (
    echo ❌ Error instalando pygame
    pause
    exit /b 1
)
echo ✅ pygame instalado
echo.

echo 📦 Verificando edge-tts...
python -m pip install edge-tts>=6.1.0
if errorlevel 1 (
    echo ❌ Error instalando edge-tts
    pause
    exit /b 1
)
echo ✅ edge-tts instalado
echo.

echo 🧪 Probando sistema de voz...
python utils/test_voz_mejorada.py
if errorlevel 1 (
    echo ⚠️  Hubo un problema con el test
    echo.
    echo Pero puedes intentar ejecutar la interfaz:
    echo   python bobi_gui.py
    echo.
    pause
    exit /b 0
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    ✅ VOZ MEJORADA                           ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Ahora ejecuta:
echo   python bobi_gui.py
echo.
echo La voz de Bobi sonará natural y no abrirá ventanas externas
echo.
pause
