#!/usr/bin/env python3
"""
Script de verificación de instalación de Bobi
Verifica que todas las dependencias estén instaladas correctamente
"""

import sys

print("🔍 Verificando instalación de Bobi...\n")
print("=" * 50)

# Python version
print(f"\n✓ Python {sys.version.split()[0]}")

# Dependencias requeridas
deps = {
    "yaml": ("pyyaml", "Configuración"),
    "google.generativeai": ("google-generativeai", "IA Gemini"),
    "pyaudio": ("pyaudio", "Captura de audio"),
    "faster_whisper": ("faster-whisper", "Reconocimiento de voz"),
    "pyttsx3": ("pyttsx3", "Síntesis de voz"),
    "rich": ("rich", "Terminal bonita"),
    "colorama": ("colorama", "Colores"),
}

# Dependencias opcionales
optional_deps = {
    "anthropic": ("anthropic", "IA Claude (opcional)"),
    "ollama": ("ollama", "IA Local (opcional)"),
    "flask": ("flask", "Dashboard web (próximamente)"),
}

print("\n📦 DEPENDENCIAS REQUERIDAS:")
print("-" * 50)

required_ok = True
for module, (package, desc) in deps.items():
    try:
        __import__(module)
        print(f"✓ {package:30} - {desc}")
    except ImportError:
        print(f"✗ {package:30} - {desc}")
        print(f"  → Instala: pip install {package}")
        required_ok = False

print("\n📦 DEPENDENCIAS OPCIONALES:")
print("-" * 50)

for module, (package, desc) in optional_deps.items():
    try:
        __import__(module)
        print(f"✓ {package:30} - {desc}")
    except ImportError:
        print(f"○ {package:30} - {desc} (no instalado)")

# Verificar API keys
print("\n🔑 API KEYS:")
print("-" * 50)

import os

gemini_key = os.getenv("GEMINI_API_KEY", "")
if gemini_key:
    print(f"✓ GEMINI_API_KEY configurada ({gemini_key[:10]}...)")
else:
    print("○ GEMINI_API_KEY no configurada")
    print("  → Obtén una gratis: https://makersuite.google.com/app/apikey")
    print("  → Configura: export GEMINI_API_KEY='tu-key'")

claude_key = os.getenv("ANTHROPIC_API_KEY", "")
if claude_key:
    print(f"✓ ANTHROPIC_API_KEY configurada ({claude_key[:10]}...)")
else:
    print("○ ANTHROPIC_API_KEY no configurada (opcional)")

# Verificar archivos core
print("\n📁 ARCHIVOS CORE:")
print("-" * 50)

from pathlib import Path

core_files = [
    "core/__init__.py",
    "core/config.py",
    "core/brain.py",
    "core/voice.py",
    "core/memory.py",
    "bobi.py",
]

files_ok = True
for file in core_files:
    if Path(file).exists():
        print(f"✓ {file}")
    else:
        print(f"✗ {file} - FALTA")
        files_ok = False

# Resultado final
print("\n" + "=" * 50)

if required_ok and files_ok:
    print("\n✅ INSTALACIÓN COMPLETA")
    print("\nPuedes iniciar Bobi con:")
    print("  python bobi.py")
    
    if not gemini_key:
        print("\n⚠️  Recuerda configurar GEMINI_API_KEY para usar IA online")
else:
    print("\n❌ INSTALACIÓN INCOMPLETA")
    print("\nInstala las dependencias faltantes:")
    print("  pip install -r requirements.txt")

print("\n" + "=" * 50)
