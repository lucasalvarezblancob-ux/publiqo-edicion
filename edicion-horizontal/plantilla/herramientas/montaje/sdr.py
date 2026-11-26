"""sdr.py [TOPE_SEG]: copias SDR (bt709) de los TROZOS de bruto HDR o LOG que usa el montaje (trabajo/video.json).

LOG (G009, 2026-11-26): los brutos en Log (DJI D-Log M, Apple Log, S-Log3…; comun.revelado()) se revelan aquí con el LUT
de su perfil (herramientas/luts/) a LUT_INTENSIDAD, igual que los HDR con libplacebo. Si cambia el LUT o la intensidad, las
copias de ese bruto se rehacen solas (trabajo/sdr/<clip>/receta.txt).

Por qué: ffmpeg no convierte HDR al leer, y los brutos de iPhone (HLG, 10 bits) salen pálidos y lavados. Convertir los
brutos ENTEROS (herramientas/proxy.sh) cuesta ~2 s por segundo de bruto en 4K: con una hora de brutos, horas. Aquí se
convierte solo lo que se ve (más 1 s de margen por cada lado), a los fps del proyecto, sin sonido:
    trabajo/sdr/<clip>/<a>_<b>.mp4      a y b = frames del proyecto contados sobre el bruto
Los demás pasos leen la imagen con comun.fuente(), que elige sola el original (bruto SDR) o la copia (bruto HDR). El sonido
sale siempre del original. Vale igual para los clips de archivo del creador (personal/<creador>/recursos/) que sean HDR.

Conversión: ffmpeg + libplacebo (el motor de mpv; nunca zscale+tonemap, que sale ~20 niveles más claro), x264 CRF 14 «veryfast»
(medido en 4K con hierba y grava: «fast» tarda 4,2 s por segundo de bruto y «veryfast» 1,75, con el mismo tamaño y calidad
de sobra para un intermedio: ~170 Mb/s).
Después, SIEMPRE, el color contra el bruto (preferencias → COLOR):
    herramientas/comparar_color.sh BRUTO trabajo/sdr/<clip>/<a>_<b>.mp4 "<t del bruto>" <a / FPS>

Uso (desde out/<slug>/, después de paso3_plan.py):
    sdr.py            hace todo lo que falta (paso4_render.py lo llama solo antes de montar los tramos)
    sdr.py 240        para a los ~240 s de reloj y sale con código 3 si queda algo; al relanzarlo sigue (equipos con poca
                      memoria o con límite de tiempo por orden)
    sdr.py lista      solo dice qué falta
Es reanudable y, si cambia el plan, solo hace los trozos nuevos. Las copias que ya no usa nadie no se borran solas."""
import math, os, subprocess, sys, time
from comun import FPS, LIBPLACEBO, TRABAJO, _cl, bruto, lut_efectivo, necesita_copia, receta, revelado, segmentos, video

MARGEN = FPS                 # 1 s por cada lado: los retoques pequeños del plan no obligan a convertir otra vez
TROZO = 45 * FPS             # una copia no pasa de ~45 s de bruto (salvo un plano acelerado más largo): cada ffmpeg dura poco
COLOR = ["-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]
HW = [["-hwaccel", "d3d11va"]] if os.name == "nt" else ([["-hwaccel", "videotoolbox"]] if sys.platform == "darwin" else [])
_dur = {}


def frames_bruto(clip):
    if clip not in _dur:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", bruto(clip)], capture_output=True, text=True).stdout.split()
        _dur[clip] = int(float(r[0]) * FPS) if r else 10 ** 9
    return _dur[clip]


def pendientes():
    """[(clip, a, b, lento)]: trozos por convertir. Cada plano del montaje queda ENTERO dentro de una sola copia."""
    nec = {}
    for v in video():
        if necesita_copia(v["clip"]): nec.setdefault(v["clip"], []).append((v["in"], v["in"] + math.ceil(v["n"] * v["speed"]) + 2, v["speed"]))
    out = []
    for clip, rs in nec.items():
        d = f"{TRABAJO}/sdr/{clip}"; rc = receta(clip)
        if os.path.isdir(d):
            ant = open(f"{d}/receta.txt", encoding="utf-8").read().strip() if os.path.exists(f"{d}/receta.txt") else "hdr"
            if ant != rc:                       # otro LUT u otra intensidad: las copias viejas ya no valen
                for f in os.listdir(d):
                    if f.endswith(".mp4"): os.remove(f"{d}/{f}")
        os.makedirs(d, exist_ok=True); open(f"{d}/receta.txt", "w", encoding="utf-8").write(rc + "\n")
        S = segmentos(clip, releer=True); p = None
        for a, b, sp in sorted(set(rs)):
            if any(x <= a and b <= y for x, y, _ in S): continue     # ya tiene copia: no hace falta ni el bruto
            tope = frames_bruto(clip)                                 # (si el bruto ya no está, el vídeo se rehace igual desde sus copias)
            if any(x <= a and min(b, tope) <= y for x, y, _ in S): continue
            a0, b0 = max(0, a - MARGEN), min(tope, b + MARGEN)
            if p and a0 <= p[2] + 2 * FPS and max(b0, p[2]) - p[1] <= TROZO: p[2] = max(p[2], b0); p[3] = p[3] or sp < 0.99
            else: p = [clip, a0, b0, sp < 0.99]; out.append(p)
    return [tuple(p) for p in out]


def hacer(clip, a, b, lento):
    """Convierte [a, b) del bruto. `lento` (algún plano a cámara lenta): conserva los fps del bruto para no repetir fotogramas."""
    d = f"{TRABAJO}/sdr/{clip}"; os.makedirs(d, exist_ok=True); o = f"{d}/{a}_{b}.mp4"
    rv = revelado(clip); log = rv["tipo"] == "log"
    conv = _cl.filtro(lut_efectivo(clip), None, rv["bits"] or 8, rv["matriz"] or "bt709", rv["rango"] or "tv") if log else LIBPLACEBO
    vf = ("" if lento else f"fps={FPS},") + conv; err = ""
    for hw in HW + [[]]:              # decodificación por la gráfica si se puede (más rápido, misma imagen); si falla, por programa
        r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *([] if log else ["-init_hw_device", "vulkan"]), *hw, "-ss", f"{a / FPS:.3f}", "-t", f"{(b - a) / FPS:.3f}", "-i", bruto(clip),
                            "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-g", str(FPS), *COLOR, "-f", "mp4", o + ".tmp"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode == 0 and os.path.getsize(o + ".tmp") > 1000: os.replace(o + ".tmp", o); return o
        err = r.stderr
    if "libplacebo" in err and "No such filter" in err: err += "\nEste ffmpeg no trae libplacebo: instala uno completo (Windows: winget install -e --id Gyan.FFmpeg) o convierte los brutos enteros con herramientas/proxy.sh."
    raise SystemExit(f"sdr: no he podido convertir {clip} {a}-{b}:\n{err[-1500:]}")


def asegurar(tope=0):
    """Hace las copias que falten. Devuelve cuántas quedan sin hacer (0 = todo listo)."""
    P = pendientes(); t0 = time.time(); total = sum(b - a for _, a, b, _ in P) / FPS
    if P: print(f"sdr: {len(P)} trozos de bruto HDR/Log por revelar ({total:.0f} s de bruto; ~2 s de espera por segundo en 4K)", flush=True)
    for i, (clip, a, b, lento) in enumerate(P):
        if tope and time.time() - t0 > tope: print(f"sdr: quedan {len(P) - i} trozos; relanza para seguir"); return len(P) - i
        t = time.time(); hacer(clip, a, b, lento); print(f"sdr {i + 1}/{len(P)} {clip} {a / FPS:.1f}-{b / FPS:.1f} s en {time.time() - t:.0f} s", flush=True)
    for clip in {p[0] for p in P}: segmentos(clip, releer=True)
    return 0


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "lista":
        P = pendientes()
        for clip, a, b, lento in P: print(f"{clip} {a / FPS:.1f}-{b / FPS:.1f} s" + (" (fps del bruto)" if lento else ""))
        print(len(P), "trozos,", f"{sum(b - a for _, a, b, _ in P) / FPS:.0f} s de bruto por convertir")
    else:
        if asegurar(float(arg) if arg else 0): sys.exit(3)
        print("sdr: todos los trozos HDR/Log del montaje tienen copia revelada. Comprueba el color de alguno: HDR con herramientas/comparar_color.sh, Log con herramientas/color_log.py comparar")
