# 🎤 MEJORAR LA VOZ DE BOBI

## Problema Actual

La voz de pyttsx3 suena robótica y falsa. Además, edge-tts abre archivos MP3 en ventanas externas.

## Solución: Edge-TTS + Pygame

Usaremos **edge-tts** (voces naturales de Microsoft) con **pygame** para reproducción inline.

---

## 📦 Instalación

### Paso 1: Instalar pygame

```bash
pip install pygame
```

O usa el script automático:

```bash
python utils/instalar_pygame.py
```

### Paso 2: Verificar que edge-tts esté instalado

```bash
pip install edge-tts
```

---

## 🧪 Probar la Voz Mejorada

Ejecuta el script de prueba:

```bash
python utils/test_voz_mejorada.py
```

Esto probará 3 voces diferentes:
- **Dalia** (mujer, México) - ⭐ Recomendada
- **Jorge** (hombre, México)
- **Elvira** (mujer, España)

---

## 🎨 Cambiar la Voz

### Voces Disponibles en Español

| Voz | Género | País | Código |
|-----|--------|------|--------|
| Dalia | Mujer | México | `es-MX-DaliaNeural` ⭐ |
| Jorge | Hombre | México | `es-MX-JorgeNeural` |
| Elvira | Mujer | España | `es-ES-ElviraNeural` |
| Álvaro | Hombre | España | `es-ES-AlvaroNeural` |
| Elena | Mujer | Argentina | `es-AR-ElenaNeural` |
| Tomás | Hombre | Argentina | `es-AR-TomasNeural` |
| Salomé | Mujer | Colombia | `es-CO-SalomeNeural` |
| Catalina | Mujer | Chile | `es-CL-CatalinaNeural` |

### Cómo Cambiar

Edita `core/voice.py` línea **280**:

```python
voice = "es-MX-DaliaNeural"  # Cambia aquí por la voz que prefieras
```

Por ejemplo, para voz masculina mexicana:

```python
voice = "es-MX-JorgeNeural"
```

---

## ✅ Ventajas de Edge-TTS

- ✅ **Voz natural**: Suena como una persona real
- ✅ **Gratis**: No requiere API key
- ✅ **Offline después de descargar**: Cachea las voces
- ✅ **Múltiples acentos**: México, España, Argentina, etc.
- ✅ **Reproducción inline**: No abre ventanas externas

---

## 🚀 Usar con la Interfaz Gráfica

Una vez instalado pygame, ejecuta:

```bash
python bobi_gui.py
```

Ahora cuando Bobi hable:
- ✅ La voz sonará natural
- ✅ No se abrirán ventanas externas
- ✅ La animación del avatar se sincronizará con la voz

---

## 🐛 Solución de Problemas

### Error: "pygame.error: No available audio device"

**Windows:**
```bash
# Reinstalar pygame
pip uninstall pygame
pip install pygame
```

**Linux:**
```bash
# Instalar dependencias de audio
sudo apt-get install python3-pygame libsdl2-mixer-2.0-0
```

### Error: "edge_tts not found"

```bash
pip install edge-tts
```

### La voz sigue sonando robótica

Verifica que edge-tts esté en la lista de engines:

```bash
python -c "from core.voice import VoiceEngine; v = VoiceEngine(); print(v.get_status())"
```

Debe aparecer `'tts_engines': ['edge-tts', ...]`

---

## 📝 Notas

- La primera vez que uses una voz, edge-tts la descargará (tarda unos segundos)
- Las voces se cachean localmente para uso futuro
- Pygame es ligero y no afecta el rendimiento

---

## 🎯 Resultado Final

Antes:
- ❌ Voz robótica de pyttsx3
- ❌ Abre MP3 en reproductor externo
- ❌ Suena falsa

Después:
- ✅ Voz natural de Microsoft
- ✅ Reproducción inline sin ventanas
- ✅ Suena como persona real
