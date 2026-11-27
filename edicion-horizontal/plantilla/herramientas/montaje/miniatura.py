"""miniatura.py: las imágenes de referencia para las miniaturas (se ejecuta desde out/<slug>/; salida en youtube/).
Claude no dibuja la miniatura: entrega el PROMPT y la IMAGEN que hay que adjuntarle (un fotograma del vídeo o una foto
del creador). Reglas y método en <skill>/base/titulos-miniaturas.md.

    miniatura.py momentos [cada_s]         hojas con un fotograma del montaje cada N s (4 por defecto), con su mm:ss
                                           -> youtube/momentos_NN.jpg. Para ELEGIR MIRANDO, junto al registro visual.
    miniatura.py sacar A 4:18.2 B 12:03    por cada letra, ráfaga de ±0,5 s alrededor del momento, sacada del BRUTO a
                                           tamaño completo: sin rótulos, sin zoom y sin recorte. Se queda el fotograma
                                           más nítido -> youtube/A.jpg, y la ráfaga numerada -> youtube/A_rafaga.jpg
                                           (mírala: ojos abiertos, gesto, sin desenfoque de movimiento).
                                           Momento = mm:ss(.d) o nº de frame del MONTAJE, o CLIP@segundos del bruto
                                           (un momento que no entró en el vídeo). A=7 fuerza el nº 7 de la ráfaga.
                                           Segunda referencia de la misma pareja (la cara, si la primera es el animal): A2.
                                           Molde único (G010): A = el retrato de frente del creador, para las cinco.
    miniatura.py foto C <ruta>             usa una foto (del creador, de personal/<creador>/recursos/) como referencia C.
    miniatura.py fotos                     lista las fotos del creador que hay (recursos/creador y recursos/fotos).
    miniatura.py hoja                      youtube/hoja.jpg: cada referencia a tamaño de miniatura grande y a 168 px
                                           (como se ve en el móvil y en la columna de sugeridos). Lo que no se entiende
                                           a 168 px no sirve de base.
    miniatura.py cara A2 [imagen]          recorte GRANDE de la cara (la más grande que encuentre) de youtube/A2.jpg o de
                                           la imagen dada -> youtube/A2_cara.jpg (cuadrado, ≥ 1024 px). Se adjunta SIEMPRE
                                           como referencia de identidad de la persona (titulos-miniaturas.md -> la cara, fiel).
    miniatura.py final A <imagen> [B …]    cuando vuelven las miniaturas ya generadas: recorte centrado a 16:9,
                                           1920x1080, JPG de menos de 2 MB -> youtube/miniatura_A.jpg, y youtube/prueba.jpg
                                           con cada una a 168 px para comprobarlas antes de subirlas. Y youtube/caras.jpg:
                                           la cara de cada miniatura al lado de la de su referencia (A_cara, A2, A; si la letra
                                           no tiene, la de A: con el molde único la misma cara vale para las cinco): si no
                                           es la misma persona, se rehace en un chat nuevo."""
import glob, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
import numpy as np, cv2
from comun import FPS, RECURSOS, TRABAJO, bruto, video, fuente

SAL = "youtube"; os.makedirs(SAL, exist_ok=True)
FF = ["ffmpeg", "-nostdin", "-v", "error", "-y"]
IMG = (".jpg", ".jpeg", ".png", ".webp")


def fmt(s): return f"{int(s) // 60}:{int(s) % 60:02d}"


def a_frame(m):
    """mm:ss(.d) o nº de frame del montaje -> frame del montaje."""
    return round((int(m.split(":")[0]) * 60 + float(m.split(":")[1])) * FPS) if ":" in m else int(m)


def origen(m):
    """Momento -> (clip, segundos del bruto). Acepta CLIP@segundos o un punto del montaje."""
    if "@" in m:
        c, t = m.split("@"); return c, float(t)
    F_ = a_frame(m); V = video()
    v = next((v for v in V if v["o"] <= F_ < v["o"] + v["n"]), None)
    if v is None: raise SystemExit(f"{m}: fuera del montaje (dura {fmt(V[-1]['o'] / FPS)})")
    return v["clip"], (v["in"] + (F_ - v["o"]) * v["speed"]) / FPS


def leer(ruta): return cv2.imdecode(np.fromfile(ruta, np.uint8), cv2.IMREAD_COLOR)
def guardar(ruta, im, q=92): cv2.imencode(".jpg", im, [cv2.IMWRITE_JPEG_QUALITY, q])[1].tofile(ruta)


def rotulo(im, txt, color=(80, 240, 240)):
    cv2.rectangle(im, (0, 0), (14 + 13 * len(txt), 28), (0, 0, 0), -1); cv2.putText(im, txt, (6, 21), cv2.FONT_HERSHEY_SIMPLEX, 0.62, color, 2); return im


def momentos(cada):
    V = video(); total = (V[-1]["o"] + V[-1]["n"]) / FPS; w, h, cols, filas = 384, 216, 6, 6

    def uno(s):
        c, t = origen(str(round(s * FPS)))
        ent, pre = fuente(c, t)
        raw = subprocess.run([*FF[:-1], *ent, "-frames:v", "1", "-vf", f"{pre}scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2", "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
        return rotulo(np.frombuffer(raw, np.uint8).reshape(h, w, 3).copy(), fmt(s)) if len(raw) >= w * h * 3 else None
    for v in V: bruto(v["clip"])                                                                    # resuelve las rutas antes de repartir
    with ThreadPoolExecutor(4) as ex: ims = [i for i in ex.map(uno, np.arange(cada / 2, total, cada)) if i is not None]
    for f in glob.glob(f"{SAL}/momentos_*.jpg"): os.remove(f)
    for k in range(0, len(ims), cols * filas):
        p = ims[k:k + cols * filas]
        while len(p) % cols: p.append(np.zeros_like(ims[0]))
        guardar(f"{SAL}/momentos_{k // (cols * filas) + 1:02d}.jpg", np.vstack([np.hstack(p[j:j + cols]) for j in range(0, len(p), cols)]), 80)
    print(len(ims), "fotogramas (uno cada", cada, "s) ->", f"{SAL}/momentos_NN.jpg ·", (len(ims) + cols * filas - 1) // (cols * filas), "hojas. La hora es la del MONTAJE: úsala tal cual en «sacar».")


def nitidez(im):
    g = cv2.cvtColor(cv2.resize(im, (960, 540)), cv2.COLOR_BGR2GRAY); h, w = g.shape
    return float(cv2.Laplacian(g[h // 8:h * 7 // 8, w // 8:w * 7 // 8], cv2.CV_64F).var())      # el centro: ahí está el sujeto


def sacar(letra, m):
    forzar = None
    if "=" in letra: letra, forzar = letra.split("="); forzar = int(forzar)
    c, t = origen(m); n = 13; t0 = max(0, t - 6 / FPS); ent, pre = fuente(c, t0, n / FPS)
    with tempfile.TemporaryDirectory() as d:
        subprocess.run([*FF, *ent, *(["-vf", pre[:-1]] if pre else []), "-frames:v", str(n), "-q:v", "1", "-qmin", "1", f"{d}/f%02d.jpg"], check=True)
        fs = sorted(glob.glob(f"{d}/f*.jpg"))
        if not fs: raise SystemExit(f"{letra}: no sale ningún fotograma de {c} en {t:.2f} s")
        ims = [leer(f) for f in fs]; nit = [nitidez(i) for i in ims]
        k = (forzar - 1) if forzar else int(np.argmax(nit))
        if not 0 <= k < len(ims): raise SystemExit(f"{letra}: la ráfaga tiene {len(ims)} fotogramas")
        shutil.copyfile(fs[k], f"{SAL}/{letra}.jpg")
        mini = []
        for i, im in enumerate(ims):
            x = cv2.resize(im, (480, round(480 * im.shape[0] / im.shape[1])))
            rotulo(x, f"{i + 1}  nit {nit[i]:.0f}", (90, 240, 90) if i == k else (80, 240, 240))
            if i == k: cv2.rectangle(x, (2, 2), (x.shape[1] - 3, x.shape[0] - 3), (90, 240, 90), 5)
            mini.append(x)
        while len(mini) % 5: mini.append(np.zeros_like(mini[0]))
        guardar(f"{SAL}/{letra}_rafaga.jpg", np.vstack([np.hstack(mini[j:j + 5]) for j in range(0, len(mini), 5)]), 82)
    h, w = ims[k].shape[:2]
    print(f"{letra}: {c} {t0 + k / FPS:.2f} s del bruto · fotograma {k + 1}/{len(ims)}{' (forzado)' if forzar else ' (el más nítido)'} · {w}x{h} -> {SAL}/{letra}.jpg  (ráfaga: {SAL}/{letra}_rafaga.jpg)")


def foto(letra, ruta):
    if not os.path.exists(ruta): raise SystemExit(f"No existe {ruta}")
    im = leer(ruta)
    if im is None: raise SystemExit(f"No puedo leer {ruta}")
    guardar(f"{SAL}/{letra}.jpg", im, 95); print(f"{letra}: foto {ruta} · {im.shape[1]}x{im.shape[0]} -> {SAL}/{letra}.jpg")


def fotos():
    if not RECURSOS: raise SystemExit("Este vídeo no tiene creador (CREADOR en proyecto.py).")
    fs = [f.replace("\\", "/") for c in ("creador", "fotos") for f in sorted(glob.glob(f"{glob.escape(RECURSOS)}/{c}/**/*", recursive=True)) if f.lower().endswith(IMG)]
    print("\n".join(fs) if fs else f"No hay fotos en {RECURSOS}/creador ni en {RECURSOS}/fotos: pídele al creador 3 o 4 (de frente, buena luz, gestos distintos) y guárdalas en recursos/creador/.")


def a_169(im, W, H):
    """Recorte centrado a 16:9 y cambio de tamaño (ChatGPT suele devolver 3:2: sobra arriba y abajo)."""
    ih, iw = im.shape[:2]; e = max(W / iw, H / ih)
    g = cv2.resize(im, (round(iw * e), round(ih * e)), interpolation=cv2.INTER_AREA if e < 1 else cv2.INTER_LANCZOS4)
    y, x = (g.shape[0] - H) // 2, (g.shape[1] - W) // 2; return g[y:y + H, x:x + W].copy()


def comparar(pares, sal):
    """Hoja con cada imagen a 640 px y a 168 px (como sale en el móvil y en la columna de sugeridos)."""
    W, H, w, h = 640, 360, 168, 94; filas = []
    for nombre, f in pares:
        g = a_169(leer(f), W, H); p = cv2.resize(g, (w, h), interpolation=cv2.INTER_AREA); fila = np.full((H, W + w + 30, 3), 24, np.uint8)
        fila[H - h - 10:H - 10, W + 15:W + 15 + w] = p; fila[:, :W] = rotulo(g, nombre, (90, 240, 90))
        cv2.putText(fila, "168 px", (W + 15, H - h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1); filas.append(fila)
    while len(filas) % 2: filas.append(np.full_like(filas[0], 24))
    guardar(sal, np.vstack([np.hstack(filas[j:j + 2]) for j in range(0, len(filas), 2)]), 88)


def hoja():
    refs = sorted(f for f in glob.glob(f"{SAL}/*.jpg") if re.fullmatch(r"[A-Z]\d?\.jpg", os.path.basename(f)))   # A.jpg, A2.jpg, B.jpg…
    if not refs: raise SystemExit("Aún no hay referencias: usa «sacar» o «foto».")
    comparar([(os.path.basename(f)[:-4], f) for f in refs], f"{SAL}/hoja.jpg"); print(len(refs), "referencias ->", f"{SAL}/hoja.jpg")


_DET = None
def caras_en(im):
    """Caras (x, y, w, h) de la imagen, de mayor a menor, con el detector de caras.py (YuNet, herramientas/modelos/)."""
    global _DET
    if _DET is None: _DET = cv2.FaceDetectorYN.create(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "modelos", "face_detection_yunet_2023mar.onnx"), "", (320, 320), 0.8, 0.3, 50)
    h, w = im.shape[:2]; k = min(1.0, 1600 / max(h, w)); g = cv2.resize(im, (round(w * k), round(h * k))) if k < 1 else im
    _DET.setInputSize((g.shape[1], g.shape[0])); _, f = _DET.detect(g)
    return sorted([tuple(int(v / k) for v in r[:4]) for r in (f if f is not None else [])], key=lambda r: -r[2] * r[3])


def recorte_cara(im, r, lado=1024):
    x, y, w, h = r; c = (x + w / 2, y + h / 2); L = int(max(w, h) * 2.2); x0, y0 = int(c[0] - L / 2), int(c[1] - L * 0.45)
    pad = cv2.copyMakeBorder(im, L, L, L, L, cv2.BORDER_REPLICATE); q = pad[y0 + L:y0 + 2 * L, x0 + L:x0 + 2 * L]
    return cv2.resize(q, (lado, lado), interpolation=cv2.INTER_LANCZOS4 if L < lado else cv2.INTER_AREA)


def cara(letra, ruta=None):
    """Lucas, 2026-11-17 (alimentacion): «en la miniatura B le ha cambiado la cara a la persona demasiado… hay que intentar
    mantener lo más fiel posible la cara de la persona» (y en la E). La IA redibuja la cara cuando en la referencia es
    pequeña o está de lado: se le da, aparte, la cara grande y de frente."""
    ruta = ruta or f"{SAL}/{letra}.jpg"; im = leer(ruta) if os.path.exists(ruta) else None
    if im is None: raise SystemExit(f"No puedo leer {ruta}")
    cs = caras_en(im)
    if not len(cs): raise SystemExit(f"No encuentro una cara de frente en {ruta}: saca otro fotograma (miniatura.py sacar {letra} …) con la cara de frente y los ojos visibles, o usa una foto del creador")
    x, y, w, h = cs[0]; sal = f"{SAL}/{letra}_cara.jpg"; guardar(sal, recorte_cara(im, cs[0]), 95)
    aviso = " · OJO: la cara mide menos de 160 px en el original: saldrá blanda; busca un fotograma más cercano" if w < 160 else ""
    print(f"{letra}: cara de {w}x{h} px en {ruta} -> {sal}{aviso}")


def final(args):
    """Miniaturas ya generadas (las devuelve ChatGPT): cada una -> youtube/miniatura_<letra>.jpg, 1920x1080, menos de 2 MB."""
    if not args or len(args) % 2: raise SystemExit("miniatura.py final A <imagen> [B <imagen> ...]")
    pares = []
    for i in range(0, len(args), 2):
        letra, ruta = args[i], args[i + 1]; im = leer(ruta) if os.path.exists(ruta) else None
        if im is None: raise SystemExit(f"No puedo leer {ruta}")
        ih, iw = im.shape[:2]; g = a_169(im, 1920, 1080); sal = f"{SAL}/miniatura_{letra}.jpg"; q = 95
        while True:
            guardar(sal, g, q)
            if os.path.getsize(sal) < 1_950_000 or q <= 70: break
            q -= 5
        pierde = round(100 * (1 - (iw * 9 / 16) / ih)) if iw / ih < 16 / 9 else 0
        print(f"{letra}: {iw}x{ih} -> {sal} (1920x1080, {os.path.getsize(sal) // 1000} kB, calidad {q})" + (f" · recortado un {pierde} % del alto: mira que no se haya cortado nada" if pierde > 3 else "") + (" · la original es pequeña: se ha ampliado" if iw < 1280 else ""))
        pares.append((letra, sal))
    comparar(pares, f"{SAL}/prueba.jpg"); print("Prueba a 168 px ->", f"{SAL}/prueba.jpg  (mírala: ¿se entiende sin leer?, ¿se lee el texto?, ¿la esquina de abajo a la derecha está libre?)")
    filas = []      # la cara de la miniatura al lado de la de su referencia: ¿es la misma persona?
    for letra, sal in pares:
        gen = leer(sal); cg = caras_en(gen)
        ref = next((f for f in (f"{SAL}/{letra}_cara.jpg", f"{SAL}/{letra}2_cara.jpg", f"{SAL}/{letra}2.jpg", f"{SAL}/{letra}.jpg", f"{SAL}/A_cara.jpg", f"{SAL}/A.jpg") if os.path.exists(f)), None)   # molde único (G010): la cara de A vale para las cinco
        if not len(cg) or not ref: print(f"{letra}: sin cara de frente que comparar (si sale la persona, compárala a ojo con su referencia)"); continue
        ri = leer(ref); cr = caras_en(ri); a = recorte_cara(gen, cg[0], 360); b = cv2.resize(ri, (360, 360)) if ref.endswith("_cara.jpg") or not len(cr) else recorte_cara(ri, cr[0], 360)
        filas.append(np.hstack([rotulo(b, f"{letra}: referencia"), rotulo(a, f"{letra}: miniatura", (90, 240, 90))]))
    if filas: guardar(f"{SAL}/caras.jpg", np.vstack(filas), 90); print("Caras ->", f"{SAL}/caras.jpg  (MÍRALA: misma nariz, ojos, mandíbula, barba y nacimiento del pelo; si no es él o ella, se rehace en un chat NUEVO)")


a = sys.argv[1:]
if not a: raise SystemExit(__doc__)
if a[0] == "momentos": momentos(float(a[1]) if len(a) > 1 else 4)
elif a[0] == "sacar" and len(a) >= 3 and len(a) % 2:
    for i in range(1, len(a), 2): sacar(a[i], a[i + 1])
elif a[0] == "foto" and len(a) == 3: foto(a[1], a[2])
elif a[0] == "fotos": fotos()
elif a[0] == "hoja": hoja()
elif a[0] == "final": final(a[1:])
elif a[0] == "cara" and len(a) in (2, 3): cara(a[1], a[2] if len(a) == 3 else None)
else: raise SystemExit(__doc__)
