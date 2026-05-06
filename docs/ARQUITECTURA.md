# 🏗️ ARQUITECTURA DE BOBI v1.0

Documentación técnica de la arquitectura del sistema.

---

## 📊 DIAGRAMA DE COMPONENTES

```
┌─────────────────────────────────────────────────────────────┐
│                         BOBI v1.0                           │
│                   Asistente Virtual                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         bobi.py (Main Entry)            │
        │  • Interfaz de usuario                  │
        │  • Ciclo de conversación                │
        │  • Comandos especiales                  │
        └─────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Brain      │    │    Voice     │    │   Memory     │
│              │    │              │    │              │
│ • Gemini     │    │ • STT        │    │ • Historial  │
│ • Claude     │    │ • TTS        │    │ • Hechos     │
│ • Ollama     │    │ • Whisper    │    │ • Usuario    │
│              │    │ • Piper      │    │ • Stats      │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                    ┌──────────────┐
                    │    Config    │
                    │              │
                    │ • YAML       │
                    │ • Env Vars   │
                    │ • Defaults   │
                    └──────────────┘
```

---

## 🧩 MÓDULOS PRINCIPALES

### 1. **bobi.py** - Punto de Entrada
```python
Responsabilidades:
• Inicializar componentes
• Manejar interfaz de usuario
• Procesar comandos especiales
• Ciclo de conversación (texto/voz)
• Manejo de errores
```

### 2. **core/brain.py** - Sistema de IA
```python
Clases:
• AIProvider (base)
  ├── GeminiProvider
  ├── ClaudeProvider
  └── OllamaProvider
• Brain (orquestador)

Responsabilidades:
• Gestionar múltiples proveedores
• Selección automática por prioridad
• Detección de internet
• Generación de respuestas
• Manejo de contexto
```

### 3. **core/voice.py** - Sistema de Voz
```python
Clases:
• STT (Speech-to-Text)
  └── Whisper
• TTS (Text-to-Speech)
  ├── Piper
  ├── espeak-ng
  ├── espeak
  ├── say (macOS)
  └── pyttsx3
• VoiceEngine (orquestador)

Responsabilidades:
• Captura de audio
• Transcripción
• Síntesis de voz
• Fallbacks automáticos
```

### 4. **core/memory.py** - Sistema de Memoria
```python
Clase:
• Memory

Responsabilidades:
• Persistencia de datos
• Historial de conversaciones
• Hechos importantes
• Preferencias del usuario
• Estadísticas de uso
• Generación de contexto
```

### 5. **core/config.py** - Configuración
```python
Clase:
• Config (singleton)

Responsabilidades:
• Carga de configuración
• Merge de defaults
• Variables de entorno
• Validación
• Acceso centralizado
```

---

## 🔄 FLUJO DE DATOS

### Conversación Típica:

```
1. Usuario habla/escribe
   │
   ▼
2. VoiceEngine.listen() o input()
   │
   ▼
3. Texto transcrito
   │
   ▼
4. bobi._process_message()
   │
   ├─→ ¿Es comando especial? → Ejecutar comando
   │
   └─→ No → Brain.think()
           │
           ├─→ Memory.get_context()
           │
           ├─→ Seleccionar proveedor
           │
           ├─→ Generar respuesta
           │
           └─→ Memory.add_interaction()
   │
   ▼
5. Respuesta generada
   │
   ▼
6. VoiceEngine.speak() o print()
   │
   ▼
7. Usuario escucha/lee
```

---

## 🗂️ ESTRUCTURA DE ARCHIVOS

```
bobi/
│
├── core/                          # Módulos principales
│   ├── __init__.py               # Exports del paquete
│   ├── brain.py                  # Sistema de IA (500 líneas)
│   ├── voice.py                  # Sistema de voz (400 líneas)
│   ├── memory.py                 # Sistema de memoria (200 líneas)
│   └── config.py                 # Configuración (200 líneas)
│
├── plugins/                       # Extensiones (futuro)
│   ├── __init__.py
│   ├── base.py                   # Clase base para plugins
│   ├── recordatorios.py          # Plugin de recordatorios
│   ├── busquedas.py              # Plugin de búsquedas
│   └── multimedia.py             # Plugin de multimedia
│
├── web/                           # Dashboard web (futuro)
│   ├── app.py                    # Servidor Flask
│   ├── static/                   # CSS, JS, imágenes
│   └── templates/                # HTML
│
├── data/                          # Datos persistentes
│   ├── .gitkeep                  # Mantiene carpeta en git
│   ├── memory.json               # Memoria de Bobi (generado)
│   ├── config.yaml               # Configuración (generado)
│   └── reminders.db              # Base de datos (futuro)
│
├── old_version/                   # Código anterior
│   ├── bobi_core.py              # v0.2
│   └── instalar_bobi.sh
│
├── bobi.py                        # Punto de entrada (300 líneas)
├── test_instalacion.py            # Script de verificación
├── requirements.txt               # Dependencias
├── .gitignore                     # Archivos ignorados
│
└── Documentación/
    ├── README.md                  # Documentación principal
    ├── EMPIEZA_AQUI.md           # Guía de inicio
    ├── INICIO_RAPIDO.md          # Guía rápida
    ├── INSTALACION_WINDOWS.md    # Guía Windows
    ├── PLAN_DESARROLLO.md        # Hoja de ruta
    ├── PROXIMOS_PASOS.md         # Siguientes pasos
    ├── RESUMEN_CAMBIOS.md        # Changelog
    └── ARQUITECTURA.md           # Este archivo
```

---

## 🔌 SISTEMA DE PLUGINS (Futuro)

### Arquitectura de Plugins:

```python
# plugins/base.py
class BasePlugin:
    def __init__(self, bobi):
        self.bobi = bobi
        self.name = "base"
        self.commands = {}
    
    def register_command(self, trigger, handler):
        self.commands[trigger] = handler
    
    def on_load(self):
        pass
    
    def on_message(self, message):
        pass

# plugins/recordatorios.py
class RecordatoriosPlugin(BasePlugin):
    def __init__(self, bobi):
        super().__init__(bobi)
        self.name = "recordatorios"
        self.register_command("recuérdame", self.crear_recordatorio)
    
    def crear_recordatorio(self, texto):
        # Lógica de recordatorio
        pass
```

### Carga Automática:

```python
# core/plugin_manager.py
class PluginManager:
    def __init__(self, bobi):
        self.bobi = bobi
        self.plugins = {}
    
    def load_plugins(self):
        for file in Path("plugins").glob("*.py"):
            if file.stem not in ["__init__", "base"]:
                module = importlib.import_module(f"plugins.{file.stem}")
                plugin_class = getattr(module, f"{file.stem.title()}Plugin")
                self.plugins[file.stem] = plugin_class(self.bobi)
```

---

## 🌐 DASHBOARD WEB (Futuro)

### Arquitectura Web:

```
┌─────────────────────────────────────────┐
│         Frontend (React/Vue)            │
│  • Dashboard visual                     │
│  • Control de dispositivos              │
│  • Historial de conversaciones          │
│  • Configuración                        │
└─────────────────────────────────────────┘
                    │
                    │ WebSocket / REST API
                    ▼
┌─────────────────────────────────────────┐
│         Backend (Flask)                 │
│  • API REST                             │
│  • WebSockets (tiempo real)             │
│  • Autenticación                        │
│  • Streaming de eventos                 │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         Bobi Core                       │
│  • Brain, Voice, Memory                 │
│  • Plugins                              │
└─────────────────────────────────────────┘
```

---

## 🏠 INTEGRACIÓN IoT (Futuro)

### Arquitectura Casa Inteligente:

```
┌─────────────────────────────────────────┐
│              Bobi Core                  │
│         (Espejo Linux)                  │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         Home Assistant                  │
│  • Hub central de dispositivos          │
│  • Automatizaciones                     │
│  • API REST                             │
└─────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
    ┌──────┐   ┌──────┐   ┌──────┐
    │Luces │   │Enchuf│   │Sensor│
    │ LED  │   │ WiFi │   │ ESP32│
    └──────┘   └──────┘   └──────┘
```

---

## 🔐 SEGURIDAD

### Manejo de API Keys:

```python
# ✅ CORRECTO
api_key = os.getenv("GEMINI_API_KEY", "")

# ❌ INCORRECTO
api_key = "AIzaSyC..."  # Nunca hardcodear
```

### Archivos Sensibles:

```gitignore
# .gitignore
data/memory.json      # Datos personales
data/config.yaml      # Puede contener keys
*.key                 # Archivos de keys
.env                  # Variables de entorno
```

---

## 📊 MÉTRICAS Y MONITOREO

### Estadísticas Disponibles:

```python
# Memory stats
{
    "sesiones": 42,
    "interacciones_totales": 1337,
    "hechos_guardados": 25,
    "historial_size": 20,
    "ultima_sesion": "2024-01-15T10:30:00",
    "tiene_nombre": True
}

# Brain stats
{
    "current_provider": "Gemini",
    "available_providers": ["gemini", "ollama"],
    "has_internet": True,
    "mode": "auto"
}

# Voice stats
{
    "enabled": True,
    "stt_available": True,
    "stt_model": "base",
    "tts_engines": ["pyttsx3"],
    "tts_engine": "pyttsx3"
}
```

---

## 🚀 ESCALABILIDAD

### Arquitectura Cliente-Servidor:

```
┌──────────────┐         ┌──────────────┐
│  PC Windows  │ ◄─────► │ Espejo Linux │
│   (Cliente)  │   API   │  (Servidor)  │
└──────────────┘         └──────────────┘
                               │
                    ┌──────────┼──────────┐
                    ▼          ▼          ▼
              ┌─────────┐ ┌─────────┐ ┌─────────┐
              │  Móvil  │ │  Tablet │ │  Otros  │
              └─────────┘ └─────────┘ └─────────┘
```

### Distribución de Carga:

- **Espejo (Servidor):** IA, memoria, plugins
- **Clientes:** Solo interfaz y captura de voz
- **Comunicación:** WebSocket para tiempo real

---

## 🔧 EXTENSIBILIDAD

### Agregar Nuevo Proveedor de IA:

```python
# core/brain.py
class NewAIProvider(AIProvider):
    def __init__(self, config: dict):
        super().__init__("NewAI", config)
        self._initialize()
    
    def _initialize(self):
        # Setup del proveedor
        pass
    
    def think(self, message: str, system_prompt: str = "") -> str:
        # Lógica de generación
        pass
```

### Agregar Nuevo Engine de TTS:

```python
# core/voice.py
def _speak_new_engine(self, text: str):
    # Lógica de síntesis
    pass

# Agregar a available_engines
if self._check_command("new_engine"):
    engines.append("new_engine")
```

---

## 📝 CONVENCIONES DE CÓDIGO

### Estilo:
- PEP 8 para Python
- Docstrings en todas las clases y funciones
- Type hints donde sea posible
- Comentarios claros y concisos

### Nombres:
- Clases: `PascalCase`
- Funciones: `snake_case`
- Constantes: `UPPER_CASE`
- Privados: `_prefijo`

### Estructura:
- Imports al inicio
- Constantes después de imports
- Clases después de constantes
- Funciones helper al final

---

*Arquitectura diseñada para ser simple, extensible y escalable.* 🏗️
