#!/usr/bin/env python3
"""
Script para limpiar archivos innecesarios antes de subir a Git
"""

import os
import shutil
from pathlib import Path

print("🧹 Limpiando proyecto Bobi...")
print("=" * 50)

# Archivos y carpetas a eliminar
TO_DELETE = [
    # Archivos de instalación
    "*.whl",
    "*.tar.xz",
    "*.tar.gz",
    "*.zip",
    
    # Código fuente de Python
    "Python-3.12.13/",
    "Python-*/",
    
    # Versión antigua
    "old_version/",
    
    # Cache de Python
    "__pycache__/",
    "*.pyc",
    "*.pyo",
    
    # Archivos temporales
    "*.log",
    "*.tmp",
    
    # Datos personales (se crean automáticamente)
    "data/memory.json",
    "data/config.yaml",
]

deleted_count = 0
kept_count = 0

def should_delete(path: Path) -> bool:
    """Verifica si un archivo/carpeta debe eliminarse"""
    path_str = str(path)
    
    for pattern in TO_DELETE:
        if pattern.endswith("/"):
            # Es una carpeta
            if pattern.rstrip("/") in path_str:
                return True
        elif "*" in pattern:
            # Es un patrón con wildcard
            ext = pattern.replace("*", "")
            if path_str.endswith(ext):
                return True
        else:
            # Es un archivo específico
            if path.name == pattern or path_str.endswith(pattern):
                return True
    
    return False

def delete_item(path: Path):
    """Elimina un archivo o carpeta"""
    global deleted_count
    
    try:
        if path.is_dir():
            shutil.rmtree(path)
            print(f"🗑️  Eliminada carpeta: {path}")
        else:
            path.unlink()
            print(f"🗑️  Eliminado archivo: {path}")
        deleted_count += 1
    except Exception as e:
        print(f"⚠️  Error eliminando {path}: {e}")

def scan_and_clean(directory: Path = Path(".")):
    """Escanea y limpia el directorio"""
    global kept_count
    
    for item in directory.rglob("*"):
        # Ignorar .git
        if ".git" in str(item):
            continue
        
        if should_delete(item):
            delete_item(item)
        else:
            kept_count += 1

# Ejecutar limpieza
print("\n📂 Escaneando archivos...")
scan_and_clean()

print("\n" + "=" * 50)
print(f"✅ Limpieza completada")
print(f"   🗑️  Eliminados: {deleted_count} items")
print(f"   ✅ Conservados: {kept_count} items")

print("\n📋 Archivos que se subirán a Git:")
print("   ✅ core/*.py")
print("   ✅ bobi.py")
print("   ✅ requirements.txt")
print("   ✅ *.md (documentación)")
print("   ✅ test_*.py")
print("   ✅ .gitignore")

print("\n❌ Archivos que NO se subirán:")
print("   ❌ data/memory.json (datos personales)")
print("   ❌ data/config.yaml (configuración personal)")
print("   ❌ *.whl (archivos de instalación)")
print("   ❌ Python-*/ (código fuente de Python)")
print("   ❌ __pycache__/ (archivos compilados)")

print("\n🚀 Siguiente paso:")
print("   Ejecuta: git add .")
print("   Luego: git commit -m 'mensaje'")
print("   Finalmente: git push")

print("\n💡 Tip: Lee SUBIR_A_GIT.md para instrucciones completas")
