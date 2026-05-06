#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              BOBI - Servidor Web con Flask                   ║
║              Interfaz moderna HTML/CSS/JavaScript            ║
╚══════════════════════════════════════════════════════════════╝
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from core.config import get_config
from core.brain import Brain
from core.memory import Memory
from core.voice import VoiceEngine
import datetime
import tempfile
import os
import base64

# Crear app Flask
app = Flask(__name__, 
            static_folder='web',
            template_folder='web')
CORS(app)

# Inicializar componentes de Bobi
config = get_config()
memory = Memory()
brain = Brain(memory)
voice = VoiceEngine()

print("╔══════════════════════════════════════════════════════════════╗")
print("║              BOBI - Servidor Web Iniciando                  ║")
print("╚══════════════════════════════════════════════════════════════╝")
print()

# Iniciar sesión
memory.start_session()

@app.route('/')
def index():
    """Página principal"""
    return send_from_directory('web', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Archivos estáticos (CSS, JS, etc.)"""
    return send_from_directory('web', path)

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Endpoint para enviar mensajes a Bobi
    
    Request JSON:
        {
            "message": "Hola Bobi"
        }
    
    Response JSON:
        {
            "response": "¡Hola! ¿En qué puedo ayudarte?",
            "audio": "base64_encoded_audio",
            "status": "success"
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'No se proporcionó mensaje',
                'status': 'error'
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'error': 'Mensaje vacío',
                'status': 'error'
            }), 400
        
        print(f"👤 Usuario: {user_message}")
        
        # Generar respuesta con Bobi
        response = brain.think(user_message)
        
        print(f"🤖 Bobi: {response}")
        
        # Generar audio con edge-tts (voz natural)
        audio_base64 = None
        try:
            import edge_tts
            import asyncio
            
            async def generate_audio():
                voice = "es-MX-DaliaNeural"  # Voz natural femenina
                communicate = edge_tts.Communicate(response, voice)
                
                # Guardar en archivo temporal
                tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
                await communicate.save(tmp.name)
                
                # Leer y convertir a base64
                with open(tmp.name, 'rb') as f:
                    audio_data = f.read()
                    audio_b64 = base64.b64encode(audio_data).decode('utf-8')
                
                # Limpiar
                os.unlink(tmp.name)
                
                return audio_b64
            
            audio_base64 = asyncio.run(generate_audio())
            print("🔊 Audio generado con edge-tts")
        
        except Exception as e:
            print(f"⚠️  Error generando audio: {e}")
        
        print()
        
        return jsonify({
            'response': response,
            'audio': audio_base64,
            'status': 'success'
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/status', methods=['GET'])
def status():
    """
    Endpoint para obtener el estado de Bobi
    
    Response JSON:
        {
            "status": "online",
            "ia_provider": "ollama",
            "voice_available": true,
            "memory_sessions": 5
        }
    """
    try:
        voice_status = voice.get_status()
        
        return jsonify({
            'status': 'online',
            'ia_provider': brain.provider_name,
            'voice_available': voice_status['enabled'],
            'voice_engines': voice_status['tts_engines'],
            'memory_sessions': len(memory.sessions) if hasattr(memory, 'sessions') else 0,
            'timestamp': datetime.datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/clear', methods=['POST'])
def clear():
    """
    Endpoint para limpiar la memoria de la sesión actual
    
    Response JSON:
        {
            "status": "success",
            "message": "Memoria limpiada"
        }
    """
    try:
        memory.start_session()  # Reiniciar sesión
        
        return jsonify({
            'status': 'success',
            'message': 'Memoria limpiada'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    """
    Endpoint para transcribir audio a texto usando Whisper
    
    Request: audio/webm blob
    
    Response JSON:
        {
            "text": "texto transcrito",
            "status": "success"
        }
    """
    try:
        # Verificar que hay audio
        if 'audio' not in request.files:
            return jsonify({
                'error': 'No se proporcionó audio',
                'status': 'error'
            }), 400
        
        audio_file = request.files['audio']
        
        # Guardar temporalmente
        tmp = tempfile.NamedTemporaryFile(suffix=".webm", delete=False)
        audio_file.save(tmp.name)
        tmp.close()
        
        print("🎙️  Transcribiendo audio...")
        
        # Transcribir con Whisper
        text = voice.stt.transcribe(tmp.name)
        
        # Limpiar
        os.unlink(tmp.name)
        
        if not text:
            return jsonify({
                'error': 'No se detectó voz',
                'status': 'error'
            }), 400
        
        print(f"📝 Transcrito: {text}")
        
        return jsonify({
            'text': text,
            'status': 'success'
        })
    
    except Exception as e:
        print(f"❌ Error transcribiendo: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

def main():
    """Punto de entrada"""
    print("✅ Componentes inicializados")
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    🚀 SERVIDOR LISTO                         ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("📱 Abre tu navegador en:")
    print()
    print("   http://localhost:5000")
    print()
    print("💡 Características:")
    print("   • Interfaz moderna y animada")
    print("   • Reconocimiento de voz (Chrome/Edge)")
    print("   • Síntesis de voz del navegador")
    print("   • Chat en tiempo real")
    print()
    print("⚠️  Presiona Ctrl+C para detener el servidor")
    print()
    
    # Iniciar servidor
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("👋 Servidor detenido")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
