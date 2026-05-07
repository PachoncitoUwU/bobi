#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bobi - Servidor Web v5
— Volumen exacto al % con pycaw
— Spotify: abre canciones especificas
— Busqueda rapida via DuckDuckGo (sin LLM)
— Respuestas cortas garantizadas
"""
import sys, os, subprocess, datetime, tempfile, base64, asyncio
import webbrowser, unicodedata, re, urllib.parse, urllib.request, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
os.environ["PYTHONUTF8"] = "1"

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from core.config import get_config
from core.brain import Brain
from core.memory import Memory
from core.voice import VoiceEngine

app = Flask(__name__, static_folder="web", template_folder="web")
CORS(app)

config  = get_config()
memory  = Memory()
brain   = Brain(memory)
voice   = VoiceEngine()
memory.start_session()

# ══════════════════════════════════════════════════════════
# TTS — Jorge (México), voz amigable y casual
# ══════════════════════════════════════════════════════════

async def _tts(text: str):
    if not text or not text.strip():
        return None
    # Limitar longitud para respuestas de voz más fluidas
    if len(text) > 300:
        text = text[:297] + "..."
    try:
        import edge_tts
        voz   = "es-MX-JorgeNeural"
        rate  = "+10%"
        pitch = "+0Hz"
        tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tmp.close()
        await edge_tts.Communicate(text, voz, rate=rate, pitch=pitch).save(tmp.name)
        with open(tmp.name, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        os.unlink(tmp.name)
        return b64
    except Exception as e:
        print(f"[TTS ERROR] {e}")
        return None

# ══════════════════════════════════════════════════════════
# HELPERS WINDOWS
# ══════════════════════════════════════════════════════════

def _ps(cmd: str, wait=False):
    try:
        flags = subprocess.CREATE_NO_WINDOW
        if wait:
            subprocess.run(["powershell", "-WindowStyle", "Hidden", "-c", cmd],
                           capture_output=True, creationflags=flags)
        else:
            subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-c", cmd],
                             creationflags=flags, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"[PS] {e}"); return False

# ── Teclas globales via Windows SendInput ─────────────────
import ctypes

class _KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class _INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ki", _KEYBDINPUT),
                ("_pad", ctypes.c_ubyte * 8)]

VK = {"play_pause":0xB3,"stop":0xB2,"next":0xB0,"prev":0xB1,
      "vol_mute":0xAD,"vol_down":0xAE,"vol_up":0xAF}

def _send_key(vk: int):
    for flags in (0, 0x0002):
        inp = _INPUT(); inp.type = 1
        inp.ki.wVk = vk; inp.ki.dwFlags = flags
        ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

# ── Volumen exacto al % con pycaw ─────────────────────────

def _set_volume(pct: int) -> str:
    """Establece el volumen del sistema al porcentaje exacto."""
    pct = max(0, min(100, pct))
    try:
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        devices = AudioUtilities.GetSpeakers()
        iface   = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        vol     = cast(iface, POINTER(IAudioEndpointVolume))
        vol.SetMasterVolumeLevelScalar(pct / 100.0, None)
        print(f"[VOL] Volumen al {pct}%")
        return f"Volumen al {pct}%."
    except Exception as e:
        print(f"[VOL] pycaw error: {e} — usando teclas")
        # Fallback: teclas
        for _ in range(50): _send_key(VK["vol_down"])   # bajar a 0
        steps = round(pct / 2)
        for _ in range(steps): _send_key(VK["vol_up"])  # subir al %
        return f"Volumen aproximado al {pct}%."

def _vol(steps: int):
    code = VK["vol_up"] if steps > 0 else VK["vol_down"]
    for _ in range(abs(steps)): _send_key(code)

# ── Detectar apps instaladas ──────────────────────────────

def _find_exe(*paths):
    import shutil
    for p in paths:
        e = os.path.expandvars(os.path.expanduser(p))
        if os.path.exists(e): return e
    return None

def _launch(exe: str, *args) -> bool:
    try:
        subprocess.Popen([exe, *args])
        print(f"[CMD] {exe}"); return True
    except Exception as e:
        print(f"[CMD] FAIL {exe}: {e}"); return False

def _open_url(url: str) -> bool:
    try:
        webbrowser.open(url); print(f"[URL] {url}"); return True
    except Exception as e:
        print(f"[URL] {e}"); return False

import shutil
SPOTIFY_EXE = (_find_exe(
    r"%APPDATA%\Spotify\Spotify.exe",
    r"%LOCALAPPDATA%\Microsoft\WindowsApps\Spotify.exe",
    r"%LOCALAPPDATA%\Programs\Spotify\Spotify.exe",
) or shutil.which("Spotify"))

CHROME_EXE = _find_exe(
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe",
)
EDGE_EXE = _find_exe(
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
)
BROWSER = CHROME_EXE or EDGE_EXE

print(f"[Apps] Spotify={'SI' if SPOTIFY_EXE else 'NO'} | Chrome={'SI' if CHROME_EXE else 'NO'} | Edge={'SI' if EDGE_EXE else 'NO'}")

def _open_browser(url="https://google.com") -> bool:
    if BROWSER: return _launch(BROWSER, url)
    return _open_url(url)

def _bring_spotify_front() -> bool:
    """Trae ventana de Spotify al frente. Devuelve True si estaba abierta."""
    u32 = ctypes.windll.user32
    for title in ("Spotify Premium", "Spotify Free", "Spotify"):
        hwnd = u32.FindWindowW(None, title)
        if hwnd:
            u32.ShowWindow(hwnd, 9)   # SW_RESTORE
            u32.SetForegroundWindow(hwnd)
            return True
    return False

def _play_music(song: str = "") -> str:
    """Abre Spotify y busca/reproduce una canción. Trae Spotify al frente."""
    import threading
    if song and len(song.strip()) > 2:
        encoded = urllib.parse.quote(song.strip())
        print(f"[SPOTIFY] Buscando: {song}")
        # Abrir Spotify con la búsqueda
        subprocess.Popen(f"start spotify:search:{encoded}", shell=True,
                         creationflags=subprocess.CREATE_NO_WINDOW)
        # Después de 2.5s, traer Spotify al frente y presionar Enter para reproducir
        def _auto_play():
            import time; time.sleep(2.5)
            _bring_spotify_front()
            time.sleep(0.4)
            _send_key(0x0D)  # Enter → reproduce el primer resultado
        threading.Thread(target=_auto_play, daemon=True).start()
        return f"Poniendo '{song}' en Spotify."
    # Sin canción — traer o abrir Spotify
    if _bring_spotify_front():
        return "Spotify listo."
    if SPOTIFY_EXE:
        _launch(SPOTIFY_EXE)
        return "Abriendo Spotify."
    subprocess.Popen("start spotify:", shell=True,
                     creationflags=subprocess.CREATE_NO_WINDOW)
    return "Abriendo Spotify."

# ── Info del sistema ──────────────────────────────────────

def _get_system_info() -> str:
    try:
        import psutil
        cpu  = psutil.cpu_percent(interval=0.3)
        ram  = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        s = (f"CPU {cpu:.0f}%, RAM {ram.percent:.0f}% "
             f"({ram.used//1024//1024}/{ram.total//1024//1024} MB), "
             f"Disco {disk.percent:.0f}%.")
        bat = psutil.sensors_battery()
        if bat:
            s += f" Bateria {bat.percent:.0f}% {'(cargando)' if bat.power_plugged else ''}."
        return s
    except:
        return "Instala psutil: pip install psutil"

# ══════════════════════════════════════════════════════════
# NORMALIZACIÓN Y PARSING
# ══════════════════════════════════════════════════════════

def _norm(text: str) -> str:
    """Quita tildes y convierte a minúsculas."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', text.lower())
        if unicodedata.category(c) != 'Mn'
    )

def _parse_percent(text: str):
    """Extrae número de porcentaje. '50%' → 50, 'al 70' → 70"""
    m = re.search(r'(\d+)\s*(?:%|por\s*ciento)', text)
    if m: return int(m.group(1))
    m = re.search(r'(?:al|a)\s+(\d+)', text)
    if m: return int(m.group(1))
    return None

def _parse_song(text: str):
    """Extrae nombre de canción/artista del mensaje."""
    # "pon [cancion] de [artista]" | "ponme [cancion]" | "busca [cancion]"
    patterns = [
        r'(?:pon|ponme|reproduce|busca|quiero\s+escuchar)\s+(?:la\s+)?(?:cancion|tema|cancioncita)?\s+"?([^"]+?)"?\s*(?:de\s+\w+)?$',
        r'(?:pon|ponme|reproduce)\s+"([^"]+)"',
        r'(?:pon|ponme)\s+(.+?)\s+(?:en\s+spotify|por\s+favor|porfavor|ahora)$',
        r'(?:busca|encuentra)\s+(.+?)\s+(?:en\s+spotify)',
    ]
    for p in patterns:
        m = re.search(p, text.strip())
        if m:
            song = _norm(m.group(1).strip())
            # Filtrar palabras genéricas
            generic = {"musica","algo","una cancion","canciones","play","spotify"}
            if song and song not in generic and len(song) > 2:
                return m.group(1).strip()  # devolver sin normalizar
    return None

# ══════════════════════════════════════════════════════════
# BÚSQUEDA RÁPIDA (sin LLM) — DuckDuckGo Instant Answers
# ══════════════════════════════════════════════════════════

def _quick_search(query: str) -> str | None:
    """Busca en DuckDuckGo. Respuesta en < 1s sin LLM."""
    try:
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1&t=bobi"
        req = urllib.request.Request(url, headers={"User-Agent": "Bobi/1.0"})
        with urllib.request.urlopen(req, timeout=4) as r:
            data = json.loads(r.read().decode())
        # Respuesta directa
        if data.get("Answer"):
            return data["Answer"][:200]
        # Resumen del tema
        if data.get("AbstractText"):
            return data["AbstractText"][:250]
        # Resultado de calculadora / conversión
        if data.get("AnswerType"):
            return data.get("Answer") or data.get("AbstractText","")[:200]
    except Exception as e:
        print(f"[DDG] {e}")
    return None

SEARCH_TRIGGERS = ["busca","investiga","que es","quien es","cuando fue","cuanto es",
                   "cuanto vale","como se hace","donde esta","que significa","define",
                   "explica","dime sobre","informacion sobre","quiero saber","buscar"]

def _is_search_query(low: str) -> bool:
    return any(t in low for t in SEARCH_TRIGGERS)

# ══════════════════════════════════════════════════════════
# REGLAS DE INTENCIÓN
# ══════════════════════════════════════════════════════════

def _has(t, *w): return all(x in t for x in w)
def _any(t, *w): return any(x in t for x in w)

INTENT_RULES = [

    # VOLUMEN AL % — PRIMERO para no confundirse con música
    (lambda t: _parse_percent(t) is not None and _any(t,"volumen","audio","sonido","vol"),
     lambda t: (None, _set_volume(_parse_percent(t))), "__VOL_PCT__"),

    # VOLUMEN SUBE/BAJA
    (lambda t: _any(t,"sube","subir","aumenta") and _any(t,"volumen","audio","sonido"),
     lambda t: (_vol(8), f"Volumen subido."), "__ACTION__"),
    (lambda t: _any(t,"baja","bajar","reduce","menos volumen") and _any(t,"volumen","audio","sonido"),
     lambda t: (_vol(-8), f"Volumen bajado."), "__ACTION__"),
    (lambda t: _any(t,"silencia","silenciar","mute","mutear","quita el sonido","sin sonido"),
     lambda t: (_send_key(VK["vol_mute"]), "Silenciado."), "__ACTION__"),
    (lambda t: _any(t,"activa el sonido","quita el silencio","unmute","pon el sonido"),
     lambda t: (_send_key(VK["vol_mute"]), "Sonido activado."), "__ACTION__"),

    # PAUSA / PLAY / SIGUIENTE
    (lambda t: _any(t,"pausa","pausar","para la musica","para la cancion","stop la"),
     lambda t: (_send_key(VK["play_pause"]), "Pausado."), "__ACTION__"),
    (lambda t: _any(t,"continua la","reanuda","sigue la musica","dale play","reproduce la musica") and not _any(t,"cancion","tema") or _any(t,"dale play"),
     lambda t: (_send_key(VK["play_pause"]), "Reproduciendo."), "__ACTION__"),
    (lambda t: _any(t,"siguiente cancion","siguiente tema","la siguiente","skip","pon otra cancion","cambia de cancion","otra cancion"),
     lambda t: (_send_key(VK["next"]), "Siguiente."), "__ACTION__"),
    (lambda t: _any(t,"cancion anterior","tema anterior","la anterior","vuelve la cancion"),
     lambda t: (_send_key(VK["prev"]), "Anterior."), "__ACTION__"),

    # MÚSICA — cancion específica (antes de la genérica)
    (lambda t: (_any(t,"pon","ponme","busca","reproduce") and
                _any(t,"cancion","tema","pista") and
                _parse_song(t)),
     lambda t: (None, _play_music(_parse_song(t) or "")), "__MUSIC_SONG__"),

    # MÚSICA — nombre directo: "ponme blinding lights", "ponme bad bunny"
    (lambda t: (_any(t,"ponme","pon") and
                not _any(t,"volumen","audio","sonido","musica","el volumen") and
                _parse_song(t) and len(t.split()) >= 2),
     lambda t: (None, _play_music(_parse_song(t) or "")), "__MUSIC_SONG__"),

    # MÚSICA — genérica (solo abrir Spotify)
    (lambda t: _any(t,"pon musica","ponme musica","reproduce musica","poner musica","quiero escuchar",
                      "abre spotify","pon spotify","abrir spotify","abre la musica"),
     lambda t: (None, _play_music("")), "__MUSIC_GENERIC__"),

    # STREAMING / WEB
    (lambda t: _any(t,"youtube music","yt music"),
     lambda t: (_open_url("https://music.youtube.com"), "Abriendo YouTube Music."), "__ACTION__"),

    (lambda t: _any(t,"youtube") and _any(t,"abre","pon","entra","abrir"),
     lambda t: (_open_url("https://youtube.com"), "Abriendo YouTube."), "__ACTION__"),

    (lambda t: _any(t,"netflix") and _any(t,"abre","pon","ver","entra"),
     lambda t: (_open_browser("https://netflix.com"), "Abriendo Netflix."), "__ACTION__"),

    (lambda t: _any(t,"twitch") and _any(t,"abre","ver","entra"),
     lambda t: (_open_browser("https://twitch.tv"), "Abriendo Twitch."), "__ACTION__"),

    (lambda t: _any(t,"discord") and _any(t,"abre","entra","abrir"),
     lambda t: (_open_url("discord://") or _open_browser("https://discord.com/app"),
                "Abriendo Discord."), "__ACTION__"),

    (lambda t: _any(t,"whatsapp") and _any(t,"abre","entra","abrir"),
     lambda t: (_open_browser("https://web.whatsapp.com"), "Abriendo WhatsApp."), "__ACTION__"),

    # NAVEGADOR
    (lambda t: _any(t,"chrome","navegador","browser") and _any(t,"abre","abrir","inicia"),
     lambda t: (_open_browser(), "Abriendo el navegador."), "__ACTION__"),

    (lambda t: _any(t,"google") and _any(t,"busca","abre","entra"),
     lambda t: (_open_browser(), "Abriendo Google."), "__ACTION__"),

    # APPS DEL SISTEMA
    (lambda t: _any(t,"explorador","mis archivos","carpeta") and _any(t,"abre","abrir","ver"),
     lambda t: (_launch("explorer.exe"), "Abriendo el explorador."), "__ACTION__"),

    (lambda t: _any(t,"calculadora") and _any(t,"abre","abrir"),
     lambda t: (_launch("calc.exe"), "Abriendo la calculadora."), "__ACTION__"),

    (lambda t: _any(t,"notepad","bloc") and _any(t,"abre","abrir"),
     lambda t: (_launch("notepad.exe"), "Abriendo el bloc de notas."), "__ACTION__"),

    (lambda t: _any(t,"paint") and _any(t,"abre","abrir"),
     lambda t: (_launch("mspaint.exe"), "Abriendo Paint."), "__ACTION__"),

    (lambda t: _any(t,"captura","screenshot") and _any(t,"toma","haz","hacer"),
     lambda t: (_launch("snippingtool.exe"), "Capturando pantalla."), "__ACTION__"),

    (lambda t: _any(t,"configuracion","ajustes") and _any(t,"abre","abrir"),
     lambda t: (subprocess.Popen("start ms-settings:", shell=True),
                "Abriendo configuracion."), "__ACTION__"),

    # SISTEMA
    (lambda t: _any(t,"bloquea","bloquear") and _any(t,"pantalla","pc"),
     lambda t: (subprocess.run(["rundll32.exe","user32.dll,LockWorkStation"]),
                "Bloqueando."), "__ACTION__"),

    (lambda t: _any(t,"apaga","apagar") and _any(t,"pc","computadora") and
               not _any(t,"no","cancel"),
     lambda t: (subprocess.run(["shutdown","/s","/t","60"]),
                "Apagando en 60 segundos. Di 'cancela apagado' para cancelar."), "__ACTION__"),

    (lambda t: _any(t,"cancela","cancelar") and _any(t,"apagado"),
     lambda t: (subprocess.run(["shutdown","/a"]), "Apagado cancelado."), "__ACTION__"),

    (lambda t: _any(t,"reinicia","reiniciar") and _any(t,"pc","computadora"),
     lambda t: (subprocess.run(["shutdown","/r","/t","60"]),
                "Reiniciando en 60 segundos."), "__ACTION__"),

    (lambda t: _any(t,"descargas","downloads") and _any(t,"abre","abrir","ver"),
     lambda t: (_launch("explorer.exe", str(Path.home()/"Downloads")),
                "Abriendo descargas."), "__ACTION__"),

    # BLUETOOTH / WIFI / CAMARA
    (lambda t: _any(t,"bluetooth","bluethoot","blutut") and _any(t,"activa","enciende","prende","pon","conecta","abre","configura"),
     lambda t: (_ps("Start-Process 'ms-settings:bluetooth'", wait=False),
                "Abriendo configuración de Bluetooth."), "__ACTION__"),

    (lambda t: _any(t,"camara","camara web","webcam") and _any(t,"abre","activa","enciende","prende","inicia"),
     lambda t: (subprocess.Popen("start microsoft.windows.camera:", shell=True),
                "Abriendo la cámara."), "__ACTION__"),

    (lambda t: _any(t,"wifi","internet","red") and _any(t,"abre","configura","ajusta","ver"),
     lambda t: (_ps("Start-Process 'ms-settings:network-wifi'", wait=False),
                "Abriendo configuración de red."), "__ACTION__"),

    (lambda t: _any(t,"modo oscuro","tema oscuro"),
     lambda t: (_ps("Set-ItemProperty -Path 'HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize' -Name AppsUseLightTheme -Value 0", wait=True),
                "Modo oscuro activado."), "__ACTION__"),

    (lambda t: _any(t,"modo claro","tema claro"),
     lambda t: (_ps("Set-ItemProperty -Path 'HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize' -Name AppsUseLightTheme -Value 1", wait=True),
                "Modo claro activado."), "__ACTION__"),

    # INFO RÁPIDA
    (lambda t: _any(t,"como esta el pc","cuanto ram","estado del pc","recursos","cuanta memoria"),
     lambda t: (None, _get_system_info()), "__INFO__"),

    (lambda t: _any(t,"que hora es","dime la hora","que horas son","hora actual","la hora"),
     lambda t: (None, f"Son las {datetime.datetime.now().strftime('%H:%M')}."), "__INFO__"),

    (lambda t: _any(t,"que dia es","que fecha","fecha de hoy","que dia estamos"),
     lambda t: (None, _date_str()), "__INFO__"),
]

def _date_str():
    now   = datetime.datetime.now()
    dias  = ["lunes","martes","miercoles","jueves","viernes","sabado","domingo"]
    meses = ["enero","febrero","marzo","abril","mayo","junio",
             "julio","agosto","septiembre","octubre","noviembre","diciembre"]
    return f"Hoy es {dias[now.weekday()]}, {now.day} de {meses[now.month-1]} de {now.year}."

def _handle_pc(msg: str):
    low = _norm(msg)
    print(f"[PC?] '{low}'")
    for test, action_fn, kind in INTENT_RULES:
        try:
            if not test(low): continue
        except: continue

        try:
            result = action_fn(low)
            if isinstance(result, tuple) and len(result) == 2:
                _, reply = result
                if reply and isinstance(reply, str):
                    return reply, True
            return "Hecho.", True
        except Exception as e:
            print(f"[CMD ERR] {e}")
            return f"Lo intente pero tuve un problema: {str(e)[:60]}", True

    return None, False

# ══════════════════════════════════════════════════════════
# IA — Respuestas cortas y directas
# ══════════════════════════════════════════════════════════

SYSTEM_PROMPT = (
    "Eres Bobi, el asistente IA del PC de tu usuario. "
    "Tienes ACCESO COMPLETO al PC: puedes abrir apps, controlar volumen, gestionar archivos, usar internet. "
    "REGLAS: "
    "1) MAXIMO 1 frase de respuesta, menos de 12 palabras. "
    "2) NUNCA digas 'no puedo', 'como IA', 'no tengo acceso', 'hazlo manualmente', 'no tengo capacidad'. "
    "3) Si el usuario pide algo del PC, confirma que lo haces. "
    "4) Habla en espanol casual como un amigo. Sin markdown ni listas."
)

def _ai_think(msg: str) -> str:
    try:
        if brain.current_provider:
            return brain.current_provider.think(msg, SYSTEM_PROMPT)
    except Exception as e:
        print(f"[AI] {e}")
    return brain.think(msg)

# ══════════════════════════════════════════════════════════
# RUTAS FLASK
# ══════════════════════════════════════════════════════════

@app.route("/")
def index(): return send_from_directory("web", "index.html")

@app.route("/<path:path>")
def static_files(path): return send_from_directory("web", path)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data:
        return jsonify({"error":"Sin datos","status":"error"}), 400

    user_msg = data.get("message","").strip()
    if not user_msg:
        return jsonify({"error":"Vacio","status":"error"}), 400

    # Saludo inicial
    if user_msg == "__greet__":
        h = datetime.datetime.now().hour
        saludo = "Buenos dias" if h<12 else "Buenas tardes" if h<19 else "Buenas noches"
        r = f"{saludo}, soy Bobi. Dime que necesitas."
        return jsonify({"response":r, "audio": asyncio.run(_tts(r)), "status":"success"})

    print(f"[User] {user_msg}")
    low = _norm(user_msg)

    # 1. Comando de PC (instantáneo)
    response, handled = _handle_pc(user_msg)
    if handled:
        print(f"[PC] {response}")
    else:
        # 2. Búsqueda rápida DuckDuckGo (sin LLM, ~1s)
        if _is_search_query(low):
            ddg = _quick_search(user_msg)
            if ddg:
                response = ddg
                print(f"[DDG] {response[:60]}")
            else:
                # 3. LLM como último recurso
                response = _ai_think(user_msg)
                print(f"[AI] {response[:60]}")
        else:
            # 3. LLM para conversación
            response = _ai_think(user_msg)
            print(f"[AI] {response[:60]}")

    audio = asyncio.run(_tts(response))
    return jsonify({"response":response, "audio":audio, "status":"success"})

@app.route("/api/status")
def status():
    return jsonify({
        "status":   "online",
        "provider": brain.get_status().get("current_provider","?"),
        "timestamp": datetime.datetime.now().isoformat(),
    })

@app.route("/api/clear", methods=["POST"])
def clear():
    memory.start_session()
    brain.clear_history()
    return jsonify({"status":"success"})

# ══════════════════════════════════════════════════════════
# ARRANQUE
# ══════════════════════════════════════════════════════════

def main():
    print("=" * 56)
    print("  BOBI v5")
    print(f"  Spotify : {'encontrado' if SPOTIFY_EXE else 'no encontrado'}")
    print(f"  Browser : {'Chrome' if CHROME_EXE else 'Edge' if EDGE_EXE else '?'}")
    print(f"  Modelo  : {config.get('ai_providers.ollama.model','?')}")
    print("  URL     : http://localhost:5000")
    print("=" * 56)
    print()
    print("  IMPORTANTE: Para respuestas rapidas obten una clave Gemini")
    print("  gratis en: https://aistudio.google.com/apikey")
    print("  Luego ponla en el archivo .env o config como GEMINI_API_KEY=...")
    print()
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
        sys.exit(0)
