"""
BOBI - Asistente Virtual Inteligente
Core Module
"""

__version__ = "1.0.0"
__author__ = "Tu Nombre"

from .config import Config
from .brain import Brain
from .voice import VoiceEngine
from .memory import Memory

__all__ = ['Config', 'Brain', 'VoiceEngine', 'Memory']
