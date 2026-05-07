/* ═══════════════════════════════════════════════════════
   BOBI app.js v3
   — Wake word "Oye Bobi" siempre activo
   — Web Speech API para voz
   — Respuestas rápidas
   ═══════════════════════════════════════════════════════ */

const API = "http://localhost:5000/api";

// ── DOM ──────────────────────────────────────────────────
const avPanel  = document.getElementById("avPanel");
const avLabel  = document.getElementById("avLabel");
const sDot     = document.getElementById("sDot");
const sText    = document.getElementById("sText");
const provPill = document.getElementById("provPill");
const messages = document.getElementById("messages");
const typing   = document.getElementById("typing");
const inp      = document.getElementById("inp");
const btnSend  = document.getElementById("btnSend");
const btnMic   = document.getElementById("btnMic");
const btnClear = document.getElementById("btnClear");
const btnMute  = document.getElementById("btnMute");
const eyeL     = document.getElementById("eyeL");
const eyeR     = document.getElementById("eyeR");
const wakeIndicator = document.getElementById("wakeIndicator");

// ── Estado ───────────────────────────────────────────────
let busy      = false;
let muted     = false;
let curAudio  = null;
let blinkTO   = null;
let wakeMode  = false;   // true = escuchando wake word en fondo

// ── Avatar ───────────────────────────────────────────────
const LABELS = {
  idle:      "Listo · Di 'Oye Bobi'",
  wake:      "Escuchando en segundo plano...",
  listening: "Te escucho...",
  thinking:  "Procesando...",
  speaking:  "Hablando...",
};

function setState(s) {
  avPanel.className = `av-panel ${s === "idle" || s === "wake" ? "" : s}`;
  if (s === "listening") avPanel.classList.add("listening");
  avLabel.textContent = LABELS[s] || "";
  sDot.className = `s-dot ${s === "idle" || s === "wake" ? "" : s}`;
  const textMap = { idle:"Listo", wake:"Activo", listening:"Escuchando", thinking:"Procesando", speaking:"Hablando" };
  sText.textContent = textMap[s] || s;
}

// Parpadeo LED
function blink() {
  [eyeL, eyeR].forEach(e => e.classList.add("blink"));
  setTimeout(() => [eyeL, eyeR].forEach(e => e.classList.remove("blink")), 130);
  blinkTO = setTimeout(blink, 2500 + Math.random() * 4000);
}

// ── Mensajes ─────────────────────────────────────────────
function esc(s) {
  return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

function addMsg(who, text) {
  const d = document.createElement("div");
  d.className = `msg ${who}`;
  d.innerHTML = `
    <div class="m-avatar">${who === "bobi" ? "🤖" : "😊"}</div>
    <div class="bubble-wrap">
      <div class="bubble-name">${who === "bobi" ? "Bobi" : "Tú"}</div>
      <div class="bubble">${esc(text)}</div>
    </div>`;
  messages.appendChild(d);
  messages.scrollTop = messages.scrollHeight;
}

function showTyping(v) { typing.style.display = v ? "flex" : "none"; }

// ── Audio ────────────────────────────────────────────────
function stopAudio() {
  if (curAudio) { curAudio.pause(); curAudio.currentTime = 0; curAudio = null; }
}

function playAudio(b64) {
  return new Promise(resolve => {
    if (muted || !b64) { resolve(); return; }
    stopAudio();
    const a = new Audio(`data:audio/mp3;base64,${b64}`);
    curAudio = a;
    a.onended = a.onerror = () => { curAudio = null; resolve(); };
    a.play().catch(resolve);
  });
}

// ── Enviar al backend ────────────────────────────────────
async function send(text) {
  if (busy || !text.trim()) return;
  busy = true;
  addMsg("user", text);
  setState("thinking");
  showTyping(true);

  try {
    const res  = await fetch(`${API}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await res.json();
    showTyping(false);

    if (data.status === "success") {
      addMsg("bobi", data.response);
      setState("speaking");
      await playAudio(data.audio);
    } else {
      addMsg("bobi", `Error: ${data.error || "desconocido"}`);
    }
  } catch {
    showTyping(false);
    addMsg("bobi", "No puedo conectar con el servidor.");
  }

  busy = false;
  setState(wakeMode ? "wake" : "idle");
  // Reanudar wake word si estaba activo
  if (wakeMode) _scheduleWake(400);

}

// ── Texto ─────────────────────────────────────────────────
btnSend.onclick = () => {
  const t = inp.value.trim();
  if (!t) return;
  inp.value = "";
  send(t);
};
inp.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); btnSend.click(); }
});

// ──────────────────────────────────────────────────────────
// RECONOCIMIENTO DE VOZ — Web Speech API
// ──────────────────────────────────────────────────────────

const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRec) {
  btnMic.disabled = true;
  btnMic.querySelector("span").textContent = "Usa Chrome/Edge";
  btnMic.style.opacity = ".4";
}

// ── WAKE WORD — sistema robusto con watchdog ──────────────

const WAKE_WORDS = [
  "bobi", "bobe", "bobby", "bovi", "vobi",
  "oye bobi", "oye bobe", "oye bobby", "oye bovi",
  "oye obi",  "hey bobi", "hey bobby", "hey bobe",
  "obi", "oby",
];

let wakeRec        = null;
let wakeAlive      = false;   // true mientras la instancia está activa
let wakeDetecting  = false;   // true mientras procesamos un comando (bloquea reinicio)
let wakeTimer      = null;    // timer de reinicio
let wakeWatchdog   = null;    // watchdog que detecta muerte silenciosa
let lastStart      = 0;       // evita reinicios demasiado rápidos

function _startWakeRec() {
  if (!SpeechRec || !wakeMode || busy) return;

  // Evitar reinicio antes de 500ms
  const now = Date.now();
  if (now - lastStart < 500) {
    clearTimeout(wakeTimer);
    wakeTimer = setTimeout(_startWakeRec, 500 - (now - lastStart));
    return;
  }
  lastStart = now;

  // Destruir instancia anterior
  if (wakeRec) { try { wakeRec.abort(); } catch(_){} wakeRec = null; }

  const rec = new SpeechRec();
  rec.lang             = "es-ES";
  rec.continuous       = false;   // más fiable que continuous:true en Chrome
  rec.interimResults   = true;
  rec.maxAlternatives  = 3;

  rec.onstart = () => {
    wakeAlive = true;
    _resetWatchdog();
  };

  rec.onresult = e => {
    const texts = [];
    for (let i = 0; i < e.results.length; i++)
      for (let j = 0; j < e.results[i].length; j++)
        texts.push(e.results[i][j].transcript.toLowerCase().trim());
    const full = texts.join(" ");

    if (WAKE_WORDS.some(w => full.includes(w))) {
      try { rec.abort(); } catch(_) {}
      wakeAlive = false;
      _onWakeDetected();
    }
  };

  rec.onerror = e => {
    wakeAlive = false;
    if (e.error === "aborted") return;
    // not-allowed = sin permiso, esperar más
    _scheduleWake(e.error === "not-allowed" ? 5000 : 600);
  };

  rec.onend = () => {
    wakeAlive = false;
    // Si estamos procesando un comando, NO reiniciar el wake word todavía
    if (wakeMode && !busy && !wakeDetecting) _scheduleWake(300);
  };

  wakeRec = rec;
  try { rec.start(); }
  catch(_) { wakeAlive = false; _scheduleWake(800); }
}

function _scheduleWake(delay = 300) {
  clearTimeout(wakeTimer);
  clearTimeout(wakeWatchdog);
  if (wakeMode && !busy)
    wakeTimer = setTimeout(_startWakeRec, delay);
}

// Si en 6s no hay señal de vida, forzar reinicio
function _resetWatchdog() {
  clearTimeout(wakeWatchdog);
  wakeWatchdog = setTimeout(() => {
    if (wakeMode && !busy && !wakeAlive) _startWakeRec();
  }, 6000);
}

function _onWakeDetected() {
  clearTimeout(wakeTimer);
  clearTimeout(wakeWatchdog);
  wakeDetecting = true;
  stopAudio();           // ← interrumpir si Bobi estaba hablando
  busy = false;          // ← liberar busy para poder escuchar
  setState("listening");
  setTimeout(startCommandListening, 200);
}

// API pública
function startWakeWord() {
  wakeMode = true;
  if (wakeIndicator) wakeIndicator.classList.add("active");
  setState("wake");
  _startWakeRec();
}

function stopWakeWord() {
  wakeMode  = false;
  wakeAlive = false;
  clearTimeout(wakeTimer);
  clearTimeout(wakeWatchdog);
  if (wakeRec) { try { wakeRec.abort(); } catch(_){} wakeRec = null; }
  if (wakeIndicator) wakeIndicator.classList.remove("active");
}



// ── COMANDO — escucha una sola vez después del wake word ──

let cmdRec = null;

function startCommandListening() {
  if (!SpeechRec) return;
  if (cmdRec) { try { cmdRec.abort(); } catch(_){} }

  wakeDetecting = false;   // ya estamos en el reconocedor de comando, desbloquear flag

  cmdRec = new SpeechRec();
  cmdRec.lang            = "es-ES";
  cmdRec.continuous      = false;
  cmdRec.interimResults  = true;   // mostrar texto mientras habla
  cmdRec.maxAlternatives = 1;

  let gotResult = false;  // si ya recibimos resultado, no mostrar "no te escuché"

  setState("listening");
  btnMic.classList.add("active");
  btnMic.querySelector("span").textContent = "Escuchando...";

  cmdRec.onresult = e => {
    const result = e.results[e.results.length - 1];
    const transcript = result[0].transcript;

    if (!result.isFinal) {
      // Solo mostrar preview en el input mientras habla, NO enviar
      inp.value = transcript;
      return;
    }

    // Resultado final — ahora sí enviar
    gotResult = true;
    inp.value = transcript;
    stopCommandListening();
    send(transcript);
    inp.value = "";
  };

  cmdRec.onerror = e => {
    if (e.error === "aborted") { stopCommandListening(); return; }
    gotResult = true; // evitar doble mensaje
    const msgs = {
      "not-allowed": "Permite el micrófono en la barra del navegador (icono del candado).",
      "no-speech":   "No te escuché. Di 'Oye Bobi' de nuevo.",
      "network":     "Error de red al reconocer voz.",
    };
    addMsg("bobi", msgs[e.error] || `Error de micrófono: ${e.error}`);
    stopCommandListening();
    busy = false;
    setState(wakeMode ? "wake" : "idle");
    if (wakeMode) _scheduleWake(500);
  };

  // onend: siempre se dispara al terminar — con o sin resultado
  cmdRec.onend = () => {
    stopCommandListening();
    if (!gotResult && !busy) {
      // Se cerró sin capturar nada — reanudar wake word silenciosamente
      setState(wakeMode ? "wake" : "idle");
      if (wakeMode) _scheduleWake(400);
    }
  };

  try { cmdRec.start(); } catch(e) {
    addMsg("bobi", "No pude abrir el micrófono.");
    setState("idle");
  }
}

function stopCommandListening() {
  btnMic.classList.remove("active");
  btnMic.querySelector("span").textContent = "Hablar";
  if (cmdRec) { try { cmdRec.stop(); } catch(_){} cmdRec = null; }
}

// ── Botón micrófono (escucha manual sin wake word) ────────
btnMic.onclick = () => {
  if (btnMic.classList.contains("active")) {
    stopCommandListening();
    busy = false;
    setState(wakeMode ? "wake" : "idle");
  } else {
    if (busy) return;
    stopWakeWord();        // pausar wake word mientras usas el botón
    startCommandListening();
  }
};

// ── Wake word toggle ──────────────────────────────────────
const btnWake = document.getElementById("btnWake");
if (btnWake) {
  btnWake.onclick = () => {
    if (wakeMode) {
      stopWakeWord();
      btnWake.querySelector("span").textContent = "Wake word OFF";
      btnWake.classList.remove("active");
      setState("idle");
    } else {
      startWakeWord();
      btnWake.querySelector("span").textContent = "Wake word ON";
      btnWake.classList.add("active");
    }
  };
}

// ── Silenciar ────────────────────────────────────────────
btnMute.onclick = () => {
  muted = !muted;
  btnMute.classList.toggle("muted", muted);
  btnMute.querySelector("span").textContent = muted ? "Voz silenciada" : "Voz activada";
  if (muted && curAudio) { curAudio.pause(); curAudio = null; }
};

// ── Limpiar ──────────────────────────────────────────────
btnClear.onclick = async () => {
  messages.innerHTML = "";
  await fetch(`${API}/clear`, { method: "POST" }).catch(() => {});
  addMsg("bobi", "Chat limpiado. ¿En qué puedo ayudarte?");
};

// ── Estado del servidor ──────────────────────────────────
async function checkServer() {
  try {
    const d = await (await fetch(`${API}/status`)).json();
    if (d.status === "online") {
      provPill.textContent = `IA: ${d.provider || "—"}`;
      sDot.classList.remove("error");
    }
  } catch {
    sDot.className = "s-dot error";
    sText.textContent = "Sin conexión";
  }
}

// ── Init ─────────────────────────────────────────────────
(async () => {
  blinkTO = setTimeout(blink, 2000);
  await checkServer();
  setInterval(checkServer, 30_000);

  // Saludo inicial
  setState("thinking");
  showTyping(true);
  try {
    const res  = await fetch(`${API}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: "__greet__" }),
    });
    const data = await res.json();
    showTyping(false);
    if (data.status === "success") {
      addMsg("bobi", data.response);
      setState("speaking");
      await playAudio(data.audio);
    }
  } catch {
    showTyping(false);
    addMsg("bobi", "Hola, soy Bobi. Di 'Oye Bobi' para hablar.");
  }

  // Activar wake word automáticamente
  setState("idle");
  busy = false;
  if (SpeechRec) {
    startWakeWord();
    if (btnWake) {
      btnWake.querySelector("span").textContent = "Wake word ON";
      btnWake.classList.add("active");
    }
  }
})();
