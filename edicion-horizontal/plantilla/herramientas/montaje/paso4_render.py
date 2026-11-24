"""Paso 4: render HÍBRIDO de vídeo largo (medido el 2026-11-11: x2,7 la duración frente a x14 de hacerlo todo en Remotion).
  capas   Remotion renderiza SOLO los rangos con gráfico, en ProRes 4444 con alfa (remotion.capas.config.ts);
  tramos  ffmpeg monta cada tramo (~24 s) desde los BRUTOS: corte, escala/zoom, concat y la capa encima;
  unir    concat sin recodificar + audio final -> el .mp4 (bt709 etiquetado, faststart).
Uso:  paso4_render.py capas [TOPE_SEG]     con TOPE_SEG no empieza otro rango pasados esos segundos y sale con código 3
                                           si quedan (equipos con poca memoria o con límite de tiempo por orden): relánzalo
      paso4_render.py tramos [auto|nvenc|x264|videotoolbox] [en_paralelo=2] [ids de tramo ...]
      paso4_render.py unir ../AAAA-MM-DD_<slug>.mp4
Reanudable: lo que ya existe no se repite. Si cambias el plan, borra trabajo/tramos (y trabajo/capas si cambian los
gráficos o sus rangos). El color del bruto no se toca: sin filtros de color, salida bt709 limitada (la única excepción es
un fail pedido en FALLOS, que va en blanco y negro).
Brutos HDR (iPhone): `tramos` hace antes, solo, la copia SDR de los trozos que se usan (sdr.py)."""
import glob, json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from comun import COMP, ESTUDIO, FPS, SLUG, TRABAJO, fuente
from dinamica import filtro_zoom

V = json.load(open(f"{TRABAJO}/video.json")); OUT = os.path.abspath(TRABAJO)
os.makedirs(f"{TRABAJO}/capas", exist_ok=True); os.makedirs(f"{TRABAJO}/tramos", exist_ok=True)
G = str(2 * FPS)
ENC = {"x264": ["-c:v", "libx264", "-preset", "fast", "-crf", "19", "-x264-params", "open-gop=0", "-g", G],
       "nvenc": ["-c:v", "h264_nvenc", "-preset", "p6", "-tune", "hq", "-rc", "constqp", "-qp", "21", "-g", G, "-bf", "2", "-profile:v", "high"],
       "videotoolbox": ["-c:v", "h264_videotoolbox", "-q:v", "65", "-g", G, "-profile:v", "high"]}   # macOS; sin probar por Lucas: compara un tramo con x264
COLOR = ["-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]
GL = ["--gl=angle"] if os.name == "nt" else []
# Navegadores a la vez al pintar las capas. 6 con 16 GB libres; si el sistema se queda sin memoria (el render se para o
# lo mata el sistema), relánzalo con menos: CAPAS_HILOS=3 PY paso4_render.py capas (es reanudable: no repite lo hecho).
HILOS = int(os.environ.get("CAPAS_HILOS", "6"))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(errors="replace")      # la salida de Remotion trae caracteres que la consola de Windows no sabe escribir
NPX = shutil.which("npx") or "npx"     # en Windows es npx.cmd: se llama por su ruta, sin pasar por la shell


def codificador():
    """nvenc si la gráfica y el controlador lo aguantan (se prueba de verdad con 5 frames); si no, x264."""
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=1280x720:r=25", "-frames:v", "5", *ENC["nvenc"], "-f", "null", "-"], capture_output=True)
    return "nvenc" if r.returncode == 0 else "x264"


def capas(tope=0):
    t = time.time()
    if not V["rangos"]: print("sin gráficos"); return
    faltan = [(a, b) for a, b in V["rangos"] if not os.path.exists(f"{OUT}/capas/c{a}.mov")]
    if not faltan: print("capas: ya están todas"); return          # rehacer solo tramos (un difuminado, un recurso) no necesita Remotion ni Node
    if not shutil.which("npx"): sys.exit(f"Faltan {len(faltan)} capas gráficas y no encuentro Node (npx): Remotion no puede dibujarlas. Instala Node (LEEME.md) y repite; lo ya hecho se conserva.")
    subprocess.run([NPX, "remotion", "bundle", f"--out-dir=build-{SLUG}"], cwd=ESTUDIO, check=True, capture_output=True)
    for a, b in V["rangos"]:
        o = f"{OUT}/capas/c{a}.mov"
        if os.path.exists(o): continue
        if tope and time.time() - t > tope:
            n = sum(not os.path.exists(f"{OUT}/capas/c{x}.mov") for x, _ in V["rangos"]); print(f"capas: quedan {n} rangos; relanza para seguir"); sys.exit(3)
        r = subprocess.run([NPX, "remotion", "render", f"build-{SLUG}", COMP, o + ".tmp.mov", "--config=remotion.capas.config.ts", f"--frames={a}-{b - 1}", *GL, f"--concurrency={HILOS}"], cwd=ESTUDIO, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode: print(r.stdout[-1500:], r.stderr[-1500:]); sys.exit(1)
        os.replace(o + ".tmp.mov", o); print(f"capa {a}-{b} lista ({time.time() - t:.0f} s)", flush=True)
    print(f"capas: {time.time() - t:.0f} s")


def tramo(i, enc):
    tr = V["tramos"][i]; o = f"{TRABAJO}/tramos/t{i:03d}.mp4"
    if os.path.exists(o): return 0
    T0 = tr[0]["o"]; T1 = tr[-1]["o"] + tr[-1]["n"]; cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y"]; fc = []
    parches = []       # parches con alfa encima del bruto, ANTES del zoom: resaltes (foco.py) y matrículas difuminadas (tapar.py)
    for j, v in enumerate(tr):
        ent, _ = fuente(v["clip"], v["in"] / FPS, v["n"] * v["speed"] / FPS, exigir=True)      # bruto SDR: el original; HDR: su copia SDR (sdr.py)
        cmd += [*ent[:-2], "-t", f"{v['n'] * v['speed'] / FPS + 0.5:.3f}", *ent[-2:]]
        f = f"[{j}:v]setpts=(PTS-STARTPTS)/{v['speed']},fps={FPS},"
        for q, d in enumerate(("foco", "tapado")):      # resalte (foco.py) y, encima, la matrícula difuminada (tapar.py)
            pj = f"{TRABAJO}/{d}/p{v['o']}"
            if not os.path.exists(pj + ".json"): continue
            P = json.load(open(pj + ".json")); m = len(tr) + len(parches); parches.append(pj + ".mov")
            f = (f"[{m}:v]setpts=PTS-STARTPTS,scale=out_color_matrix=bt709:out_range=limited,format=yuva420p[p{j}_{q}];" + f[:-1] +
                 f"[r{j}_{q}];[r{j}_{q}][p{j}_{q}]overlay=x={P['x']}:y={P['y']}:eof_action=pass,")
        if v.get("bn"): f += "hue=s=0,"      # fail (FALLOS en plan.py): blanco y negro solo en ese tramo
        f += filtro_zoom(v)
        f += f"tpad=stop_mode=clone:stop_duration=1,trim=end_frame={v['n']},setpts=PTS-STARTPTS,setsar=1,format=yuv420p[v{j}]"; fc.append(f)
    for p in parches: cmd += ["-i", p]
    fc.append("".join(f"[v{j}]" for j in range(len(tr))) + f"concat=n={len(tr)}:v=1:a=0[b0]"); n = len(tr) + len(parches); k = 0
    for a, b in V["rangos"]:
        if a >= T0 and b <= T1:
            cmd += ["-i", f"{TRABAJO}/capas/c{a}.mov"]
            fc.append(f"[{n}:v]setpts=PTS-STARTPTS+{(a - T0) / FPS:.3f}/TB[g{k}];[b{k}][g{k}]overlay=enable='between(n,{a - T0},{b - T0 - 1})':eof_action=pass[b{k + 1}]"); n += 1; k += 1
        else: assert b <= T0 or a >= T1, f"gráfico {a}-{b} partido por el tramo {i}"
    # persona por ENCIMA de los gráficos (detras.py, DETRAS en plan.py): el recorte con alfa lleva el mismo zoom y encuadre
    # que su plano (filtro_zoom con el tiempo del plano) y se pone solo en sus fotogramas. Sin trabajo/detras, nada.
    for v in tr:
        for pj in sorted(glob.glob(f"{TRABAJO}/detras/p{v['o']}_*.json")):
            P = json.load(open(pj)); cmd += ["-i", pj[:-5] + ".mov"]
            fc.append(f"[{n}:v]setpts=PTS-STARTPTS+{(P['f0'] - v['o']) / FPS:.4f}/TB,format=rgba," + filtro_zoom(v) +
                      f"setpts=PTS+{(v['o'] - T0) / FPS:.4f}/TB,format=yuva420p[d{k}];[b{k}][d{k}]overlay=enable='between(n,{P['f0'] - T0},{P['f1'] - T0 - 1})':eof_action=pass[b{k + 1}]")
            n += 1; k += 1
    fc.append(f"[b{k}]format=yuv420p[out]")
    open(f"{TRABAJO}/tramos/t{i:03d}.fc", "w").write(";\n".join(fc))     # el filtro va en un archivo: en Windows no cabe en la línea de órdenes
    cmd += ["-/filter_complex", f"{TRABAJO}/tramos/t{i:03d}.fc", "-map", "[out]", "-frames:v", str(T1 - T0), *ENC[enc], *COLOR, "-an", o + ".tmp.mp4"]
    t = time.time(); r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode: print("TRAMO", i, r.stderr[-2000:]); return -1
    os.replace(o + ".tmp.mp4", o); d = time.time() - t; print(f"tramo {i} ({(T1 - T0) / FPS:.0f} s de vídeo) en {d:.0f} s", flush=True); return d


orden = sys.argv[1] if len(sys.argv) > 1 else ""
if orden == "capas": capas(float(sys.argv[2]) if len(sys.argv) > 2 else 0)
elif orden == "tramos":
    enc = sys.argv[2] if len(sys.argv) > 2 else "auto"; par = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    if enc == "auto": enc = codificador()
    import sdr
    if sdr.asegurar(): sys.exit(3)                 # brutos HDR: antes de montar, la copia SDR de cada trozo que se usa
    ids = [int(x) for x in sys.argv[4:]] or range(len(V["tramos"])); t = time.time()
    with ThreadPoolExecutor(par) as ex: res = list(ex.map(lambda i: tramo(i, enc), ids))
    print(f"tramos ({enc}): {time.time() - t:.0f} s; fallos: {[i for i, r in zip(ids, res) if r == -1]}")
elif orden == "unir":
    salida = sys.argv[2]; faltan = [i for i in range(len(V["tramos"])) if not os.path.exists(f"{TRABAJO}/tramos/t{i:03d}.mp4")]
    if faltan: raise SystemExit(f"faltan tramos: {faltan}")
    open(f"{TRABAJO}/lista.txt", "w").write("".join(f"file 'tramos/t{i:03d}.mp4'\n" for i in range(len(V["tramos"]))))
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TRABAJO}/lista.txt", "-i", f"{TRABAJO}/audio_final.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1", "-c:a", "aac", "-b:a", "320k",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", salida], check=True)
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=nb_frames,width,height", "-of", "default=nw=1", salida], capture_output=True, text=True).stdout
    print(salida, " ".join(r.split()), f"(esperados {V['total']} frames)")
else: print(__doc__)
