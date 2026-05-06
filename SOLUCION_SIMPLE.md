# 🔧 SOLUCIÓN SIMPLE - Paso a Paso

Miguel, sigue estos pasos **exactamente** en orden:

---

## 📋 Paso 1: Verificar Todo

```bash
probar_todo.bat
```

Esto verifica que tengas todo instalado. Si falta algo, lo instala automáticamente.

---

## 📋 Paso 2: Iniciar Servidor

```bash
iniciar_web.bat
```

Debes ver algo como:

```
╔══════════════════════════════════════════════════════════════╗
║                    🚀 SERVIDOR LISTO                         ║
╚══════════════════════════════════════════════════════════════╝

📱 Abre tu navegador en:

   http://localhost:5000
```

**NO CIERRES ESTA VENTANA** - Déjala abierta mientras usas Bobi.

---

## 📋 Paso 3: Abrir Navegador

Abre **Chrome** o **Edge** (no Firefox) y ve a:

```
http://localhost:5000
```

Debes ver la interfaz de Bobi con:
- Avatar animado en el centro
- Campo de texto abajo
- Botones: Enviar, Hablar, Limpiar

---

## 📋 Paso 4: Probar Escribiendo

1. Escribe en el campo de texto: **"Hola"**
2. Presiona **Enter**
3. Espera 5-10 segundos
4. Debes ver:
   - Respuesta de Bobi en el chat
   - Avatar se anima (boca se mueve)
   - **DEBES ESCUCHAR** la voz de Bobi

### ❌ Si NO escuchas nada:

**Verifica el volumen:**
- Volumen de Windows: Debe estar alto
- Volumen del navegador: Clic derecho en la pestaña → Verificar que no esté silenciado
- Altavoces: Deben estar conectados y encendidos

**Verifica la consola del navegador:**
- Presiona **F12** en el navegador
- Ve a la pestaña **Console**
- Busca mensajes de error
- Debe decir: `🔊 Audio reproduciendo`

**Verifica la consola del servidor:**
- Mira la ventana donde ejecutaste `iniciar_web.bat`
- Debe decir: `🔊 Audio generado con edge-tts`
- Si dice error, copia el error y dímelo

---

## 📋 Paso 5: Probar Micrófono

1. Clic en botón **🎤 Hablar**
2. El navegador pedirá permiso para usar el micrófono
3. Clic en **Permitir**
4. Habla durante 3-5 segundos (di algo como "Hola Bobi")
5. Espera a que transcriba
6. Debe aparecer lo que dijiste en el chat
7. Bobi responderá

### ❌ Si NO funciona el micrófono:

**Verifica permisos:**
- Chrome: Clic en el candado (izquierda de la URL)
- Clic en "Permisos del sitio"
- Micrófono: Debe estar en "Permitir"

**Verifica que el micrófono funcione:**
- Abre la app "Grabadora de voz" de Windows
- Graba algo
- Si no funciona ahí, el problema es tu micrófono

**Verifica la consola del navegador:**
- Presiona **F12**
- Ve a **Console**
- Debe decir: `🎤 Grabando...`
- Si dice error, copia el error

---

## 🐛 Problemas Comunes

### "No se puede conectar al servidor"

El servidor no está corriendo. Ejecuta:
```bash
iniciar_web.bat
```

### "Error 500" al enviar mensaje

Ollama no está corriendo o no tiene el modelo. Ejecuta:
```bash
ollama list
```

Debe aparecer `llama3.2` o `phi3`. Si no:
```bash
ollama pull llama3.2
```

### "Tarda mucho en responder"

Usa modelo más rápido:
```bash
acelerar_bobi.bat
```

### "La voz suena robótica"

Verifica que edge-tts esté instalado:
```bash
pip install edge-tts
```

Reinicia el servidor:
```bash
# Cierra la ventana del servidor (Ctrl+C)
# Vuelve a ejecutar:
iniciar_web.bat
```

---

## 📊 Checklist de Verificación

Marca cada paso que funciona:

- [ ] Ejecuté `probar_todo.bat` sin errores
- [ ] Ejecuté `iniciar_web.bat` y el servidor inició
- [ ] Abrí http://localhost:5000 en Chrome/Edge
- [ ] Veo la interfaz de Bobi
- [ ] Escribí "Hola" y presioné Enter
- [ ] Bobi respondió en el chat
- [ ] **ESCUCHÉ** la voz de Bobi (IMPORTANTE)
- [ ] Clic en 🎤 Hablar
- [ ] Permití acceso al micrófono
- [ ] Hablé y Bobi transcribió correctamente
- [ ] Bobi respondió a mi mensaje de voz

---

## 🆘 Si Nada Funciona

Copia y pégame:

1. **Consola del servidor** (ventana de `iniciar_web.bat`):
   - Los últimos 20 mensajes

2. **Consola del navegador** (F12 → Console):
   - Los mensajes de error en rojo

3. **Qué pasa exactamente**:
   - ¿Escribes y no responde?
   - ¿Responde pero no escuchas?
   - ¿El micrófono no funciona?
   - ¿Otro problema?

---

## ✅ Si Todo Funciona

¡Perfecto! Ahora puedes:

- **Escribir** mensajes a Bobi
- **Hablar** con el botón 🎤
- **Escuchar** respuestas con voz natural
- **Limpiar** el chat con 🗑️

---

**Sigue estos pasos en orden y dime en cuál te atoras.**
