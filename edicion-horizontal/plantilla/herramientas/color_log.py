#!/usr/bin/env python3
"""color_log.py: brutos grabados en LOG (DJI D-Log M, Apple Log, S-Log3…) → su LUT de conversión a Rec.709, y los LOOKS
creativos opcionales. Cambio global G009 (Lucas, 2026-11-26: «si está grabado en logarítmico, obviamente se le pondrá un
LUT, porque si no el vídeo sale muy gris»). Lo usan comun.py (fuente/sdr), paso0_preparar.py y arranque.py.

Dos cosas distintas:
  · REVELAR el Log (técnico, siempre y sin preguntar): cada clip en Log se convierte con el LUT de su perfil
    (herramientas/luts/, el oficial del fabricante). Esto no es «tocar el color del bruto»: sin él se ve gris.
  · LOOK creativo (opcional, se pregunta en la ventana de arranque): por defecto NINGUNO. Si se elige, va encima de todo.

Detección del Log, de más fiable a menos:
  1. metadatos (ffprobe; exiftool si está; el .SRT de DJI al lado): texto «D-Log M», «S-Log3», «Apple Log»…  → seguro
  2. pistas (10 bits + cámara que graba en Log + sin etiqueta HDR) Y la imagen (negros levantados, sin altas luces,
     poca saturación)                                                                                        → probable
  Los «probables» también se revelan, pero avisan: hay que mirar el antes/después (color_log.py comparar …).
  Forzar a mano (proyecto.py o plan.py): LOG_CLIPS = {"DJI_0012": "dlogm", "IMG_0040": None}  (None = no es Log).

Uso:
  color_log.py BRUTO [BRUTO…]           detecta y dice perfil, motivo y LUT
  color_log.py luts                     qué LUT hay y cuáles faltan (y de dónde bajarlos)
  color_log.py comparar BRUTO SEG SALIDA.jpg [--look nombre]   antes | después del mismo fotograma, lado a lado
  color_log.py looks                    genera los looks de la casa (herramientas/luts/looks/*.cube) si faltan
"""
import glob, json, math, os, re, shutil, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
LUTS = os.path.join(AQUI, "luts")
LOOKS = os.path.join(LUTS, "looks")

# perfil → nombre, regex sobre los metadatos (en minúsculas), regex sobre el NOMBRE del .cube (normalizado: sin - _ espacios)
PERFILES = {
    "dlogm":    ("DJI D-Log M",     r"d-?log[\s_-]?m\b|dlog_m",            r"dlogm"),
    "dlog":     ("DJI D-Log",       r"\bd-?log\b(?![\s_-]?m)",             r"dlog(?!m)"),
    "applelog": ("Apple Log",       r"apple[\s_-]?log",                    r"applelog"),
    "slog3":    ("Sony S-Log3",     r"s-?log3",                            r"slog3"),
    "slog2":    ("Sony S-Log2",     r"s-?log2",                            r"slog2"),
    "vlog":     ("Panasonic V-Log", r"\bv-log\b|\bv_log\b",                r"vlog"),
    "clog3":    ("Canon C-Log3",    r"c-?log3",                            r"clog3"),
    "clog2":    ("Canon C-Log2",    r"c-?log2",                            r"clog2"),
    "clog":     ("Canon C-Log",     r"\bc-?log\b(?![23])",                 r"clog(?![23])"),
    "flog2":    ("Fujifilm F-Log2", r"f-?log2",                            r"flog2"),
    "flog":     ("Fujifilm F-Log",  r"\bf-?log\b(?!2)",                    r"flog(?!2)"),
    "nlog":     ("Nikon N-Log",     r"\bn-?log\b",                         r"nlog"),
    "gplog":    ("GoPro Log",       r"gp-?log",                            r"gplog"),
    "logc":     ("ARRI LogC",       r"\blog-?c[34]?\b",                    r"logc"),
}
# Cámaras que graban en Log y, si la imagen lo parece, en qué perfil suele ser.
MARCAS = [(r"\bdji\b|osmo|mavic|avata|^dji_|^ac\d{3}|^dji", "dlogm"), (r"apple|iphone", "applelog"), (r"sony|xavc|^c\d{4}", "slog3"),
          (r"panasonic|lumix|^p\d{7}", "vlog"), (r"canon|^mvi_|^a\d{3}c\d{3}", "clog3"), (r"fujifilm|^dscf", "flog"),
          (r"nikon", "nlog"), (r"gopro|^g[xh]\d{6}|^gopr", "gplog")]
# Umbrales de la IMAGEN (8 bits, rango tv 16–235), sobre 6 fotogramas. Provisionales: se afinan con brutos reales.
UMBRAL_NEGRO = 44        # el 10 % más oscuro no baja de aquí → negros levantados
UMBRAL_BLANCO = 212      # el píxel más claro de los 6 fotogramas no pasa de aquí → sin altas luces
UMBRAL_SAT = 20          # saturación media por debajo → apagado
PAGINAS = {  # dónde bajar el oficial (se baja a mano o lo baja Claude con permiso; nunca se sube al repo de la skill)
    "dlogm": "https://www.dji.com/downloads (busca «<tu cámara> D-Log M to Rec.709 LUT»; Osmo Action 5 Pro: https://www.dji.com/br/downloads/softwares/dji-osmo-action-5-pro-d-log-m-to-rec-709-vivid-lut)",
    "dlog": "https://www.dji.com/downloads (busca «<tu cámara> D-Log to Rec.709 LUT»)",
    "applelog": "https://developer.apple.com/download/all/?q=Apple%20Log (Apple Log Profile / LUT)",
    "slog3": "https://pro.sony/en_IN/technology/professional-video-lut-look-up-table (S-Gamut3.Cine/S-Log3 → 709)",
    "slog2": "https://pro.sony/en_IN/technology/professional-video-lut-look-up-table",
    "vlog": "https://pro-av.panasonic.net/en/cinema_camera_varicam_eva/support/lut/ (VariCam LUT Library, V-Log → V-709)",
    "clog3": "https://www.usa.canon.com (soporte de la cámara → LUT de C-Log3 a BT.709)",
    "clog2": "https://www.usa.canon.com (soporte de la cámara → LUT de C-Log2 a BT.709)",
    "clog": "https://www.usa.canon.com (soporte de la cámara → LUT de C-Log a BT.709)",
    "flog2": "https://www.fujifilm-x.com (soporte → F-Log2 LUT)", "flog": "https://www.fujifilm-x.com (soporte → F-Log LUT)",
    "nlog": "https://downloadcenter.nikonimglib.com (N-Log 3D LUT)", "gplog": "https://community.gopro.com (GoPro Log LUT)",
    "logc": "https://www.arri.com/en/learn-help/learn-help-camera-system/tools/lut-generator",
}
# Looks de la casa: generados aquí (sin licencias de terceros), suaves y respetando la piel.
LOOKS_CASA = {
    "natural": "Contraste y color un pelo más vivos, sin cambiar el tono: «revelado» limpio.",
    "calido": "Cálido de tarde: blancos algo más dorados, sombras neutras, piel protegida.",
    "cine": "Cine suave: sombras hacia azul verdoso y luces cálidas (teal & orange flojo), negros apenas levantados.",
}


def _run(cmd, timeout=120):
    try: return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    except (OSError, subprocess.TimeoutExpired): return None


def sonda(ruta):
    r = _run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", ruta])
    try: return json.loads(r.stdout) if r else {}
    except ValueError: return {}


def _textos(j, ruta):
    """Todo el texto de los metadatos (y del .SRT de DJI, y exiftool si está), en minúsculas."""
    t = []
    for s in j.get("streams", []):
        t += [str(v) for v in (s.get("tags") or {}).values()]
        t += [str(s.get(k, "")) for k in ("color_transfer", "codec_tag_string", "profile")]
    t += [str(v) for v in (j.get("format", {}).get("tags") or {}).values()]
    base = os.path.splitext(ruta)[0]
    for srt in (base + ".SRT", base + ".srt"):
        if os.path.exists(srt):
            try: t.append(open(srt, encoding="utf-8", errors="replace").read(20000))
            except OSError: pass
    if shutil.which("exiftool"):
        r = _run(["exiftool", "-j", "-a", "-G1", "-api", "LargeFileSupport=1", ruta], timeout=60)
        if r and r.stdout: t.append(r.stdout)
    return " | ".join(t).lower()


def _bits(v):
    pf = v.get("pix_fmt", "") or ""
    b = v.get("bits_per_raw_sample")
    if b and str(b).isdigit(): return int(b)
    m = re.search(r"p(\d{2})(le|be)?$", pf)
    return int(m.group(1)) if m else 8


def medir(ruta, dur):
    """Luz y saturación de 6 fotogramas (8 bits): {negro: el 10 % más oscuro (mínimo), blanco: máximo, sat: media}."""
    vals = []
    for k in range(6):
        t = max(0.0, dur * (0.08 + 0.168 * k))
        r = _run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.2f}", "-i", ruta, "-frames:v", "1",
                  "-vf", "scale=320:-2,format=yuv420p,signalstats,metadata=print:file=-", "-f", "null", "-"], timeout=60)
        if not r: continue
        d = dict(re.findall(r"lavfi\.signalstats\.(\w+)=([\d.]+)", r.stdout))
        if "YLOW" in d: vals.append({k2: float(d[k2]) for k2 in ("YLOW", "YMAX", "YHIGH", "SATAVG") if k2 in d})
    if not vals: return None
    vals.sort(key=lambda x: x["SATAVG"])
    return {"negro": min(v["YLOW"] for v in vals), "blanco": max(v["YMAX"] for v in vals),
            "sat": vals[len(vals) // 2]["SATAVG"], "n": len(vals)}


def detectar(ruta, medir_imagen=True):
    """{"perfil": clave|None, "seguro": "metadatos"|"probable"|None, "motivo": str, "hdr": bool, "bits", "matriz", "rango"}"""
    j = sonda(ruta); vs = [s for s in j.get("streams", []) if s.get("codec_type") == "video"]
    v = vs[0] if vs else {}
    out = {"perfil": None, "seguro": None, "motivo": "", "bits": _bits(v),
           "matriz": "bt2020" if "2020" in (v.get("color_space") or "") else "bt709",
           "rango": "pc" if v.get("color_range") == "pc" else "tv",
           "hdr": (v.get("color_transfer") or "") in ("arib-std-b67", "smpte2084")}
    if out["hdr"]: out["motivo"] = "HDR (HLG/PQ): va por sdr.py con libplacebo, no por LUT"; return out
    txt = _textos(j, ruta)
    for clave, (nombre, rx, _) in PERFILES.items():
        m = re.search(rx, txt)
        if m:
            out.update(perfil=clave, seguro="metadatos", motivo=f"metadatos: «{txt[max(0, m.start() - 30):m.end() + 10].strip()}»")
            return out
    # pistas: marca/cámara (metadatos o nombre del archivo)
    nombre = os.path.basename(ruta).lower()
    cand = next((p for rx, p in MARCAS if re.search(rx, txt) or re.search(rx, nombre)), None)
    if not (cand or out["bits"] >= 10) or not medir_imagen:
        out["motivo"] = "sin señales de Log"; return out
    try: dur = float(j.get("format", {}).get("duration") or 0)
    except ValueError: dur = 0
    m = medir(ruta, dur) if dur else None
    if not m: out["motivo"] = "no he podido medir la imagen"; return out
    puntos = [m["negro"] >= UMBRAL_NEGRO, m["blanco"] <= UMBRAL_BLANCO, m["sat"] <= UMBRAL_SAT]
    out["medida"] = m
    desc = f"negros {m['negro']:.0f} (≥{UMBRAL_NEGRO}?), blanco máx {m['blanco']:.0f} (≤{UMBRAL_BLANCO}?), saturación {m['sat']:.1f} (≤{UMBRAL_SAT}?)"
    if sum(puntos) >= 2 and (cand or out["bits"] >= 10) and (out["bits"] >= 10 or sum(puntos) == 3):
        out.update(perfil=cand or "dlogm", seguro="probable",
                   motivo=f"probable por la imagen ({desc}; {out['bits']} bits{', cámara ' + cand if cand else ''}): MIRA el antes/después")
    else:
        out["motivo"] = f"no parece Log ({desc})"
    return out


def _norm(s): return re.sub(r"[\s_\-.]+", "", s.lower())


def lut_de(perfil, modelo="", extra=()):
    """El .cube de conversión de un perfil: primero los del creador (extra), luego herramientas/luts/. Si hay varios, el que
    lleve el modelo de la cámara en el nombre."""
    if not perfil: return None
    rx = PERFILES[perfil][2]; cands = []
    for d in list(extra) + [LUTS]:
        if d and os.path.isdir(d):
            cands += sorted(f for f in glob.glob(os.path.join(d, "*.cube")) if re.search(rx, _norm(os.path.basename(f))))
    if not cands: return None
    mm = _norm(modelo)
    return next((f for f in cands if mm and mm in _norm(os.path.basename(f))), cands[0])


# ---------- .cube ----------
def leer_cube(ruta):
    n, dat, dmin, dmax = 0, [], [0.0] * 3, [1.0] * 3
    for l in open(ruta, encoding="utf-8", errors="replace"):
        l = l.strip()
        if not l or l.startswith("#") or l.upper().startswith("TITLE"): continue
        p = l.split()
        if p[0].upper() == "LUT_3D_SIZE": n = int(p[1])
        elif p[0].upper() == "DOMAIN_MIN": dmin = [float(x) for x in p[1:4]]
        elif p[0].upper() == "DOMAIN_MAX": dmax = [float(x) for x in p[1:4]]
        elif p[0].upper() == "LUT_1D_SIZE": raise ValueError(f"{ruta}: es un LUT 1D, hace falta 3D")
        elif re.match(r"^[-\d.eE+]+$", p[0]) and len(p) >= 3: dat.append((float(p[0]), float(p[1]), float(p[2])))
    if not n or len(dat) != n ** 3: raise ValueError(f"{ruta}: .cube 3D mal formado ({len(dat)} valores para tamaño {n})")
    return n, dat, dmin, dmax


def escribir_cube(ruta, n, dat, titulo):
    os.makedirs(os.path.dirname(ruta) or ".", exist_ok=True)
    with open(ruta + ".tmp", "w", encoding="utf-8", newline="\n") as f:
        f.write(f'TITLE "{titulo}"\nLUT_3D_SIZE {n}\nDOMAIN_MIN 0.0 0.0 0.0\nDOMAIN_MAX 1.0 1.0 1.0\n')
        f.writelines(f"{r:.6f} {g:.6f} {b:.6f}\n" for r, g, b in dat)
    os.replace(ruta + ".tmp", ruta)


def mezclar(ruta, intensidad, dest):
    """El LUT a `intensidad` (0–1): mezcla con la identidad punto a punto (lo mismo que bajar la opacidad del LUT)."""
    n, dat, dmin, dmax = leer_cube(ruta); i = max(0.0, min(1.0, float(intensidad))); out = []
    for k, (r, g, b) in enumerate(dat):          # orden .cube: R cambia más rápido, luego G, luego B
        x = (k % n, (k // n) % n, k // (n * n))
        idn = [dmin[c] + (dmax[c] - dmin[c]) * x[c] / (n - 1) for c in range(3)]
        out.append(tuple(idn[c] * (1 - i) + v * i for c, v in enumerate((r, g, b))))
    escribir_cube(dest, n, out, f"{os.path.basename(ruta)} al {i * 100:.0f} %")
    return dest


# ---------- looks de la casa ----------
def _hsv_sat(r, g, b, f, piel=0.35):
    """Satura (f > 1) o desatura sin tocar tanto la piel (tonos 10–50°)."""
    mx, mn = max(r, g, b), min(r, g, b); l = (mx + mn) / 2
    if mx - mn < 1e-6: return r, g, b
    if mx == r: h = ((g - b) / (mx - mn)) % 6
    elif mx == g: h = (b - r) / (mx - mn) + 2
    else: h = (r - g) / (mx - mn) + 4
    h *= 60
    w = max(0.0, 1 - abs(h - 30) / 25) if h < 60 else 0.0                # cuánto es «piel»
    ff = 1 + (f - 1) * (1 - piel * w)
    return tuple(l + (c - l) * ff for c in (r, g, b))


def _curva(x, k):
    """Curva en S suave (k = fuerza, 0 = recta): pendiente 1 + k en los medios y 1 − k en los extremos; 0 y 1 no se mueven."""
    return x - k * math.sin(2 * math.pi * x) / (2 * math.pi)


def generar_look(nombre, n=33):
    dat = []
    for bi in range(n):
        for gi in range(n):
            for ri in range(n):
                r, g, b = ri / (n - 1), gi / (n - 1), bi / (n - 1)
                lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
                if nombre == "natural":
                    r, g, b = (_curva(c, 0.18) for c in (r, g, b)); r, g, b = _hsv_sat(r, g, b, 1.10)
                elif nombre == "calido":
                    t = lum ** 1.5                                           # más en las luces que en las sombras
                    r, g, b = r * (1 + 0.035 * t), g * (1 + 0.012 * t), b * (1 - 0.05 * t)
                    r, g, b = (_curva(c, 0.10) for c in (r, g, b)); r, g, b = _hsv_sat(r, g, b, 1.05)
                elif nombre == "cine":
                    s, h = (1 - lum) ** 2, lum ** 2                          # sombras → teal, luces → naranja
                    r, g, b = r - 0.014 * s + 0.028 * h, g + 0.006 * s + 0.008 * h, b + 0.016 * s - 0.03 * h
                    r, g, b = (_curva(c, 0.14) for c in (r, g, b)); r, g, b = _hsv_sat(r, g, b, 0.94)
                    r, g, b = (0.012 + c * 0.988 for c in (r, g, b))         # negro apenas levantado
                dat.append(tuple(min(1.0, max(0.0, c)) for c in (r, g, b)))
    dest = os.path.join(LOOKS, f"{nombre}.cube")
    escribir_cube(dest, n, dat, f"look {nombre} (edicion-horizontal)")
    return dest


def look_de(nombre, extra=()):
    """Ruta del .cube de un look: los de la casa (se generan si faltan), uno del creador (extra) por nombre, o una ruta."""
    if not nombre: return None
    if nombre in LOOKS_CASA:
        f = os.path.join(LOOKS, f"{nombre}.cube")
        return f if os.path.exists(f) else generar_look(nombre)
    if os.path.exists(nombre) and nombre.lower().endswith(".cube"): return nombre
    for d in list(extra) + [LOOKS]:
        f = os.path.join(d, nombre if nombre.lower().endswith(".cube") else nombre + ".cube") if d else ""
        if f and os.path.exists(f): return f
    raise SystemExit(f"No encuentro el look «{nombre}» (los de la casa: {', '.join(LOOKS_CASA)}; los tuyos, en personal/<creador>/recursos/luts/)")


def looks_disponibles(extra=()):
    L = [{"id": k, "nombre": k.upper(), "que": v, "casa": True} for k, v in LOOKS_CASA.items()]
    for d in extra:
        if d and os.path.isdir(d):
            for f in sorted(glob.glob(os.path.join(d, "*.cube"))):
                n = os.path.splitext(os.path.basename(f))[0]
                if not any(re.search(p[2], _norm(n)) for p in PERFILES.values()):       # los de conversión no son looks
                    L.append({"id": os.path.basename(f), "nombre": n.upper(), "que": "LUT propio del creador", "casa": False})
    return L


# ---------- filtro de ffmpeg ----------
def _esc(p):
    """Ruta para un filtro de ffmpeg: RELATIVA a la carpeta actual y sin «:», espacios ni comillas (en Windows «C:» rompe
    el filtro). Si no se puede, copia el .cube a ./luts_tmp/ y usa esa copia."""
    try: q = os.path.relpath(p).replace("\\", "/")
    except ValueError: q = p.replace("\\", "/")
    if re.search(r"[:\s'\[\],;]", q):
        d = os.path.join("trabajo" if os.path.isdir("trabajo") else ".", "luts_tmp"); os.makedirs(d, exist_ok=True)
        q = os.path.join(d, re.sub(r"[^\w.-]", "_", os.path.basename(p))).replace("\\", "/"); shutil.copyfile(p, q)
    return q


def filtro(lut=None, look=None, bits=8, matriz="bt709", rango="tv"):
    """Cadena de filtros (sin coma final): YUV → RGB con la matriz del bruto → LUT de conversión → look → YUV bt709."""
    if not lut and not look: return ""
    fmt = "gbrp16le" if bits > 8 else "gbrp"
    c = [f"scale=in_color_matrix={matriz}:in_range={rango},format={fmt}"]
    if lut: c.append(f"lut3d=file={_esc(lut)}:interp=tetrahedral")
    if look: c.append(f"lut3d=file={_esc(look)}:interp=tetrahedral")
    c.append("scale=out_color_matrix=bt709:out_range=tv,format=yuv420p")
    return ",".join(c)


# ---------- línea de órdenes ----------
def _cli():
    a = sys.argv[1:]
    if not a: print(__doc__); return
    if a[0] == "luts":
        print(f"LUT de conversión en {LUTS}:")
        for k, (nombre, _, _) in PERFILES.items():
            f = lut_de(k); print(f"  {nombre:17} {'✓ ' + os.path.basename(f) if f else '— falta · ' + PAGINAS.get(k, '')}")
        print(f"Looks de la casa: {', '.join(LOOKS_CASA)} (se generan solos en {LOOKS})"); return
    if a[0] == "looks":
        for k in LOOKS_CASA: print("✓", generar_look(k))
        return
    if a[0] == "comparar":
        if len(a) < 4: raise SystemExit("comparar BRUTO SEGUNDO SALIDA.jpg [--look nombre]")
        ruta, t, sal = a[1], float(a[2]), a[3]; lk = a[a.index("--look") + 1] if "--look" in a else None
        d = detectar(ruta); lut = lut_de(d["perfil"]) if d["perfil"] else None
        if d["perfil"] and not lut: raise SystemExit(f"Es {PERFILES[d['perfil']][0]} pero falta su LUT: {PAGINAS.get(d['perfil'])}")
        fl = filtro(lut, look_de(lk), d["bits"], d["matriz"], d["rango"]) or "null"
        r = _run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", ruta, "-frames:v", "1", "-filter_complex",
                  f"[0:v]scale=960:-2,split[a][b];[b]{fl},scale=960:-2[d];[a]format=yuv420p[a2];[a2][d]hstack", "-q:v", "3", sal], timeout=120)
        if not r or r.returncode: raise SystemExit((r.stderr if r else "ffmpeg no responde")[-800:])
        print(f"{sal}: izquierda el bruto, derecha revelado ({os.path.basename(lut) if lut else 'sin LUT'}{' + look ' + lk if lk else ''})"); return
    for ruta in a:
        d = detectar(ruta); lut = lut_de(d["perfil"]) if d["perfil"] else None
        p = PERFILES[d["perfil"]][0] if d["perfil"] else ("HDR" if d["hdr"] else "normal")
        print(f"{os.path.basename(ruta):28} {p:16} {d['seguro'] or '':10} {d['bits']} bits · {d['motivo']}"
              + (f" · LUT: {os.path.basename(lut)}" if lut else (f" · FALTA LUT: {PAGINAS.get(d['perfil'])}" if d["perfil"] else "")))


if __name__ == "__main__":
    _cli()
