"""arranque.py [--espera 600] [--sin-abrir] [--estilo X]: la VENTANA DE ARRANQUE de un vídeo (SKILL.md § 2, paso 0).
Se lanza desde la carpeta del vídeo (out/<slug>/), con paso0_preparar.py ya en segundo plano, y EN SEGUNDO PLANO también:
abre en el navegador una página local («Configuración de edición») con lo del creador recomendado (estilo, recursos) y lo
que hay en los brutos, espera a que el creador pulse Empezar (o a que se acabe la cuenta atrás) y termina.

Resultado: trabajo/arranque.json, `ESTILO` y una línea `# Arranque (...)` en proyecto.py, y una línea ARRANQUE: en la salida.
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
try:
    sys.path.insert(0, os.path.dirname(AQUI)); from git_bash import BASH          # en Windows, Git Bash (no el de WSL)
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
        "recursos": recursos_estado(),
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
    out = {"fecha": datetime.datetime.now().isoformat(timespec="seconds"), "por_tiempo": por_tiempo,
           "estilo": estilo or None, "recursos": recursos,
           "stock_sin_confirmar": (recursos in ("libreria_stock", "stock")) and not por_tiempo,
           "brutos": brutos, "otra": otra}
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
    open("proyecto.py", "w", encoding="utf-8", newline="\n").write(t)
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
print("→ trabajo/arranque.json y proyecto.py")
