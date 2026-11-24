"""detras.py: TEXTO POR DETRÁS DE LA PERSONA (Nil OGT: el «24%» que se tumba detrás de la mano, las estrellas Michelin y
las franjas de vídeo por detrás de él). Desde out/<slug>/, después de paso3_plan.py y antes de paso4_render.py tramos.

En plan.py:  DETRAS = [(ancla, segundos), ...]   tramos del montaje en los que la PERSONA va por encima de los gráficos
             (los gráficos de ese momento —GOLPES, DATOS, CONTADORES, PROPIOS…— se piden como siempre).
Qué hace: recorta a la persona fotograma a fotograma desde el bruto (rembg u2net_human_seg, la máscara a media
resolución y suavizada) y la guarda con alfa en trabajo/detras/p<o>_<f0>.mov + .json. paso4_render.py le aplica el MISMO
zoom y encuadre que al plano y la pone encima de las capas solo en esos fotogramas: el texto queda detrás de ella.
  detras.py           -> recorta lo que falte (reanudable; ~0,3 s por fotograma en CPU)
  detras.py hoja      -> trabajo/detras/hoja_N.jpg: la máscara sobre el plano cada 3 fotogramas. MIRARLAS: pelo, manos.
Sin DETRAS en plan.py no hace nada y el montaje sale como siempre. Si cambias el plan, borra trabajo/detras."""
import json, os, subprocess, sys, tempfile
import numpy as np, cv2
from comun import FPS, TRABAJO, Linea, bruto, fuente
import plan

D = f"{TRABAJO}/detras"; os.makedirs(D, exist_ok=True)
TRAMOS = getattr(plan, "DETRAS", [])
if not TRAMOS: print("Sin DETRAS en plan.py: nada que hacer."); sys.exit(0)
V = json.load(open(f"{TRABAJO}/video.json")); L = Linea()
planos = [v for tr in V["tramos"] for v in tr]


def trozos():
    """(plano, f0, f1) de montaje para cada tramo DETRAS, partido por planos (solo planos del bruto, no recursos fijos)."""
    for a, d in TRAMOS:
        g0 = L.ancla(a); g1 = g0 + int(round(d * FPS))
        for v in planos:
            a0, a1 = max(g0, v["o"]), min(g1, v["o"] + v["n"])
            if a0 < a1: yield v, a0, a1


def recortar(v, f0, f1):
    base = f"{D}/p{v['o']}_{f0}"
    if os.path.exists(base + ".json"): return
    from rembg import new_session, remove
    ses = new_session("u2net_human_seg")
    t = (v["in"] + (f0 - v["o"]) * v["speed"]) / FPS; n = f1 - f0
    ent, pre = fuente(v["clip"], t, n * v["speed"] / FPS, exigir=True)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["ffmpeg", "-v", "error", "-y", *ent, "-vf", (pre or "") + f"setpts=(PTS-STARTPTS)/{v['speed']},fps={FPS}",
                        "-frames:v", str(n), f"{tmp}/f%05d.png"], check=True)
        fs = sorted(x for x in os.listdir(tmp) if x.startswith("f"))
        for k, nm in enumerate(fs):
            img = cv2.imread(f"{tmp}/{nm}"); h, w = img.shape[:2]
            peq = cv2.resize(img, (960, int(960 * h / w)))
            m = np.array(remove(cv2.cvtColor(peq, cv2.COLOR_BGR2RGB), session=ses, only_mask=True))
            m = cv2.GaussianBlur(cv2.resize(m, (w, h), interpolation=cv2.INTER_LINEAR), (0, 0), max(1.5, w / 1600))
            cv2.imwrite(f"{tmp}/r{k:05d}.png", np.dstack([img, m]))
            print(f"\r  p{v['o']}: {k + 1}/{len(fs)}", end="", flush=True)
        print()
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{tmp}/r%05d.png", "-c:v", "prores_ks",
                        "-profile:v", "4444", "-pix_fmt", "yuva444p10le", base + ".mov"], check=True)
    json.dump({"o": v["o"], "f0": f0, "f1": f1, "clip": v["clip"]}, open(base + ".json", "w"))


def hoja():
    for i, (v, f0, f1) in enumerate(trozos()):
        base = f"{D}/p{v['o']}_{f0}"
        if not os.path.exists(base + ".mov"): continue
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", base + ".mov", "-vf", "select='not(mod(n\\,3))',scale=480:-2",
                            "-fps_mode", "vfr", "-pix_fmt", "rgba", f"{tmp}/h%04d.png"], check=True)
            cel = []
            for nm in sorted(os.listdir(tmp)):
                im = cv2.imread(f"{tmp}/{nm}", cv2.IMREAD_UNCHANGED); a = im[:, :, 3:4] / 255.0
                fondo = np.zeros_like(im[:, :, :3]); fondo[:] = (180, 60, 220)          # magenta: lo que NO es persona
                cel.append((im[:, :, :3] * a + fondo * (1 - a)).astype(np.uint8))
            if cel:
                filas = [np.hstack(cel[k:k + 6] + [np.zeros_like(cel[0])] * (6 - len(cel[k:k + 6]))) for k in range(0, len(cel), 6)]
                cv2.imwrite(f"{D}/hoja_{i}.jpg", np.vstack(filas)); print(f"{D}/hoja_{i}.jpg")


if len(sys.argv) > 1 and sys.argv[1] == "hoja": hoja()
else:
    for v, f0, f1 in trozos():
        if v.get("b"): print(f"AVISO: {f0}-{f1} cae en un recurso ({v['clip']}): se recorta igual; si no sale nadie, quítalo de DETRAS");
        recortar(v, f0, f1)
    print("Hecho. Mira las hojas: detras.py hoja")
