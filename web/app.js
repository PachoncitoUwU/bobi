// ═══════════════════════════════════════════════════════════
//  BOBI - Interfaz Web JavaScript
//  Maneja la interacción con el usuario y el servidor
// ═══════════════════════════════════════════════════════════

class BobiApp {
    constructor() {
        // Elementos del DOM
        this.chatMessages = document.getElementById('chatMessages');
        this.inputField = document.getElementById('inputField');
        this.sendBtn = document.getElementById('sendBtn');
        this.voiceBtn = document.getElementById('voiceBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.avatar = document.getElementById('avatar');
        this.statusDot = document.getElementById('statusDot');
        this.statusText = document.getElementById('statusText');
        
        // Estado
        this.isProcessing = false;
        this.isListening = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
        
        // Inicializar
        this.init();
    }
    
    init() {
        // Event listeners
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.inputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !this.isProcessing) {
                this.sendMessage();
            }
        });
        this.voiceBtn.addEventListener('click', () => this.toggleVoice());
        this.clearBtn.addEventListener('click', () => this.clearChat());
        
        // Focus en input
        this.inputField.focus();
        
        console.log('✅ Bobi App inicializada');
        console.log('✅ Reconocimiento de voz con Whisper disponible');
    }
    
    // ═══ RECONOCIMIENTO DE VOZ ═══
    async toggleVoice() {
        if (this.isListening) {
            this.stopRecording();
        } else {
            this.startRecording();
        }
    }
    
    async startRecording() {
        try {
            console.log('🎤 Solicitando acceso al micrófono...');
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };
            
            this.mediaRecorder.onstop = async () => {
                console.log('🎤 Grabación detenida, transcribiendo...');
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                await this.transcribeAudio(audioBlob);
                
                // Detener stream
                stream.getTracks().forEach(track => track.stop());
            };
            
            this.mediaRecorder.start();
            this.isListening = true;
            this.voiceBtn.classList.add('listening');
            this.avatar.classList.add('listening');
            this.setStatus('Escuchando... (habla ahora)', '#00d9ff');
            
            console.log('🎤 Grabando...');
            
            // Detener automáticamente después de 5 segundos
            setTimeout(() => {
                if (this.isListening) {
                    console.log('🎤 Tiempo límite alcanzado');
                    this.stopRecording();
                }
            }, 5000);
            
        } catch (error) {
            console.error('❌ Error accediendo al micrófono:', error);
            this.addMessage('system', '⚠️ No se pudo acceder al micrófono. Permite el acceso en tu navegador.');
            this.setStatus('Listo', '#4ade80');
        }
    }
    
    stopRecording() {
        if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
            this.mediaRecorder.stop();
        }
        this.stopListening();
    }
    
    stopListening() {
        this.isListening = false;
        this.voiceBtn.classList.remove('listening');
        this.avatar.classList.remove('listening');
    }
    
    async transcribeAudio(audioBlob) {
        try {
            this.setStatus('Transcribiendo...', '#fbbf24');
            
            const formData = new FormData();
            formData.append('audio', audioBlob, 'audio.webm');
            
            console.log('📤 Enviando audio al servidor...');
            
            const response = await fetch('/api/transcribe', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Error al transcribir');
            }
            
            const data = await response.json();
            
            console.log('📝 Transcripción:', data.text);
            
            if (data.text && data.text.trim()) {
                this.inputField.value = data.text;
                this.addMessage('system', `🎤 Escuché: "${data.text}"`);
                this.sendMessage();
            } else {
                this.addMessage('system', '⚠️ No se detectó voz. Intenta de nuevo.');
                this.setStatus('Listo', '#4ade80');
            }
            
        } catch (error) {
            console.error('❌ Error transcribiendo:', error);
            this.addMessage('system', `❌ Error al transcribir: ${error.message}`);
            this.setStatus('Listo', '#4ade80');
        }
    }
    
    // ═══ MENSAJES ═══
    async sendMessage() {
        const message = this.inputField.value.trim();
        
        if (!message || this.isProcessing) return;
        
        // Limpiar input
        this.inputField.value = '';
        
        // Agregar mensaje del usuario
        this.addMessage('user', message);
        
        // Procesar
        this.isProcessing = true;
        this.setStatus('Pensando...', '#fbbf24');
        this.avatar.classList.add('thinking');
        
        console.log('💬 Enviando mensaje:', message);
        
        try {
            // Enviar al servidor
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }
            
            const data = await response.json();
            
            console.log('✅ Respuesta recibida');
            
            // Quitar animación de pensamiento
            this.avatar.classList.remove('thinking');
            
            // Agregar respuesta de Bobi
            this.addMessage('bobi', data.response);
            
            // Reproducir audio si está disponible
            if (data.audio) {
                console.log('🔊 Reproduciendo audio...');
                this.playAudio(data.audio);
            } else {
                console.warn('⚠️ No se recibió audio del servidor');
                this.setStatus('Listo', '#4ade80');
            }
            
        } catch (error) {
            console.error('❌ Error:', error);
            this.avatar.classList.remove('thinking');
            this.addMessage('system', '❌ Error al conectar con Bobi. Asegúrate de que el servidor esté corriendo.');
            this.setStatus('Listo', '#4ade80');
        } finally {
            this.isProcessing = false;
            this.inputField.focus();
        }
    }
    
    addMessage(type, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const avatar = type === 'user' ? '👤' : type === 'bobi' ? '🤖' : '⚙️';
        const name = type === 'user' ? 'Tú' : type === 'bobi' ? 'Bobi' : 'Sistema';
        
        messageDiv.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <div class="message-name">${name}</div>
                <div class="message-text">${this.escapeHtml(text)}</div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    clearChat() {
        // Mantener solo el mensaje de bienvenida
        const firstMessage = this.chatMessages.firstElementChild;
        this.chatMessages.innerHTML = '';
        if (firstMessage) {
            this.chatMessages.appendChild(firstMessage);
        }
    }
    
    // ═══ TEXT-TO-SPEECH ═══
    playAudio(audioBase64) {
        try {
            console.log('🔊 Procesando audio...');
            
            // Convertir base64 a blob
            const audioData = atob(audioBase64);
            const arrayBuffer = new ArrayBuffer(audioData.length);
            const view = new Uint8Array(arrayBuffer);
            for (let i = 0; i < audioData.length; i++) {
                view[i] = audioData.charCodeAt(i);
            }
            const blob = new Blob([arrayBuffer], { type: 'audio/mpeg' });
            const url = URL.createObjectURL(blob);
            
            console.log('🔊 Audio procesado, reproduciendo...');
            
            // Crear elemento de audio
            const audio = new Audio(url);
            
            audio.onplay = () => {
                console.log('🔊 Audio reproduciendo');
                this.avatar.classList.add('speaking');
                this.setStatus('Hablando...', '#4ade80');
            };
            
            audio.onended = () => {
                console.log('✅ Audio terminado');
                this.avatar.classList.remove('speaking');
                this.setStatus('Listo', '#4ade80');
                URL.revokeObjectURL(url);
            };
            
            audio.onerror = (error) => {
                console.error('❌ Error reproduciendo audio:', error);
                this.avatar.classList.remove('speaking');
                this.setStatus('Listo', '#4ade80');
                this.addMessage('system', '⚠️ Error al reproducir audio');
            };
            
            // Reproducir
            audio.play().catch(error => {
                console.error('❌ Error al iniciar reproducción:', error);
                this.addMessage('system', '⚠️ Error al reproducir audio. Verifica el volumen.');
                this.setStatus('Listo', '#4ade80');
            });
            
        } catch (error) {
            console.error('❌ Error procesando audio:', error);
            this.avatar.classList.remove('speaking');
            this.setStatus('Listo', '#4ade80');
            this.addMessage('system', '⚠️ Error al procesar audio');
        }
    }
    
    // ═══ UTILIDADES ═══
    setStatus(text, color) {
        this.statusText.textContent = text;
        this.statusDot.style.background = color;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Iniciando Bobi App...');
    window.bobiApp = new BobiApp();
});
