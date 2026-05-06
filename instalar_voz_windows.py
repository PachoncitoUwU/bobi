#!/usr/bin/env python3
"""
Instalador automático de componentes de voz para Windows
Descarga e instala PyAudio precompilado
"""

import sys
import subprocess
import urllib.request
import os
from pathlib import Path

print("🎤 INSTALADOR DE VOZ PARA BOBI (Windows)")
print("=" * 50)

# Detectar versión de Python
py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
py_version_short = f"{sys.version_info.major}{sys.version_info.minor}"

print(f"\n✓ Python {py_version} detectado")

# URLs de PyAudio precompilado
PYAUDIO_URLS = {
    "3.14": "https://github.com/intxcc/pyaudio_portaudio/releases/download/v0.2.14/PyAudio-0.2.14-cp314-cp314-win_amd64.whl",
    "3.13": "https://github.com/intxcc/pyaudio_portaudio/releases/download/v0.2.14/PyAudio-0.2.14-cp313-cp313-win_amd64.whl",
    "3.12": "https://github.com/intxcc/pyaudio_portaudio/releases/download/v0.2.14/PyAudio-0.2.14-cp312-cp312-win_amd64.whl",
    "3.11": "https://github.com/intxcc/pyaudio_portaudio/releases/download/v0.2.14/PyAudio-0.2.14-cp311-cp311-win_amd64.whl",
    "3.10": "https://github.com/intxcc/pyaudio_portaudio/releases/download/v0.2.14/PyAudio-0.2.14-cp310-cp310-win_amd64.whl",
}

def instalar_pyaudio():
    """Instala PyAudio precompilado"""
    print("\n📦 Instalando PyAudio...")
    
    if py_version not in PYAUDIO_URLS:
        print(f"❌ No hay PyAudio precompilado para Python {py_version}")
        print("   Opciones:")
        print("   1. Instala Python 3.11, 3.12 o 3.13")
        print("   2. Instala Visual C++ Build Tools y luego: pip install pyaudio")
        return False
    
    url = PYAUDIO_URLS[py_version]
    filename = f"PyAudio-0.2.14-cp{py_version_short}-cp{py_version_short}-win_amd64.whl"
    
    try:
        # Descargar
        print(f"⬇️  Descargando desde GitHub...")
        urllib.request.urlretrieve(url, filename)
        print(f"✓ Descargado: {filename}")
        
        # Instalar
        print("📦 Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", filename], check=True)
        print("✅ PyAudio instalado correctamente")
        
        # Limpiar
        os.remove(filename)
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Alternativa:")
        print("   Descarga manualmente desde:")
        print(f"   {url}")
        print(f"   Luego ejecuta: pip install {filename}")
        return False

def instalar_faster_whisper():
    """Instala faster-whisper"""
    print("\n📦 Instalando faster-whisper...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "faster-whisper"], check=True)
        print("✅ faster-whisper instalado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def instalar_pyttsx3():
    """Instala pyttsx3"""
    print("\n📦 Instalando pyttsx3...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyttsx3"], check=True)
        print("✅ pyttsx3 instalado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verificar_instalacion():
    """Verifica que todo esté instalado"""
    print("\n🔍 Verificando instalación...")
    
    exitos = []
    fallos = []
    
    # PyAudio
    try:
        import pyaudio
        print("✓ PyAudio")
        exitos.append("PyAudio")
    except ImportError:
        print("✗ PyAudio")
        fallos.append("PyAudio")
    
    # faster-whisper
    try:
        import faster_whisper
        print("✓ faster-whisper")
        exitos.append("faster-whisper")
    except ImportError:
        print("✗ faster-whisper")
        fallos.append("faster-whisper")
    
    # pyttsx3
    try:
        import pyttsx3
        print("✓ pyttsx3")
        exitos.append("pyttsx3")
    except ImportError:
        print("✗ pyttsx3")
        fallos.append("pyttsx3")
    
    return len(fallos) == 0

def main():
    print("\nEste script instalará:")
    print("  • PyAudio (captura de micrófono)")
    print("  • faster-whisper (reconocimiento de voz)")
    print("  • pyttsx3 (síntesis de voz)")
    
    respuesta = input("\n¿Continuar? (s/n): ").lower()
    if respuesta != 's':
        print("Instalación cancelada.")
        return
    
    # Instalar componentes
    pyaudio_ok = instalar_pyaudio()
    whisper_ok = instalar_faster_whisper()
    tts_ok = instalar_pyttsx3()
    
    # Verificar
    print("\n" + "=" * 50)
    if verificar_instalacion():
        print("\n✅ ¡INSTALACIÓN COMPLETA!")
        print("\nAhora puedes usar Bobi con voz:")
        print("  python bobi.py")
        print("\nBobi iniciará en modo voz automáticamente.")
    else:
        print("\n⚠️  INSTALACIÓN INCOMPLETA")
        print("\nAlgunos componentes fallaron.")
        print("Bobi funcionará en modo texto.")
        print("\nPara instalar manualmente:")
        print("  pip install pyaudio faster-whisper pyttsx3")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstalación cancelada.")
        sys.exit(1)
