"""Común del montaje horizontal. Todo se ejecuta DESDE la carpeta del vídeo (out/<slug>/), que tiene proyecto.py,
edl.py y plan.py; los pasos viven en herramientas/montaje/ y son iguales para todos los vídeos:

    cd out/<slug> && ../../herramientas/.venv/Scripts/python ../../herramientas/montaje/paso1_alinear.py   (macOS: .venv/bin/python)

proyecto.py (lo crea nuevo_video.py) dice dónde están los brutos, el lienzo y el idioma. Aquí se lee una sola vez."""
import glob, json, os, re, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
for p in (AQUI, os.getcwd()):
    if p not in sys.path: sys.path.insert(0, p)
try:
    import proyecto as _p
except ModuleNotFoundError:
    raise SystemExit("Ejecuta desde la carpeta del vídeo (out/<slug>/): aquí no hay proyecto.py. Créala con herramientas/montaje/nuevo_video.py")

_g = lambda n, d=None: getattr(_p, n, d)
SLUG = _p.SLUG
COMP = _g("COMP") or (lambda c: ("V" + c) if c[0].isdigit() else c)("".join(x.capitalize() for x in re.split(r"[^a-zA-Z0-9]+", SLUG) if x) + "Capas")   # id de la composición Remotion (nunca empieza por cifra)
BRUTOS = [_p.BRUTOS] if isinstance(_p.BRUTOS, str) else list(_p.BRUTOS)       # carpeta(s) con los brutos
ANALISIS = _g("ANALISIS", f"../../bruto/{SLUG}-analisis")                    # transcripciones, hojas y registro visual
TRANSCRIPCIONES = _g("TRANSCRIPCIONES", f"{ANALISIS}/transcripcion")         # <clip>.json, <clip>.txt, <clip>.w.json
FPS = _g("FPS", 25)
ANCHO, ALTO = _g("ANCHO", 3840), _g("ALTO", 2160)                            # lienzo = el del mejor bruto (nunca menos)
IDIOMA = _g("IDIOMA")                                                        # idioma HABLADO (lo detecta paso0); nunca supuesto
NUMEROS = _g("NUMEROS", {})                                                  # cifras -> como se dicen, para alinear: {"100": "onehundred"}
SINCRO = _g("SINCRO", {})                                                    # otra cámara: {"C0132": ("IMG_2120", 2.82)} (sincro.py lo mide)
ESTUDIO = os.path.abspath(_g("ESTUDIO", "../../estudio"))
TRABAJO = "trabajo"
CAPAS_JSON = f"{ESTUDIO}/src/videos/{SLUG}/capas.json"
PY = sys.executable
F = lambda s: int(round(s * FPS))                                            # segundos -> frames
os.makedirs(TRABAJO, exist_ok=True)

# Personalización del CREADOR: personal/<creador>/ de la carpeta de edición (local, nunca en la skill).
# Orden: estándar de la skill < estilo del vídeo (si lo pide) < personal/<creador>/ajustes.py < plan.py del vídeo.
# El creador de un vídeo es CREADOR en su proyecto.py; si en personal/ solo hay uno, es ese.
RAIZ = os.path.dirname(os.path.dirname(AQUI)).replace("\\", "/")
_cre = sorted(d for d in (os.listdir(f"{RAIZ}/personal") if os.path.isdir(f"{RAIZ}/personal") else []) if os.path.isdir(f"{RAIZ}/personal/{d}") and not d.startswith(("_", ".")))
CREADOR = _g("CREADOR") or (_cre[0] if len(_cre) == 1 else None)
if CREADOR is None and len(_cre) > 1: raise SystemExit(f"Hay varios creadores en personal/ ({', '.join(_cre)}): pon CREADOR = '...' en proyecto.py")
if CREADOR and CREADOR not in _cre: raise SystemExit(f"No existe personal/{CREADOR}/ (créalo con herramientas/montaje/nuevo_creador.py {CREADOR})")
PERSONAL = f"{RAIZ}/personal/{CREADOR}" if CREADOR else None
# TODO el material del creador está en su carpeta, ordenado por subcarpetas: marca/ (intro, outro, logos), temas (clips de
# archivo y b-roll), fotos/, mapas/, musica/, sonidos/.
RECURSOS = f"{PERSONAL}/recursos" if PERSONAL else None
MUSICA = _g("MUSICA") or (f"{RECURSOS}/musica" if RECURSOS else None)
# ESTILO (opcional, en proyecto.py): capa de refs/dinamicos/estilos/ (vlog, viaje, reto…). Sin ESTILO no se carga nada
# y todo queda como siempre. Sus números van en <estilo>.py: el de la skill y, encima, el local de refs/ de la carpeta.
ESTILO = _g("ESTILO") or None
_ESTILOS = [f"{RAIZ}/.claude/skills/edicion-horizontal/base/refs/dinamicos/estilos", f"{RAIZ}/refs/dinamicos/estilos"]
if ESTILO and not any(os.path.exists(f"{d}/{ESTILO}.md") for d in _ESTILOS):
    _hay = sorted({os.path.splitext(f)[0] for d in _ESTILOS if os.path.isdir(d) for f in os.listdir(d) if f.endswith(".md") and f != "LEEME.md"})
    raise SystemExit(f"No existe el estilo '{ESTILO}' (hay: {', '.join(_hay) or 'ninguno'}). Quita ESTILO de proyecto.py o créalo en refs/dinamicos/estilos/.")


def _cargar(ruta, en):
    if ruta and os.path.exists(ruta): exec(compile(open(ruta, encoding="utf-8").read(), ruta, "exec"), en)
    return {k: v for k, v in en.items() if not k.startswith("_")}


_aj = {}
for _d in (_ESTILOS if ESTILO else []): _aj.update(_cargar(f"{_d}/{ESTILO}.py", {}))
for _k, _v in _cargar(f"{PERSONAL}/ajustes.py" if PERSONAL else "", {}).items():   # el creador manda sobre el estilo;
    _aj[_k] = {**_aj[_k], **_v} if isinstance(_v, dict) and isinstance(_aj.get(_k), dict) else _v   # SFX, MUSICA_NIVELES: se suman


def ajuste(nombre, defecto):
    """Valor del creador (personal/<creador>/ajustes.py), si no del estilo del vídeo (ESTILO), si no el estándar."""
    return _aj.get(nombre, defecto)


def marca():
    """personal/<creador>/marca.json (color de acento, canal, @, código, logo): paso3 la mete en capas.json para Remotion.
    Fuentes del creador: "fuentes": {"titulos": "<Google Font>", "textos": "<Google Font>"} (o {"familia", "pesos"}).
    Si el creador tiene una marca distinta por idioma (un canal en español y otro en inglés), marca.json lleva
    "idiomas": {"en": {"canal": "...", "handle": "...", "logo": "..."}}: los campos del IDIOMA del vídeo tapan a los generales."""
    f = f"{PERSONAL}/marca.json" if PERSONAL else ""
    m = json.load(open(f, encoding="utf-8")) if f and os.path.exists(f) else {}
    r = {**{k: v for k, v in m.items() if k != "idiomas"}, **m.get("idiomas", {}).get(IDIOMA or "", {})}
    # MARCA en proyecto.py = cambio SOLO para este vídeo (ventana de arranque: «Solo este vídeo»), p. ej.
    # MARCA = {"acento": "#E6EC52", "fuentes": {"titulos": "Anton", "textos": "Montserrat"}}. Manda sobre marca.json;
    # "fuentes" se mezcla clave a clave (se puede cambiar solo la de títulos).
    for k, v in (_g("MARCA") or {}).items():
        r[k] = {**(r.get(k) or {}), **v} if isinstance(v, dict) and isinstance(r.get(k), dict) else v
    return r


def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def norm(s):
    """Palabra normalizada para comparar texto con transcripción: minúsculas, sin tildes ni signos."""
    return re.sub(r"[^a-z0-9%']", "", sin_tildes(s.lower()))


_brutos = {}
def bruto(clip):
    """Ruta del bruto de un clip (nombre sin extensión), buscándolo en BRUTOS."""
    if clip not in _brutos:
        # además de los brutos, valen como piezas los clips del creador, estén en la carpeta que estén de
        # personal/<creador>/recursos/ (marca/intro.mp4, <tema>/<clip de archivo>…). Si el nombre se repite, manda el bruto.
        dirs = BRUTOS + ([RECURSOS] if RECURSOS else [])
        hits = [f for d in BRUTOS for f in glob.glob(os.path.join(d, clip + ".*"))]
        if RECURSOS: hits += sorted(glob.glob(os.path.join(glob.escape(RECURSOS), "**", glob.escape(clip) + ".*"), recursive=True))
        hits = [f for f in hits if f.lower().endswith((".mp4", ".mov", ".m4v", ".mxf", ".mkv"))]
        if not hits: raise SystemExit(f"No encuentro el bruto {clip} en {dirs}")
        _brutos[clip] = hits[0].replace("\\", "/")
    return _brutos[clip]


def clips():
    """Todos los brutos (nombre sin extensión), en orden."""
    fs = [f for d in BRUTOS for f in glob.glob(os.path.join(d, "*")) if f.lower().endswith((".mp4", ".mov", ".m4v", ".mxf", ".mkv"))]
    return sorted({os.path.splitext(os.path.basename(f))[0] for f in fs})


# Brutos HDR (iPhone HLG, PQ). ffmpeg NO convierte HDR al leer: la imagen sale pálida y lavada. La IMAGEN de un bruto
# se lee siempre con fuente(); el SONIDO, del original con bruto(). sdr.py hace copias SDR solo de los trozos que usa el
# montaje (trabajo/sdr/<clip>/<a>_<b>.mp4, a y b en frames del proyecto contados sobre el bruto).
LIBPLACEBO = "libplacebo=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv:format=yuv420p"   # el motor de mpv; nunca zscale+tonemap
_hdr = None
def es_hdr(clip):
    """¿El bruto es HDR? Se mira una vez por clip y se apunta en trabajo/hdr.json."""
    global _hdr
    if _hdr is None:
        try: _hdr = json.load(open(f"{TRABAJO}/hdr.json", encoding="utf-8"))
        except (FileNotFoundError, ValueError): _hdr = {}
    if clip not in _hdr:
        import subprocess
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer", "-of", "default=nw=1:nk=1", bruto(clip)], capture_output=True, text=True).stdout.split()
        _hdr[clip] = bool(r) and r[0].strip(",") in ("arib-std-b67", "smpte2084")
        json.dump(_hdr, open(f"{TRABAJO}/hdr.json", "w", encoding="utf-8"), ensure_ascii=False)
    return _hdr[clip]


_seg = {}
def segmentos(clip, releer=False):
    """Copias SDR que ya hay de un bruto HDR: [(a, b, ruta)], en frames del proyecto sobre el bruto."""
    if releer or clip not in _seg:
        _seg[clip] = sorted((int(os.path.basename(f)[:-4].split("_")[0]), int(os.path.basename(f)[:-4].split("_")[1]), f.replace("\\", "/"))
                            for f in glob.glob(f"{TRABAJO}/sdr/{glob.escape(clip)}/*.mp4"))
    return _seg[clip]


def fuente(clip, t, dur=0.0, exigir=False):
    """De dónde leer la IMAGEN de un bruto entre t y t + dur (s): devuelve (entrada, pre), donde `entrada` son los
    argumentos de ffmpeg («-ss … -i …») y `pre` lo que hay que poner al PRINCIPIO de la cadena de filtros de esa entrada.
    Bruto SDR: el original. Bruto HDR: su copia SDR (sdr.py) si hay una que cubra el trozo; si no, el original convertido
    al vuelo con libplacebo (vale para sacar fotogramas sueltos; para renderizar, exigir=True: sin copia no se sigue)."""
    if not es_hdr(clip): return ["-ss", f"{t:.3f}", "-i", bruto(clip)], ""
    for a, b, f in segmentos(clip):
        if a / FPS <= t + 1e-6 and t + dur <= b / FPS + 1e-6: return ["-ss", f"{max(0, t - a / FPS):.3f}", "-i", f], ""
    if exigir: raise SystemExit(f"{clip} es HDR y no hay copia SDR de {t:.2f}-{t + dur:.2f} s: lanza antes sdr.py")
    return ["-init_hw_device", "vulkan", "-ss", f"{t:.3f}", "-i", bruto(clip)], LIBPLACEBO + ","


_pal = {}
def palabras(clip):
    """Palabras de la transcripción de un bruto: [{p, t, fin, prob}] (las escribe paso0_preparar.py)."""
    if clip not in _pal:
        ruta = f"{TRANSCRIPCIONES}/{clip}.w.json"
        if not os.path.exists(ruta): raise SystemExit(f"Falta {ruta}: lanza antes paso0_preparar.py")
        _pal[clip] = json.load(open(ruta, encoding="utf-8"))
    return _pal[clip]


_AVISADAS = set()
def buscar(W, clip, frase, n):
    """Índices (primera, última) de una frase literal dentro de las palabras del MONTAJE (linea.json).
    n = 0 primera vez que suena (p. ej. en el tráiler), -1 la última, 1 la segunda…
    Si la frase suena más de una vez avisa (AVISO ANCLA) con el minuto de cada una: una frase corta casi siempre está
    dentro de otra y lo del tráiler suena dos veces (vaciamos-estanque-2, 2026-11-19: la garza bajo la ficha del cormorán
    porque «es un ave grande» casaba antes con «el cormorán es un ave grande»)."""
    q = [norm(x) for x in frase.split()]; q = [x for x in q if x]
    idx = [i for i, w in enumerate(W) if w["clip"] == clip and norm(w["w"])]
    hits = [idx[j] for j in range(len(idx) - len(q) + 1) if [norm(W[i]["w"]) for i in idx[j:j + len(q)]] == q]
    if not hits: raise SystemExit(f"frase no encontrada en el montaje: {clip} {frase!r}")
    if len(hits) > 1 and (clip, frase, n) not in _AVISADAS:      # la misma frase suena varias veces (tráiler y cuerpo, frase dentro de otra)
        _AVISADAS.add((clip, frase, n)); mm = lambda h: f"{int(W[h]['o0'] / FPS // 60)}:{W[h]['o0'] / FPS % 60:04.1f}"
        print(f"AVISO ANCLA: «{frase}» ({clip}) suena {len(hits)} veces en el montaje ({', '.join(mm(h) for h in hits)}); n={n} → {mm(hits[n])}")
    i = hits[n]; return i, idx[idx.index(i) + len(q) - 1]


def texto_dicho(W, txt, f0, f1):
    """Hasta cuándo tiene que aguantar un texto (Lucas, 2026-11-14: «aparecen en buen timing pero desaparecen antes de que
    la persona acabe de decirlo, por lo que no te da tiempo ni a leerlo»). Devuelve (frame mínimo de salida, última palabra
    del texto que suena en la voz o None):
      - la ÚLTIMA palabra del texto que se dice (casadas en orden, cada una una vez, sin más de 1,5 s entre una y otra), y de
        ahí +0,5 s; si la frase sigue sin pausa, hasta la pausa (como mucho 0,8 s más);
      - y como mínimo el tiempo de leerlo: 0,6 s + 0,3 s por palabra, nunca menos de 1,2 s."""
    pal = [norm(p) for p in re.split(r"[\s|/·:,.!?¡¿*'\"()+«»…-]+", str(txt)) if norm(p)]
    ks = [p for p in pal if len(p) >= 4 or any(c.isdigit() for c in p)] or list(pal)
    def es(n, k): return n == k or (len(n) >= 5 and len(k) >= 5 and (n.startswith(k[:5]) or k.startswith(n[:5])))
    ult, j = None, 0                  # cada palabra del texto se casa UNA vez y en orden (lo que repite después no cuenta)
    for w in W:
        if j >= len(ks): break
        if w["o0"] < f0 - 0.3 * FPS: continue
        if ult is None and w["o0"] > f1 + 0.5 * FPS: break
        if ult is not None and w["o0"] - ult["o1"] > 1.5 * FPS: break
        n = norm(w["w"]); m = next((i for i in range(j, len(ks)) if es(n, ks[i])), None)
        if m is not None: ult, j = w, m + 1
    fin = f0 + max(F(1.2), F(0.6 + 0.3 * len(pal)))
    if ult is not None:
        fin = max(fin, int(round(ult["o1"])) + F(0.5)); k = W.index(ult)
        while k + 1 < len(W) and W[k + 1]["o0"] - W[k]["o1"] < 0.3 * FPS and W[k + 1]["o1"] - ult["o1"] <= 0.8 * FPS: k += 1
        fin = max(fin, int(round(W[k]["o1"])) + F(0.2))
    return fin, ult


class Linea:
    """trabajo/linea.json + resolución de anclas. Un ancla dice DÓNDE del montaje cae algo, siempre colgado de lo que se
    dice o de una marca del EDL, nunca de un número de frame puesto a mano:
        (clip, "frase literal", n)        frame en que empieza esa frase (n = 0 primera vez, -1 la última)
        ((clip, "frase", n), segundos)    lo mismo, desplazado
        ("@marca", segundos)              marca del EDL (tag de una pieza, X("…") o "s3" = sección 3) + segundos
        "inicio" / "fin"
    """
    def __init__(self):
        if not os.path.exists(f"{TRABAJO}/linea.json"): raise SystemExit("Falta trabajo/linea.json: lanza antes paso1_alinear.py")
        d = json.load(open(f"{TRABAJO}/linea.json", encoding="utf-8"))
        self.piezas, self.palabras, self.marcas, self.secciones, self.total = d["piezas"], d["palabras"], d["marcas"], d["secciones"], d["total"]

    def ancla(self, a):
        if a == "inicio": return 0
        if a == "fin": return self.total
        if isinstance(a[0], str) and a[0].startswith("@"):
            if a[0][1:] not in self.marcas: raise SystemExit(f"marca desconocida {a[0]}; hay: {sorted(self.marcas)}")
            return self.marcas[a[0][1:]] + F(a[1] if len(a) > 1 else 0)
        if isinstance(a[0], (tuple, list)): return self.ancla(tuple(a[0])) + F(a[1])
        return int(round(self.palabras[buscar(self.palabras, *a)[0]]["o0"])) - 1

    def fin_frase(self, a):
        """Frame en que acaba la frase de un ancla de frase."""
        return int(round(self.palabras[buscar(self.palabras, *a)[1]]["o1"]))


def video():
    """Planos del montaje (trabajo/video.json), en una lista plana."""
    return [v for t in json.load(open(f"{TRABAJO}/video.json"))["tramos"] for v in t]


# ---- Dónde cae cada gráfico en pantalla (para que dos textos no se pisen y para la hoja de textos) ----
# Lucas, 2026-11-17 (alimentacion): «en el punto 2/7 se solapan dos textos, esto no puede pasar nunca» y «vuelven a
# sobreponerse textos, NO PUEDE PASAR». Causa: la tarjeta de capítulo (abajo a la izquierda, 3 s) y el rótulo de la
# especie que se nombra en la primera frase del capítulo (abajo al centro) caían a la vez y nada comparaba sus sitios;
# solo se comprobaba el botón de suscribir. Ahora paso3_plan.py calcula la caja de cada gráfico y se para si dos se cruzan.
# Las medidas copian las de estudio/src/comun/Graficos.tsx (si cambias un gráfico de serie, cambia aquí su caja). Los
# gráficos propios de un creador se miden como un rótulo abajo al centro (con "lado", "x" o "y" si los lleva) o como una
# mascota a un lado si llevan "anim"; si alguno va en otro sitio, su caja va en personal/<creador>/ajustes.py:
#   CAJAS = {"tipo": (x0, y0, x1, y1)}  o  {"tipo": {"der": (…), "izq": (…)}}   (en partes del lienzo, 0-1)
BOTON_ESC = ajuste("BOTON_ESC", 0.34)      # tamaño de serie de los botones de suscribir (ancho de su lienzo original / ancho del vídeo)


MARGEN = 0.04       # ningún texto se sale del cuadro: margen al borde, como Graficos.tsx (MARGEN, dentro)


def dentro(centro, mitad):
    return min(max(centro, ANCHO * MARGEN + mitad), ANCHO * (1 - MARGEN) - mitad)


def fuera(cajas, tol=0.004):
    """Lo que se sale del cuadro (en partes del lienzo, la mayor de las cuatro); 0 si cabe entero."""
    return max((max(-x0, -y0, x1 - 1, y1 - 1) for x0, y0, x1, y1 in cajas), default=0) if cajas else 0


def caja_texto(it, f=None):
    """[(x0, y0, x1, y1)] en partes del lienzo (0-1) que ocupa el gráfico `it` de capas.json; [] si no ocupa sitio.
    Con `f` (frame del montaje), la de ese instante (los rótulos con flecha se mueven con su sujeto)."""
    W, H = ANCHO, ALTO; t = it["t"]; cj = ajuste("CAJAS", {}).get(t)
    s = lambda k: str(it.get(k) or "")
    if cj: return [tuple(cj[it.get("lado", "der")] if isinstance(cj, dict) else cj)]
    if t in ("titulo", "mapa", "cartela_dia") or (t == "maquina" and it.get("fondo") != "ninguno"): return [(0.0, 0.0, 1.0, 1.0)]
    if t == "oscurecer": return []
    if t == "partida":          # Intro.tsx: dos palabras a media altura, ancladas a cada lado
        fs = H * it.get("alto", 0.042) * 1.38; y = it.get("y", 0.495); h = fs / H; ch = fs * 0.58 / W
        iz = it.get("margen_izq", 0.077); de = it.get("margen_der", 0.095)
        return [(iz, y - h / 2, iz + len(s("izq")) * ch, y + h / 2), (1 - de - len(s("der")) * ch, y - h / 2, 1 - de, y + h / 2)]
    if t == "maquina":
        fs = min(H * it.get("alto", 0.034) * 1.38, W * 0.84 / (max(len(s("txt")), 8) * 0.55)); w = len(s("txt")) * fs * 0.55
        return [((W - w) / 2 / W, 0.5 - fs / 2 / H, (W + w) / 2 / W, 0.5 + fs / 2 / H)]
    if t == "contador":
        txt = f"{it.get('prefijo', '')}{it.get('hasta', '')}{it.get('sufijo', '')}" + ("  " if it.get("flecha") else "")
        fs = min(H * it.get("alto", 0.14), W * 0.42 / (max(len(txt), 2) * 0.62)); w = len(txt) * fs * 0.62; x, y = it.get("x", 0.5) * W, it.get("y", 0.4) * H
        return [((x - w / 2) / W, (y - fs / 2) / H, (x + w / 2) / W, (y + fs / 2) / H)]
    if t == "seccion":
        x0 = 0.07 * H; de = it.get("de") or 0
        numw = 0.23 * H * 0.62 * len(str(it.get("n", ""))) + (0.085 * H * 0.62 * (1 + len(str(de))) if de else 0)
        fs = min(0.075 * H, 0.62 * W / (max(len(s("titulo")), 2) * 0.82))
        txt = max(len(s("titulo")) * fs * 0.75, len(s("sub")) * 0.034 * H * 0.5, de * 0.056 * H)
        y1 = H * 0.93; return [(x0 / W, (y1 - 0.23 * H * 0.9) / H, (x0 + numw + 0.03 * H + txt) / W, y1 / H)]
    if t == "golpe":
        ls = s("txt").split("|"); n = max(len(l) for l in ls); fs = min(0.105 * H, 0.66 * W / (max(n, 2) * 0.82))
        w, h = n * fs * 0.75 * 1.22, len(ls) * fs * 1.12 * 1.22; y1 = 1 - it.get("y", 0.1); return [((W - w) / 2 / W, y1 - h / H, (W + w) / 2 / W, y1)]
    if t in ("nota", "sub"):
        fs = (0.046 if t == "nota" else 0.05) * H; b = 0.075 if t == "nota" else 0.1; w = len(s("txt")) * fs * 0.52
        return [((W - w) / 2 / W, 1 - b - fs * 1.3 / H, (W + w) / 2 / W, 1 - b)]
    if t == "dato":
        fs = min(0.22 * H, W * it.get("mw", 0.4) / (max(len(s("grande")), 2) * 0.82)); w = max(len(s("grande")) * fs * 0.9, len(s("peq")) * 0.04 * H * 0.6) * 1.15; h = fs + 0.06 * H
        x, y = dentro(it.get("x", 0.5) * W, w / 2), it.get("y", 0.74) * H; return [((x - w / 2) / W, (y - h / 2) / H, (x + w / 2) / W, (y + h / 2) / H)]
    if t == "trk":
        pos = it.get("pos") or []; out = []
        w = max(len(s("grande")) * 0.06 * H * 0.9, len(s("peq")) * 0.034 * H * 0.6) * 1.12; h = 0.06 * H * 1.1 + 0.04 * H
        muestras = [pos[min(max(f - it["f0"], 0), len(pos) - 1)]] if (pos and f is not None) else ([pos[0], pos[len(pos) // 2], pos[-1]] if pos else [])
        for x, y in muestras:
            sitio = lambda iz: (lambda t: t - w >= W * 0.02 if iz else t + w <= W * 0.98)(min(max(x + (-1 if iz else 1) * 0.13 * H, 0.3 * H), W - 0.3 * H))
            izq = it.get("lado") == "izq"
            if not sitio(izq) and sitio(not izq): izq = not izq          # como Graficos.tsx: al otro lado si no cabe
            tx = min(max(x + (-1 if izq else 1) * 0.13 * H, 0.3 * H), W - 0.3 * H); tx = max(tx, W * 0.02 + w) if izq else min(tx, W * 0.98 - w)
            ty = max(y - 0.13 * H, 0.12 * H)
            out.append(((tx - w if izq else tx) / W, (ty - h) / H, (tx if izq else tx + w) / W, ty / H))
        return out
    if t == "boton":
        c = it["caja"]; k = W * it.get("esc", BOTON_ESC) / c["ancho_original"]
        x0 = W * it.get("x", 0.5) + (c["x"] - c["ancho_original"] / 2) * k; y0 = H * it.get("y", 0.8) + (c["y"] - c["alto_original"] / 2) * k
        return [(x0 / W, y0 / H, (x0 + c["w"] * k) / W, (y0 + c["h"] * k) / H)]
    if t == "suscribe": return [(0.04, 0.8, 0.3, 0.93)]
    if it.get("anim"):      # mascota que asoma por un lado con su burbuja
        return [(0.0, 0.25, 0.45, 1.0)] if it.get("lado") == "izq" else [(0.55, 0.25, 1.0, 1.0)]
    if any(it.get(k) for k in ("txt", "grande")):      # rótulo propio: abajo; con «lado», pegado a ese borde (con margen)
        ls = (s("txt") or s("grande")).split("|"); n = max(len(l) for l in ls); lado = it.get("lado") if it.get("lado") in ("izq", "der") else None
        disp = (0.58 if lado else 0.86) * W / 1.08; fs = min(0.08 * H, disp / (max(n, 2) * 0.9))
        sub = s("sub"); sfs = max(0.04 * H, fs * 0.55); sfs = min(sfs, disp / (len(sub) * 0.6)) if sub else sfs
        w = max(n * fs * 0.9, len(sub) * sfs * 0.6) * 1.08; h = (len(ls) * fs * 1.12 + (sfs * 1.2 if sub else 0)) * 1.08
        x0 = MARGEN * W if lado == "izq" else (1 - MARGEN) * W - w if lado == "der" else (W - w) / 2; y1 = (1 - it.get("y", 0.1)) * H
        return [(x0 / W, (y1 - h) / H, (x0 + w) / W, y1 / H)]
    return []


def cruce(a, b):
    """Área (en partes del lienzo) en que se pisan dos listas de cajas."""
    return max((max(0, min(p[2], q[2]) - max(p[0], q[0])) * max(0, min(p[3], q[3]) - max(p[1], q[1])) for p in a for q in b), default=0)
