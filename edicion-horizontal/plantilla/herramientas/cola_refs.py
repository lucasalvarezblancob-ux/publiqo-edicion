#!/usr/bin/env python3
"""Cola de referencias para estudiar su EDICIÓN: baja, precalcula, espera la ficha y borra. Reanudable.

Desde la raíz de la carpeta de edición (PY = herramientas/.venv/Scripts/python.exe en Windows, .venv/bin/python en mac):
  PY herramientas/cola_refs.py añadir --estilo vlog URL [URL…]   [--creador slug] [--tipo dinamicos]
  PY herramientas/cola_refs.py avanzar [--max-abiertos 2] [--ram-min 25] [--ligero]
        baja y precalcula los siguientes hasta tener --max-abiertos vídeos «listos para ver» (sin ficha). Se para
        si la RAM libre baja de --ram-min % o queda poco disco, y lo dice. Si algo falla, se reintenta (3 veces).
  PY herramientas/cola_refs.py hecho <id|archivo>      la ficha está escrita: borra el mp4 y lo pesado (stems)
  PY herramientas/cola_refs.py saltar <id> "motivo"    no se puede (privado, región…): queda apuntado
  PY herramientas/cola_refs.py reintentar <id>         uno en «error» vuelve a «bajado» (o «pendiente») tras arreglarlo
  PY herramientas/cola_refs.py estado                  tabla de la cola

Estado en refs/<tipo>/_analisis/cola.json. Mientras trabaja escribe un latido (refs/<tipo>/_analisis/latido.json: hora,
pid, paso y vídeo) cada 20 s: el vigilante de Windows (herramientas/windows/vigilante.ps1) lo lee para saber si
algo se ha colgado; si mata un proceso, deja relanzar.flag y la siguiente llamada a «avanzar» repite ese paso.
Pasos de cada vídeo: pendiente → bajado → precalculado (cortes, transcripción, hojas, LUFS, audio, efectos) →
listo (para que Claude lo vea y escriba la ficha) → hecho (mp4 borrado) | saltado."""
import argparse, json, os, re, shutil, subprocess, sys, threading, time
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
sys.path.insert(0, AQUI)
from git_bash import BASH          # en Windows, el de Git Bash (el «bash» de WSL no vale)
ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="orden", required=True)
x = sub.add_parser("añadir"); x.add_argument("urls", nargs="+"); x.add_argument("--estilo", required=True)
x.add_argument("--creador", default=""); x.add_argument("--tipo", default="dinamicos")
x = sub.add_parser("avanzar"); x.add_argument("--max-abiertos", type=int, default=2); x.add_argument("--ram-min", type=float, default=25)
x.add_argument("--disco-min", type=float, default=20); x.add_argument("--ligero", action="store_true"); x.add_argument("--tipo", default="dinamicos")
x = sub.add_parser("hecho"); x.add_argument("cual"); x.add_argument("--tipo", default="dinamicos")
x = sub.add_parser("saltar"); x.add_argument("cual"); x.add_argument("motivo"); x.add_argument("--tipo", default="dinamicos")
x = sub.add_parser("estado"); x.add_argument("--tipo", default="dinamicos")
x = sub.add_parser("reintentar"); x.add_argument("cual"); x.add_argument("--tipo", default="dinamicos")
a = ap.parse_args()
if not os.path.exists("personal/LEEME.md"): raise SystemExit("Lánzalo desde la raíz de la carpeta de edición (la que tiene personal/LEEME.md)")
AN = f"refs/{a.tipo}/_analisis"; os.makedirs(AN, exist_ok=True)
COLA, LATIDO, FLAG = f"{AN}/cola.json", f"{AN}/latido.json", f"{AN}/relanzar.flag"
ahora = lambda: datetime.now().isoformat(timespec="seconds")


def leer():
    return json.load(open(COLA, encoding="utf-8")) if os.path.exists(COLA) else []


def guardar(c):
    tmp = COLA + ".tmp"; json.dump(c, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(tmp, COLA)


class Bloqueo:
    """Una sola orden escribe cola.json a la vez (avanzar tarda minutos; hecho/añadir/saltar pueden ir mientras)."""
    def __enter__(s):
        s.f = COLA + ".lock"; t0 = time.time()
        while True:
            try: os.close(os.open(s.f, os.O_CREAT | os.O_EXCL | os.O_WRONLY)); return s
            except FileExistsError:
                try:
                    if time.time() - os.path.getmtime(s.f) > 120: os.remove(s.f); continue     # bloqueo huérfano
                except OSError: pass
                if time.time() - t0 > 120: raise SystemExit("cola.json lleva 2 min bloqueada: borra refs/<tipo>/_analisis/cola.json.lock si no hay otra orden en marcha")
                time.sleep(0.3)
    def __exit__(s, *x):
        try: os.remove(s.f)
        except OSError: pass


def guardar_entrada(sig):
    """avanzar: relee la cola y cambia SOLO esta entrada. Si mientras tanto otra orden la marcó hecha o saltada, gana esa."""
    with Bloqueo():
        c2 = leer()
        for k, e in enumerate(c2):
            if e["id"] == sig["id"]:
                if e["estado"] in ("hecho", "saltado") and sig["estado"] not in ("hecho", "saltado"): return
                c2[k] = {**e, **sig}; break
        else: c2.append(sig)
        guardar(c2)


def vid(u):
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})", u); return m.group(1) if m else None


def buscar(c, cual):
    for e in c:
        if cual in (e["id"], e.get("archivo"), os.path.basename(e.get("archivo") or "")): return e
    raise SystemExit(f"No está en la cola: {cual}")


def ram_libre_pct():
    try:
        import psutil; return psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    except Exception: pass
    try:
        if os.name == "nt":
            o = subprocess.run(["powershell", "-NoProfile", "-Command",
                                "$o=Get-CimInstance Win32_OperatingSystem; [math]::Round($o.FreePhysicalMemory*100/$o.TotalVisibleMemorySize,1)"],
                               capture_output=True, text=True, timeout=20).stdout.strip()
            return float(o.replace(",", "."))
        if sys.platform == "darwin":
            o = subprocess.run(["memory_pressure"], capture_output=True, text=True, timeout=20).stdout
            m = re.search(r"free percentage:\s*(\d+)", o); return float(m.group(1)) if m else 100.0
        mi = dict(l.split(":", 1) for l in open("/proc/meminfo")); return 100 * int(mi["MemAvailable"].split()[0]) / int(mi["MemTotal"].split()[0])
    except Exception: return 100.0


class Latido:
    def __init__(s): s.paso, s.video, s.vivo = "", "", True; threading.Thread(target=s.bucle, daemon=True).start()
    def bucle(s):
        while s.vivo:
            try: json.dump({"hora": ahora(), "epoch": time.time(), "pid": os.getpid(), "paso": s.paso, "video": s.video},
                           open(LATIDO, "w", encoding="utf-8"))
            except Exception: pass
            time.sleep(20)


def correr(cmd, lat, paso, video, limite):
    lat.paso, lat.video = paso, video
    print(f"  · {paso}: {video}", flush=True)
    try:
        r = subprocess.run(cmd, timeout=limite, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        return r.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"    ⚠️  {paso} pasó de {limite // 60} min: lo corto y se reintentará"); return False


if a.orden in ("añadir", "reintentar", "hecho", "saltar"):
    import atexit; _bl = Bloqueo().__enter__(); atexit.register(_bl.__exit__)     # se suelta aunque la orden falle
c = leer()
if a.orden == "añadir":
    for u in a.urls:
        i = vid(u)
        if not i: print(f"  ✗ no reconozco {u}"); continue
        e = next((e for e in c if e["id"] == i), None)
        if e:
            if a.estilo not in e["estilos"]: e["estilos"].append(a.estilo)
            print(f"  = {i} ya estaba (estilos: {', '.join(e['estilos'])})"); continue
        c.append({"id": i, "url": f"https://www.youtube.com/watch?v={i}", "estilos": [a.estilo], "creador": a.creador,
                  "estado": "pendiente", "archivo": None, "analisis": None, "intentos": 0, "error": None, "cambiado": ahora()})
        print(f"  + {i} ({a.estilo})")
    guardar(c)

elif a.orden == "estado":
    for e in c:
        print(f"{e['id']}  {e['estado']:<12} {'/'.join(e['estilos']):<12} {os.path.basename(e.get('archivo') or '-'):<55} "
              f"{('⚠️ ' + e['error'][:60]) if e.get('error') else ''}")
    print(f"\n{sum(e['estado'] == 'hecho' for e in c)}/{len(c)} hechos · listos para ver: "
          f"{', '.join(e['id'] for e in c if e['estado'] == 'listo') or 'ninguno'} · RAM libre {ram_libre_pct():.0f} %")

elif a.orden == "reintentar":
    e = buscar(c, a.cual); e["estado"] = "bajado" if e.get("archivo") and os.path.exists(e["archivo"]) else "pendiente"
    e["intentos"], e["error"], e["cambiado"] = 0, None, ahora(); guardar(c); print(f"↻ {e['id']} vuelve a «{e['estado']}»")

elif a.orden in ("hecho", "saltar"):
    e = buscar(c, a.cual)
    if a.orden == "hecho":
        if e.get("archivo") and os.path.exists(e["archivo"]): os.remove(e["archivo"])
        if e.get("analisis") and os.path.isdir(f"{e['analisis']}/stems"): shutil.rmtree(f"{e['analisis']}/stems", ignore_errors=True)
        e["estado"] = "hecho"; print(f"✓ {e['id']}: mp4 y stems borrados ({shutil.disk_usage('.').free / 1e9:.0f} GB libres)")
    else:
        e["estado"], e["error"] = "saltado", a.motivo; print(f"– {e['id']} saltado: {a.motivo}")
    e["cambiado"] = ahora(); guardar(c)

elif a.orden == "avanzar":
    pre = open(f"{AQUI}/precalcular_ref.sh", encoding="utf-8").read()
    if "--ligero" not in pre or "escuchar_sfx.py" not in pre:
        raise SystemExit("herramientas/precalcular_ref.sh es una versión vieja (sin intro fotograma a fotograma, LUFS, audio ni "
                         "efectos): actualizar.sh no lo tocó porque estaba cambiado en local. Cópialo de la plantilla de la skill "
                         "(.claude/skills/edicion-horizontal/plantilla/herramientas/precalcular_ref.sh) y vuelve a lanzar.")
    if os.path.exists(FLAG):
        print("El vigilante cortó un paso: se repite."); os.remove(FLAG)
    lat = Latido()
    try:
        while True:
            c = leer()
            abiertos = [e for e in c if e["estado"] in ("bajado", "precalculado", "listo")]
            listos = [e for e in c if e["estado"] == "listo"]
            sig = next((e for e in c if e["estado"] in ("bajado", "precalculado")), None) or \
                  (next((e for e in c if e["estado"] == "pendiente" and e["intentos"] < 3), None) if len(abiertos) < a.max_abiertos else None)
            if not sig:
                print(f"Nada más por ahora: {len(listos)} listo(s) para ver ({', '.join(e['id'] for e in listos) or '-'}); "
                      f"{sum(e['estado'] == 'pendiente' for e in c)} pendiente(s)."); break
            ram = ram_libre_pct(); disco = shutil.disk_usage(".").free / 1e9
            if ram < a.ram_min: print(f"⏸  RAM libre {ram:.0f} % (< {a.ram_min}): espero a que baje la carga y vuelve a lanzarme."); break
            if sig["estado"] == "pendiente" and disco < a.disco_min: print(f"⏸  Solo {disco:.0f} GB libres: marca como hechos los ya vistos."); break
            if sig["estado"] == "pendiente":
                cmd = [PY, f"{AQUI}/bajar_ref.py", sig["url"], "--estilo", "/".join(sig["estilos"]), "--tipo", a.tipo]
                if sig.get("creador"): cmd += ["--creador", sig["creador"]]
                lat.paso, lat.video = "bajar", sig["id"]; print(f"  · bajar: {sig['id']}", flush=True)
                try:
                    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600)
                    ult = [l for l in r.stdout.splitlines() if l.startswith("{")]
                    ok = r.returncode == 0 and ult
                except subprocess.TimeoutExpired: ok, r = False, None
                if ok:
                    info = json.loads(ult[-1]); sig.update(archivo=info["archivo"], titulo=info["titulo"], canal=info["canal"],
                                                           duracion_s=info["duracion_s"], estado="bajado", error=None)
                    sig["analisis"] = f"{AN}/{os.path.splitext(os.path.basename(info['archivo']))[0]}"
                else:
                    sig["intentos"] += 1; sig["error"] = ((r.stderr or r.stdout)[-300:] if r else "tiempo agotado bajando")
                    if sig["intentos"] >= 3: sig["estado"] = "saltado"
            elif sig["estado"] == "bajado":
                cmd = [BASH, f"{AQUI}/precalcular_ref.sh", sig["archivo"], sig["analisis"]] + (["--ligero"] if a.ligero else [])
                if correr(cmd, lat, "precalcular", sig["id"], 4 * 3600): sig["estado"], sig["error"] = "listo", None
                else:
                    sig["intentos"] += 1; sig["error"] = "falló el precálculo (se repite desde el paso que faltaba)"
                    if sig["intentos"] >= 4:
                        sig["estado"] = "error"; sig["error"] = "el precálculo ha fallado 4 veces: mira el error, arréglalo y devuélvelo a «bajado»"
                        sig["cambiado"] = ahora(); guardar_entrada(sig); print(f"✗ {sig['id']}: {sig['error']}"); break
            sig["cambiado"] = ahora(); guardar_entrada(sig)
    finally:
        lat.vivo = False
        try: json.dump({"hora": ahora(), "epoch": time.time(), "pid": None, "paso": "parado", "video": ""}, open(LATIDO, "w", encoding="utf-8"))
        except Exception: pass
