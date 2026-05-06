#!/usr/bin/env python3
"""
Script de prueba para verificar que Gemini funcione
"""

import os
import sys

print("🔍 Probando conexión con Gemini...")
print("=" * 50)

# Verificar API key
api_key = os.getenv("GEMINI_API_KEY", "")
if not api_key:
    print("❌ No hay API key configurada")
    print("\nConfigura con:")
    print('  $env:GEMINI_API_KEY="tu-key-aqui"')
    sys.exit(1)

print(f"✓ API key encontrada: {api_key[:20]}...")

# Intentar importar librería
try:
    from google import genai
    print("✓ Librería google-genai instalada")
except ImportError:
    print("❌ Librería google-genai no instalada")
    print("\nInstala con:")
    print("  pip install google-genai")
    sys.exit(1)

# Intentar conectar
print("\n🔌 Conectando con Gemini...")
try:
    client = genai.Client(api_key=api_key)
    print("✓ Cliente creado")
except Exception as e:
    print(f"❌ Error creando cliente: {e}")
    sys.exit(1)

# Probar modelos
print("\n🧪 Probando modelos disponibles...")
models_to_try = [
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-pro",
]

working_model = None
for model in models_to_try:
    try:
        print(f"\n  Probando {model}...", end=" ")
        response = client.models.generate_content(
            model=model,
            contents="Say hello"
        )
        
        if hasattr(response, 'text') and response.text:
            print(f"✅ FUNCIONA")
            print(f"    Respuesta: {response.text[:50]}...")
            working_model = model
            break
        else:
            print("❌ Sin respuesta")
    
    except Exception as e:
        error_str = str(e)
        if "404" in error_str or "not found" in error_str.lower():
            print("❌ No encontrado")
        elif "API key" in error_str or "invalid" in error_str.lower():
            print(f"❌ API key inválida")
            print(f"\n⚠️  Error: {e}")
            print("\nVerifica tu API key en:")
            print("  https://aistudio.google.com/apikey")
            sys.exit(1)
        else:
            print(f"❌ Error: {str(e)[:60]}")

# Resultado final
print("\n" + "=" * 50)
if working_model:
    print(f"\n✅ ¡GEMINI FUNCIONA!")
    print(f"   Modelo: {working_model}")
    print("\nBobi debería funcionar ahora.")
    print("Ejecuta: python bobi.py")
else:
    print("\n❌ NINGÚN MODELO FUNCIONA")
    print("\nPosibles causas:")
    print("  1. API key inválida o expirada")
    print("  2. Límite de requests alcanzado")
    print("  3. Problema de conexión a internet")
    print("\nSoluciones:")
    print("  1. Verifica tu API key en: https://aistudio.google.com/apikey")
    print("  2. Crea una nueva API key si es necesario")
    print("  3. Espera unos minutos si alcanzaste el límite")
