#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                   BOBI - Asistente Virtual                   ║
║                        Versión 1.0                           ║
║                                                              ║
║  🤖 IA: Gemini (gratis) + Ollama (local)                     ║
║  🎙️  Voz: Whisper (STT) + Piper/espeak (TTS)                ║
║  🧠 Memoria persistente y personalidad                       ║
║  🔌 Sistema de plugins extensible                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

import sys
import time
import datetime
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from core.config import get_config
from core.brain import Brain
from core.voice import VoiceEngine
from core.memory import Memory

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    console = Console()
    RICH_OK = True
except ImportError:
    RICH_OK = False
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
    console = Console()


class Bobi:
    """Asistente Virtual Principal"""
    
    def __init__(self):
        self.config = get_config()
        self.nombre = self.config.get("nombre", "Bobi")
        
        # Inicializar componentes
        print("🚀 Iniciando Bobi...")
        self.memory = Memory()
        self.brain = Brain(self.memory)
        self.voice = VoiceEngine()
        
        # Modo de entrada
        self.voice_mode = self.voice.is_available()
        
        print(f"✅ {self.nombre} listo\n")
    
    def _print_message(self, speaker: str, message: str):
        """Imprime mensaje formateado"""
        if RICH_OK:
            if speaker == "Tú":
                console.print(f"[bold blue]{speaker}:[/] {message}")
            elif speaker == self.nombre:
                console.print(f"[bold purple]{speaker}:[/] {message}")
            else:
                console.print(f"[bold]{speaker}:[/] {message}")
        else:
            print(f"{speaker}: {message}")
    
    def _show_banner(self):
        """Muestra banner de inicio"""
        status = self.brain.get_status()
        voice_status = self.voice.get_status()
        
        provider = status["current_provider"] or "Ninguno"
        internet = "✓" if status["has_internet"] else "✗"
        voice_input = "🎙️  Voz" if self.voice_mode else "⌨️  Texto"
        
        info = f"""[bold purple]{self.nombre}[/] [dim]v1.0[/]

IA: [bold]{provider}[/]
Internet: {internet}
Entrada: [green]{voice_input}[/]

[dim]Comandos: 'ayuda' · 'estado' · 'salir'[/]"""
        
        if RICH_OK:
            console.print(Panel.fit(
                info,
                title="🤖 Asistente Virtual",
                border_style="purple"
            ))
        else:
            print("=" * 50)
            print(f"  {self.nombre} v1.0")
            print(f"  IA: {provider}")
            print(f"  Internet: {internet}")
            print(f"  Entrada: {voice_input}")
            print("=" * 50)
    
    def _greeting(self):
        """Saludo inicial"""
        h = datetime.datetime.now().hour
        momento = "buenos días" if h < 12 else "buenas tardes" if h < 19 else "buenas noches"
        
        if self.memory.is_first_time():
            mensaje = f"¡Hola! Soy {self.nombre}, tu asistente personal. ¿Cómo te llamas?"
            self._print_message(self.nombre, mensaje)
            self.voice.speak(mensaje)
            self._waiting_for_name = True
        else:
            nombre_usuario = self.memory.get_user_name()
            saludo = f"¡{momento}"
            if nombre_usuario:
                saludo += f", {nombre_usuario}"
            saludo += "! ¿En qué te ayudo?"
            
            self._print_message(self.nombre, saludo)
            self.voice.speak(saludo)
            self._waiting_for_name = False
        
        self.memory.start_session()
    
    def _process_command(self, text: str) -> bool:
        """
        Procesa comandos especiales
        
        Returns:
            True si fue un comando, False si debe ir a la IA
        """
        text_lower = text.lower().strip()
        
        # Salir
        if text_lower in ["salir", "exit", "adiós", "adios", "bye", "chao", "quit"]:
            mensaje = "¡Hasta luego! Aquí estaré cuando me necesites."
            self._print_message(self.nombre, mensaje)
            self.voice.speak(mensaje, async_mode=False)
            return True
        
        # Ayuda
        if text_lower in ["ayuda", "help", "comandos"]:
            ayuda = """Puedo ayudarte con:
• Conversación natural sobre cualquier tema
• Recordatorios y alarmas (próximamente)
• Búsquedas en internet
• Control de dispositivos (próximamente)

Comandos especiales:
• 'estado' - Ver estado del sistema
• 'cambiar a [gemini/ollama]' - Cambiar IA
• 'modo [voz/texto]' - Cambiar entrada
• 'salir' - Cerrar Bobi"""
            
            self._print_message(self.nombre, ayuda)
            return True
        
        # Estado
        if text_lower in ["estado", "status", "info"]:
            status = self.brain.get_status()
            voice_status = self.voice.get_status()
            mem_stats = self.memory.get_stats()
            
            info = f"""Estado del sistema:
• IA actual: {status['current_provider']}
• IAs disponibles: {', '.join(status['available_providers'])}
• Internet: {'Sí' if status['has_internet'] else 'No'}
• Voz: {'Activa' if voice_status['enabled'] else 'Inactiva'}
• Sesiones: {mem_stats['sesiones']}
• Interacciones: {mem_stats['interacciones_totales']}"""
            
            self._print_message(self.nombre, info)
            return True
        
        # Cambiar IA
        if text_lower.startswith("cambiar a "):
            provider = text_lower.replace("cambiar a ", "").strip()
            if self.brain.switch_provider(provider):
                mensaje = f"Cambiado a {provider}."
                self._print_message(self.nombre, mensaje)
                self.voice.speak(mensaje)
            else:
                mensaje = f"No puedo cambiar a {provider}. No está disponible."
                self._print_message(self.nombre, mensaje)
                self.voice.speak(mensaje)
            return True
        
        # Cambiar modo de entrada
        if text_lower in ["modo voz", "activar voz"]:
            if self.voice.is_available():
                self.voice_mode = True
                mensaje = "Modo voz activado."
                self._print_message(self.nombre, mensaje)
                self.voice.speak(mensaje)
            else:
                mensaje = "El sistema de voz no está disponible."
                self._print_message(self.nombre, mensaje)
            return True
        
        if text_lower in ["modo texto", "desactivar voz"]:
            self.voice_mode = False
            mensaje = "Modo texto activado."
            self._print_message(self.nombre, mensaje)
            return True
        
        return False
    
    def _process_message(self, text: str):
        """Procesa mensaje del usuario"""
        if not text.strip():
            return
        
        self._print_message("Tú", text)
        
        # Verificar si es comando especial
        if self._process_command(text):
            return
        
        # Si estamos esperando el nombre
        if hasattr(self, '_waiting_for_name') and self._waiting_for_name:
            if len(text.split()) <= 3:  # Probablemente es un nombre
                self.memory.set_user_name(text.strip())
                self._waiting_for_name = False
                mensaje = f"¡Un placer, {text}! ¿En qué te puedo ayudar?"
                self._print_message(self.nombre, mensaje)
                self.voice.speak(mensaje)
                return
        
        # Enviar a la IA
        if RICH_OK:
            console.print("[dim]  pensando...[/]", end="\r")
        
        try:
            response = self.brain.think(text)
            self._print_message(self.nombre, response)
            self.voice.speak(response)
        except Exception as e:
            error_msg = f"Error: {str(e)[:100]}"
            self._print_message(self.nombre, error_msg)
    
    def run_text_mode(self):
        """Modo texto (teclado)"""
        self._greeting()
        
        while True:
            try:
                if RICH_OK:
                    text = Prompt.ask("\n[bold blue]Tú[/]")
                else:
                    text = input("\n[Tú] → ").strip()
                
                if text.lower() in ["salir", "exit", "quit"]:
                    self._process_command("salir")
                    break
                
                self._process_message(text)
            
            except (KeyboardInterrupt, EOFError):
                print()
                self._process_command("salir")
                break
    
    def run_voice_mode(self):
        """Modo voz (micrófono)"""
        self._greeting()
        
        while True:
            try:
                if RICH_OK:
                    console.print("\n[dim]🎙️  Presiona Enter para hablar (Ctrl+C para salir)[/]")
                else:
                    print("\n🎙️  Presiona Enter para hablar (Ctrl+C para salir)")
                
                input()
                
                # Grabar y transcribir
                text = self.voice.listen()
                
                if not text:
                    continue
                
                if text.lower() in ["salir", "adiós", "bye", "chao"]:
                    self._process_command("salir")
                    break
                
                self._process_message(text)
            
            except (KeyboardInterrupt, EOFError):
                print()
                self._process_command("salir")
                break
    
    def run(self):
        """Inicia Bobi"""
        self._show_banner()
        
        if self.voice_mode:
            if RICH_OK:
                console.print("[green]✓ Modo voz activado[/]")
                console.print("[dim]  (Escribe 'modo texto' para cambiar)[/]\n")
            self.run_voice_mode()
        else:
            if RICH_OK:
                console.print("[yellow]⚠️  Modo texto (voz no disponible)[/]")
                console.print("[dim]  Instala: pip install pyaudio faster-whisper[/]\n")
            self.run_text_mode()


def main():
    """Punto de entrada principal"""
    try:
        bobi = Bobi()
        bobi.run()
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
