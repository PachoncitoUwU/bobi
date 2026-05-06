# 🤖 BOBI - Asistente Virtual Inteligente

> 🆓 100% Gratuito · 🎙️ Control por Voz · 🧠 IA Local · 🎨 Interfaz Gráfica

**Bobi** es tu asistente virtual personal con IA, control por voz natural y interfaz gráfica animada. Funciona completamente local con Ollama, sin suscripciones ni límites.

---

## ✨ Características

- 🤖 **IA Local con Ollama** - Sin API keys, sin límites, 100% privado
- 🎙️ **Voz Natural** - Edge-TTS de Microsoft (muy realista)
- 🎨 **Interfaz Gráfica** - Avatar animado que responde visualmente
- 🧠 **Memoria Inteligente** - Recuerda conversaciones y preferencias
- 🔌 **Extensible** - Sistema de plugins modular

---

## 🚀 Inicio Rápido

### 1. Instalar Ollama
```powershell
# Descargar desde: https://ollama.com/download
# Instalar y luego:
ollama pull llama3.2
```

### 2. Instalar dependencias
```powershell
pip install -r requirements.txt
```

### 3. Iniciar Bobi

**Interfaz Gráfica (Recomendado):**
```powershell
python bobi_gui.py
```

**Modo Terminal:**
```powershell
python bobi.py
```

---

## 🎨 Interfaz Gráfica

La nueva interfaz incluye:
- ✅ **Avatar animado** que cambia según el estado
- ✅ **Chat visual** con colores diferenciados
- ✅ **Entrada de texto** y botón de voz
- ✅ **Animaciones:**
  - 🎤 Pulso azul cuando escucha
  - 🤔 Parpadeo cuando piensa
  - 🗣️ Boca moviéndose cuando habla

---

## 🗂️ Estructura del Proyecto

```
bobi/
├── bobi.py                 # ⭐ Modo terminal
├── bobi_gui.py             # ⭐ Interfaz gráfica (NUEVO)
├── requirements.txt        # ⭐ Dependencias
├── README.md               # ⭐ Esta guía
│
├── core/                   # Motor principal
│   ├── brain.py           # Sistema de IA
│   ├── voice.py           # Voz (STT + TTS mejorado)
│   ├── memory.py          # Memoria persistente
│   └── config.py          # Configuración
│
├── data/                   # Datos persistentes
│   ├── memory.json        # Tu memoria con Bobi
│   └── config.yaml        # Tu configuración
│
├── plugins/                # Extensiones (futuro)
│
├── docs/                   # 📚 Documentación completa
│   ├── EMPIEZA_AQUI.md
│   ├── INSTALACION_WINDOWS.md
│   ├── PLAN_DESARROLLO.md
│   └── Más guías...
│
└── utils/                  # 🔧 Utilidades
    ├── test_instalacion.py
    └── Otros scripts...
```

---

## 🎙️ Voz Natural

Bobi ahora usa **edge-tts** (Microsoft) para una voz mucho más natural:

**Voces disponibles:**
- `es-MX-DaliaNeural` - Mujer, México (por defecto) ⭐
- `es-MX-JorgeNeural` - Hombre, México
- `es-ES-ElviraNeural` - Mujer, España
- `es-ES-AlvaroNeural` - Hombre, España
- `es-AR-ElenaNeural` - Mujer, Argentina

Para cambiar la voz, edita `core/voice.py` línea ~180.

---

## 🎮 Uso

### Interfaz Gráfica
1. Ejecuta: `python bobi_gui.py`
2. Escribe en el campo de texto o click en "🎤 Hablar"
3. Bobi responderá con voz y animación

### Modo Terminal
1. Ejecuta: `python bobi.py`
2. Escribe o presiona Enter para hablar
3. Bobi responderá por voz

### Comandos Especiales
- `estado` - Ver estado del sistema
- `ayuda` - Ver comandos disponibles
- `modo texto` / `modo voz` - Cambiar modo
- `salir` - Cerrar Bobi

---

## ⚙️ Configuración

Edita `data/config.yaml`:

```yaml
nombre: "Bobi"
idioma: "es"

ai_providers:
  ollama:
    model: "llama3.2"  # o phi3 (más rápido)

voice:
  stt_model: "base"
  tts_engine: "edge-tts"  # Voz natural
```

---

## 🐛 Solución de Problemas

**Voz no funciona:**
```powershell
pip install edge-tts
```

**Interfaz no abre:**
```powershell
# tkinter viene con Python, pero si falla:
pip install tk
```

**Respuestas lentas (>20 seg):**
```powershell
# Usa modelo más rápido
ollama pull phi3
# Edita data/config.yaml: model: "phi3"
```

**PyAudio no instala:**
- Requiere Python 3.11 o 3.12 (no 3.14)
- O usa solo modo texto (funciona igual)

---

## 📚 Documentación

- **[docs/EMPIEZA_AQUI.md](docs/EMPIEZA_AQUI.md)** - Guía de inicio
- **[docs/INSTALACION_WINDOWS.md](docs/INSTALACION_WINDOWS.md)** - Instalación detallada
- **[docs/PLAN_DESARROLLO.md](docs/PLAN_DESARROLLO.md)** - Hoja de ruta completa

---

## 🗺️ Próximas Funcionalidades

- [ ] Recordatorios y alarmas
- [ ] Búsquedas web inteligentes
- [ ] Control de dispositivos IoT
- [ ] Dashboard web
- [ ] Wake word ("Oye Bobi")
- [ ] App móvil

---

## 💻 Requisitos

| Componente | Mínimo | Recomendado |
|---|---|---|
| RAM | 8 GB | 16 GB |
| CPU | Intel i5 / Ryzen 5 | Intel i7 / Ryzen 7 |
| Almacenamiento | 5 GB | 10 GB |
| Python | 3.11+ | 3.12 |

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

MIT License - Código abierto y gratuito

---

## 🙏 Agradecimientos

- [Ollama](https://ollama.ai/) - IA local
- [Whisper](https://github.com/openai/whisper) - Reconocimiento de voz
- [edge-tts](https://github.com/rany2/edge-tts) - Voz natural de Microsoft

---

## 📞 Contacto

- GitHub: [@PachoncitoUwU](https://github.com/PachoncitoUwU)
- Repositorio: [bobi](https://github.com/PachoncitoUwU/bobi)

---

**¡Construye tu casa inteligente con Bobi!** 🏠🤖
