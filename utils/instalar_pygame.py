#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║           INSTALADOR DE PYGAME PARA BOBI                     ║
║           Instala pygame para reproducción de audio          ║
╚══════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys

def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           INSTALANDO PYGAME PARA AUDIO                      ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    print("📦 Instalando pygame...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pygame>=2.5.0"],
            check=True
        )
        print("✅ pygame instalado correctamente")
        print()
        
        # Verificar instalación
        print("🔍 Verificando instalación...")
        import pygame
        print(f"✅ pygame {pygame.version.ver} detectado")
        print()
        
        # Probar audio
        print("🔊 Probando sistema de audio...")
        pygame.mixer.init()
        print("✅ Sistema de audio funcionando")
        print()
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                    ✅ INSTALACIÓN EXITOSA                    ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()
        print("Ahora puedes ejecutar:")
        print("  python bobi_gui.py")
        print()
        print("La voz de Bobi sonará natural y se reproducirá inline")
        print("(sin abrir ventanas externas)")
        
    except subprocess.CalledProcessError:
        print("❌ Error instalando pygame")
        print()
        print("Intenta manualmente:")
        print("  pip install pygame")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
