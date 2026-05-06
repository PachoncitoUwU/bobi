"""
Sistema de Voz - Speech-to-Text y Text-to-Speech
Soporta múltiples engines con fallbacks automáticos
Incluye edge-tts para voces naturales de Microsoft
"""

import os
import struct
import wave
import tempfile
import subprocess
import threading
import asyncio
from pathlib import Path
from typing import Optional

from .config import get_config

# Imports opcionales
try:
    import pyaudio
    AUDIO_OK = True
except ImportError:
    AUDIO_OK = False
    print("⚠️  PyAudio no instalado. Voz no disponible.")

try:
    from faster_whisper import WhisperModel
    WHISPER_OK = True
except ImportError:
    WHISPER_OK = False
    print("⚠️  faster-whisper no instalado. STT no disponible.")

try:
    import pyttsx3
    PYTTSX3_OK = True
except ImportError:
    PYTTSX3_OK = False

try:
    import edge_tts
    EDGE_TTS_OK = True
except ImportError:
    EDGE_TTS_OK = False

try:
    import pygame
    PYGAME_OK = True
except ImportError:
    PYGAME_OK = False


class STT:
    """Speech-to-Text usando Whisper"""
    
    def __init__(self):
        self.config = get_config()
        self.model = None
        self.model_name = self.config.get("voice.stt_model", "base")
        self.idioma = self.config.get("idioma", "es")
        self.available = False
        
        if WHISPER_OK:
            self._load_model()
    
    def _load_model(self):
        """Carga el modelo de Whisper"""
        try:
            print(f"🎙️  Cargando Whisper ({self.model_name})...")
            self.model = WhisperModel(
                self.model_name,
                device="cpu",
                compute_type="int8"  # Optimizado para CPU
            )
            self.available = True
            print("✅ Whisper listo")
        except Exception as e:
            print(f"❌ Error cargando Whisper: {e}")
    
    def record(self, silence_duration: float = 2.0, max_duration: float = 15.0) -> Optional[str]:
        """
        Graba audio del micrófono hasta detectar silencio
        
        Args:
            silence_duration: Segundos de silencio para detener
            max_duration: Duración máxima de grabación
            
        Returns:
            Ruta al archivo WAV temporal o None
        """
        if not AUDIO_OK:
            print("❌ PyAudio no disponible")
            return None
        
        CHUNK = 1024
        RATE = 16000
        THRESHOLD = 500  # Umbral de volumen
        
        p = pyaudio.PyAudio()
        
        try:
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
        except Exception as e:
            print(f"❌ Error abriendo micrófono: {e}")
            p.terminate()
            return None
        
        frames = []
        silence_chunks = 0
        max_silence_chunks = int(RATE / CHUNK * silence_duration)
        max_chunks = int(RATE / CHUNK * max_duration)
        recording = False
        
        print("🎙️  Escuchando...")
        
        try:
            for _ in range(max_chunks):
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
                
                # Calcular volumen
                volume = sum(
                    abs(struct.unpack_from('<h', data, i)[0])
                    for i in range(0, len(data), 2)
                ) / (len(data) // 2)
                
                if volume > THRESHOLD:
                    if not recording:
                        print("🔴 Grabando...")
                        recording = True
                    silence_chunks = 0
                elif recording:
                    silence_chunks += 1
                    if silence_chunks > max_silence_chunks:
                        print("⏹️  Silencio detectado")
                        break
        
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
        
        if not recording:
            print("⚠️  No se detectó voz")
            return None
        
        # Guardar a archivo temporal
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        with wave.open(tmp.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        
        return tmp.name
    
    def transcribe(self, audio_file: str) -> str:
        """
        Transcribe archivo de audio a texto
        
        Args:
            audio_file: Ruta al archivo de audio
            
        Returns:
            Texto transcrito
        """
        if not self.available or not audio_file:
            return ""
        
        try:
            segments, info = self.model.transcribe(
                audio_file,
                language=self.idioma,
                beam_size=1,  # Más rápido
                vad_filter=True,  # Filtro de actividad de voz
            )
            
            text = " ".join(segment.text for segment in segments).strip()
            return text
        
        except Exception as e:
            print(f"❌ Error transcribiendo: {e}")
            return ""
        
        finally:
            # Limpiar archivo temporal
            try:
                os.unlink(audio_file)
            except:
                pass
    
    def listen(self) -> str:
        """
        Graba y transcribe en un solo paso
        
        Returns:
            Texto transcrito
        """
        audio_file = self.record()
        if not audio_file:
            return ""
        
        return self.transcribe(audio_file)


class TTS:
    """Text-to-Speech con múltiples engines"""
    
    def __init__(self):
        self.config = get_config()
        self.engine_name = self.config.get("voice.tts_engine", "piper")
        self.voice = self.config.get("voice.tts_voice", "es_ES-davefx-medium")
        self.available_engines = self._detect_engines()
        
        print(f"🔊 TTS engines disponibles: {', '.join(self.available_engines)}")
    
    def _detect_engines(self) -> list:
        """Detecta qué engines de TTS están disponibles"""
        engines = []
        
        # edge-tts (Microsoft, muy natural) - MEJOR OPCIÓN
        if EDGE_TTS_OK:
            engines.append("edge-tts")
        
        # Piper (mejor calidad)
        if self._check_command("piper"):
            engines.append("piper")
        
        # espeak-ng (buena calidad, Linux)
        if self._check_command("espeak-ng"):
            engines.append("espeak-ng")
        
        # espeak (fallback, Linux)
        if self._check_command("espeak"):
            engines.append("espeak")
        
        # say (macOS)
        if self._check_command("say"):
            engines.append("say")
        
        # pyttsx3 (multiplataforma, fallback)
        if PYTTSX3_OK:
            engines.append("pyttsx3")
        
        return engines
    
    def _check_command(self, cmd: str) -> bool:
        """Verifica si un comando está disponible"""
        try:
            subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                timeout=2
            )
            return True
        except:
            return False
    
    def speak(self, text: str, async_mode: bool = True):
        """
        Convierte texto a voz
        
        Args:
            text: Texto a hablar
            async_mode: Si True, habla en background (no bloquea)
        """
        if not text.strip():
            return
        
        if async_mode:
            threading.Thread(
                target=self._speak_sync,
                args=(text,),
                daemon=True
            ).start()
        else:
            self._speak_sync(text)
    
    def _speak_sync(self, text: str):
        """Habla de forma sincrónica (bloquea hasta terminar)"""
        # Intentar engines en orden de preferencia
        for engine in self.available_engines:
            try:
                if engine == "edge-tts":
                    self._speak_edge_tts(text)
                    return
                elif engine == "piper":
                    self._speak_piper(text)
                    return
                elif engine == "espeak-ng":
                    self._speak_espeak_ng(text)
                    return
                elif engine == "espeak":
                    self._speak_espeak(text)
                    return
                elif engine == "say":
                    self._speak_say(text)
                    return
                elif engine == "pyttsx3":
                    self._speak_pyttsx3(text)
                    return
            except Exception as e:
                print(f"⚠️  Error con {engine}: {e}")
                continue
        
        print(f"❌ No se pudo hablar: {text}")
    
    def _speak_edge_tts(self, text: str):
        """TTS con edge-tts (Microsoft, muy natural)"""
        # Voces en español disponibles:
        # es-ES-AlvaroNeural (hombre, España)
        # es-ES-ElviraNeural (mujer, España)
        # es-MX-DaliaNeural (mujer, México)
        # es-MX-JorgeNeural (hombre, México)
        # es-AR-ElenaNeural (mujer, Argentina)
        # es-AR-TomasNeural (hombre, Argentina)
        
        # 🎙️ VOZ MASCULINA NEUTRAL - opciones disponibles:
        # "es-ES-AlvaroNeural"    → Hombre, España    (neutral, profesional) ← ACTUAL
        # "es-MX-JorgeNeural"    → Hombre, México    (cálido, amigable)
        # "es-AR-TomasNeural"    → Hombre, Argentina  (expresivo)
        # "es-ES-AbrilNeural"    → Mujer, España     (si prefieres femenino)
        voice = self.config.get("voice.tts_voice", "es-ES-AlvaroNeural")
        rate  = self.config.get("voice.tts_rate",  "+0%")   # ej: "+10%" más rápido, "-10%" más lento
        pitch = self.config.get("voice.tts_pitch", "+0Hz")  # ej: "-5Hz" más grave
        
        tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        
        try:
            # Generar audio con edge-tts
            async def generate():
                communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
                await communicate.save(tmp.name)
            
            # Ejecutar async
            asyncio.run(generate())
            
            # Reproducir con pygame (inline, sin abrir ventana externa)
            if PYGAME_OK:
                try:
                    # Inicializar pygame mixer si no está inicializado
                    if not pygame.mixer.get_init():
                        pygame.mixer.init()
                    
                    # Cargar y reproducir
                    pygame.mixer.music.load(tmp.name)
                    pygame.mixer.music.play()
                    
                    # Esperar a que termine
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                    
                    return
                except Exception as e:
                    print(f"⚠️  Error con pygame: {e}")
            
            # Fallback: reproducir con comando del sistema
            if os.name == 'nt':  # Windows
                # Usar PowerShell para reproducir sin abrir ventana
                subprocess.run(
                    ['powershell', '-c', f'(New-Object Media.SoundPlayer "{tmp.name}").PlaySync()'],
                    capture_output=True
                )
            else:  # Linux/Mac
                subprocess.run(["mpg123", "-q", tmp.name], capture_output=True)
        
        finally:
            try:
                import time
                time.sleep(0.5)  # Esperar un poco antes de borrar
                os.unlink(tmp.name)
            except:
                pass
    
    def _speak_piper(self, text: str):
        """TTS con Piper (mejor calidad)"""
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        
        try:
            # Generar audio
            subprocess.run(
                f'echo "{text}" | piper --model {self.voice} --output_file {tmp.name}',
                shell=True,
                check=True,
                capture_output=True
            )
            
            # Reproducir
            if os.name == 'nt':  # Windows
                os.startfile(tmp.name)
            else:  # Linux/Mac
                subprocess.run(["aplay", tmp.name], capture_output=True)
        
        finally:
            try:
                os.unlink(tmp.name)
            except:
                pass
    
    def _speak_espeak_ng(self, text: str):
        """TTS con espeak-ng"""
        subprocess.run(
            ["espeak-ng", "-v", "es", "-s", "150", text],
            capture_output=True
        )
    
    def _speak_espeak(self, text: str):
        """TTS con espeak"""
        subprocess.run(
            ["espeak", "-v", "es", text],
            capture_output=True
        )
    
    def _speak_say(self, text: str):
        """TTS con say (macOS)"""
        subprocess.run(
            ["say", "-v", "Mónica", text],
            capture_output=True
        )
    
    def _speak_pyttsx3(self, text: str):
        """TTS con pyttsx3 (multiplataforma)"""
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('voice', 'spanish')
        engine.say(text)
        engine.runAndWait()


class VoiceEngine:
    """Motor de voz completo (STT + TTS)"""
    
    def __init__(self):
        self.config = get_config()
        self.stt = STT()
        self.tts = TTS()
        self.enabled = self.stt.available and len(self.tts.available_engines) > 0
        
        if not self.enabled:
            print("⚠️  Sistema de voz no completamente disponible")
            if not self.stt.available:
                print("   - STT (Whisper) no disponible")
            if not self.tts.available_engines:
                print("   - TTS no disponible")
    
    def listen(self) -> str:
        """Escucha y transcribe"""
        if not self.stt.available:
            return ""
        return self.stt.listen()
    
    def speak(self, text: str, async_mode: bool = True):
        """Habla el texto"""
        if not self.tts.available_engines:
            print(f"[Bobi]: {text}")  # Fallback a texto
            return
        self.tts.speak(text, async_mode)
    
    def is_available(self) -> bool:
        """Verifica si el sistema de voz está disponible"""
        return self.enabled
    
    def get_status(self) -> dict:
        """Obtiene estado del sistema de voz"""
        return {
            "enabled": self.enabled,
            "stt_available": self.stt.available,
            "stt_model": self.stt.model_name,
            "tts_engines": self.tts.available_engines,
            "tts_engine": self.tts.engine_name,
        }
