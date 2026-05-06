# 🚀 INSTALACIÓN DE BOBI EN WINDOWS

Guía paso a paso para instalar Bobi en tu PC Windows.

---

## 📋 REQUISITOS PREVIOS

- Windows 10/11
- Python 3.9 o superior
- 16 GB RAM (tienes ✓)
- Conexión a internet (para instalación)

---

## 🔧 PASO 1: INSTALAR PYTHON (si no lo tienes)

1. Ve a https://www.python.org/downloads/
2. Descarga Python 3.11 o 3.12
3. **IMPORTANTE:** Durante instalación, marca "Add Python to PATH"
4. Verifica instalación:
   ```bash
   python --version
   ```

---

## 🎯 PASO 2: OBTENER API KEY DE GEMINI (GRATIS)

Gemini es la IA que usaremos. Es **100% gratis** hasta 1500 requests/día.

1. Ve a: https://makersuite.google.com/app/apikey
2. Inicia sesión con tu cuenta de Google
3. Click en "Create API Key"
4. Copia la key (algo como: `AIzaSyC...`)
5. **GUÁRDALA**, la necesitaremos después

---

## 📦 PASO 3: INSTALAR DEPENDENCIAS

Abre **PowerShell** o **CMD** en la carpeta de Bobi:

### 3.1 Instalar dependencias básicas
```bash
pip install pyyaml google-generativeai requests python-dateutil rich colorama
```

### 3.2 Instalar PyAudio (para micrófono)
```bash
pip install pipwin
pipwin install pyaudio
```

Si `pipwin` falla, descarga PyAudio manualmente:
- Ve a: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Descarga el `.whl` para tu versión de Python
- Instala: `pip install PyAudio‑0.2.14‑cp311‑cp311‑win_amd64.whl`

### 3.3 Instalar Whisper (reconocimiento de voz)
```bash
pip install faster-whisper
```

### 3.4 Instalar TTS (síntesis de voz)
```bash
pip install pyttsx3
```

---

## 🔑 PASO 4: CONFIGURAR API KEY

### Opción A: Variable de entorno (recomendado)

1. Busca "Variables de entorno" en Windows
2. Click en "Variables de entorno"
3. En "Variables de usuario", click "Nueva"
4. Nombre: `GEMINI_API_KEY`
5. Valor: Tu API key de Gemini
6. Click OK y reinicia PowerShell

### Opción B: Archivo de configuración

Crea el archivo `data/config.yaml` con:

```yaml
ai_providers:
  gemini:
    enabled: true
    api_key: "TU_API_KEY_AQUI"
```

---

## ✅ PASO 5: PROBAR BOBI

```bash
python bobi.py
```

Si todo está bien, verás:

```
🚀 Iniciando Bobi...
✅ Gemini listo (gemini-2.0-flash-exp)
🔊 TTS engines disponibles: pyttsx3
🎙️  Cargando Whisper (base)...
✅ Whisper listo
✅ Bobi listo

╔════════════════════════════════════╗
║      🤖 Asistente Virtual          ║
║                                    ║
║  Bobi v1.0                         ║
║  IA: Gemini                        ║
║  Internet: ✓                       ║
║  Entrada: 🎙️  Voz                  ║
╚════════════════════════════════════╝
```

---

## 🎤 PASO 6: PRIMERA CONVERSACIÓN

### Modo Voz (recomendado)

1. Presiona Enter
2. Habla cuando veas "🔴 Grabando..."
3. Espera a que Bobi responda
4. Repite

### Modo Texto (si voz no funciona)

Si Bobi inicia en modo texto:
```
[Tú] → Hola Bobi
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### "No module named 'google.generativeai'"
```bash
pip install google-generativeai
```

### "PyAudio no disponible"
- Sigue el paso 3.2 cuidadosamente
- Asegúrate de descargar el `.whl` correcto para tu Python

### "Whisper no disponible"
```bash
pip install faster-whisper
```

### "Gemini: No hay API key"
- Verifica que configuraste la variable de entorno
- O crea el archivo `data/config.yaml` con tu key

### "Error abriendo micrófono"
- Verifica que tu micrófono esté conectado
- Dale permisos a Python en Configuración > Privacidad > Micrófono

### Bobi no me escucha bien
- Habla más cerca del micrófono
- Reduce ruido de fondo
- Cambia a modelo Whisper "small" (más preciso pero más lento):
  ```yaml
  voice:
    stt_model: "small"
  ```

### Voz muy robótica
- Por ahora usamos pyttsx3 (básico)
- En Linux tendremos Piper (mucho mejor)
- Funciona bien para pruebas

---

## 🎯 PRÓXIMOS PASOS

Una vez que Bobi funcione:

1. **Prueba comandos:**
   - "¿Qué hora es?"
   - "Cuéntame un chiste"
   - "¿Qué es Python?"
   - "estado" (ver info del sistema)

2. **Personaliza:**
   - Edita `data/config.yaml` para cambiar nombre, personalidad, etc.

3. **Agrega funcionalidades:**
   - Próximamente: recordatorios, búsquedas web, control de dispositivos

---

## 📊 VERIFICAR INSTALACIÓN

Ejecuta este script para verificar todo:

```python
# test_instalacion.py
import sys

print("🔍 Verificando instalación...\n")

# Python
print(f"✓ Python {sys.version.split()[0]}")

# Dependencias
deps = {
    "yaml": "pyyaml",
    "google.generativeai": "google-generativeai",
    "pyaudio": "pyaudio",
    "faster_whisper": "faster-whisper",
    "pyttsx3": "pyttsx3",
    "rich": "rich",
}

for module, package in deps.items():
    try:
        __import__(module)
        print(f"✓ {package}")
    except ImportError:
        print(f"✗ {package} - Instala: pip install {package}")

print("\n✅ Verificación completa")
```

Ejecuta:
```bash
python test_instalacion.py
```

---

## 🆘 AYUDA

Si tienes problemas:

1. Verifica que Python esté en PATH
2. Usa PowerShell como administrador
3. Actualiza pip: `python -m pip install --upgrade pip`
4. Reinstala dependencias: `pip install -r requirements.txt --force-reinstall`

---

## 🎉 ¡LISTO!

Ahora tienes Bobi funcionando en Windows. 

**Siguiente:** Cuando consigas el portátil para el espejo, instalaremos Linux y configuraremos Bobi como servidor 24/7.

Por ahora, disfruta conversando con Bobi y probando sus capacidades. 🚀
