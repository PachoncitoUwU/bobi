#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║           TEST DE VOZ MEJORADA CON EDGE-TTS                  ║
║           Prueba la voz natural de Microsoft                 ║
╚══════════════════════════════════════════════════════════════╝
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.voice import VoiceEngine

def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           TEST DE VOZ MEJORADA - EDGE-TTS                   ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    print("🔊 Inicializando sistema de voz...")
    voice = VoiceEngine()
    
    print()
    print("📊 Estado del sistema:")
    status = voice.get_status()
    print(f"  • Voz habilitada: {'✅' if status['enabled'] else '❌'}")
    print(f"  • STT disponible: {'✅' if status['stt_available'] else '❌'}")
    print(f"  • Modelo STT: {status['stt_model']}")
    print(f"  • Engines TTS: {', '.join(status['tts_engines'])}")
    print()
    
    if not status['tts_engines']:
        print("❌ No hay engines de TTS disponibles")
        print()
        print("Instala edge-tts y pygame:")
        print("  pip install edge-tts pygame")
        sys.exit(1)
    
    # Probar diferentes voces
    voces_test = [
        ("es-MX-DaliaNeural", "Hola, soy Dalia, una voz femenina de México"),
        ("es-MX-JorgeNeural", "Hola, soy Jorge, una voz masculina de México"),
        ("es-ES-ElviraNeural", "Hola, soy Elvira, una voz femenina de España"),
    ]
    
    print("🎤 Probando diferentes voces...")
    print("(Escucharás 3 voces diferentes)")
    print()
    
    for i, (voz, texto) in enumerate(voces_test, 1):
        print(f"{i}. Probando {voz}...")
        
        # Cambiar voz temporalmente
        voice.tts.voice = voz
        
        # Hablar (modo sincrónico para que se escuche en orden)
        voice.speak(texto, async_mode=False)
        
        print(f"   ✅ {voz} reproducida")
        print()
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    ✅ TEST COMPLETADO                        ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("¿Cuál voz te gustó más?")
    print("  1. Dalia (mujer, México) - Recomendada ⭐")
    print("  2. Jorge (hombre, México)")
    print("  3. Elvira (mujer, España)")
    print()
    print("Para cambiar la voz, edita core/voice.py línea 280:")
    print('  voice = "es-MX-DaliaNeural"  # Cambia aquí')
    print()
    print("Otras voces disponibles:")
    print("  • es-ES-AlvaroNeural (hombre, España)")
    print("  • es-AR-ElenaNeural (mujer, Argentina)")
    print("  • es-AR-TomasNeural (hombre, Argentina)")
    print("  • es-CO-SalomeNeural (mujer, Colombia)")
    print("  • es-CL-CatalinaNeural (mujer, Chile)")

if __name__ == "__main__":
    main()
