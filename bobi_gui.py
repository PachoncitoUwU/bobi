#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              BOBI - Interfaz Gráfica Mejorada                ║
║              Asistente Virtual con Animación                 ║
╚══════════════════════════════════════════════════════════════╝
"""

import sys
import threading
import time
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from core.config import get_config
from core.brain import Brain
from core.voice import VoiceEngine
from core.memory import Memory

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, font
    GUI_OK = True
except ImportError:
    GUI_OK = False
    print("❌ tkinter no disponible")
    sys.exit(1)


class ModernButton(tk.Canvas):
    """Botón moderno con hover effect"""
    
    def __init__(self, parent, text, command, bg_color, hover_color, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text = text
        
        self.config(
            width=kwargs.get('width', 120),
            height=kwargs.get('height', 40),
            bg=parent['bg'],
            highlightthickness=0
        )
        
        # Crear rectángulo redondeado
        self.rect = self.create_rounded_rect(
            5, 5, 115, 35, radius=10, fill=bg_color, outline=""
        )
        
        # Texto
        self.text_id = self.create_text(
            60, 20,
            text=text,
            fill="white",
            font=("Segoe UI", 11, "bold")
        )
        
        # Eventos
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        
        self.tag_bind(self.rect, "<Button-1>", self._on_click)
        self.tag_bind(self.text_id, "<Button-1>", self._on_click)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        """Crea rectángulo con esquinas redondeadas"""
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)
        self.config(cursor="hand2")
    
    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color)
        self.config(cursor="")
    
    def _on_click(self, event):
        if self.command:
            self.command()


class BobiGUI:
    """Interfaz gráfica mejorada de Bobi"""
    
    def __init__(self):
        self.config = get_config()
        self.nombre = self.config.get("nombre", "Bobi")
        
        # Inicializar componentes
        self.memory = Memory()
        self.brain = Brain(self.memory)
        self.voice = VoiceEngine()
        
        # Estado
        self.listening = False
        self.thinking = False
        self.speaking = False
        self.processing = False
        
        # Crear ventana
        self.root = tk.Tk()
        self.root.title(f"{self.nombre} - Asistente Virtual")
        self.root.geometry("900x700")
        self.root.configure(bg="#0f0f1e")
        self.root.resizable(False, False)
        
        # Fuentes
        self.title_font = font.Font(family="Segoe UI", size=24, weight="bold")
        self.chat_font = font.Font(family="Segoe UI", size=11)
        self.input_font = font.Font(family="Segoe UI", size=12)
        
        self._create_widgets()
        self._start_session()
    
    def _create_widgets(self):
        """Crea los widgets de la interfaz"""
        
        # ═══ HEADER ═══
        header = tk.Frame(self.root, bg="#1a1a2e", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Título
        title_label = tk.Label(
            header,
            text=f"🤖 {self.nombre}",
            font=self.title_font,
            bg="#1a1a2e",
            fg="#00d9ff"
        )
        title_label.pack(side=tk.LEFT, padx=30, pady=20)
        
        # Estado
        self.status_label = tk.Label(
            header,
            text="● Listo",
            font=("Segoe UI", 12),
            bg="#1a1a2e",
            fg="#4ade80"
        )
        self.status_label.pack(side=tk.RIGHT, padx=30)
        
        # ═══ MAIN CONTAINER ═══
        main_container = tk.Frame(self.root, bg="#0f0f1e")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ═══ AVATAR MEJORADO ═══
        avatar_frame = tk.Frame(main_container, bg="#0f0f1e")
        avatar_frame.pack(pady=20)
        
        # Canvas más grande
        self.canvas = tk.Canvas(
            avatar_frame,
            width=250,
            height=250,
            bg="#0f0f1e",
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Círculo exterior (glow effect)
        self.glow_circle = self.canvas.create_oval(
            25, 25, 225, 225,
            fill="",
            outline="#00d9ff",
            width=2
        )
        
        # Círculo principal
        self.avatar_circle = self.canvas.create_oval(
            40, 40, 210, 210,
            fill="#1a1a2e",
            outline="#00d9ff",
            width=4
        )
        
        # Ojos más grandes
        self.left_eye = self.canvas.create_oval(
            80, 90, 105, 115,
            fill="#00d9ff"
        )
        self.right_eye = self.canvas.create_oval(
            145, 90, 170, 115,
            fill="#00d9ff"
        )
        
        # Boca sonriente
        self.mouth = self.canvas.create_arc(
            80, 130, 170, 180,
            start=0,
            extent=-180,
            style=tk.ARC,
            outline="#00d9ff",
            width=4
        )
        
        # ═══ CHAT MEJORADO ═══
        chat_container = tk.Frame(main_container, bg="#1a1a2e", relief=tk.FLAT)
        chat_container.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Área de chat con scroll
        self.chat_area = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            font=self.chat_font,
            bg="#1a1a2e",
            fg="#e0e0e0",
            insertbackground="#00d9ff",
            relief=tk.FLAT,
            padx=20,
            pady=15,
            spacing1=5,
            spacing3=5
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        # Tags para colores
        self.chat_area.tag_config("user", foreground="#00d9ff", font=("Segoe UI", 11, "bold"))
        self.chat_area.tag_config("bobi", foreground="#4ade80", font=("Segoe UI", 11, "bold"))
        self.chat_area.tag_config("system", foreground="#fbbf24", font=("Segoe UI", 10, "italic"))
        self.chat_area.tag_config("message", foreground="#e0e0e0")
        
        # ═══ INPUT MEJORADO ═══
        input_container = tk.Frame(main_container, bg="#0f0f1e")
        input_container.pack(fill=tk.X, pady=10)
        
        # Frame para input con borde
        input_frame = tk.Frame(input_container, bg="#1a1a2e", relief=tk.FLAT)
        input_frame.pack(fill=tk.X)
        
        # Campo de texto
        self.input_field = tk.Entry(
            input_frame,
            font=self.input_font,
            bg="#1a1a2e",
            fg="#e0e0e0",
            insertbackground="#00d9ff",
            relief=tk.FLAT,
            bd=0
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=12)
        self.input_field.bind("<Return>", lambda e: self._send_message())
        self.input_field.focus()
        
        # Botones
        button_frame = tk.Frame(input_container, bg="#0f0f1e")
        button_frame.pack(pady=10)
        
        # Botón enviar
        self.send_button = ModernButton(
            button_frame,
            text="Enviar",
            command=self._send_message,
            bg_color="#00d9ff",
            hover_color="#00b8d4",
            width=120,
            height=45
        )
        self.send_button.pack(side=tk.LEFT, padx=5)
        
        # Botón voz
        if self.voice.stt.available:
            self.voice_button = ModernButton(
                button_frame,
                text="🎤 Hablar",
                command=self._voice_input,
                bg_color="#4ade80",
                hover_color="#22c55e",
                width=120,
                height=45
            )
            self.voice_button.pack(side=tk.LEFT, padx=5)
        
        # Botón limpiar
        self.clear_button = ModernButton(
            button_frame,
            text="🗑️ Limpiar",
            command=self._clear_chat,
            bg_color="#ef4444",
            hover_color="#dc2626",
            width=120,
            height=45
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
    
    def _add_message(self, sender: str, message: str):
        """Agrega mensaje al chat"""
        self.chat_area.config(state=tk.NORMAL)
        
        if sender == "user":
            self.chat_area.insert(tk.END, "Tú\n", "user")
        elif sender == "bobi":
            self.chat_area.insert(tk.END, f"{self.nombre}\n", "bobi")
        else:
            self.chat_area.insert(tk.END, "Sistema\n", "system")
        
        self.chat_area.insert(tk.END, message + "\n\n", "message")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)
    
    def _clear_chat(self):
        """Limpia el chat"""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.config(state=tk.DISABLED)
    
    def _set_status(self, status: str, color: str):
        """Actualiza el estado"""
        self.status_label.config(text=f"● {status}", fg=color)
    
    def _animate_listening(self):
        """Animación de escucha"""
        self.listening = True
        self._set_status("Escuchando...", "#00d9ff")
        
        def pulse():
            colors = ["#00d9ff", "#00b8d4", "#0096b8", "#00b8d4"]
            widths = [4, 6, 8, 6]
            i = 0
            while self.listening:
                self.canvas.itemconfig(self.avatar_circle, outline=colors[i % len(colors)])
                self.canvas.itemconfig(self.glow_circle, outline=colors[i % len(colors)], width=widths[i % len(widths)])
                i += 1
                time.sleep(0.2)
            self.canvas.itemconfig(self.avatar_circle, outline="#00d9ff", width=4)
            self.canvas.itemconfig(self.glow_circle, outline="#00d9ff", width=2)
        
        threading.Thread(target=pulse, daemon=True).start()
    
    def _animate_thinking(self):
        """Animación de pensamiento"""
        self.thinking = True
        self._set_status("Pensando...", "#fbbf24")
        
        def blink():
            while self.thinking:
                # Cerrar ojos
                self.canvas.itemconfig(self.left_eye, fill="#1a1a2e")
                self.canvas.itemconfig(self.right_eye, fill="#1a1a2e")
                time.sleep(0.4)
                # Abrir ojos
                self.canvas.itemconfig(self.left_eye, fill="#00d9ff")
                self.canvas.itemconfig(self.right_eye, fill="#00d9ff")
                time.sleep(0.6)
        
        threading.Thread(target=blink, daemon=True).start()
    
    def _animate_speaking(self):
        """Animación de habla"""
        self.speaking = True
        self._set_status("Hablando...", "#4ade80")
        
        def talk():
            while self.speaking:
                # Boca abierta
                self.canvas.itemconfig(self.mouth, extent=-180, width=4)
                time.sleep(0.15)
                # Boca semi-abierta
                self.canvas.itemconfig(self.mouth, extent=-120, width=3)
                time.sleep(0.15)
        
        threading.Thread(target=talk, daemon=True).start()
    
    def _stop_animations(self):
        """Detiene todas las animaciones"""
        self.listening = False
        self.thinking = False
        self.speaking = False
        self._set_status("Listo", "#4ade80")
        # Restaurar boca
        self.canvas.itemconfig(self.mouth, extent=-180, width=4)
    
    def _send_message(self):
        """Envía mensaje de texto"""
        if self.processing:
            return
        
        message = self.input_field.get().strip()
        if not message:
            return
        
        self.input_field.delete(0, tk.END)
        self._add_message("user", message)
        
        # Procesar en thread separado
        self.processing = True
        threading.Thread(
            target=self._process_message,
            args=(message,),
            daemon=True
        ).start()
    
    def _voice_input(self):
        """Entrada por voz"""
        if not self.voice.stt.available or self.processing:
            self._add_message("system", "Reconocimiento de voz no disponible")
            return
        
        self._animate_listening()
        self.processing = True
        
        def listen():
            text = self.voice.listen()
            self.listening = False
            
            if text:
                self.root.after(0, lambda: self._add_message("user", text))
                self._process_message(text)
            else:
                self.processing = False
                self.root.after(0, lambda: self._stop_animations())
        
        threading.Thread(target=listen, daemon=True).start()
    
    def _process_message(self, message: str):
        """Procesa mensaje y genera respuesta"""
        # Animación de pensamiento
        self.root.after(0, self._animate_thinking)
        
        # Generar respuesta
        response = self.brain.think(message)
        
        # Detener pensamiento
        self.thinking = False
        
        # Mostrar respuesta
        self.root.after(0, lambda: self._add_message("bobi", response))
        
        # Hablar respuesta
        self.root.after(0, self._animate_speaking)
        self.voice.speak(response, async_mode=False)
        self.speaking = False
        
        # Volver a estado normal
        self.processing = False
        self.root.after(0, self._stop_animations)
    
    def _start_session(self):
        """Inicia sesión"""
        self.memory.start_session()
        
        # Saludo
        if self.memory.is_first_time():
            greeting = f"¡Hola! Soy {self.nombre}, tu asistente personal. ¿Cómo te llamas?"
        else:
            import datetime
            h = datetime.datetime.now().hour
            momento = "buenos días" if h < 12 else "buenas tardes" if h < 19 else "buenas noches"
            nombre_usuario = self.memory.get_user_name()
            greeting = f"¡{momento}"
            if nombre_usuario:
                greeting += f", {nombre_usuario}"
            greeting += "! ¿En qué te ayudo?"
        
        self._add_message("bobi", greeting)
        self.voice.speak(greeting)
    
    def run(self):
        """Inicia la interfaz"""
        self.root.mainloop()


def main():
    """Punto de entrada"""
    if not GUI_OK:
        print("❌ tkinter no disponible")
        sys.exit(1)
    
    try:
        app = BobiGUI()
        app.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
