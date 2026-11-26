"""Paso 0: prepara los brutos de un vídeo. Por cada bruto:
  1. ficha técnica (resolución, fps, duración, giro, HDR) -> avisa del lienzo y los fps que tocan;
  2. transcripción con tiempos por palabra (faster-whisper, local) -> ANALISIS/transcripcion/<clip>.json, .txt y .w.json;
     el IDIOMA se DETECTA (nunca se supone): si proyecto.py no lo fija, se imprime el detectado en cada bruto;
  3. posición de la cara 5 veces por segundo (para centrar los zooms) -> trabajo/caras_<clip>.json;
  4. hojas densas, un fotograma por segundo, para el REGISTRO VISUAL -> ANALISIS/visual/hojas/<clip>_NN.jpg.
Lo ya hecho no se repite. Uso: paso0_preparar.py [clip ...]   (sin argumentos: todos los brutos)

EN PARALELO, con el mismo resultado que bruto a bruto (cada bruto lo procesa el mismo programa con los mismos ajustes;
solo cambia cuántos van a la vez). Dos colas que trabajan al mismo tiempo, los brutos más largos primero:
  - el SONIDO (transcripción): con gráfica NVIDIA, de uno en uno (la gráfica ya va llena); sin ella (Mac, o PC sin
    NVIDIA), de dos en dos si hay 10 núcleos o más, porque cada Whisper en procesador usa solo 4 hilos;
  - la IMAGEN (caras + hojas): varios brutos a la vez según la memoria (2 con menos de 24 GB, 3 hasta 48, 4 con más) y
    los núcleos (uno por cada 4).
Para fijarlo a mano: PASO0_WHISPER=N y PASO0_HILOS=N (con 1 y 1, como antes: uno detrás de otro).
Medido el 2026-11-17 (i7-13700HX + RTX 4060, 16 GB; 6 brutos 4K de iPhone, 17 min): 651 s bruto a bruto -> 420 s (-35 %),
con transcripciones, caras y hojas idénticas byte a byte. En Mac debería ganarse más (allí la transcripción va por procesador, de dos en dos): SIN MEDIR todavía."""
import json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from comun import ALTO, ANALISIS, ANCHO, AQUI, BRUTOS, FPS, IDIOMA, PY, TRABAJO, TRANSCRIPCIONES, _cl, bruto, clips, revelado
from vigilar_render import memoria

H = os.path.dirname(AQUI)   # herramientas/
HOJAS = f"{ANALISIS}/visual/hojas"
os.makedirs(TRANSCRIPCIONES, exist_ok=True); os.makedirs(HOJAS, exist_ok=True)
lista = sys.argv[1:] or clips()
if not lista: raise SystemExit(f"No hay brutos en {BRUTOS}")
t0 = time.time()

# 1. Ficha técnica (rápida): en orden, para que la tabla salga entera y ordenada
durs = {}; LOGS = []
print(f"{'clip':14} {'tamaño':>11} {'fps':>6} {'dur':>8}  notas")
for c in lista:
    f = bruto(c)
    s = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate,color_transfer:stream_side_data=rotation:format=duration", "-of", "json", f], capture_output=True, text=True).stdout)
    st = s["streams"][0]; a, b = st["r_frame_rate"].split("/"); fps = float(a) / float(b); dur = float(s["format"]["duration"]); durs[c] = dur
    rot = next((abs(int(float(x["rotation"]))) for x in st.get("side_data_list", []) if "rotation" in x), 0)
    w, h = (st["height"], st["width"]) if rot in (90, 270) else (st["width"], st["height"])
    notas = []
    if st.get("color_transfer") in ("arib-std-b67", "smpte2084"): notas.append("HDR: no hace falta proxy del bruto entero; tras paso3_plan.py, sdr.py convierte a SDR solo los trozos que se usan (comprueba el color de alguno con comparar_color.sh)")
    rv = revelado(c)                                  # G009: ¿grabado en LOG? → se revela con su LUT (sin él sale gris)
    if rv["tipo"] == "log":
        notas.append(f"LOG {_cl.PERFILES[rv['perfil']][0]} ({rv['seguro']}): " + (f"se revela con {os.path.basename(rv['lut'])}" if rv["lut"] else f"FALTA SU LUT → {_cl.PAGINAS.get(rv['perfil'])}")
                     + (" · MIRA el antes/después: color_log.py comparar" if rv["seguro"] == "probable" else ""))
        LOGS.append((c, rv))
    if h > w: notas.append("VERTICAL (irá con bordes o recortado)")
    if abs(fps - FPS) > 0.5: notas.append(f"fps distintos del proyecto ({FPS})")
    if (w, h) != (ANCHO, ALTO): notas.append(f"tamaño distinto del lienzo ({ANCHO}x{ALTO})")
    print(f"{c:14} {w:>5}x{h:<5} {fps:6.2f} {dur:7.1f}s  {'; '.join(notas)}", flush=True)

if LOGS:
    falta = sorted({_cl.PERFILES[r["perfil"]][0] for _, r in LOGS if not r["lut"]})
    print(f"\nLOG (G009): {len(LOGS)} brutos en Log → se revelan solos con su LUT en sdr.py (como los HDR)."
          + (f" AVISO LOG: falta el LUT de {', '.join(falta)}: bájalo a herramientas/luts/ antes de montar (color_log.py luts)." if falta else "")
          + (" AVISO LOG: hay «probables» (solo por la imagen): saca un antes/después y, si no es Log, LOG_CLIPS = {'clip': None} en proyecto.py." if any(r["seguro"] == "probable" for _, r in LOGS) else ""), flush=True)

# 2. Cuántos a la vez (no cambia el resultado, solo el tiempo)
nuc = os.cpu_count() or 4
_, total = memoria()
nvidia = bool(shutil.which("nvidia-smi")) and subprocess.run(["nvidia-smi", "-L"], capture_output=True).returncode == 0
N_SON = int(os.environ.get("PASO0_WHISPER") or (1 if nvidia else 2 if nuc >= 10 and total >= 12 else 1))
N_IMG = int(os.environ.get("PASO0_HILOS") or max(1, min(nuc // 4, 2 if total < 24 else 3 if total < 48 else 4)))
largos = sorted(lista, key=lambda c: -durs[c])      # los largos primero: así ninguno se queda solo al final
print(f"\nEn paralelo: transcripción de {N_SON} en {N_SON} ({'gráfica NVIDIA' if nvidia else 'procesador'}), "
      f"imagen (caras + hojas) de {N_IMG} en {N_IMG} ({nuc} núcleos, {total:.0f} GB)", flush=True)


def sonido(c):
    j = f"{TRANSCRIPCIONES}/{c}.json"
    if not os.path.exists(j):
        subprocess.run([PY, f"{H}/transcribir.py", bruto(c), j, "--idioma", IDIOMA or "auto"], check=True, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    d = json.load(open(j, encoding="utf-8"))
    wj = f"{TRANSCRIPCIONES}/{c}.w.json"
    if not os.path.exists(wj) or os.path.getmtime(wj) < os.path.getmtime(j):
        json.dump([p for fr in d["frases"] for p in fr["palabras"]], open(wj, "w", encoding="utf-8"), ensure_ascii=False)
    return d.get("idioma")


def imagen(c):
    cj = f"{TRABAJO}/caras_{c}.json"
    if not os.path.exists(cj): subprocess.run([PY, f"{H}/caras.py", bruto(c), cj], check=True)
    subprocess.run([PY, f"{H}/hojas_bruto.py", bruto(c), HOJAS], check=True)


with ThreadPoolExecutor(N_SON) as ps, ThreadPoolExecutor(N_IMG) as pi:
    fs = {c: ps.submit(sonido, c) for c in largos}
    fi = [pi.submit(imagen, c) for c in largos]
    errores = [e for e in (x.exception() for x in [*fs.values(), *fi]) if e]
if errores: raise SystemExit(f"paso0: {len(errores)} fallo(s); lo ya hecho se conserva, relanza para seguir. Primero: {errores[0]}")
idiomas = {c: fs[c].result() for c in lista}

print(f"\nIdioma detectado por bruto: {idiomas}   ({time.time() - t0:.0f} s)")
if not IDIOMA:
    print("-> Pon IDIOMA en proyecto.py con el idioma HABLADO (mira los .txt: si un bruto corto sale en otro idioma, suele ser un error de detección:")
    print("   bórrale el .json y relanza con IDIOMA fijado). Rótulos, título y descripción van en ese idioma.")
print(f"Siguiente: REGISTRO VISUAL de cada bruto (qué se ve en cada momento) con {HOJAS} y herramientas/montaje/ENCARGO_REGISTRO_VISUAL.md;")
print("luego escribe edl.py leyendo los .txt de la transcripción.")
