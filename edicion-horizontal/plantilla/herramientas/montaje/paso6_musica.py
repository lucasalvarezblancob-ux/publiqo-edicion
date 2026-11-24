"""Paso 6: música SOLO donde toca (Lucas, 2026-11-11: «no hace falta que la pongas en cada momento, solo cuando toque,
a veces poniendo planos»). Nada de cama continua: VENTANAS con entrada rápida y salida de 3 s, y silencio musical entre ellas.
Dónde toca: gancho + ráfaga + título + arranque; la entrada de cada sección (rótulo + ~10-14 s); secuencias de planos sin
voz; explicación con mapas; la frase emotiva; el cierre. Orientación: 30-40 % del vídeo, 14-17 dB bajo la voz.
En plan.py:
  PISTAS = {"alegre": ("archivo-de-su-recursos-musica.wav", BPM), ...}     de personal/<creador>/recursos/musica/
  VENTANAS = [("alegre", ancla_inicio, ancla_fin), ...]     anclas como en el resto del plan; "inicio" y "fin" valen
             (opcional 4.º elemento {"seco": True}: entra y sale sin fundido, en un corte — G005)
  HUECOS_MUSICA = [(ancla_del_remate, segundos), ...]      la música se va en seco antes del remate y vuelve en el corte (G005)
  NIVELES = {...}                                            opcional: cambia los dB de abajo
Ningún plano sin voz se queda sin música: si un respiro entre ventanas cae donde no se habla, la ventana de antes se
alarga sola («puente», lo imprime). Cada ventana arranca en un compás entero de su pista (se va avanzando por la canción); la que llega al final del vídeo
usa el final real de la canción, para que acabe con él. Sin PISTAS/VENTANAS no hace nada (vídeo sin música).
Salida: trabajo/musica.wav y trabajo/audio_final.wav (voz + efectos + música a -14 LUFS). Lanza antes paso5_audio.py."""
import json, os, subprocess
import numpy as np, soundfile as sf
from comun import CAPAS_JSON, F, FPS, MUSICA, TRABAJO, Linea, ajuste
import plan      # después de comun: es quien mete la carpeta del vídeo en el path
from paso5_audio import normalizar

SR = 48000
PISTAS, VENTANAS = getattr(plan, "PISTAS", {}), getattr(plan, "VENTANAS", [])
if not PISTAS or not VENTANAS: raise SystemExit("plan.py no define PISTAS y VENTANAS: el vídeo va sin música (audio_final.wav es el del paso 5).")
# dB sobre la pista normalizada a -14 LUFS: BASE bajo la voz; TRAILER antes de la marca "cuerpo"; TITULO de la marca "rafaga"
# (o "titulo") a "cuerpo"; SECCION durante el rótulo de capítulo; MAPA durante un mapa; SINVOZ en planos sin habla (V).
NV = {"BASE": -24.0, "TRAILER": -16.0, "TITULO": -6.0, "SECCION": -15.0, "MAPA": -19.0, "SINVOZ": -13.0, "CIERRE": -20.0, **ajuste("MUSICA_NIVELES", {}), **getattr(plan, "NIVELES", {})}
ENT, SAL = F(0.48), F(3.0)      # fundidos de entrada y salida de cada ventana
L = Linea(); M, TOTAL, P = L.marcas, L.total, L.piezas
C = json.load(open(CAPAS_JSON, encoding="utf-8"))


def cargar(nombre, bpm):
    if not MUSICA: raise SystemExit("No hay creador en personal/: la música va en personal/<creador>/recursos/musica/ (o pon MUSICA = '...' en proyecto.py)")
    p = f"{MUSICA}/{nombre}"
    if not os.path.exists(p): raise SystemExit(f"Falta la pista {p} (la descarga el creador con su licencia; ver personal/<creador>/recursos/musica/CATALOGO.md)")
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", p, "-af", "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    lufs = float(json.loads(r[r.rindex("{"):r.rindex("}") + 1])["input_i"])
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", p, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    y = np.frombuffer(raw, np.float32).reshape(-1, 2) * 10 ** ((-14 - lufs) / 20)
    # La canción entra por su primer compás con volumen normal: se salta el silencio y la intro floja (como mucho 16
    # compases). Una ventana que empieza en un plano sin voz con 2 s mudos de intro deja el hueco igual de mudo (1311).
    compas = int(240 / bpm * SR); nb = min(len(y) // compas, 64)
    rms = [20 * np.log10(np.sqrt(np.mean(y[i * compas:(i + 1) * compas] ** 2)) + 1e-9) for i in range(nb)]
    i0 = next((i for i, r in enumerate(rms) if r >= np.median(rms) - 6), 0) if nb else 0
    return {"y": y, "bpm": bpm, "pos": min(i0, 16) * compas}


def trozo(t, n, final=False):
    """n muestras de la pista desde su puntero (compás entero). Si la canción se acaba, vuelve al compás 8 con un cruce
    de medio segundo, también EN MITAD de una ventana (ventanas más largas que la canción: música en casi todo el vídeo).
    final: los últimos n, para que la canción acabe con el vídeo."""
    y, compas = t["y"], 240 / t["bpm"] * SR
    if final and len(y) >= n: return y[len(y) - n:].copy()
    x, ini, fin = SR // 2, int(round(8 * compas)), len(y) - int(4 * compas) - SR // 2
    if fin - ini < 8 * compas: ini = 0                                     # pista muy corta: se repite entera
    if t["pos"] + min(n, int(8 * compas)) > fin: t["pos"] = ini
    out = np.zeros((n, 2), np.float32); k = 0
    while k < n:
        m = min(n - k, fin - t["pos"]); seg = y[t["pos"]:t["pos"] + m].copy()
        if k: c = min(x, m); seg[:c] *= np.linspace(0, 1, c, dtype=np.float32)[:, None]
        out[k:k + m] += seg; k += m; t["pos"] += m
        if k < n:                                                           # se acabó en mitad de la ventana: cruce y vuelta al compás 8
            c = min(x, n - k); out[k:k + c] += y[t["pos"]:t["pos"] + c] * np.linspace(1, 0, c, dtype=np.float32)[:, None]; t["pos"] = ini
    t["pos"] = int(round(np.ceil(t["pos"] / (4 * compas)) * 4 * compas))
    return out


# ---- Nunca un plano sin voz y sin música (Lucas, 2026-11-14, 1311 v2: «sale caminando y no habla ni nada y no hay música;
# ponle música a eso»). Los respiros entre ventanas solo pueden caer donde se habla: si un hueco de más de HUECO_MAX s queda
# sin palabras y sin música audible (la cola del fundido no cuenta), la ventana que acaba justo antes se alarga hasta que
# vuelve la voz; si la siguiente empieza justo al acabar el hueco, es esa la que entra antes, con el plano sin voz. Lo que no tiene ventana antes, se avisa.
HUECO_MAX = ajuste("MUSICA_HUECO_MAX", 1.0)
W = []
SECAS = set()      # G005: ventanas con {"seco": True} entran y salen sin fundido (en un corte), como las referencias (12 de 15)
for v in VENTANAS:
    k, a0, a1 = v[:3]; op = v[3] if len(v) > 3 else {}
    f0, f1 = max(0, L.ancla(a0)), min(TOTAL, L.ancla(a1))
    if f1 - f0 < F(2): print(f"AVISO: ventana de {k} demasiado corta o al revés ({f0}-{f1}); se salta"); continue
    W.append([k, f0, f1])
    if op.get("seco"): SECAS.add(len(W) - 1)
voz = np.zeros(TOTAL + 1, bool)
for w in L.palabras:
    if "o0" in w: voz[max(0, int(w["o0"]) - F(0.25)):int(w["o1"]) + F(0.25)] = True


def huecos():
    oye = np.zeros(TOTAL + 1, bool)
    for _, f0, f1 in W: oye[f0:f1 if f1 >= TOTAL else max(f0, f1 - SAL // 2)] = True
    h, i = [], 0
    while i <= TOTAL:
        if voz[i] or oye[i]: i += 1; continue
        j = i
        while j <= TOTAL and not voz[j] and not oye[j]: j += 1
        if j - i >= F(HUECO_MAX): h.append((i, j))
        i = j
    return h


mmss = lambda f: f"{f / FPS // 60:.0f}:{f / FPS % 60:04.1f}"
for i, j in huecos():
    despues = [w for w in W if j - F(0.5) <= w[1] <= j + F(1.0)]
    if despues:          # la canción siguiente empieza justo al acabar el hueco: entra antes, con el plano sin voz
        w = min(despues, key=lambda w: w[1]); w[1] = max(0, i - F(0.2))
        print(f"puente: {w[0]} entra antes, en {mmss(w[1])} (de {mmss(i)} a {mmss(j)} no se habla y no había música)"); continue
    antes = [w for w in W if w[2] <= i + SAL]
    if not antes: print(f"AVISO: {mmss(i)}-{mmss(j)} sin voz ni música y sin ventana antes ni después: añade una en VENTANAS"); continue
    w = max(antes, key=lambda w: w[2]); w[2] = min(TOTAL, max(w[2], j + SAL))      # suena entera hasta que vuelve la voz
    print(f"puente: {w[0]} alargada hasta {mmss(w[2])} (de {mmss(i)} a {mmss(j)} no se habla y no había música)")
for i, j in huecos(): print(f"AVISO: sigue sin voz ni música {mmss(i)}-{mmss(j)}")

N = TOTAL * SR // FPS; mus = np.zeros((N, 2), np.float32); cat = {}; cubierto = np.zeros(TOTAL + 1, bool)
for iw, (k, f0, f1) in enumerate(W):
    if k not in cat: cat[k] = cargar(*PISTAS[k])
    s0, s1 = f0 * SR // FPS, f1 * SR // FPS
    seg = trozo(cat[k], s1 - s0, final=(f1 == TOTAL)); n = len(seg)
    e, s = min(ENT * SR // FPS, n // 4), min(SAL * SR // FPS, n // 2)
    if iw in SECAS: e = s = min(SR // FPS, n // 4)          # seca: 1 fotograma de rampa, solo para que no chasque
    if f0 > 0: seg[:e] *= np.linspace(0, 1, e)[:, None] ** 2
    if f1 < TOTAL: seg[-s:] *= np.cos(np.linspace(0, np.pi / 2, s))[:, None] ** 2
    mus[s0:s0 + n] += seg; cubierto[f0:f1] = True
    print(f"{k:10} {f0 / FPS // 60:.0f}:{f0 / FPS % 60:04.1f} - {f1 / FPS // 60:.0f}:{f1 / FPS % 60:04.1f}  ({(f1 - f0) / FPS:.0f} s)")
print(f"música en el {100 * cubierto.mean():.0f} % del vídeo")

# niveles por tramos (dB), suavizados
g = np.full(TOTAL + 1, NV["BASE"]); cuerpo = M.get("cuerpo", 0)
g[:cuerpo] = NV["TRAILER"]
if cuerpo and ("rafaga" in M or "titulo" in M): g[M.get("rafaga", M.get("titulo")):cuerpo] = NV["TITULO"]
for p in P:
    if p["k"] == "V" and p["o"] >= cuerpo: g[p["o"]:p["o"] + p["n"]] = NV["SINVOZ"]
i = cuerpo                 # y en cualquier rato de más de 1,5 s sin palabras (él andando, mirando), aunque sea plano suyo
while i < TOTAL:
    if voz[i]: i += 1; continue
    j = i
    while j < TOTAL and not voz[j]: j += 1
    if j - i >= F(1.5): g[i:j] = np.maximum(g[i:j], NV["SINVOZ"])
    i = j
for it in C["items"]:
    if it["t"] == "seccion":
        a, b = max(0, it["f0"] - F(0.2)), it["f0"] + F(2.8); g[a:b] = np.maximum(g[a:b], NV["SECCION"])
    if it["t"] == "mapa": g[it["f0"]:it["f1"]] = np.maximum(g[it["f0"]:it["f1"]], NV["MAPA"])
if "cierre" in M: g[M["cierre"]:] = np.maximum(g[M["cierre"]:], NV["CIERRE"])
k = np.hanning(21); g = np.convolve(np.pad(g, 10, mode="edge"), k / k.sum(), "valid")
env = 10 ** (np.interp(np.arange(N) / SR * FPS, np.arange(len(g)), g) / 20)
env[-3 * SR:] *= np.linspace(1, 0, 3 * SR) ** 2
# G005: SILENCIO COMO REMATE (8 de 15 vlogs, 7 de 7 retos). En plan.py: HUECOS_MUSICA = [(ancla_del_remate, segundos), ...]
# La música se va EN SECO `segundos` antes del remate (0,7–6 s) y vuelve de golpe en el primer corte tras el remate.
# Va después del suavizado, con 1 fotograma de rampa (sin chasquido). Sin HUECOS_MUSICA no cambia nada.
_V = json.load(open(f"{TRABAJO}/video.json")); _cortes = sorted({v["o"] for tr in _V["tramos"] for v in tr} | {TOTAL})
for anc, seg_ in getattr(plan, "HUECOS_MUSICA", []):
    r = L.ancla(anc); a = max(0, r - F(seg_)); b = next((c for c in _cortes if c > r), TOTAL)
    sa, sb, ram = a * SR // FPS, b * SR // FPS, SR // FPS
    env[sa:sb] = 0; env[max(0, sa - ram):sa] *= np.linspace(1, 0, sa - max(0, sa - ram))
    env[sb:sb + ram] *= np.linspace(0, 1, len(env[sb:sb + ram]))
    print(f"hueco de música {mmss(a)}–{mmss(b)} (remate en {mmss(r)}, vuelve en el corte)")
mus *= env[:, None].astype(np.float32); sf.write(f"{TRABAJO}/musica.wav", mus, SR)

subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{TRABAJO}/mezcla.wav", "-i", f"{TRABAJO}/musica.wav", "-filter_complex", "[0:a][1:a]amix=inputs=2:normalize=0[m]", "-map", "[m]", f"{TRABAJO}/mezcla_musica.wav"], check=True)
if os.path.exists(f"{TRABAJO}/audio_final.wav"): os.replace(f"{TRABAJO}/audio_final.wav", f"{TRABAJO}/audio_final_sin_musica.wav")
m = normalizar(f"{TRABAJO}/mezcla_musica.wav", f"{TRABAJO}/audio_final.wav")
# comprobación: nivel de la música respecto a la voz donde suenan a la vez
v, _ = sf.read(f"{TRABAJO}/mezcla.wav", dtype="float32"); db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
voz = np.zeros(TOTAL + 1, bool)
for p in P:
    if p["k"] == "T": voz[p["o"]:p["o"] + p["n"]] = True
voz[:cuerpo] = False      # el gancho y el título van más altos a propósito
sel = np.repeat((voz & cubierto)[:TOTAL], SR // FPS)[:N]
if sel.sum() > SR: print(f"en el cuerpo, donde suenan a la vez: voz {db(v[:N][sel]):.1f} dB RMS, música {db(mus[sel]) - db(v[:N][sel]):+.1f} dB respecto a la voz (objetivo: de -14 a -17)")
print("audio_final.wav listo (con música); el de sin música queda en audio_final_sin_musica.wav; entrada", m["input_i"], "LUFS")
