"""
Sistema de Configuración Centralizado
Soporta múltiples proveedores de IA y configuración flexible
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any

class Config:
    """Configuración centralizada de Bobi"""
    
    # Rutas
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    PLUGINS_DIR = BASE_DIR / "plugins"
    
    # Configuración por defecto
    DEFAULTS = {
        # Identidad
        "nombre": "Bobi",
        "idioma": "es",
        "personalidad": "amigable",
        
        # IA - Proveedores (en orden de prioridad)
        "ai_providers": {
            "gemini": {
                "enabled": True,
                "api_key": "",  # Se obtiene de variable de entorno
                "model": "gemini-pro",  # Modelo estable
                "priority": 1,  # Prioridad más alta
            },
            "claude": {
                "enabled": False,
                "api_key": "",
                "model": "claude-haiku-4-5-20251001",
                "priority": 2,
            },
            "ollama": {
                "enabled": True,
                "model": "llama3.2",
                "url": "http://localhost:11434",
                "priority": 3,  # Fallback local
            }
        },
        
        # Voz
        "voice": {
            "stt_engine": "whisper",  # Speech-to-Text
            "stt_model": "base",      # tiny, base, small, medium
            "tts_engine": "piper",    # Text-to-Speech
            "tts_voice": "es_ES-davefx-medium",
            "wake_word": "bobi",
            "wake_word_enabled": False,  # Por ahora manual
        },
        
        # Memoria
        "memory": {
            "file": "data/memory.json",
            "max_history": 20,
            "max_facts": 50,
        },
        
        # Web Dashboard
        "web": {
            "enabled": True,
            "host": "0.0.0.0",  # Accesible desde red local
            "port": 5000,
            "debug": False,
        },
        
        # Plugins
        "plugins": {
            "enabled": ["recordatorios", "busquedas", "multimedia", "sistema"],
            "disabled": [],
        },
        
        # Red
        "network": {
            "check_url": "https://www.google.com",
            "check_timeout": 3,
            "mode": "auto",  # auto, online, offline
        },
        
        # Avanzado
        "advanced": {
            "temperature": 0.7,
            "max_tokens": 500,
            "log_level": "INFO",
        }
    }
    
    def __init__(self, config_file: str = None):
        """
        Inicializa la configuración
        
        Args:
            config_file: Ruta al archivo de configuración YAML (opcional)
        """
        self.config_file = config_file or str(self.DATA_DIR / "config.yaml")
        self.config = self._load_config()
        self._ensure_directories()
        self._load_api_keys()
    
    def _ensure_directories(self):
        """Crea directorios necesarios si no existen"""
        self.DATA_DIR.mkdir(exist_ok=True)
        self.PLUGINS_DIR.mkdir(exist_ok=True)
    
    def _load_config(self) -> Dict[str, Any]:
        """Carga configuración desde archivo o usa defaults"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f) or {}
                # Merge con defaults
                return self._deep_merge(self.DEFAULTS.copy(), user_config)
            except Exception as e:
                print(f"⚠️  Error cargando config: {e}. Usando defaults.")
                return self.DEFAULTS.copy()
        else:
            # Primera vez: crear archivo con defaults
            self.save()
            return self.DEFAULTS.copy()
    
    def _deep_merge(self, base: dict, override: dict) -> dict:
        """Merge recursivo de diccionarios"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                base[key] = self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base
    
    def _load_api_keys(self):
        """Carga API keys desde variables de entorno"""
        # Gemini
        gemini_key = os.getenv("GEMINI_API_KEY", "")
        if gemini_key:
            self.config["ai_providers"]["gemini"]["api_key"] = gemini_key
        
        # Claude
        claude_key = os.getenv("ANTHROPIC_API_KEY", "")
        if claude_key:
            self.config["ai_providers"]["claude"]["api_key"] = claude_key
    
    def save(self):
        """Guarda configuración actual a archivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"⚠️  Error guardando config: {e}")
    
    def get(self, key: str, default=None):
        """
        Obtiene valor de configuración usando notación de punto
        
        Ejemplo:
            config.get("voice.stt_model")  # "base"
        """
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        """
        Establece valor de configuración usando notación de punto
        
        Ejemplo:
            config.set("voice.stt_model", "small")
        """
        keys = key.split('.')
        target = self.config
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value
    
    def __getitem__(self, key):
        """Permite acceso con config['key']"""
        return self.config[key]
    
    def __setitem__(self, key, value):
        """Permite asignación con config['key'] = value"""
        self.config[key] = value


# Instancia global (singleton)
_config_instance = None

def get_config(config_file: str = None) -> Config:
    """Obtiene instancia global de configuración"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_file)
    return _config_instance
