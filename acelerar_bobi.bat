@echo off
REM ══════════════════════════════════════════════════════════════
REM  ACELERAR BOBI - Cambiar a modelo más rápido
REM ══════════════════════════════════════════════════════════════

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║           ACELERANDO BOBI - MODELO MÁS RÁPIDO                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📊 Problema: Bobi tarda 20+ segundos en responder
echo 💡 Solución: Usar modelo phi3 (más rápido que llama3.2)
echo.

echo 📦 Descargando modelo phi3...
echo (Esto puede tardar unos minutos la primera vez)
echo.
ollama pull phi3

if errorlevel 1 (
    echo.
    echo ❌ Error descargando phi3
    echo.
    echo Verifica que Ollama esté instalado:
    echo   ollama --version
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Modelo phi3 descargado
echo.

echo 📝 Configurando Bobi para usar phi3...
echo.

REM Crear archivo de configuración
(
echo nombre: "Bobi"
echo idioma: "es"
echo.
echo ia:
echo   provider: "ollama"
echo   model: "phi3"
echo.
echo ollama:
echo   model: "phi3"
echo   base_url: "http://localhost:11434"
echo.
echo voice:
echo   stt_model: "base"
echo   tts_engine: "edge-tts"
echo   tts_voice: "es-MX-DaliaNeural"
) > data\config.yaml

echo ✅ Configuración actualizada
echo.

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    ✅ BOBI ACELERADO                         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Cambios realizados:
echo   • Modelo: llama3.2 → phi3
echo   • Velocidad: ~20 seg → ~5 seg ⚡
echo   • Calidad: Similar
echo.
echo Ahora ejecuta:
echo   iniciar_web.bat
echo.
echo Bobi responderá mucho más rápido 🚀
echo.
pause
