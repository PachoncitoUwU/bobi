# 📤 GUÍA PARA SUBIR A GIT

## 🎯 Repositorio
https://github.com/PachoncitoUwU/bobi.git

---

## 📋 PASOS PARA SUBIR

### 1. Inicializar Git (si no está inicializado)

```powershell
git init
```

### 2. Agregar el repositorio remoto

```powershell
git remote add origin https://github.com/PachoncitoUwU/bobi.git
```

### 3. Verificar archivos a subir

```powershell
git status
```

Deberías ver:
- ✅ Archivos del core (brain.py, voice.py, etc.)
- ✅ Documentación (.md)
- ✅ bobi.py
- ✅ requirements.txt
- ❌ NO deberías ver: data/memory.json, *.whl, Python-3.12.13/

### 4. Agregar archivos

```powershell
# Agregar todo excepto lo que está en .gitignore
git add .
```

### 5. Hacer commit

```powershell
git commit -m "🚀 Bobi v1.0 - Asistente Virtual con IA Local

✨ Características:
- IA local con Ollama (Llama 3.2)
- Reconocimiento de voz (Whisper)
- Síntesis de voz (pyttsx3)
- Memoria persistente
- Arquitectura modular

📚 Documentación completa incluida
🔧 Configuración flexible con YAML
🎯 Listo para agregar funcionalidades"
```

### 6. Subir a GitHub

```powershell
# Primera vez (crear rama main)
git branch -M main
git push -u origin main

# Siguientes veces
git push
```

---

## 🔐 SI PIDE AUTENTICACIÓN

### Opción 1: HTTPS con Token

1. Ve a GitHub → Settings → Developer settings → Personal access tokens
2. Genera un token con permisos de "repo"
3. Usa el token como contraseña cuando Git lo pida

### Opción 2: SSH

```powershell
# Generar clave SSH
ssh-keygen -t ed25519 -C "tu-email@example.com"

# Agregar a GitHub
# Copia el contenido de: ~/.ssh/id_ed25519.pub
# Pégalo en GitHub → Settings → SSH keys

# Cambiar remote a SSH
git remote set-url origin git@github.com:PachoncitoUwU/bobi.git
```

---

## 📦 ARCHIVOS QUE SE SUBIRÁN

### ✅ Código Principal
- `bobi.py`
- `core/*.py`
- `requirements.txt`
- `.gitignore`

### ✅ Documentación
- `README.md`
- `EMPIEZA_AQUI.md`
- `INSTALACION_WINDOWS.md`
- `PLAN_DESARROLLO.md`
- `ARQUITECTURA.md`
- `ESTADO_ACTUAL.md`
- Otros .md

### ✅ Utilidades
- `test_instalacion.py`
- `test_gemini.py`
- `instalar_voz_windows.py`

### ✅ Estructura
- `data/.gitkeep` (mantiene carpeta vacía)
- `plugins/` (vacío por ahora)

### ❌ NO se subirán (están en .gitignore)
- `data/memory.json` (datos personales)
- `data/config.yaml` (configuración personal)
- `*.whl` (archivos de instalación)
- `Python-3.12.13/` (código fuente de Python)
- `old_version/` (código antiguo)
- `__pycache__/` (archivos compilados)

---

## 🔄 ACTUALIZAR DESPUÉS

Cuando hagas cambios:

```powershell
# Ver qué cambió
git status

# Agregar cambios
git add .

# Commit con mensaje descriptivo
git commit -m "✨ Agrega recordatorios y alarmas"

# Subir
git push
```

---

## 📝 CONVENCIONES DE COMMITS

Usa estos prefijos:

- `✨ feat:` - Nueva funcionalidad
- `🐛 fix:` - Corrección de bug
- `📚 docs:` - Documentación
- `🎨 style:` - Formato, estilo
- `♻️ refactor:` - Refactorización
- `⚡ perf:` - Mejora de rendimiento
- `✅ test:` - Tests
- `🔧 chore:` - Mantenimiento

**Ejemplos:**
```powershell
git commit -m "✨ feat: Agrega sistema de recordatorios"
git commit -m "🐛 fix: Corrige error en reconocimiento de voz"
git commit -m "📚 docs: Actualiza guía de instalación"
git commit -m "⚡ perf: Optimiza velocidad de respuesta"
```

---

## 🌿 BRANCHES (Opcional)

Para desarrollo organizado:

```powershell
# Crear rama para nueva funcionalidad
git checkout -b feature/recordatorios

# Trabajar en la rama
# ... hacer cambios ...
git add .
git commit -m "✨ feat: Agrega recordatorios"

# Subir rama
git push -u origin feature/recordatorios

# Volver a main
git checkout main

# Mergear cuando esté listo
git merge feature/recordatorios
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### "fatal: remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/PachoncitoUwU/bobi.git
```

### "Updates were rejected"
```powershell
# Forzar push (cuidado, sobrescribe)
git push -f origin main
```

### "Permission denied"
- Verifica tu token de GitHub
- O configura SSH

### Ver historial
```powershell
git log --oneline
```

### Deshacer último commit (sin perder cambios)
```powershell
git reset --soft HEAD~1
```

---

## ✅ CHECKLIST ANTES DE SUBIR

- [ ] Código funciona correctamente
- [ ] No hay API keys en el código
- [ ] .gitignore está configurado
- [ ] README.md está actualizado
- [ ] Documentación está completa
- [ ] No hay archivos personales (memory.json, config.yaml)
- [ ] No hay archivos grandes innecesarios (.whl, Python-3.12.13/)

---

## 🎉 DESPUÉS DE SUBIR

Tu repositorio estará en:
https://github.com/PachoncitoUwU/bobi

Otros podrán:
- ✅ Ver el código
- ✅ Clonar el proyecto
- ✅ Contribuir con Pull Requests
- ✅ Reportar issues
- ✅ Hacer fork

---

**¡Listo para subir!** 🚀

Ejecuta los comandos en orden y tu proyecto estará en GitHub.
