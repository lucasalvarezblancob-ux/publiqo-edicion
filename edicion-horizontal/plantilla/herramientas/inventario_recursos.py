#!/usr/bin/env python3
"""inventario_recursos.py: dar de alta (o mejorar) los recursos de un creador con un CONTEXTO RICO para cada clip.
Igual en edicion-horizontal y edicion-reels. Solo necesita Python 3 y ffmpeg/ffprobe. Se lanza desde la carpeta de edición.

Por qué (Lucas, 2026-11-17): «tanto para los verticales como los horizontales tiene que haber un buen contexto generado de
cada vídeo de recursos. No puede ser un contexto pobre, porque así los timings son buenos a la hora de meter la edición».
Antes el método estaba escrito pero cada agente hacía la ficha a su manera: unas con la línea de tiempo segundo a
segundo y otras con una frase y sin Vibe ni Temas. Esta herramienta prepara el material, reparte los clips en lotes para
los agentes (ENCARGO_RECURSOS.md, al lado de este archivo), junta sus fichas en el índice y NO da por buena una ficha
pobre.

  inventario_recursos.py pendientes             qué clips no tienen ficha, qué fichas son pobres (y por qué), duplicados,
                                                nombres repetidos entre carpetas y fichas de archivos que ya no existen
  inventario_recursos.py preparar [--transcribir] [--por-lote 8] [--max N] [--todo]
                                                material de cada clip pendiente o pobre (técnica, hoja de contactos con
                                                su leyenda de segundos, audio y, con --transcribir, lo que se dice) y los
                                                lotes para los agentes: herramientas/alta_recursos/lote_NN.md. Se retoma
                                                donde se quedó. --todo: también las fichas que ya pasan (re-análisis)
  inventario_recursos.py hoja CLIP INICIO DUR PASO [salida.jpg]
                                                hoja fina de un tramo (p. ej. 0.25 s) para dar tiempos exactos
  inventario_recursos.py juntar [--mover]       mete en INDICE.md las fichas de herramientas/alta_recursos/lote_*.fichas.md
                                                (sustituye la ficha vieja del mismo archivo). --mover: además mueve y
                                                renombra cada archivo a la carpeta y el nombre de su ficha (deshacer:
                                                alta_recursos/deshacer_movimientos.sh)
  inventario_recursos.py comprobar              como «pendientes», pero sale con código 1 si queda algo por resolver

Opciones: --recursos <carpeta> (por defecto: recursos/ en la raíz —reels— o personal/<creador>/recursos —horizontal—;
con varios creadores, --creador <nombre>)."""
import hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

VIDEO = {".mp4", ".mov", ".m4v", ".mxf", ".mts", ".avi", ".mkv", ".webm"}
NO_ENTRAN = {"musica", "sonidos", "fotos", "mapas", "marca"}      # no son clips de recurso (tienen su catálogo o su ficha)
RAIZ = Path.cwd()
args = sys.argv[1:]


def op(k, d=None):
    return args[args.index(k) + 1] if k in args and args.index(k) + 1 < len(args) else d


def carpeta_recursos():
    if op("--recursos"): return Path(op("--recursos")).expanduser()
    if (RAIZ / "recursos").is_dir() and not (RAIZ / ".claude" / "skills" / "edicion-horizontal").exists():
        return RAIZ / "recursos"                                          # edicion-reels: recursos/ en la raíz
    cs = [p for p in sorted((RAIZ / "personal").glob("*/recursos")) if not p.parent.name.startswith("_")]
    if op("--creador"): cs = [p for p in cs if p.parent.name == op("--creador")]
    if len(cs) == 1: return cs[0]
    sin = [p.name for p in sorted((RAIZ / "personal").glob("*/")) if not p.name.startswith("_") and not (p / "recursos").exists()]
    if not cs and sin:
        raise SystemExit(f"No se puede abrir personal/<creador>/recursos de: {', '.join(sin)}. Si sus recursos están en un disco, "
                         "conéctalo y lanza  bash .claude/skills/edicion-horizontal/conectar_disco.sh <creador>  (o pasa --recursos <carpeta>).")
    raise SystemExit("No sé qué carpeta de recursos usar: pasa --recursos <carpeta> o --creador <nombre>."
                     + (f" Hay: {', '.join(p.parent.name for p in cs)}" if cs else ""))


REC = carpeta_recursos()
if not REC.is_dir(): raise SystemExit(f"No puedo abrir {REC} (si está enlazada a un disco, ¿está conectado?)")
INDICE = REC / "INDICE.md"
VERTICAL = (RAIZ / ".claude" / "skills" / "edicion-reels").exists() or (not (RAIZ / ".claude" / "skills" / "edicion-horizontal").exists() and (RAIZ / "recursos") == REC)
LIENZO = "vertical 9:16 (reel)" if VERTICAL else "horizontal 16:9 (YouTube)"
TRAB = RAIZ / "herramientas" / "alta_recursos"


def num(x): return float(x.replace(",", "."))


def clips():
    out = []
    for p in sorted(REC.rglob("*")):
        rel = p.relative_to(REC)
        if p.is_file() and p.suffix.lower() in VIDEO and not any(s.startswith((".", "_")) for s in rel.parts) and rel.parts[0] not in NO_ENTRAN:
            out.append(p)
    return out


# ---------- el índice: fichas = bloques que empiezan con «- `ruta`» (y sus líneas sangradas) ----------
def leer_indice():
    if not INDICE.exists(): return [], {}
    ls = INDICE.read_text(encoding="utf-8").split("\n"); fichas = {}; cab = ""; i = 0
    while i < len(ls):
        l = ls[i]
        if l.startswith("#"): cab = ""
        m = re.match(r"- (?:⚠️[^`]*)?`([^`]+\.(?:%s))`" % "|".join(e[1:] for e in VIDEO), l, re.I)
        if m:
            j = i + 1
            while j < len(ls) and ls[j].startswith(("  ", "\t")) and ls[j].strip(): j += 1
            fichas.setdefault(os.path.basename(m.group(1)).lower(), []).append({"ruta": m.group(1), "i": i, "j": j, "texto": "\n".join(ls[i:j]), "sesion": cab})
            i = j; continue
        if not l.startswith("- ") and l.strip() and not l.startswith("|"): cab += " " + l      # cabecera de sesión: lo común
        i += 1
    return ls, fichas


def sondear(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(p)], capture_output=True, text=True)
    try: d = json.loads(r.stdout)
    except ValueError: return {"error": r.stderr.strip()[:200]}
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {}); a = any(s.get("codec_type") == "audio" for s in d.get("streams", []))
    rot = 0
    for sd in v.get("side_data_list", []) or []:
        if "rotation" in sd: rot = int(float(sd["rotation"]))
    rot = rot or int(float((v.get("tags") or {}).get("rotate", 0)))
    w, h = v.get("width", 0), v.get("height", 0)
    if abs(rot) % 180 == 90: w, h = h, w
    fr = v.get("avg_frame_rate", "0/1").split("/"); fps = round(float(fr[0]) / float(fr[1]), 2) if len(fr) == 2 and float(fr[1]) else 0
    return {"duracion": round(float(d.get("format", {}).get("duration", 0)), 2), "ancho": w, "alto": h, "fps": fps,
            "hdr": v.get("color_transfer") in ("arib-std-b67", "smpte2084"), "audio": a, "codec": v.get("codec_name"),
            "grabado": (d.get("format", {}).get("tags") or {}).get("creation_time", "") or (v.get("tags") or {}).get("creation_time", "")}


# ---------- calidad de una ficha ----------
RANGO = re.compile(r"(\d+(?:[.,]\d+)?)\s*(?:–|-|—)\s*(\d+(?:[.,]\d+)?)")
PUNTO = re.compile(r"(?:≈\s*|·\s*|\b)(\d+(?:[.,]\d+)?)\s*(?:s\b|\+)")


def duracion_ficha(f, p):
    m = re.search(r"\(([^)]*?)(\d+(?:[.,]\d+)?)\s*s\b", f["texto"].split("\n")[0])
    if m: return num(m.group(2))
    return sondear(p)["duracion"] if p else 0


def pobre(f, p):
    """Lista de motivos por los que una ficha NO vale (vacía = vale)."""
    t = f["texto"]; ses = f["sesion"]; mot = []; dur = duracion_ficha(f, p)
    cuerpo = re.sub(r"`[^`]+`", "", t)
    if len(re.findall(r"\w+", cuerpo)) < 35: mot.append("descripción corta (< 35 palabras): falta qué se ve, quién, dónde, encuadre")
    tramos = [(num(a), num(b)) for a, b in RANGO.findall(cuerpo) if num(a) < num(b) <= (dur or 1e9) + 1]
    puntos = [num(x) for x in PUNTO.findall(cuerpo)]
    if dur:
        cub = sorted(tramos); tot = 0; fin = 0
        for a, b in cub:
            a = max(a, fin)
            if b > a: tot += b - a; fin = b
        cobertura = (tot + len(puntos) * 0.5) / dur
        minimo = 0.7 if dur <= 180 else 0.5
        if cobertura < minimo: mot.append(f"línea de tiempo pobre: cubre el {min(cobertura, 1) * 100:.0f} % de {dur:.0f} s (mínimo {minimo * 100:.0f} %): cada tramo con su segundo, también lo que no sirve")
        if dur > 20 and len(tramos) < max(2, dur / 15): mot.append(f"pocos tramos ({len(tramos)}) para {dur:.0f} s: uno cada ~10–15 s como mucho")
    if "**útil" not in t.lower() and not re.search(r"\*\*\d", t): mot.append("sin tramos útiles marcados (**Útil** o lo mejor en negrita)")
    if "vibe" not in (t + ses).lower(): mot.append("sin **Vibe** (sitio, luz, época, energía)")
    temas = re.search(r"\*\*Temas\*\*:?\s*(.+)", t + "\n" + ses)
    if not temas: mot.append("sin **Temas** (3–5 frases de voz en las que encaja)")
    elif len(re.findall(r"«[^»]+»", temas.group(1))) + len(re.split(r";|·", temas.group(1))) - 1 < 2: mot.append("**Temas** con menos de 2 frases")
    if not re.search(r"audio", t + ses, re.I): mot.append("sin **Audio** (sirve / quitar y por qué)")
    if VERTICAL and not re.search(r"outfit|ropa|camiseta|sudadera|sin camiseta|pantal", t + ses, re.I): mot.append("sin **Outfit** (si sale una persona)")
    return mot


def huella(p):
    h = hashlib.sha1(); h.update(str(p.stat().st_size).encode())
    with open(p, "rb") as fh: h.update(fh.read(4 << 20))
    return h.hexdigest()


def estado():
    cs = clips(); _, fichas = leer_indice(); por_nombre = {}
    for c in cs: por_nombre.setdefault(c.name.lower(), []).append(c)
    sin, pobres, ok = [], [], []
    abrev = [(k.split("…", 1)[1], v) for k, v in fichas.items() if "…" in k]   # rutas abreviadas: «espalda/…_jalon.MOV»
    usadas = set()
    for c in cs:
        f = fichas.get(c.name.lower()) or next((v for suf, v in abrev if suf and c.name.lower().endswith(suf)), None)
        if f: usadas.add(os.path.basename(f[0]["ruta"]).lower())
        if not f: sin.append(c); continue
        m = pobre(f[0], c)
        (pobres if m else ok).append((c, m))
    repes = {n: v for n, v in por_nombre.items() if len(v) > 1}
    huerf = [f[0]["ruta"] for n, f in fichas.items() if n not in por_nombre and n not in usadas]
    dup = {}
    for c in cs: dup.setdefault(huella(c), []).append(c)
    dup = [v for v in dup.values() if len(v) > 1]
    return cs, sin, pobres, ok, repes, huerf, dup


def informe(salir=False):
    cs, sin, pobres, ok, repes, huerf, dup = estado()
    print(f"{REC}  ·  lienzo {LIENZO}\n{len(cs)} clips: {len(ok)} con ficha buena, {len(pobres)} con ficha POBRE, {len(sin)} SIN ficha")
    for c in sin: print(f"  SIN FICHA  {c.relative_to(REC)}")
    for c, m in pobres: print(f"  POBRE      {c.relative_to(REC)}\n             - " + "\n             - ".join(m))
    for n, v in repes.items(): print(f"  NOMBRE REPETIDO entre carpetas (el plan los pide por nombre): {', '.join(str(x.relative_to(REC)) for x in v)}")
    for v in dup: print(f"  DUPLICADO (mismo archivo): {', '.join(str(x.relative_to(REC)) for x in v)}")
    for r in huerf: print(f"  FICHA SIN ARCHIVO: {r} (¿movido o borrado? corrige la ruta o quita la ficha)")
    if not (sin or pobres or repes or dup or huerf): print("✓ Todo clip tiene ficha completa.")
    elif not salir: print(f"\nSiguiente: inventario_recursos.py preparar  →  un agente por lote con {Path(__file__).with_name('ENCARGO_RECURSOS.md')}")
    if salir: sys.exit(1 if (sin or pobres or repes or dup or huerf) else 0)


# ---------- material para los agentes ----------
def paso_hoja(d): return 1 if d <= 60 else 2 if d <= 180 else 4 if d <= 600 else 8


def hoja(clip, ini, dur, paso, sal):
    """Hoja de contactos: 6 columnas, una celda cada `paso` s desde `ini`; leyenda de segundos en .txt al lado."""
    n = max(1, int(dur / paso + 0.999)); cols = 6; filas = (n + cols - 1) // cols
    vf = f"fps=1/{paso},scale=360:-2,tile={cols}x{filas}:padding=4:margin=4"
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{ini}", "-t", f"{dur}", "-i", str(clip), "-vf", vf, "-frames:v", "1", "-q:v", "4", str(sal)], capture_output=True, text=True)
    if r.returncode: raise RuntimeError(r.stderr.strip()[:300])
    ley = [f"Hoja de {clip.name}: {cols} columnas, {filas} filas; celda k (de 0, leyendo por filas) = segundo {ini} + k × {paso}"]
    ley += [f"fila {f + 1}: " + " · ".join(f"{ini + (f * cols + c) * paso:g}s" for c in range(cols) if f * cols + c < n) for f in range(filas)]
    Path(str(sal)[:-4] + ".txt").write_text("\n".join(ley) + "\n", encoding="utf-8")


def audio(clip):
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "info", "-i", str(clip), "-vn", "-af", "silencedetect=n=-40dB:d=0.6,volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    media = re.search(r"mean_volume: (-?[\d.]+)", r); pico = re.search(r"max_volume: (-?[\d.]+)", r)
    sil = sum(float(x) for x in re.findall(r"silence_duration: ([\d.]+)", r))
    return {"media_db": float(media.group(1)) if media else None, "pico_db": float(pico.group(1)) if pico else None, "silencio_s": round(sil, 1)}


def transcribir(clip, sal):
    h = RAIZ / "herramientas"
    py = next((p for p in (h / ".venv/bin/python", h / ".venv/Scripts/python.exe") if p.exists()), None)
    if (h / "transcribir.py").exists() and py:
        subprocess.run([str(py), str(h / "transcribir.py"), str(clip), str(sal) + ".json"], capture_output=True); return Path(str(sal) + ".txt").exists()
    if (h / "transcribir.sh").exists():
        from git_bash import BASH
        r = subprocess.run([BASH, str(h / "transcribir.sh"), str(clip), str(sal)], capture_output=True, text=True)
        Path(str(sal) + ".txt").write_text(r.stdout, encoding="utf-8"); return bool(r.stdout.strip())
    return False


def preparar():
    cs, sin, pobres, ok, *_ = estado()
    cola = sin + [c for c, _ in pobres] + ([c for c, _ in ok] if "--todo" in args else [])
    if op("--max"): cola = cola[:int(op("--max"))]
    if not cola: print("No hay clips pendientes ni fichas pobres."); return
    TRAB.mkdir(parents=True, exist_ok=True); _, fichas = leer_indice(); info = {}
    for k, c in enumerate(cola, 1):
        d = TRAB / "material" / re.sub(r"[^\w.-]", "_", str(c.relative_to(REC))); d.mkdir(parents=True, exist_ok=True)
        if not (d / "tecnica.json").exists():
            t = sondear(c); t["audio_medido"] = audio(c) if t.get("audio") else None
            (d / "tecnica.json").write_text(json.dumps(t, indent=1, ensure_ascii=False), encoding="utf-8")
        t = json.loads((d / "tecnica.json").read_text(encoding="utf-8")); dur = t.get("duracion") or 0
        if not (d / "hoja.jpg").exists() and dur:
            try: hoja(c, 0, dur, paso_hoja(dur), d / "hoja.jpg")
            except RuntimeError as e: print(f"  ⚠️ {c.name}: no sale la hoja ({e})")
        am = t.get("audio_medido") or {}
        habla = am.get("media_db") is not None and am["media_db"] > -45 and dur and am["silencio_s"] < 0.7 * dur
        if "--transcribir" in args and habla and not (d / "dice.txt").exists(): transcribir(c, d / "dice")
        info[c] = (d, t)
        print(f"  [{k}/{len(cola)}] {c.relative_to(REC)}  ({dur:.0f} s)")
    # lotes: por carpeta y fecha (misma sesión junta), hasta N clips o ~6 min de material
    porlote = int(op("--por-lote", 8)); grupos = {}
    for c in cola: grupos.setdefault((c.parent, (info[c][1].get("grabado") or "")[:10]), []).append(c)
    lotes, act, seg = [], [], 0
    for g in grupos.values():
        for c in g:
            dur = info[c][1].get("duracion") or 0
            if act and (len(act) >= porlote or seg + dur > 360): lotes.append(act); act, seg = [], 0
            act.append(c); seg += dur
    if act: lotes.append(act)
    previos = len(list(TRAB.glob("lote_*.md"))) - len(list(TRAB.glob("lote_*.fichas.md")))
    enc = Path(__file__).with_name("ENCARGO_RECURSOS.md")
    for n, lote in enumerate(lotes, previos + 1):
        txt = [f"# Lote {n:02d} — {len(lote)} clips · lienzo {LIENZO}", "",
               f"Encargo: {enc} (léelo entero antes de empezar). Escribe las fichas en `{TRAB / f'lote_{n:02d}.fichas.md'}`.",
               f"Carpeta de recursos: `{REC}` · índice: `{INDICE}` (míralo para ver las carpetas y el estilo)", ""]
        for c in lote:
            d, t = info[c]
            txt += [f"## `{c.relative_to(REC)}`", f"- archivo: `{c}`",
                    f"- técnica: {t.get('duracion')} s, {t.get('ancho')}×{t.get('alto')}, {t.get('fps')} fps, {'HDR' if t.get('hdr') else 'SDR'}, {t.get('codec')}, grabado {t.get('grabado') or '¿?'}"
                    + (f"; audio media {t['audio_medido']['media_db']} dB, silencio {t['audio_medido']['silencio_s']} s" if t.get("audio_medido") else "; sin audio"),
                    f"- hoja: `{d / 'hoja.jpg'}` (leyenda de segundos: `{d / 'hoja.txt'}`)"]
            if (d / "dice.txt").exists(): txt.append(f"- lo que se dice: `{d / 'dice.txt'}`")
            f = fichas.get(c.name.lower())
            if f: txt += ["- ficha actual (POBRE: rehazla entera, conservando lo que esté bien medido):", "", "```", f[0]["texto"], "```"]
            txt.append("")
        (TRAB / f"lote_{n:02d}.md").write_text("\n".join(txt), encoding="utf-8")
    print(f"\n{len(lotes)} lotes en {TRAB}/lote_NN.md. Un agente por lote (hasta 4–5 a la vez en Mac, 2 en Windows con 16 GB),")
    print(f"con el encargo {enc}. Al acabar: inventario_recursos.py juntar  y  inventario_recursos.py comprobar")


# ---------- juntar las fichas de los agentes en el índice ----------
def juntar():
    nuevos = sorted(TRAB.glob("lote_*.fichas.md"))
    if not nuevos: raise SystemExit(f"No hay fichas en {TRAB}/lote_*.fichas.md")
    ls, fichas = leer_indice()
    if not ls: ls = ["# Índice de recursos", "", "Tiempos en segundos del archivo original. Método: la skill → base/recursos.md.", ""]
    bloques = []
    for f in nuevos:
        t = f.read_text(encoding="utf-8").split("\n"); i = 0
        while i < len(t):
            if t[i].startswith("- `"):
                j = i + 1
                while j < len(t) and t[j].startswith(("  ", "\t")) and t[j].strip(): j += 1
                bloques.append(t[i:j]); i = j
            else: i += 1
    movs = []; reemplazos = {}; nuevas = {}
    for b in bloques:
        ruta = re.match(r"- `([^`]+)`", b[0]).group(1); nombre = os.path.basename(ruta).lower()
        orig = next((re.search(r"`([^`]+)`", l).group(1) for l in b if re.match(r"\s+(?:\*\*)?Original(?:\*\*)?:", l) and "`" in l), None)
        if "--mover" in args and orig and orig != ruta:
            src, dst = REC / orig, REC / ruta
            if src.exists() and not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True); shutil.move(str(src), str(dst)); movs.append((dst, src))
            elif not src.exists(): print(f"  ⚠️ no existe {orig}: no se mueve")
            else: print(f"  ⚠️ ya existe {ruta}: no se mueve {orig}")
        clave = os.path.basename(orig).lower() if orig and os.path.basename(orig).lower() in fichas else nombre
        b = [l for l in b if not re.match(r"\s+(?:\*\*)?Original(?:\*\*)?:", l)] + [f"  Original: `{orig}`"] if orig and orig != ruta else b
        if clave in fichas: reemplazos[fichas[clave][0]["i"]] = (fichas[clave][0]["j"], b)
        else: nuevas.setdefault(ruta.split("/")[0] + "/", []).append(b)
    out, i = [], 0
    while i < len(ls):
        if i in reemplazos: j, b = reemplazos[i]; out += b; i = j
        else: out.append(ls[i]); i += 1
    for sec, bs in nuevas.items():
        k = next((n for n, l in enumerate(out) if l.strip() == f"## {sec}"), None)
        add = [l for b in bs for l in b]
        if k is None: out += ["", f"## {sec}"] + add
        else:
            e = k + 1
            while e < len(out) and not out[e].startswith("## "): e += 1
            while e > k + 1 and not out[e - 1].strip(): e -= 1
            out[e:e] = add
    INDICE.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    if movs:
        (TRAB / "deshacer_movimientos.sh").write_text("#!/usr/bin/env bash\n" + "".join(f'mv -n "{a}" "{b}"\n' for a, b in reversed(movs)), encoding="utf-8")
    for f in nuevos: f.rename(f.with_suffix(".juntado.md"))
    print(f"{len(bloques)} fichas en {INDICE} ({len(reemplazos)} sustituidas, {sum(map(len, nuevas.values()))} nuevas)" + (f"; {len(movs)} archivos movidos (deshacer: {TRAB / 'deshacer_movimientos.sh'})" if movs else ""))
    informe()


if __name__ == "__main__":
    if not args or args[0] in ("-h", "--help"): print(__doc__); sys.exit()
    if args[0] == "pendientes": informe()
    elif args[0] == "comprobar": informe(salir=True)
    elif args[0] == "preparar": preparar()
    elif args[0] == "juntar": juntar()
    elif args[0] == "hoja" and len(args) >= 5:
        c = Path(args[1]); sal = Path(args[5]) if len(args) > 5 and not args[5].startswith("--") else TRAB / f"fino_{c.stem}_{args[2]}.jpg"
        sal.parent.mkdir(parents=True, exist_ok=True); hoja(c, float(args[2]), float(args[3]), float(args[4]), sal); print(sal, "+ leyenda", str(sal)[:-4] + ".txt")
    else: print(__doc__)
