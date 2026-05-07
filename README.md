# Bobi 🤖

Asistente de voz para PC — interfaz web en `localhost:5000`.

## Iniciar

```
iniciar.bat
```

Luego abre **http://localhost:5000** en tu navegador.

## Estructura

```
bobi/
├── iniciar.bat       ← ejecuta esto
├── bobi_web.py       ← servidor Flask (puerto 5000)
├── requirements.txt  ← dependencias Python
├── core/
│   ├── brain.py      ← lógica de IA (Gemini / Ollama)
│   ├── config.py     ← configuración
│   ├── memory.py     ← memoria de conversación
│   └── voice.py      ← motor de voz
├── web/
│   ├── index.html    ← interfaz web
│   ├── app.js        ← lógica frontend
│   └── style.css     ← estilos
└── data/
    └── config.yaml   ← ajustes (API keys, etc.)
```

## Configurar Gemini (IA rápida)

Consigue tu clave gratis en https://aistudio.google.com/apikey  
Luego edita `data/config.yaml` y pon:

```yaml
ai_providers:
  gemini:
    api_key: "TU_CLAVE_AQUI"
```

## Dependencias

```
pip install flask flask-cors edge-tts pycaw comtypes psutil google-generativeai
```
