@echo off
REM ══════════════════════════════════════════════════════════════
REM  PROBAR TODO - Verificar que Bobi funciona
REM ══════════════════════════════════════════════════════════════

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              PROBANDO BOBI - VERIFICACIÓN                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 1️⃣  Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ Python no encontrado
    pause
    exit /b 1
)
echo ✅ Python OK
echo.

echo 2️⃣  Verificando Ollama...
ollama list
if errorlevel 1 (
    echo ❌ Ollama no encontrado
    echo.
    echo Instala Ollama desde: https://ollama.ai/download
    pause
    exit /b 1
)
echo ✅ Ollama OK
echo.

echo 3️⃣  Verificando dependencias...
python -c "import flask; print('✅ Flask OK')"
python -c "import flask_cors; print('✅ Flask-CORS OK')"
python -c "import edge_tts; print('✅ Edge-TTS OK')"
python -c "from faster_whisper import WhisperModel; print('✅ Whisper OK')"

if errorlevel 1 (
    echo.
    echo ❌ Faltan dependencias
    echo.
    echo Instalando...
    pip install flask flask-cors edge-tts faster-whisper
    echo.
)

echo.
echo 4️⃣  Verificando modelo de IA...
ollama list | findstr /C:"phi3"
if errorlevel 1 (
    echo ⚠️  Modelo phi3 no encontrado
    echo.
    echo ¿Descargar phi3 (más rápido)? (S/N)
    set /p respuesta=
    if /i "%respuesta%"=="S" (
        echo Descargando phi3...
        ollama pull phi3
    )
) else (
    echo ✅ Modelo phi3 disponible
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    ✅ VERIFICACIÓN COMPLETA                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Todo está listo. Ahora ejecuta:
echo.
echo   iniciar_web.bat
echo.
echo Luego abre tu navegador en:
echo   http://localhost:5000
echo.
echo 💡 Consejos:
echo   • Permite acceso al micrófono cuando el navegador lo pida
echo   • Verifica el volumen de tu PC
echo   • Usa Chrome o Edge (mejor compatibilidad)
echo.
pause
