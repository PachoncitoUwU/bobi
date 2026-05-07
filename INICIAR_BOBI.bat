@echo off
chcp 65001 >nul
title 🤖 Iniciando BOBI...

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🤖 BOBI - Asistente Virtual                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Verificar si Ollama está corriendo
echo [1/3] Verificando Ollama...
ollama list >nul 2>&1
if errorlevel 1 (
    echo ❌ Ollama no está corriendo
    echo 💡 Iniciando Ollama...
    start "" ollama serve
    timeout /t 3 >nul
)
echo ✅ Ollama listo

REM Verificar si el modelo está instalado
echo.
echo [2/3] Verificando modelo de IA...
ollama list | findstr "llama3.2" >nul
if errorlevel 1 (
    ollama list | findstr "phi3" >nul
    if errorlevel 1 (
        echo ❌ No hay modelo instalado
        echo 💡 Descargando llama3.2 (esto puede tardar)...
        ollama pull llama3.2
    )
)
echo ✅ Modelo listo

REM Verificar dependencias
echo.
echo [3/3] Verificando dependencias...
python -c "import edge_tts" >nul 2>&1
if errorlevel 1 (
    echo 💡 Instalando edge-tts...
    pip install edge-tts >nul 2>&1
)
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo 💡 Instalando pygame...
    pip install pygame >nul 2>&1
)
echo ✅ Dependencias listas

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🚀 INICIANDO BOBI                         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 💡 Elige tu interfaz:
echo    [1] Interfaz Gráfica (Recomendado)
echo    [2] Interfaz Web
echo    [3] Modo Terminal
echo.
choice /c 123 /n /m "Selecciona (1/2/3): "

if errorlevel 3 goto terminal
if errorlevel 2 goto web
if errorlevel 1 goto gui

:gui
echo.
echo 🎨 Iniciando interfaz gráfica...
python bobi_gui.py
goto end

:web
echo.
echo 🌐 Iniciando interfaz web...
echo 📱 Abre tu navegador en: http://localhost:5000
echo.
python bobi_web.py
goto end

:terminal
echo.
echo 💻 Iniciando modo terminal...
python bobi.py
goto end

:end
echo.
echo 👋 ¡Hasta luego!
pause
