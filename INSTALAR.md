# 🚀 INSTALACIÓN RÁPIDA DE BOBI

## ✨ NOVEDADES

- 🎨 **Interfaz gráfica** con avatar animado
- 🎙️ **Voz natural** con edge-tts (Microsoft)
- 🗂️ **Proyecto organizado** en carpetas

---

## 📦 PASO 1: Instalar Ollama

1. Ve a: https://ollama.com/download
2. Descarga "Ollama for Windows"
3. Instala (siguiente, siguiente, finalizar)
4. Abre PowerShell y ejecuta:

```powershell
ollama pull llama3.2
```

---

## 🐍 PASO 2: Instalar Dependencias

```powershell
# Dependencias principales
pip install -r requirements.txt

# Si edge-tts falla, instálalo aparte:
pip install edge-tts
```

---

## 🎨 PASO 3: Iniciar Bobi

### Interfaz Gráfica (Recomendado):
```powershell
python bobi_gui.py
```

### Modo Terminal:
```powershell
python bobi.py
```

---

## 🎙️ MEJORAR LA VOZ

La voz ahora es **mucho más natural** con edge-tts.

**Si quieres cambiar la voz:**

Edita `core/voice.py` línea ~180:

```python
# Voces disponibles:
voice = "es-MX-DaliaNeural"  # Mujer, México (actual)
# voice = "es-MX-JorgeNeural"  # Hombre, México
# voice = "es-ES-ElviraNeural"  # Mujer, España
# voice = "es-ES-AlvaroNeural"  # Hombre, España
```

---

## ⚡ OPTIMIZAR VELOCIDAD

Si Bobi tarda mucho (>20 seg):

```powershell
# Instalar modelo más rápido
ollama pull phi3

# Editar data/config.yaml
# Cambiar: model: "phi3"
```

Phi3 responde en ~8-10 segundos.

---

## 🐛 PROBLEMAS COMUNES

### "No module named 'edge_tts'"
```powershell
pip install edge-tts
```

### "No module named 'tkinter'"
tkinter viene con Python, pero si falla:
```powershell
pip install tk
```

### PyAudio no instala
- Requiere Python 3.11 o 3.12 (no 3.14)
- O simplemente usa modo texto (funciona igual)

### Ollama no responde
```powershell
# Verifica que esté corriendo
ollama serve

# En otra terminal
python bobi_gui.py
```

---

## ✅ VERIFICAR INSTALACIÓN

```powershell
python utils/test_instalacion.py
```

Debería mostrar:
- ✓ Python
- ✓ ollama
- ✓ edge-tts
- ✓ rich
- ✓ Otros...

---

## 🎉 ¡LISTO!

Ahora tienes:
- ✅ Bobi con IA local
- ✅ Voz natural (edge-tts)
- ✅ Interfaz gráfica animada
- ✅ Todo organizado

**Ejecuta:** `python bobi_gui.py`

---

## 📚 MÁS INFORMACIÓN

- **docs/EMPIEZA_AQUI.md** - Guía completa
- **docs/INSTALACION_WINDOWS.md** - Instalación detallada
- **README.md** - Documentación principal

---

**¡Disfruta de Bobi!** 🤖✨
