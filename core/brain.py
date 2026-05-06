"""
Sistema de IA Multi-Proveedor
Soporta Gemini (gratis), Claude (pago), y Ollama (local)
"""

import time
import urllib.request
from typing import Optional, List, Dict
from .config import get_config

# Imports opcionales
try:
    from google import genai
    from google.genai import types
    GEMINI_OK = True
except ImportError:
    try:
        import google.generativeai as genai
        GEMINI_OK = True
        GEMINI_OLD = True
    except ImportError:
        GEMINI_OK = False
        GEMINI_OLD = False

try:
    import anthropic
    ANTHROPIC_OK = True
except ImportError:
    ANTHROPIC_OK = False

try:
    import ollama
    OLLAMA_OK = True
except ImportError:
    OLLAMA_OK = False


class AIProvider:
    """Clase base para proveedores de IA"""
    
    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config
        self.available = False
        self.history = []
    
    def is_available(self) -> bool:
        """Verifica si el proveedor está disponible"""
        return self.available
    
    def think(self, message: str, system_prompt: str = "") -> str:
        """Genera respuesta (debe ser implementado por subclases)"""
        raise NotImplementedError
    
    def clear_history(self):
        """Limpia historial de conversación"""
        self.history = []


class GeminiProvider(AIProvider):
    """Proveedor Gemini (Google) - GRATIS"""
    
    def __init__(self, config: dict):
        super().__init__("Gemini", config)
        self.client = None
        self.model_name = None
        self._initialize()
    
    def _initialize(self):
        """Inicializa cliente de Gemini"""
        if not GEMINI_OK:
            print("⚠️  google-genai no instalado. Instala: pip install google-genai")
            return
        
        api_key = self.config.get("api_key", "")
        if not api_key:
            print("⚠️  Gemini: No hay API key. Obtén una gratis en: https://aistudio.google.com/apikey")
            return
        
        try:
            # Configurar cliente con la nueva API
            self.client = genai.Client(api_key=api_key)
            
            # Modelos a probar (en orden de preferencia)
            models_to_try = [
                "gemini-2.0-flash-exp",
                "gemini-1.5-flash",
                "gemini-1.5-pro",
            ]
            
            # Probar cada modelo
            for model in models_to_try:
                try:
                    # Test simple con la nueva API
                    response = self.client.models.generate_content(
                        model=model,
                        contents="Hi"
                    )
                    
                    # Verificar que la respuesta tenga texto
                    if hasattr(response, 'text') and response.text:
                        self.model_name = model
                        self.available = True
                        print(f"✅ Gemini listo ({model})")
                        return
                    
                except Exception as e:
                    error_str = str(e).lower()
                    # Solo mostrar errores que no sean de modelo no encontrado
                    if "404" not in error_str and "not found" not in error_str:
                        print(f"⚠️  Probando {model}... {str(e)[:60]}")
                    continue
            
            print("❌ No se encontró un modelo de Gemini disponible")
            print("   Verifica tu API key en: https://aistudio.google.com/apikey")
            
        except Exception as e:
            print(f"❌ Error inicializando Gemini: {e}")
            print("   Verifica tu API key y conexión a internet")
    
    def think(self, message: str, system_prompt: str = "") -> str:
        """Genera respuesta con Gemini"""
        if not self.available:
            return "Gemini no está disponible. Verifica tu API key."
        
        try:
            # Construir contenido
            if system_prompt:
                full_message = f"{system_prompt}\n\nUsuario: {message}\nAsistente:"
            else:
                full_message = message
            
            # Generar respuesta
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_message,
                config=types.GenerateContentConfig(
                    temperature=get_config().get("advanced.temperature", 0.7),
                    max_output_tokens=get_config().get("advanced.max_tokens", 500),
                )
            )
            
            return response.text
        
        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower():
                return "La API key de Gemini no es válida. Verifica en Google AI Studio."
            elif "RATE_LIMIT" in error_msg or "quota" in error_msg.lower():
                return "Límite de requests alcanzado. Espera un momento."
            else:
                return f"Error en Gemini: {error_msg[:150]}"


class ClaudeProvider(AIProvider):
    """Proveedor Claude (Anthropic) - PAGO"""
    
    def __init__(self, config: dict):
        super().__init__("Claude", config)
        self.client = None
        self._initialize()
    
    def _initialize(self):
        """Inicializa cliente de Claude"""
        if not ANTHROPIC_OK:
            return
        
        api_key = self.config.get("api_key", "")
        if not api_key:
            return
        
        try:
            self.client = anthropic.Anthropic(api_key=api_key)
            self.available = True
            print(f"✅ Claude listo ({self.config.get('model')})")
        except Exception as e:
            print(f"❌ Error inicializando Claude: {e}")
    
    def think(self, message: str, system_prompt: str = "") -> str:
        """Genera respuesta con Claude"""
        if not self.available:
            return "Claude no está disponible."
        
        try:
            self.history.append({"role": "user", "content": message})
            
            response = self.client.messages.create(
                model=self.config.get("model", "claude-haiku-4-5-20251001"),
                max_tokens=get_config().get("advanced.max_tokens", 500),
                system=system_prompt,
                messages=self.history[-20:],  # Últimos 20 mensajes
            )
            
            answer = response.content[0].text
            self.history.append({"role": "assistant", "content": answer})
            return answer
        
        except Exception as e:
            return f"Error en Claude: {str(e)[:100]}"


class OllamaProvider(AIProvider):
    """Proveedor Ollama - LOCAL (sin internet)"""
    
    def __init__(self, config: dict):
        super().__init__("Ollama", config)
        self._initialize()
    
    def _initialize(self):
        """Inicializa cliente de Ollama"""
        if not OLLAMA_OK:
            print("⚠️  ollama no instalado. Instala: pip install ollama")
            return
        
        try:
            # Verificar si Ollama está corriendo
            models = ollama.list()
            model_name = self.config.get("model", "llama3.2")
            
            # Verificar si el modelo está descargado
            if not any(model_name in m.model for m in models.models):
                print(f"⬇️  Descargando {model_name}... (esto puede tardar)")
                ollama.pull(model_name)
            
            self.available = True
            print(f"✅ Ollama listo ({model_name})")
        
        except Exception as e:
            print(f"⚠️  Ollama no disponible: {e}")
            print("   Tip: Ejecuta 'ollama serve' en otra terminal")
    
    def think(self, message: str, system_prompt: str = "") -> str:
        """Genera respuesta con Ollama"""
        if not self.available:
            return "Ollama no está disponible. ¿Está corriendo 'ollama serve'?"
        
        try:
            self.history.append({"role": "user", "content": message})
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.extend(self.history[-20:])
            
            response = ollama.chat(
                model=self.config.get("model", "llama3.2"),
                messages=messages,
                options={
                    "temperature": get_config().get("advanced.temperature", 0.7),
                    "num_predict": get_config().get("advanced.max_tokens", 500),
                }
            )
            
            answer = response.message.content
            self.history.append({"role": "assistant", "content": answer})
            return answer
        
        except Exception as e:
            return f"Error en Ollama: {str(e)[:100]}"


class Brain:
    """
    Cerebro de Bobi - Gestiona múltiples proveedores de IA
    Selecciona automáticamente el mejor disponible
    """
    
    def __init__(self, memory=None):
        self.config = get_config()
        self.memory = memory
        self.providers: Dict[str, AIProvider] = {}
        self.current_provider: Optional[AIProvider] = None
        self._internet_cache = {"status": False, "timestamp": 0}
        
        self._initialize_providers()
        self._select_provider()
    
    def _initialize_providers(self):
        """Inicializa todos los proveedores configurados"""
        ai_config = self.config["ai_providers"]
        
        # Gemini
        if ai_config["gemini"]["enabled"]:
            self.providers["gemini"] = GeminiProvider(ai_config["gemini"])
        
        # Claude
        if ai_config["claude"]["enabled"]:
            self.providers["claude"] = ClaudeProvider(ai_config["claude"])
        
        # Ollama
        if ai_config["ollama"]["enabled"]:
            self.providers["ollama"] = OllamaProvider(ai_config["ollama"])
    
    def _check_internet(self) -> bool:
        """Verifica conexión a internet (con cache)"""
        now = time.time()
        if now - self._internet_cache["timestamp"] < 30:  # Cache 30 segundos
            return self._internet_cache["status"]
        
        try:
            url = self.config.get("network.check_url", "https://www.google.com")
            timeout = self.config.get("network.check_timeout", 3)
            urllib.request.urlopen(url, timeout=timeout)
            self._internet_cache["status"] = True
        except:
            self._internet_cache["status"] = False
        
        self._internet_cache["timestamp"] = now
        return self._internet_cache["status"]
    
    def _select_provider(self):
        """Selecciona el mejor proveedor disponible según prioridad"""
        mode = self.config.get("network.mode", "auto")
        
        # Modo manual
        if mode == "offline":
            if "ollama" in self.providers and self.providers["ollama"].is_available():
                self.current_provider = self.providers["ollama"]
                return
        
        # Modo automático: seleccionar por prioridad
        has_internet = self._check_internet()
        
        # Ordenar proveedores por prioridad
        sorted_providers = sorted(
            self.providers.items(),
            key=lambda x: self.config["ai_providers"][x[0]].get("priority", 99)
        )
        
        for name, provider in sorted_providers:
            # Si no hay internet, solo considerar Ollama
            if not has_internet and name != "ollama":
                continue
            
            if provider.is_available():
                self.current_provider = provider
                return
        
        # Fallback
        print("⚠️  No hay proveedores de IA disponibles")
        self.current_provider = None
    
    def think(self, message: str) -> str:
        """
        Genera respuesta usando el proveedor actual
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            Respuesta generada
        """
        if not self.current_provider:
            self._select_provider()
            if not self.current_provider:
                return ("No tengo ningún proveedor de IA disponible. "
                       "Configura Gemini (gratis) o instala Ollama.")
        
        # Construir system prompt con contexto
        system_prompt = self._build_system_prompt()
        
        # Generar respuesta
        try:
            response = self.current_provider.think(message, system_prompt)
            
            # Guardar en memoria si está disponible
            if self.memory:
                self.memory.add_interaction(message, response)
            
            return response
        
        except Exception as e:
            # Si falla, intentar con siguiente proveedor
            print(f"⚠️  Error con {self.current_provider.name}: {e}")
            self.current_provider = None
            self._select_provider()
            
            if self.current_provider:
                return self.think(message)  # Reintentar
            else:
                return f"Error generando respuesta: {str(e)[:100]}"
    
    def _build_system_prompt(self) -> str:
        """Construye el system prompt con personalidad y contexto"""
        nombre = self.config.get("nombre", "Bobi")
        
        prompt = f"""Eres {nombre}, un asistente virtual inteligente que vive en esta casa.

PERSONALIDAD:
- Amigable y cercano, hablas de forma natural
- Directo: respuestas concretas sin rodeos
- Con humor sutil cuando es apropiado
- Recuerdas conversaciones anteriores
- Hablas en español latinoamericano

FORMATO:
- Responde como si hablaras en voz alta
- Sin markdown, sin listas con viñetas
- Máximo 2-3 oraciones (salvo que pidan más detalle)
- No empieces siempre con "Claro" o "Por supuesto"

CAPACIDADES:
- Controlar dispositivos de la casa (luces, enchufes)
- Recordatorios y alarmas
- Búsquedas en internet
- Control de música y multimedia
- Conversación natural sobre cualquier tema
"""
        
        # Agregar contexto de memoria
        if self.memory:
            context = self.memory.get_context()
            if context:
                prompt += f"\n\nCONTEXTO:\n{context}"
        
        return prompt
    
    def get_status(self) -> dict:
        """Obtiene estado actual del cerebro"""
        return {
            "current_provider": self.current_provider.name if self.current_provider else None,
            "available_providers": [name for name, p in self.providers.items() if p.is_available()],
            "has_internet": self._check_internet(),
            "mode": self.config.get("network.mode", "auto"),
        }
    
    def switch_provider(self, provider_name: str) -> bool:
        """Cambia manualmente de proveedor"""
        if provider_name in self.providers and self.providers[provider_name].is_available():
            self.current_provider = self.providers[provider_name]
            return True
        return False
    
    def clear_history(self):
        """Limpia historial de todos los proveedores"""
        for provider in self.providers.values():
            provider.clear_history()
