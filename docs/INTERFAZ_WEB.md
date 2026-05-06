# 🌐 INTERFAZ WEB DE BOBI

## ¿Por qué Interfaz Web?

La interfaz web es **mucho más bonita** que tkinter:
- ✅ Diseño moderno con animaciones suaves
- ✅ Colores vibrantes y gradientes
- ✅ Avatar animado que parpadea y habla
- ✅ Funciona en cualquier navegador
- ✅ Reconocimiento de voz integrado (Chrome/Edge)
- ✅ Síntesis de voz del navegador
- ✅ Responsive (se adapta a móviles)

---

## 🚀 Inicio Rápido

### Opción 1: Script Automático (Recomendado)

```bash
iniciar_web.bat
```

### Opción 2: Manual

```bash
# Instalar dependencias
pip install flask flask-cors

# Iniciar servidor
python bobi_web.py
```

### Paso 3: Abrir Navegador

Abre tu navegador en:
```
http://localhost:5000
```

**Recomendado:** Chrome o Edge (para reconocimiento de voz)

---

## 🎨 Características de la Interfaz

### 1. Diseño Moderno
- **Tema oscuro** profesional
- **Gradientes** y efectos de glow
- **Animaciones suaves** en CSS
- **Tipografía** Segoe UI

### 2. Avatar Animado
- **Parpadea** cada 4 segundos
- **Boca se mueve** cuando habla
- **Brilla** cuando escucha
- **Ojos parpadean rápido** cuando piensa

### 3. Chat Interactivo
- **Mensajes con colores**:
  - Tú: Cyan (#00d9ff)
  - Bobi: Verde (#4ade80)
  - Sistema: Amarillo (#fbbf24)
- **Scroll automático**
- **Animaciones** al aparecer mensajes

### 4. Reconocimiento de Voz
- **Botón de micrófono** 🎤
- **Funciona en Chrome y Edge**
- **Transcripción automática** a texto
- **Animación** mientras escucha

### 5. Síntesis de Voz
- **Voz del navegador** (Web Speech API)
- **Automática** al responder
- **Avatar se anima** mientras habla

---

## 🎤 Cómo Usar

### Escribir Mensajes
1. Escribe en el campo de texto
2. Presiona **Enter** o clic en **Enviar** ➤
3. Bobi responderá con texto y voz

### Hablar con Micrófono
1. Clic en botón **🎤 Hablar**
2. Habla cuando veas "Escuchando..."
3. Bobi transcribirá y responderá

**Nota:** Requiere Chrome o Edge

### Limpiar Chat
1. Clic en botón **🗑️ Limpiar**
2. Se borrará el historial (excepto mensaje de bienvenida)

---

## 🔧 Configuración

### Cambiar Puerto

Edita `bobi_web.py` línea final:

```python
app.run(
    host='0.0.0.0',
    port=5000,  # Cambia aquí
    debug=False
)
```

### Cambiar Idioma de Voz

Edita `web/app.js` líneas 30 y 180:

```javascript
// Reconocimiento de voz
this.recognition.lang = 'es-MX';  // Español México

// Síntesis de voz
utterance.lang = 'es-MX';
```

Opciones:
- `es-ES` - España
- `es-MX` - México
- `es-AR` - Argentina
- `es-CO` - Colombia

---

## 📡 API REST

El servidor expone una API REST:

### POST /api/chat
Enviar mensaje a Bobi

**Request:**
```json
{
  "message": "Hola Bobi"
}
```

**Response:**
```json
{
  "response": "¡Hola! ¿En qué puedo ayudarte?",
  "status": "success"
}
```

### GET /api/status
Obtener estado del servidor

**Response:**
```json
{
  "status": "online",
  "ia_provider": "ollama",
  "voice_available": true,
  "voice_engines": ["edge-tts", "pyttsx3"],
  "timestamp": "2026-05-06T10:30:00"
}
```

### POST /api/clear
Limpiar memoria de sesión

**Response:**
```json
{
  "status": "success",
  "message": "Memoria limpiada"
}
```

---

## 🎯 Ventajas vs Tkinter

| Aspecto | Tkinter | Web |
|---------|---------|-----|
| **Diseño** | Básico, limitado | Moderno, ilimitado |
| **Animaciones** | Difíciles | Fáciles con CSS |
| **Voz** | Requiere PyAudio | Integrada en navegador |
| **Responsive** | No | Sí |
| **Personalización** | Limitada | Total |
| **Multiplataforma** | Requiere instalación | Solo navegador |
| **Actualizaciones** | Reiniciar app | Recargar página |

---

## 🐛 Solución de Problemas

### "No se puede conectar al servidor"

Verifica que el servidor esté corriendo:
```bash
python bobi_web.py
```

### "El micrófono no funciona"

- Usa **Chrome** o **Edge** (Firefox no soporta Web Speech API)
- Permite acceso al micrófono cuando el navegador lo pida
- Verifica que tu micrófono esté conectado

### "No se escucha la voz"

- Verifica el volumen del navegador
- Verifica que los altavoces estén conectados
- Algunas voces pueden no estar disponibles en tu idioma

### "Error 500 al enviar mensaje"

- Verifica que Ollama esté corriendo: `ollama list`
- Revisa la consola del servidor para ver el error
- Asegúrate de tener el modelo instalado: `ollama pull llama3.2`

---

## 📱 Acceso desde Móvil

Puedes acceder desde tu celular en la misma red:

1. Obtén la IP de tu PC:
   ```bash
   ipconfig
   ```
   Busca "IPv4 Address" (ej: 192.168.1.100)

2. En tu celular, abre el navegador:
   ```
   http://192.168.1.100:5000
   ```

3. ¡Listo! Puedes usar Bobi desde tu celular

---

## 🎨 Personalización

### Cambiar Colores

Edita `web/style.css` líneas 15-25:

```css
:root {
    --accent-primary: #00d9ff;    /* Color principal */
    --accent-secondary: #4ade80;  /* Color secundario */
    --bg-primary: #0a0a0f;        /* Fondo principal */
}
```

### Cambiar Tamaño del Avatar

Edita `web/style.css` línea 180:

```css
.avatar {
    width: 300px;   /* Cambia aquí */
    height: 300px;  /* Cambia aquí */
}
```

### Agregar Más Animaciones

Edita `web/style.css` y agrega tus propias animaciones:

```css
@keyframes mi-animacion {
    0% { transform: scale(1); }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); }
}

.mi-elemento {
    animation: mi-animacion 2s infinite;
}
```

---

## 📚 Archivos de la Interfaz Web

```
web/
├── index.html    # Estructura HTML
├── style.css     # Estilos y animaciones
└── app.js        # Lógica JavaScript

bobi_web.py       # Servidor Flask
iniciar_web.bat   # Script de inicio
```

---

## 🎉 Resultado Final

Con la interfaz web tendrás:

- ✅ Diseño moderno y profesional
- ✅ Animaciones suaves y fluidas
- ✅ Avatar expresivo que reacciona
- ✅ Reconocimiento de voz integrado
- ✅ Síntesis de voz automática
- ✅ Chat interactivo con colores
- ✅ Responsive para móviles
- ✅ Fácil de personalizar

**¡Mucho mejor que tkinter!** 🚀
