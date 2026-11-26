"""arranque.py [--espera 600] [--sin-abrir] [--estilo X]: la VENTANA DE ARRANQUE de un vídeo (SKILL.md § 2, paso 0).
Se lanza desde la carpeta del vídeo (out/<slug>/), con paso0_preparar.py ya en segundo plano, y EN SEGUNDO PLANO también:
abre en el navegador una página local («Configuración de edición») con lo del creador recomendado (estilo, recursos) y lo
que hay en los brutos, espera a que el creador pulse Empezar (o a que se acabe la cuenta atrás) y termina.

Resultado: trabajo/arranque.json, `ESTILO` y una línea `# Arranque (...)` en proyecto.py, y una línea ARRANQUE: en la salida.
Color y fuente (dentro de «Cambiar estilo»): «Solo este vídeo» → `MARCA = {...}` en proyecto.py (comun.marca() lo mezcla
sobre marca.json); «Guardar para el creador» → su marca.json + una línea con fecha en su preferencias.md.
Sin respuesta (cierra la página, cuenta atrás a cero o tope de tiempo): la configuración recomendada, con el stock con
confirmación por tanda, como hasta ahora. Todo es local: un servidor en 127.0.0.1 que se apaga al recibir la respuesta.
Solo biblioteca estándar + ffmpeg/ffprobe. Por qué: Lucas, 2026-11-24 (página propia en vez de las preguntas de Claude)."""
import argparse, datetime, glob, html, json, os, re, runpy, subprocess, sys, threading, time, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

AQUI = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.getcwd()
if not os.path.exists("proyecto.py"):
    raise SystemExit("Ejecuta desde la carpeta del vídeo (out/<slug>/): aquí no hay proyecto.py")
RAIZ = os.path.abspath(os.path.join(VIDEO, "..", ".."))
SKILL = os.path.join(RAIZ, ".claude", "skills", "edicion-horizontal")
EXT = (".mp4", ".mov", ".m4v", ".mxf", ".mkv")
sys.path.insert(0, os.path.dirname(AQUI))
import color_log
try:
    from git_bash import BASH          # en Windows, Git Bash (no el de WSL)
except Exception: BASH = "bash"

ap = argparse.ArgumentParser()
ap.add_argument("--espera", type=int, default=600, help="segundos de cuenta atrás (por defecto 600 = 10 min)")
ap.add_argument("--sin-abrir", action="store_true", help="no abre el navegador (para probar)")
ap.add_argument("--estilo", default=None, help="estilo pedido en el mensaje para este vídeo (sale preseleccionado)")
args = ap.parse_args()

P = runpy.run_path("proyecto.py")
SLUG = P.get("SLUG", os.path.basename(VIDEO))
cres = sorted(x for x in os.listdir(os.path.join(RAIZ, "personal")) if os.path.isdir(os.path.join(RAIZ, "personal", x)) and not x.startswith(("_", "."))) if os.path.isdir(os.path.join(RAIZ, "personal")) else []
CREADOR = P.get("CREADOR") or (cres[0] if len(cres) == 1 else "")
PERS = os.path.join(RAIZ, "personal", CREADOR) if CREADOR else ""
TRAB = os.path.join(VIDEO, "trabajo", "arranque"); os.makedirs(TRAB, exist_ok=True)


def leer(p):
    try: return open(p, encoding="utf-8").read()
    except OSError: return ""


# ---------- creador ----------
marca = {}
try: marca = json.load(open(os.path.join(PERS, "marca.json"), encoding="utf-8")) if PERS else {}
except (OSError, ValueError): pass
ACENTO = marca.get("acento") or "#E6EC52"
CANAL = marca.get("canal") or CREADOR or "Sin creador"
perfil = leer(os.path.join(PERS, "perfil.md")) if PERS else ""


# ---------- color y fuentes ----------
def familias_google():
    t = leer(os.path.join(RAIZ, "estudio", "node_modules", "@remotion", "google-fonts", "dist", "cjs", "index.js"))
    return set(re.findall(r"fontFamily:\s*'([^']+)'", t))


GOOGLE = familias_google()


def fam(v):
    return (v.get("familia") if isinstance(v, dict) else v) or ""


def fuentes_marca_ts():
    """Las fuentes por defecto de la carpeta (estudio/src/comun/marca.ts, LOCAL): F_ANCHA y F_TXT."""
    t = leer(os.path.join(RAIZ, "estudio", "src", "comun", "marca.ts"))
    imp = dict(re.findall(r'loadFont as (\w+) \} from "@remotion/google-fonts/(\w+)"', t))
    out = {}
    for var, clave in (("F_ANCHA", "titulos"), ("F_TXT", "textos")):
        m = re.search(rf"{var}\s*=\s*(\w+)\(", t)
        imp_name = imp.get(m.group(1)) if m else None
        if imp_name:
            out[clave] = next((g for g in GOOGLE if g.replace(" ", "").lower() == imp_name.lower()), imp_name)
    return out


def fuentes_de_sus_videos():
    """Familias de Google Fonts que salen en los campos «fuente…» de las fichas de sus vídeos (personal/<creador>/refs)."""
    vistos = []
    def recorre(x, clave=""):
        if isinstance(x, dict):
            for k, v in x.items(): recorre(v, k)
        elif isinstance(x, list):
            for v in x: recorre(v, clave)
        elif isinstance(x, str) and "fuente" in clave.lower():
            for g in sorted(GOOGLE, key=len, reverse=True):
                if len(g) >= 4 and re.search(rf"(?<!\w){re.escape(g)}(?!\w)", x) and g not in vistos: vistos.append(g)
    for f in sorted(glob.glob(os.path.join(PERS, "refs", "*.json"))) if PERS else []:
        try: recorre(json.load(open(f, encoding="utf-8")))
        except (OSError, ValueError): pass
    return vistos


MARCA_PROY = P.get("MARCA") or {}
BASE_FZ = fuentes_marca_ts()
FZ = dict(BASE_FZ); FZ.update({k: fam(v) for k, v in (marca.get("fuentes") or {}).items() if fam(v)})
FZ.update({k: fam(v) for k, v in (MARCA_PROY.get("fuentes") or {}).items() if fam(v)})
ACENTO_ACT = MARCA_PROY.get("acento") or ACENTO
SUYAS = fuentes_de_sus_videos()


SOLO_ROTULO = {"Anton", "Bebas Neue", "Archivo Black", "Oswald", "Unbounded", "Bangers", "Impact"}   # no valen para texto pequeño


def lista(actual, extra, textos=False):
    out = []
    for x in [actual] + [f for f in SUYAS if not (textos and f in SOLO_ROTULO)] + extra:
        if x and x not in out and (not GOOGLE or x in GOOGLE): out.append(x)
    return out[:9]


MARCA_UI = {
    "acento": ACENTO_ACT, "titulos": FZ.get("titulos", ""), "textos": FZ.get("textos", ""), "suyas": SUYAS,
    "colores": list(dict.fromkeys([ACENTO_ACT, ACENTO, "#E6EC52", "#FBBA1C", "#FF5A36", "#4DD7FF", "#FFFFFF"])),
    "f_titulos": lista(FZ.get("titulos", ""), ["Anton", "Bebas Neue", "Unbounded", "Archivo Black", "Oswald", "Montserrat"]),
    "f_textos": lista(FZ.get("textos", ""), ["Montserrat", "Lexend", "Inter", "Poppins", "DM Sans"], textos=True),
}


# ---------- estilos: los de la skill y los locales (los locales mandan) ----------
def estilos():
    out = {}
    for d in (os.path.join(SKILL, "base", "refs", "dinamicos", "estilos"), os.path.join(RAIZ, "refs", "dinamicos", "estilos")):
        for f in sorted(glob.glob(os.path.join(d, "*.md"))):
            n = os.path.splitext(os.path.basename(f))[0]
            if n.upper() == "LEEME" or n.startswith("_"): continue
            t = leer(f)
            que = re.search(r"\*\*Qué es\*\*:\s*(.+)", t)
            est = re.search(r"\*\*Estado\*\*:\s*(.+)", t)
            sin = bool(est and "sin analizar" in est.group(1).lower())
            q = que.group(1).strip() if que else ""
            q = q[:1].upper() + q[1:]
            out[n] = {"id": n, "nombre": n.upper(), "que": q.rstrip("."), "reglas": not sin}
    return out


EST = estilos()


def defecto_perfil():
    m = re.search(r"Estilo (?:por defecto|de edición)\*{0,2}:\*{0,2}\s*([^\n(]*)", perfil, re.I)
    if not m: return None
    v = m.group(1).strip().lower()
    for n in EST:
        if re.search(rf"\b{re.escape(n)}\b", v): return n
    return None


ESTILO_PROY = P.get("ESTILO") or None
rec_estilo = None
for cand in (args.estilo, ESTILO_PROY, defecto_perfil()):
    if cand and cand in EST and EST[cand]["reglas"]: rec_estilo = cand; break
estilo_perfil = defecto_perfil()


# ---------- recursos: librería del creador y stock ----------
def libreria():
    d = os.path.join(PERS, "recursos") if PERS else ""
    if not d: return {"hay": False, "ok": False, "texto": "sin creador"}
    try:
        n = sum(len(fs) for _, _, fs in os.walk(d) if True) if os.path.isdir(d) else None
    except OSError:
        n = None
    if n is None:
        enlazada = os.path.islink(d) or "disco" in leer(os.path.join(PERS, "recursos.md")).lower() or os.path.isdir(os.path.join(SKILL, "creadores", CREADOR))
        return {"hay": True, "ok": False, "texto": "disco sin conectar" if enlazada else "no se abre"}
    return {"hay": True, "ok": True, "texto": f"{n} archivos"}


def stock():
    t = leer(os.path.join(RAIZ, "personal", "bancos.md"))
    m = re.search(r"Shutterstock:\s*([^\n—-]+)", t)
    if not m: return {"ok": False, "texto": "sin probar"}
    v = m.group(1).strip().upper()
    if v.startswith("SÍ") or v.startswith("SI "): return {"ok": True, "texto": "Shutterstock listo"}
    if "SIN SESI" in v: return {"ok": False, "texto": "Shutterstock sin sesión"}
    return {"ok": False, "texto": "sin Shutterstock"}


def recursos_estado():
    lib, st = libreria(), stock()
    if lib["hay"] and st["ok"]: rec = "libreria_stock"
    elif lib["hay"]: rec = "libreria"
    elif st["ok"]: rec = "stock"
    else: rec = "brutos"
    return {"libreria": lib, "stock": st, "recomendado": rec}


# ---------- brutos: duración, cámaras y fotogramas ----------
def brutos_lista():
    b = P.get("BRUTOS", "")
    ds = b if isinstance(b, (list, tuple)) else [b]
    fs = []
    for d in ds:
        d = d if os.path.isabs(d) else os.path.join(VIDEO, d)
        fs += [f for f in glob.glob(os.path.join(d, "*")) if f.lower().endswith(EXT)]
    return sorted(fs)


def sonda(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer:format=duration", "-of", "json", f], capture_output=True, text=True)
    try:
        j = json.loads(r.stdout); return float(j["format"]["duration"]), (j["streams"][0].get("color_transfer") or "")
    except (ValueError, KeyError, IndexError):
        return 0.0, ""


def camara(nombre):
    n = nombre.upper()
    if n.startswith(("DJI", "MAX_", "AVATA")): return "dron"
    if n.startswith(("IMG_", "PXL_", "VID_")): return "móvil"
    if n.startswith(("GX", "GH", "GOPR")): return "GoPro"
    if re.match(r"^C\d{4}", n): return "Sony"
    if n.startswith(("DSC", "MVI_", "MAH", "P10")): return "cámara"
    return "otra"


FS = brutos_lista()
INFO = [(f,) + sonda(f) for f in FS]
TOTAL_MIN = sum(d for _, d, _ in INFO) / 60
CAMS = {}
for f, d, _ in INFO: CAMS[camara(os.path.basename(f))] = CAMS.get(camara(os.path.basename(f)), 0) + 1
hdr = any(t in ("smpte2084", "arib-std-b67") for _, _, t in INFO)


def fotograma(f, dur, tr, sal):
    if os.path.exists(sal) and os.path.getsize(sal) > 0: return True
    t = max(0.0, dur * 0.4)
    base = ["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", f, "-frames:v", "1", "-q:v", "4"]
    if tr in ("smpte2084", "arib-std-b67"):
        vf = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=640:-2"
        if subprocess.run(base + ["-vf", vf, sal], capture_output=True).returncode == 0: return True
    return subprocess.run(base + ["-vf", "scale=640:-2", sal], capture_output=True).returncode == 0


FOTOS = []
if INFO:
    k = min(8, len(INFO)); idx = sorted({round(i * (len(INFO) - 1) / max(1, k - 1)) for i in range(k)})
    for i in idx:
        f, d, tr = INFO[i]; n = os.path.splitext(os.path.basename(f))[0]
        sal = os.path.join(TRAB, f"{n}.jpg")
        if fotograma(f, d, tr, sal): FOTOS.append({"nombre": n, "url": f"/img/{n}.jpg"})
CARA = None
if PERS:
    for p in sorted(glob.glob(os.path.join(PERS, "recursos", "creador", "*"))):
        if p.lower().endswith((".jpg", ".jpeg", ".png")): CARA = p; break

# ---------- color (G009) ----------
# Log: solo por metadatos aquí (rápido); paso0_preparar.py lo confirma clip a clip midiendo la imagen.
LUTS_CRE = [os.path.join(PERS, "recursos", "luts")] if PERS else []
LOGS = []
for f, _, tr in INFO:
    if tr in ("smpte2084", "arib-std-b67"): continue
    d = color_log.detectar(f, medir_imagen=False)
    if d["perfil"]: LOGS.append(d["perfil"])
def ajuste_creador(nombre):
    try:
        en = {}; exec(compile(leer(os.path.join(PERS, "ajustes.py")), "ajustes.py", "exec"), en); return en.get(nombre)
    except Exception: return None
LOOK_ACT = P.get("LOOK") or (ajuste_creador("LOOK") if PERS else None) or ""
COLOR = {"log": {"n": len(LOGS), "perfiles": sorted({color_log.PERFILES[p][0] for p in LOGS}),
                 "faltan": sorted({color_log.PERFILES[p][0] for p in LOGS if not color_log.lut_de(p, extra=LUTS_CRE)})},
         "looks": color_log.looks_disponibles(LUTS_CRE), "actual": LOOK_ACT}

detectado = []
if sum(1 for c in CAMS if c != "dron") >= 2: detectado.append("dos_camaras")
if "dron" in CAMS: detectado.append("dron")


def datos():
    est = [{"id": "", "nombre": "COMO SIEMPRE", "que": "El de su perfil: como edita siempre" if not estilo_perfil else "Sin estilo: la base de la skill", "reglas": True}]
    est += list(EST.values())
    return {
        "slug": SLUG, "canal": CANAL, "acento": ACENTO, "espera": args.espera,
        "brutos": {"n": len(INFO), "min": round(TOTAL_MIN, 1), "camaras": CAMS, "hdr": hdr, "detectado": detectado},
        "fotos": FOTOS, "cara": "/img/_cara" if CARA else "",
        "estilos": est, "estilo_recomendado": rec_estilo or "",
        "recursos": recursos_estado(), "marca": MARCA_UI, "color": COLOR,
    }


# ---------- resultado ----------
FIN = threading.Event(); RES = {}; LIMITE = [time.time() + args.espera + 60]


def guardar(r, por_tiempo):
    D = datos()
    estilo = r.get("estilo", D["estilo_recomendado"]) or ""
    if estilo and not (estilo in EST and EST[estilo]["reglas"]): estilo = ""
    recursos = r.get("recursos", D["recursos"]["recomendado"])
    if recursos not in ("libreria_stock", "libreria", "stock", "brutos"): recursos = D["recursos"]["recomendado"]
    brutos = [b for b in r.get("brutos", D["brutos"]["detectado"]) if b in ("dos_camaras", "teleprompter", "dictado", "dron", "solo_recurso")]
    otra = str(r.get("otra", ""))[:300].strip()
    # color y fuente: solo lo que cambia respecto a lo de ahora
    m = r.get("marca") or {}
    cambio = {}
    if re.fullmatch(r"#[0-9A-Fa-f]{6}", str(m.get("acento", ""))) and m["acento"].upper() != ACENTO_ACT.upper(): cambio["acento"] = m["acento"].upper()
    fz = {k: m[k] for k in ("titulos", "textos") if m.get(k) and m[k] != FZ.get(k) and (not GOOGLE or m[k] in GOOGLE)}
    if fz: cambio["fuentes"] = fz
    donde = "creador" if m.get("donde") == "creador" else "video"
    out = {"fecha": datetime.datetime.now().isoformat(timespec="seconds"), "por_tiempo": por_tiempo,
           "estilo": estilo or None, "recursos": recursos,
           "stock_sin_confirmar": (recursos in ("libreria_stock", "stock")) and not por_tiempo,
           "brutos": brutos, "otra": otra, "marca": ({**cambio, "donde": donde} if cambio else None)}
    json.dump(out, open(os.path.join(VIDEO, "trabajo", "arranque.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    # proyecto.py: ESTILO y una línea de resumen (se reescriben si ya estaban)
    t = open("proyecto.py", encoding="utf-8").read()
    t = re.sub(r"(?m)^ESTILO\s*=.*\n?", "", t); t = re.sub(r"(?m)^# Arranque \(.*\n?", "", t)
    if not t.endswith("\n"): t += "\n"
    if estilo: t += f'ESTILO = "{estilo}"                    # elegido en la ventana de arranque\n'
    orden = {"libreria_stock": "brutos → librería → stock", "libreria": "brutos → librería", "stock": "brutos → stock", "brutos": "solo brutos"}[recursos]
    t += (f"# Arranque ({out['fecha'][:10]}{', sin respuesta' if por_tiempo else ''}): recursos {orden}"
          f"{' (stock sin confirmar por tanda)' if out['stock_sin_confirmar'] else ''} · brutos: {', '.join(brutos) or 'nada especial'}"
          f"{' · ' + otra if otra else ''}\n")
    if cambio and donde == "video":
        nueva = dict(MARCA_PROY); nf = dict(nueva.get("fuentes") or {}); nf.update(cambio.get("fuentes", {}))
        if "acento" in cambio: nueva["acento"] = cambio["acento"]
        if nf: nueva["fuentes"] = nf
        t = re.sub(r"(?m)^MARCA\s*=.*\n?", "", t)
        t += f"MARCA = {json.dumps(nueva, ensure_ascii=False)}    # color/fuente solo de este vídeo (ventana de arranque)\n"
    # LOOK (G009): "" = directo, sin look. «Guardar para el creador» → su ajustes.py (+ preferencias.md); «Solo este vídeo» → proyecto.py
    look = str(r.get("look", LOOK_ACT) or ""); ids = {l["id"] for l in COLOR["looks"]}
    if look and look not in ids: look = LOOK_ACT
    out["look"] = look or None
    json.dump(out, open(os.path.join(VIDEO, "trabajo", "arranque.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    if look != LOOK_ACT or r.get("look_donde") == "video":
        t = re.sub(r"(?m)^LOOK\s*=.*\n?", "", t)
        if r.get("look_donde") == "video" or not PERS:
            t += f"LOOK = {json.dumps(look or None)}    # look de color solo de este vídeo (ventana de arranque)\n".replace("null", "None")
        else:
            aj = os.path.join(PERS, "ajustes.py"); ta = leer(aj)
            ta = re.sub(r"(?m)^LOOK\s*=.*\n?", "", ta)
            if ta and not ta.endswith("\n"): ta += "\n"
            ta += f"LOOK = {json.dumps(look or None)}    # look de color (ventana de arranque, {out['fecha'][:10]}); None = directo, sin look\n".replace("null", "None")
            open(aj, "w", encoding="utf-8", newline="\n").write(ta)
            with open(os.path.join(PERS, "preferencias.md"), "a", encoding="utf-8", newline="\n") as f:
                f.write(f"\n- **Color** ({out['fecha'][:10]}, ventana de arranque, vídeo `{SLUG}`): {'look ' + look if look else 'directo, sin look'} (LOOK en ajustes.py).\n")
    open("proyecto.py", "w", encoding="utf-8", newline="\n").write(t)
    if cambio and donde == "creador" and PERS:
        mj = os.path.join(PERS, "marca.json"); d = dict(marca)
        if "acento" in cambio: d["acento"] = cambio["acento"]
        if "fuentes" in cambio: d["fuentes"] = {**(d.get("fuentes") or {}), **cambio["fuentes"]}
        open(mj, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
        partes = ([f"acento {cambio['acento']}"] if "acento" in cambio else []) + [f"fuente de {'títulos' if k == 'titulos' else 'textos'}: {v}" for k, v in cambio.get("fuentes", {}).items()]
        with open(os.path.join(PERS, "preferencias.md"), "a", encoding="utf-8", newline="\n") as f:
            f.write(f"\n- **Marca** ({out['fecha'][:10]}, ventana de arranque, vídeo `{SLUG}`): {' · '.join(partes)}. Guardado en marca.json.\n")
    RES.update(out); FIN.set()


class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _env(self, code, cuerpo, tipo):
        b = cuerpo if isinstance(cuerpo, bytes) else cuerpo.encode("utf-8")
        self.send_response(code); self.send_header("Content-Type", tipo); self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store"); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            t = open(os.path.join(AQUI, "arranque.html"), encoding="utf-8").read()
            d = json.dumps(datos(), ensure_ascii=False).replace("</", "<\\/")
            return self._env(200, t.replace("/*DATOS*/null", d).replace("__TITULO__", html.escape(f"Configuración de edición · {SLUG}")), "text/html; charset=utf-8")
        if self.path == "/img/_cara" and CARA:
            return self._env(200, open(CARA, "rb").read(), "image/png" if CARA.lower().endswith(".png") else "image/jpeg")
        m = re.fullmatch(r"/img/([\w.-]+\.jpg)", self.path)
        if m and os.path.exists(os.path.join(TRAB, m.group(1))):
            return self._env(200, open(os.path.join(TRAB, m.group(1)), "rb").read(), "image/jpeg")
        self._env(404, "no", "text/plain")

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        try: r = json.loads(self.rfile.read(n) or b"{}")
        except ValueError: r = {}
        if self.path == "/recomprobar":
            sh = os.path.join(SKILL, "conectar_disco.sh")
            if CREADOR and os.path.exists(sh) and not libreria()["ok"]:
                subprocess.run([BASH, sh, CREADOR], cwd=RAIZ, capture_output=True, timeout=120)
            return self._env(200, json.dumps(recursos_estado(), ensure_ascii=False), "application/json")
        if self.path == "/vivo":
            LIMITE[0] = time.time() + args.espera + 60
            return self._env(200, '{"ok":true}', "application/json")
        if self.path == "/enviar":
            guardar(r, bool(r.get("por_tiempo")))
            return self._env(200, '{"ok":true}', "application/json")
        self._env(404, "no", "text/plain")


srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
url = f"http://127.0.0.1:{srv.server_address[1]}/"
threading.Thread(target=srv.serve_forever, daemon=True).start()
print(f"Ventana de arranque: {url}  (cuenta atrás {args.espera // 60} min)", flush=True)
if not args.sin_abrir: webbrowser.open(url)
while not FIN.wait(5):
    if time.time() > LIMITE[0]: guardar({}, True); break
time.sleep(0.5); srv.shutdown()
r = RES
print("ARRANQUE: estilo=%s · recursos=%s · stock_sin_confirmar=%s · brutos=%s%s%s" % (
    r["estilo"] or "como siempre", r["recursos"], "sí" if r["stock_sin_confirmar"] else "no", ",".join(r["brutos"]) or "nada",
    " · otra=" + r["otra"] if r["otra"] else "", " · SIN RESPUESTA (configuración recomendada)" if r["por_tiempo"] else ""))
if r.get("marca"): print("MARCA: %s → %s" % (json.dumps({k: v for k, v in r["marca"].items() if k != "donde"}, ensure_ascii=False), "proyecto.py (solo este vídeo)" if r["marca"]["donde"] == "video" else "marca.json + preferencias.md del creador"))
print("COLOR: %s · %s" % ("look " + r["look"] if r.get("look") else "directo, sin look",
      f"{COLOR['log']['n']} brutos en Log por metadatos (se revelan solos)" if COLOR["log"]["n"] else "sin Log por metadatos (paso0 lo confirma con la imagen)"))
print("→ trabajo/arranque.json y proyecto.py")
