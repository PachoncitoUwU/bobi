"""
Sistema de Memoria Persistente
Recuerda conversaciones, hechos y preferencias del usuario
"""

import json
import datetime
from pathlib import Path
from typing import List, Dict, Optional
from .config import get_config


class Memory:
    """Sistema de memoria de Bobi"""
    
    def __init__(self, memory_file: str = None):
        self.config = get_config()
        self.memory_file = memory_file or self.config.get("memory.file", "data/memory.json")
        self.data = self._load()
        self.max_history = self.config.get("memory.max_history", 20)
        self.max_facts = self.config.get("memory.max_facts", 50)
    
    def _load(self) -> dict:
        """Carga memoria desde archivo"""
        if Path(self.memory_file).exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error cargando memoria: {e}")
        
        # Memoria inicial
        return {
            "usuario": {
                "nombre": None,
                "preferencias": {},
            },
            "hechos": [],  # Lista de hechos importantes
            "historial": [],  # Últimas conversaciones
            "estadisticas": {
                "primera_vez": True,
                "sesiones": 0,
                "interacciones_totales": 0,
                "ultima_sesion": None,
            }
        }
    
    def save(self):
        """Guarda memoria a archivo"""
        try:
            Path(self.memory_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  Error guardando memoria: {e}")
    
    def add_interaction(self, user_message: str, bot_response: str):
        """Registra una interacción"""
        interaction = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user": user_message,
            "bot": bot_response,
        }
        
        self.data["historial"].append(interaction)
        
        # Mantener solo las últimas N interacciones
        if len(self.data["historial"]) > self.max_history:
            self.data["historial"] = self.data["historial"][-self.max_history:]
        
        self.data["estadisticas"]["interacciones_totales"] += 1
        self.save()
    
    def add_fact(self, fact: str, category: str = "general"):
        """Agrega un hecho importante a la memoria"""
        fact_entry = {
            "hecho": fact,
            "categoria": category,
            "timestamp": datetime.datetime.now().isoformat(),
        }
        
        self.data["hechos"].append(fact_entry)
        
        # Mantener solo los últimos N hechos
        if len(self.data["hechos"]) > self.max_facts:
            self.data["hechos"] = self.data["hechos"][-self.max_facts:]
        
        self.save()
    
    def set_user_name(self, name: str):
        """Establece el nombre del usuario"""
        self.data["usuario"]["nombre"] = name
        self.add_fact(f"El usuario se llama {name}", "usuario")
        self.save()
    
    def get_user_name(self) -> Optional[str]:
        """Obtiene el nombre del usuario"""
        return self.data["usuario"].get("nombre")
    
    def set_preference(self, key: str, value):
        """Establece una preferencia del usuario"""
        self.data["usuario"]["preferencias"][key] = value
        self.save()
    
    def get_preference(self, key: str, default=None):
        """Obtiene una preferencia del usuario"""
        return self.data["usuario"]["preferencias"].get(key, default)
    
    def start_session(self):
        """Inicia una nueva sesión"""
        self.data["estadisticas"]["sesiones"] += 1
        self.data["estadisticas"]["ultima_sesion"] = datetime.datetime.now().isoformat()
        self.data["estadisticas"]["primera_vez"] = False
        self.save()
    
    def is_first_time(self) -> bool:
        """Verifica si es la primera vez que se usa Bobi"""
        return self.data["estadisticas"].get("primera_vez", True)
    
    def get_context(self) -> str:
        """
        Genera contexto para el sistema de IA
        Incluye información relevante de la memoria
        """
        context_parts = []
        
        # Nombre del usuario
        if self.data["usuario"]["nombre"]:
            context_parts.append(f"El usuario se llama {self.data['usuario']['nombre']}.")
        
        # Hechos recientes (últimos 5)
        if self.data["hechos"]:
            recent_facts = [f["hecho"] for f in self.data["hechos"][-5:]]
            context_parts.append("Cosas que recuerdas: " + " | ".join(recent_facts))
        
        # Fecha y hora actual
        now = datetime.datetime.now()
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                 "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        
        fecha_str = f"{dias[now.weekday()]} {now.day} de {meses[now.month-1]} de {now.year}, {now.strftime('%H:%M')}"
        context_parts.append(f"Fecha y hora: {fecha_str}.")
        
        # Estadísticas
        sesiones = self.data["estadisticas"]["sesiones"]
        if sesiones > 0:
            context_parts.append(f"Llevan {sesiones} sesiones juntos.")
        
        return "\n".join(context_parts)
    
    def get_recent_history(self, n: int = 5) -> List[Dict]:
        """Obtiene las últimas N interacciones"""
        return self.data["historial"][-n:]
    
    def search_facts(self, query: str) -> List[Dict]:
        """Busca hechos que contengan el query"""
        query_lower = query.lower()
        return [
            fact for fact in self.data["hechos"]
            if query_lower in fact["hecho"].lower()
        ]
    
    def clear_history(self):
        """Limpia el historial de conversaciones (mantiene hechos)"""
        self.data["historial"] = []
        self.save()
    
    def reset(self):
        """Resetea toda la memoria (usar con cuidado)"""
        self.data = self._load.__func__(self)  # Carga memoria inicial
        self.save()
    
    def get_stats(self) -> dict:
        """Obtiene estadísticas de uso"""
        return {
            "sesiones": self.data["estadisticas"]["sesiones"],
            "interacciones_totales": self.data["estadisticas"]["interacciones_totales"],
            "hechos_guardados": len(self.data["hechos"]),
            "historial_size": len(self.data["historial"]),
            "ultima_sesion": self.data["estadisticas"].get("ultima_sesion"),
            "tiene_nombre": self.data["usuario"]["nombre"] is not None,
        }
