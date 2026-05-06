# ⚡ INICIO RÁPIDO - BOBI

Guía ultra-rápida para tener Bobi funcionando en 5 minutos.

---

## 🎯 PASO 1: API KEY DE GEMINI (2 minutos)

1. Ve a: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copia la key

---

## 🎯 PASO 2: INSTALAR (2 minutos)

```bash
# Instalar dependencias básicas
pip install pyyaml google-generativeai rich colorama

# Instalar voz (opcional, para después)
pip install pyaudio faster-whisper pyttsx3
```

**Si PyAudio falla en Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

---

## 🎯 PASO 3: CONFIGURAR API KEY (30 segundos)

### Windows PowerShell:
```powershell
$env:GEMINI_API_KEY="tu-api-key-aqui"
```

### Linux/Mac:
```bash
export GEMINI_API_KEY="tu-api-key-aqui"
```

---

## 🎯 PASO 4: INICIAR (30 segundos)

```bash
python bobi.py
```

---

## 🎉 ¡LISTO!

Ahora puedes:
- Hablar con Bobi (si instalaste voz)
- O escribir en modo texto

**Ejemplos:**
- "Hola Bobi"
- "¿Qué es Python?"
- "Cuéntame un chiste"
- "estado" (ver info del sistema)

---

## 🐛 Si algo falla:

```bash
# Verificar instalación
python test_instalacion.py

# Ver guía completa
# Windows: INSTALACION_WINDOWS.md
# Linux: README.md
```

---

## 📚 Próximos pasos:

1. **Personaliza:** Edita `data/config.yaml`
2. **Explora:** Lee `PLAN_DESARROLLO.md` para ver el futuro
3. **Disfruta:** Conversa con Bobi y prueba sus capacidades

---

*¿Problemas? Revisa INSTALACION_WINDOWS.md para soluciones detalladas.*
