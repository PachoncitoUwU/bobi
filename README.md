# 🤖 BOBI - Asistente Virtual Inteligente

> 🆓 100% Gratuito · 🎙️ Control por Voz · 🧠 IA Local · 🏠 Casa Inteligente

**Bobi** es tu asistente virtual personal con IA, control por voz y capacidad de automatizar tu casa. Funciona completamente local con Ollama, sin suscripciones ni límites.

---

## ✨ Características

- 🤖 **IA Local con Ollama** - Sin API keys, sin límites, 100% privado
- 🎙️ **Control por Voz** - Whisper para reconocimiento, pyttsx3 para síntesis
- 🧠 **Memoria Inteligente** - Recuerda conversaciones y preferencias
- 🔌 **Extensible** - Sistema de plugins modular
- 🌐 **Multiplataforma** - Windows y Linux

---

## 🚀 Instalación Rápida

### Requisitos
- Python 3.11+ (recomendado 3.12)
- 16 GB RAM (mínimo 8 GB)
- 5 GB espacio libre

### Windows

#### 1. Instalar Ollama
```powershell
# Descargar desde: https://ollama.com/download
# Instalar y luego:
ollama pull llama3.2
```

#### 2. Instalar dependencias
```powershell
pip install -r requirements.txt
```

#### 3. Iniciar Bobi
```powershell
python bobi.py
```

### Linux

```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2

# Instalar dependencias
pip install -r requirements.txt

# Iniciar Bobi
python bobi.py
```

---

## 📖 Documentación

- **[EMPIEZA_AQUI.md](EMPIEZA_AQUI.md)** - Guía de inicio rápido
- **[INSTALACION_WINDOWS.md](INSTALACION_WINDOWS.md)** - Instalación detallada para Windows
- **[PLAN_DESARROLLO.md](PLAN_DESARROLLO.md)** - Hoja de ruta completa (12 fases)
- **[ARQUITECTURA.md](ARQUITECTURA.md)** - Documentación técnica

---

## 🎮 Uso

### Modo Texto
```
[Tú] → Hola Bobi
[Bobi]: ¡Hola! ¿En qué te puedo ayudar?

[Tú] → ¿Qué es Python?
[Bobi]: Python es un lenguaje de programación...
```

### Modo Voz (requiere PyAudio)
1. Presiona Enter
2. Habla cuando veas "🔴 Grabando..."
3. Espera la respuesta de Bobi

### Comandos Especiales
- `estado` - Ver estado del sistema
- `ayuda` - Ver comandos disponibles
- `modo texto` / `modo voz` - Cambiar modo de entrada
- `salir` - Cerrar Bobi

---

## 📁 Estructura del Proyecto

```
bobi/
├── core/                   # Motor principal
│   ├── brain.py           # Sistema de IA
│   ├── voice.py           # Reconocimiento y síntesis de voz
│   ├── memory.py          # Memoria persistente
│   └── config.py          # Configuración
│
├── plugins/                # Extensiones (futuro)
│
├── data/                   # Datos persistentes
│   ├── memory.json        # Memoria de Bobi
│   └── config.yaml        # Configuración
│
├── bobi.py                 # Punto de entrada
├── requirements.txt        # Dependencias
└── README.md              # Esta guía
```

---

## ⚙️ Configuración

Edita `data/config.yaml` para personalizar:

```yaml
# Identidad
nombre: "Bobi"
idioma: "es"

# IA
ai_providers:
  ollama:
    enabled: true
    model: "llama3.2"  # o phi3, mistral, qwen2.5

# Voz
voice:
  stt_model: "base"  # tiny, base, small, medium
  tts_engine: "pyttsx3"

# Memoria
memory:
  max_history: 20
  max_facts: 50
```

---

## 🗺️ Hoja de Ruta

### ✅ v1.0 (Actual)
- [x] IA local con Ollama
- [x] Reconocimiento de voz (Whisper)
- [x] Síntesis de voz (pyttsx3)
- [x] Memoria persistente
- [x] Arquitectura modular

### 🔜 v1.1 (Próximamente)
- [ ] Sistema de plugins completo
- [ ] Recordatorios y alarmas
- [ ] Búsquedas web inteligentes
- [ ] Dashboard web
- [ ] Wake word ("Oye Bobi")

### 🔮 v2.0 (Futuro)
- [ ] Control de dispositivos IoT
- [ ] Espejo inteligente
- [ ] App móvil
- [ ] Sistema multiroom

---

## 💻 Requisitos del Sistema

| Componente | Mínimo | Recomendado |
|---|---|---|
| RAM | 8 GB | 16 GB |
| CPU | Intel i5 / Ryzen 5 | Intel i7 / Ryzen 7 |
| Almacenamiento | 5 GB | 10 GB |
| SO | Windows 10+ / Linux | Linux |

---

## 🐛 Solución de Problemas

**Ollama no disponible**
```bash
# Verifica que Ollama esté corriendo
ollama serve

# En otra terminal
python bobi.py
```

**Voz no funciona**
- Windows: Requiere Python 3.11 o 3.12 para PyAudio
- Linux: `sudo apt install portaudio19-dev && pip install pyaudio`

**Respuestas lentas**
- Usa un modelo más pequeño: `ollama pull phi3`
- Edita `data/config.yaml` y cambia `model: "phi3"`

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

## 🙏 Agradecimientos

- [Ollama](https://ollama.ai/) - IA local
- [Whisper](https://github.com/openai/whisper) - Reconocimiento de voz
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) - Implementación optimizada

---

## 📞 Contacto

- GitHub: [@PachoncitoUwU](https://github.com/PachoncitoUwU)
- Repositorio: [bobi](https://github.com/PachoncitoUwU/bobi)

---

**¡Construye tu casa inteligente con Bobi!** 🏠🤖
