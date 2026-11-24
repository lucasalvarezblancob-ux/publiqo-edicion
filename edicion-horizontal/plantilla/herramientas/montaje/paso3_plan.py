"""Paso 3: de la línea de voz al plan de IMAGEN (trabajo/video.json) y de GRÁFICOS (estudio/src/videos/<slug>/capas.json).
Lee plan.py del vídeo (todo opcional; lo que no esté, no se pone):
  BROLL     planos de recurso sobre la voz           FUERTES   frases con punch-in de golpe x1,65
  TRK       rótulos anclados a un sujeto             ENTRADAS  zoom-in animado rápido (con frenada)
  DETALLE   rótulos tras los que se cierra al sujeto  DATOS     cifra junto a la cara
  MAPAS     mapa a pantalla completa                 GOLPES    palabra-golpe grande abajo
  SUBS      subtítulos (solo donde se oye mal)       NOTAS     comentario del editor
  TITULO    título sobre la marca "titulo"           SUSCRIBE  (antiguo) botón dibujado; para suscribirse se usa BOTONES
  BOTONES   botones animados de la skill (suscríbete, me gusta, campana): [(ancla, nº, {x, y, esc, vel}?)]; SIEMPRE que se
            pide suscribirse, like o campana, y abajo en el CENTRO (de serie). Catálogo: base/recursos.md -> «Botones de
            YouTube». Llevan texto en español: si hay versión en el IDIOMA del vídeo (bNN_<idioma>.webm, la hace
            herramientas/boton_idioma.py) se coge sola. vel: 1.25 = un 25 % más rápido, para que quepa (el sonido también).
            esc: tamaño (comun.BOTON_ESC, 0,34 de serie: un tercio del ancho)
  FALLOS    [(ancla_inicio, ancla_fin)]: un fail (se cae la cámara, se va la luz, se le cae algo): el tramo en BLANCO Y NEGRO
            y la voz algo saturada (paso5_audio.py), hasta que se recupera («¡hemos vuelto!»)
  REPETIR_OK [(clip, segundo)]: tramos del bruto que salen dos veces A PROPÓSITO (si no, paso3 se para: «REPETIDO»)
  PROPIOS   gráficos PROPIOS del creador (su mascota, su logo…): [(ancla, segundos, "tipo", {datos})]; los pinta
            estudio/src/personal/<creador>/ y se documentan en personal/<creador>/recursos.md
Los cortes de escala los pone dinamica.py. Al final imprime el ritmo (mediana de plano, cortes/min) y los avisos."""
import json, os, subprocess, sys
import numpy as np, cv2
from comun import ALTO as AH, ANCHO as AW, BOTON_ESC, CAPAS_JSON, CREADOR, ESTUDIO, F, FPS, IDIOMA, SINCRO, TRABAJO, Linea, ajuste, bruto, buscar, caja_texto, cruce, fuera, marca, texto_dicho
import plan      # después de comun: es quien mete la carpeta del vídeo en el path
from dinamica import Caras, Z_FUERTE, encuadre, planos_de_voz

g = lambda n, d: getattr(plan, n, d)
BROLL, TRK, DETALLE, MAPAS, SUBS = g("BROLL", []), g("TRK", []), set(g("DETALLE", ())), g("MAPAS", []), g("SUBS", [])
FUERTES, ENTRADAS, DATOS, GOLPES, NOTAS = g("FUERTES", []), g("ENTRADAS", []), g("DATOS", []), g("GOLPES", []), g("NOTAS", [])
TITULO, SUSCRIBE, BOTONES, PROPIOS = g("TITULO", None), g("SUSCRIBE", None), g("BOTONES", []), g("PROPIOS", [])
FALLOS, REPETIR_OK = g("FALLOS", []), g("REPETIR_OK", [])
L = Linea(); P, W, M = L.piezas, L.palabras, L.marcas


def src2out(c, t):
    """Frame de salida (y pieza) en que se ve el segundo t del bruto c."""
    f = round(t * FPS)
    for p in P:
        if p["clip"] == c and p["speed"] == 1 and p["k"] == "T" and p["in"] <= f < p["out"]: return p["o"] + f - p["in"], p
    for p in P:
        if p["clip"] == c and p["speed"] == 1 and p["n"] > F(1.6) and p["in"] <= f < p["out"]: return p["o"] + f - p["in"], p
    raise SystemExit(f"{c} {t}s no está en el montaje")


_TRK_TAPADO = 0.0
# --legado: para retocar un vídeo YA ENTREGADO con una versión anterior de la skill. Las comprobaciones que se añadieron
# después (REPETIDO, PISA) avisan pero no paran, para poder corregir un detalle sin rehacer el vídeo entero. Lo que nunca
# se deja pasar: un texto que se sale del cuadro ni un rótulo con flecha sobre el plano equivocado. (planto-estanque,
# 2026-11-17: la v3.5 paraba en 46 REPETIDO y 3 PISA sobre un vídeo ya aprobado.)
LEGADO = "--legado" in sys.argv or os.environ.get("PLAN_LEGADO") == "1"
def parar(msg):
    if LEGADO: print("LEGADO (aviso, no para): " + msg)
    else: raise SystemExit(msg)


def seguir(c, t0, t1, caja):
    """Seguimiento a 960 px de ancho; devuelve [x, y] por frame en px del lienzo.
    Lucas-Kanade (ida y vuelta: solo cuentan los puntos que vuelven a su sitio) + mediana, y una COMPROBACIÓN DE ASPECTO:
    el recorte del sujeto del primer fotograma se compara en cada frame con lo que hay en el punto. Si algo lo tapa (una
    mano que pasa, alguien que cruza) el punto se queda quieto en vez de irse con lo que tapa, y cuando el sujeto vuelve a
    verse se le busca alrededor y se recupera. Por qué (alimentacion, 2026-11-17): en «HIBISCUS» pasó un guante por
    delante de la flor y la flecha se fue con la mano hasta quedarse 150 px al lado, en una hoja."""
    global _TRK_TAPADO
    n = round((t1 - t0) * FPS); sw = 960; sh = 2 * round(sw * AH / AW / 2); k = AW / sw
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t0}", "-i", bruto(c), "-frames:v", str(n), "-vf", f"fps={FPS},scale={sw}:{sh}", "-pix_fmt", "gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, sh, sw); cx, cy, r = [v / k for v in caja]; pos = [[cx, cy]]
    r = max(r, 10.0); R = int(round(r))
    def recorte(im, x, y, rr):
        x0, y0 = int(round(x)) - rr, int(round(y)) - rr
        if x0 < 0 or y0 < 0 or x0 + 2 * rr > sw or y0 + 2 * rr > sh: return None
        return im[y0:y0 + 2 * rr, x0:x0 + 2 * rr]
    def parecido(im, x, y):
        p = recorte(im, x, y, R)
        return -1.0 if p is None or ref is None else float(cv2.matchTemplate(p, ref, cv2.TM_CCOEFF_NORMED)[0, 0])
    ref = recorte(fr[0], cx, cy, R); tapado = 0
    for i in range(1, len(fr)):
        nx, ny = cx, cy; buenos = 0; paso = 0.0
        m = np.zeros((sh, sw), np.uint8); m[max(0, int(cy - r)):int(cy + r), max(0, int(cx - r)):int(cx + r)] = 255
        p0 = cv2.goodFeaturesToTrack(fr[i - 1], 80, 0.01, 4, mask=m)
        if p0 is not None:
            p1, st, _ = cv2.calcOpticalFlowPyrLK(fr[i - 1], fr[i], p0, None, winSize=(31, 31), maxLevel=3)
            pb, stb, _ = cv2.calcOpticalFlowPyrLK(fr[i], fr[i - 1], p1, None, winSize=(31, 31), maxLevel=3)
            ok = (st.ravel() == 1) & (stb.ravel() == 1) & (np.linalg.norm((pb - p0).reshape(-1, 2), axis=1) < 1.0)
            if ok.sum() >= 4:
                d = np.median((p1 - p0)[ok].reshape(-1, 2), axis=0); nx, ny = cx + float(d[0]), cy + float(d[1])
                buenos = int(ok.sum()); paso = float(np.hypot(*d))
        # se acepta el paso si el sujeto se sigue pareciendo, o si es un paso pequeño y con muchos puntos de acuerdo (un
        # animal que come cambia de forma, pero no salta); lo que se rechaza es el salto de algo que pasa por delante
        if ref is None or parecido(fr[i], nx, ny) >= 0.45 or (buenos >= 8 and paso < 0.35 * r): cx, cy = nx, ny
        else:      # tapado o perdido: se busca el sujeto alrededor; si no aparece, el punto se queda donde estaba
            tapado += 1; S = int(3 * r)
            x0, y0 = max(0, int(cx) - S - R), max(0, int(cy) - S - R); x1, y1 = min(sw, int(cx) + S + R), min(sh, int(cy) + S + R)
            zona = fr[i][y0:y1, x0:x1]
            if zona.shape[0] > 2 * R and zona.shape[1] > 2 * R:
                res = cv2.matchTemplate(zona, ref, cv2.TM_CCOEFF_NORMED); _, sc, _, (bx, by) = cv2.minMaxLoc(res)
                if sc >= 0.6: cx, cy = x0 + bx + R, y0 + by + R
        pos.append([cx, cy])
    _TRK_TAPADO = tapado / max(len(fr) - 1, 1)
    pos = np.array(pos) * k
    q = np.ones(5) / 5; sm = np.stack([np.convolve(np.pad(pos[:, j], 2, mode="edge"), q, "valid") for j in (0, 1)], 1)
    return sm.round(1).tolist()


items = []; esp = []; TRK_PRINCIPAL = []   # TRK de 7 campos: se comprueban DESPUÉS de pegar los BROLL
# ---- rótulos con seguimiento: (clip, t0, t1 del bruto, caja inicial [cx, cy, medio lado] en px del lienzo, grande, pequeño, lado) ----
TRK_REC = [t for t in TRK if len(t) == 8]      # con ancla: van sobre un plano de RECURSO (se colocan después de BROLL)
for c, t0, t1, caja, grande, peq, lado in [t for t in TRK if len(t) == 7]:
    o0, p = src2out(c, t0); o1, p1 = src2out(c, t1 - 0.04)
    assert p is p1, f"rótulo con seguimiento cruza un corte: {c} {t0}-{t1}"
    resto = (p["o"] + p["n"] - o1) / FPS; extra = min(2.6, resto - 0.4) if resto > 1.6 else 0     # zoom al detalle después del rótulo
    if grande not in DETALLE: extra = 0      # solo donde se ha comprobado a ojo que el seguimiento aguanta
    pos = seguir(c, t0, t1 + extra, caja); n = round((t1 - t0) * FPS)
    items.append({"t": "trk", "f0": o0, "f1": o0 + n, "pos": pos[:n], "grande": grande, "peq": peq, "lado": lado})
    esp.append({"tipo": "fijo", "z": 1.0, "f0": o0 - F(0.4), "f1": o0 + n})
    TRK_PRINCIPAL.append((items[-1], esp[-1], c, t0, caja))
    if extra:
        cx, cy = np.median(np.array(pos[n:]), axis=0); esp.append({"tipo": "detalle", "z": 1.6, "t": F(0.4), "f0": o0 + n, "f1": o0 + len(pos), "cx": float(cx), "cy": float(cy)})
    mov = np.ptp(np.array(pos), axis=0)
    print("seguimiento", grande, round(o0 / FPS, 1), "s; desplazamiento", mov.round(), "detalle", round(extra, 1), "s")
    if _TRK_TAPADO > 0.2: print(f"AVISO TRK: «{grande}»: el sujeto está tapado o no se reconoce el {_TRK_TAPADO * 100:.0f} % del tramo (el punto se queda quieto mientras): mira su trk_N.jpg")
    if max(mov) > 3 * max(caja[2], 40):      # un sujeto pequeño con la cámara casi quieta no se mueve 300 px: sigue al fondo
        print(f"AVISO TRK: el seguimiento de «{grande}» se mueve {max(mov):.0f} px (más de 3 veces el medio lado, {caja[2]}): puede haberse ido al fondo. Mira su trk_N.jpg (hoja_seguimiento.py)")

# ---- especiales: frase fuerte, entrada animada, dato ----
for c, fr, n in FUERTES:
    a, b = buscar(W, c, fr, n); f0 = int(W[a]["o0"]) - F(0.08); esp.append({"tipo": "fuerte", "z": Z_FUERTE, "f0": f0, "f1": max(int(round(W[b]["o1"])) + F(0.12), f0 + F(0.64))})
for c, fr, n, z in ENTRADAS:
    a, b = buscar(W, c, fr, n); f0 = int(W[a]["o0"]) - F(0.08); esp.append({"tipo": "entra", "z": z, "f0": f0, "f1": max(int(round(W[b]["o1"])) + F(0.12), f0 + F(1.6))})
for i, (an, grande, peq, d) in enumerate(DATOS):
    a, b = buscar(W, *an); f0 = int(W[a]["o0"]) - F(0.08)
    esp.append({"tipo": "dato", "z": 1.3, "ax": 0.3 if i % 2 == 0 else 0.7, "f0": f0, "f1": max(int(round(W[b]["o1"])) + F(0.12), f0 + F(d)), "grande": grande, "peq": peq})
orden = sorted(esp, key=lambda e: e["f0"])
for x, y in zip(orden, orden[1:]):
    if y["f0"] < x["f1"]: print("AVISO: especiales solapados", x["tipo"], x["f0"], x["f1"], y["tipo"], y["f0"]); x["f1"] = y["f0"]

vid = planos_de_voz(P, W, Caras(TRABAJO), esp, L.secciones)


def cortar(f):   # parte el plano que contiene el frame f
    for i, v in enumerate(vid):
        if v["o"] < f < v["o"] + v["n"]:
            k = f - v["o"]; b = dict(v); b["in"] = v["in"] + round(k * v["speed"]); b["n"] = v["n"] - k; b["o"] = f; v["n"] = k
            if b.get("t"): b["z0"] = b["z1"]; b["t"] = 0
            vid.insert(i + 1, b); return


# ---- planos de recurso sobre la voz ----
#   (ancla, clip, segundo, duración s | None = hasta el final de la pieza[, (zoom, cx, cy)])
#   (zoom, cx, cy): zoom fijo a ese punto del bruto. (None, cx, cy): el corte de escala a la mitad de un recurso largo
#                   (×1,0 -> ×1,25) se cierra hacia (cx, cy) en vez de al centro: hacia el SUJETO (Lucas, 2026-11-17: el
#                   ×1,25 al centro dejaba la tortuga abajo, tapada por el rótulo: «el zoom un poco más centrado en la tortuga»).
#   (ancla, [(clip, segundo, duración[, (zoom, cx, cy)]), …]): VARIOS planos seguidos sobre la misma voz (montaje). Para
#                   el tráiler-resumen: «más de 100 animales» con tres animales distintos de 1,5–2 s, no un plano de 6 s.
#   (ancla, "@sync:<clip>", duración | None[, zoom]): la OTRA CÁMARA en el MISMO instante que suena la voz (SINCRO en
#                   proyecto.py, medido con sincro.py). El segundo sale del montaje (pieza de voz que suena + desfase), nunca
#                   a mano, y el plano no pasa del final de esa pieza. Zoom (1,9 si no se da) con la cara a ~30 % del alto.
#                   Por qué: vaciamos-estanque-2 (2026-11-19), «hay lag con mi voz y mis labios»: un plano de la Sony puesto
#                   a ojo iba 0,47 s adelantado y otros dos eran de otra toma de la misma frase.
nb = 0; _caras = Caras(TRABAJO)
def pegar(f):   # nada de planos de un puñado de frames: el recurso se pega al corte más cercano
    cs = [v["o"] for v in vid] + [L.total]; c_ = min(cs, key=lambda x: abs(x - f)); return c_ if abs(c_ - f) <= F(0.48) else f
for b_ in BROLL:
    a = b_[0]; f0 = L.ancla(a); sync = None
    if isinstance(b_[1], str) and b_[1].startswith("@sync:"):
        sync = b_[1][6:]
        if sync not in SINCRO: raise SystemExit(f"BROLL {b_[1]}: falta {sync!r} en SINCRO de proyecto.py (mídelo con sincro.py)")
        zsync = float(b_[3]) if len(b_) > 3 and b_[3] else 1.9
        b_ = (a, sync, 0.0, b_[2] if len(b_) > 2 else None)      # el segundo se calcula después de pegar al corte
    if isinstance(b_[1], list): fuentes = [(x[0], x[1], x[2], *x[3:]) for x in b_[1]]; f1 = f0 + sum(F(x[2]) for x in b_[1])
    else:
        c, t, d, *zz = b_[1:]
        if d is None:
            p = next(p for p in P if p["o"] <= f0 < p["o"] + p["n"]); f1 = p["o"] + p["n"]
        else: f1 = f0 + F(d)
        fuentes = None
    f0, f1 = pegar(f0), pegar(f1)
    if sync:
        voz, off = SINCRO[sync]
        p = next((p for p in P if p["o"] <= f0 < p["o"] + p["n"]), None)
        if not p or p["clip"] != voz: raise SystemExit(f"BROLL @sync:{sync} en {f0 / FPS:.1f} s: ahí suena {p and p['clip']}, no {voz}: no hay toma sincronizable")
        if abs(p.get("speed", 1) - 1) > 1e-6: raise SystemExit(f"BROLL @sync:{sync} en {f0 / FPS:.1f} s: la voz va acelerada (x{p['speed']}): así no se sincroniza")
        f1 = min(f1, p["o"] + p["n"])            # nunca pasa del corte de la pieza: si la voz salta a otra toma, se desincroniza
        t = (p["in"] + (f0 - p["o"])) / FPS + off
        z = zsync; cara = _caras.en(sync, round(t * FPS), f1 - f0); alto = AH / z
        cx, cy = (cara["cx"], cara["cy"]) if cara else (AW / 2, alto / 2)
        cy = max(alto / 2, min(AH - alto / 2, cy + alto * 0.2))       # la cara a ~30 % del alto del cuadro
        zz = [(z, int(cx), int(cy))]
        if not cara: print(f"AVISO SYNC: @sync:{sync} en {f0 / FPS:.1f} s: sin cara detectada en {sync} {t:.1f} s; encuadre arriba al centro (míralo en hoja_recursos.py)")
    cortar(f0); cortar(f1)
    i0 = next(i for i, v in enumerate(vid) if v["o"] == f0); i1 = next((i for i, v in enumerate(vid) if v["o"] == f1), len(vid))
    n = f1 - f0; base = {"speed": 1.0, "b": 1, "t": 0, "cx": None, "cy": None, "ax": 0.5, "ay": 0.5}
    if fuentes:     # montaje: cada plano su duración; el último se ajusta a lo que queda
        nuevos = []; o = f0
        for k, (c, t, d, *zz) in enumerate(fuentes):
            m = (f1 - o) if k == len(fuentes) - 1 else F(d)
            z = zz[0] if zz and zz[0][0] else None
            nuevos.append({**base, "clip": c, "in": round(t * FPS), "n": m, "o": o, "z0": z[0] if z else 1.0, "z1": z[0] if z else 1.0, "cx": z[1] if z else None, "cy": z[2] if z else None}); o += m
    elif zz and zz[0][0]: nuevos = [{**base, "clip": c, "in": round(t * FPS), "n": n, "o": f0, "z0": zz[0][0], "z1": zz[0][0], "cx": zz[0][1], "cy": zz[0][2]}]   # zoom al sujeto
    elif n >= F(3.2):   # recurso largo: corte de escala a la mitad (x1,0 -> x1,25), sin zoom lento; con (None, cx, cy), hacia el sujeto
        h = round(n * 0.52); cx2, cy2 = (zz[0][1], zz[0][2]) if zz else (None, None)
        nuevos = [{**base, "clip": c, "in": round(t * FPS), "n": h, "o": f0, "z0": 1.0, "z1": 1.0}, {**base, "clip": c, "in": round(t * FPS) + h, "n": n - h, "o": f0 + h, "z0": 1.25, "z1": 1.25, "cx": cx2, "cy": cy2}]
    else: nuevos = [{**base, "clip": c, "in": round(t * FPS), "n": n, "o": f0, "z0": 1.0, "z1": 1.0}]
    vid[i0:i1] = nuevos; nb += 1
assert all(vid[i]["o"] + vid[i]["n"] == vid[i + 1]["o"] for i in range(len(vid) - 1)) and vid[-1]["o"] + vid[-1]["n"] == L.total
# ---- la otra cámara sobre la voz: ¿va en el MISMO instante? (los @sync ya lo van; esto pilla los puestos a mano) ----
for v in vid:
    if not v["b"] or v["clip"] not in SINCRO: continue
    voz, off = SINCRO[v["clip"]]; p = next((p for p in P if p["o"] <= v["o"] < p["o"] + p["n"]), None); mm = f"{int(v['o'] / FPS // 60)}:{v['o'] / FPS % 60:04.1f}"
    if p and p["clip"] == v["clip"]: continue          # recurso del mismo clip que la voz: no es la otra cámara
    if not p or p["clip"] != voz:
        print(f"AVISO LABIOS: {v['clip']} en {mm} va sobre la voz de {p and p['clip']} (otra toma): si habla a cámara, que no se le vean los labios, o usa @sync:{v['clip']}")
        continue
    dif = (v["in"] - (p["in"] + (v["o"] - p["o"]) * p.get("speed", 1)) - off * FPS) / FPS
    if abs(dif) > 1.0 / FPS: print(f"AVISO LABIOS: {v['clip']} en {mm} va {dif:+.2f} s desfasado de la voz: usa (ancla, \"@sync:{v['clip']}\", …) en BROLL")
# rótulo con seguimiento sobre un plano de recurso: (clip, t0, t1, caja, grande, pequeño, lado, ancla del frame en que suena t0)
for c, t0, t1, caja, grande, peq, lado, a in TRK_REC:
    o0 = L.ancla(a); v = next(v for v in vid if v["o"] <= o0 < v["o"] + v["n"]); n = round((t1 - t0) * FPS)
    if not (v["b"] and v["clip"] == c and v["z0"] == v["z1"] and o0 + n <= v["o"] + v["n"]): raise SystemExit(f"rótulo {grande}: en el frame {o0} no hay un recurso de {c} con zoom fijo que dure {n} frames (hay {v['clip']}, recurso={v['b']}, hasta {v['o'] + v['n']})")
    dt = (v["in"] + o0 - v["o"]) / FPS - t0
    if abs(dt) > 0.06: raise SystemExit(f"rótulo {grande}: en el frame {o0} el recurso enseña el segundo {t0 + dt:.2f} de {c}, no el {t0}")
    z = v["z0"]; w, h, x, y = encuadre(z, v.get("cx"), v.get("cy"), v.get("ax", 0.5), v.get("ay", 0.5))
    pos = [[round(px * z - x, 1), round(py * z - y, 1)] for px, py in seguir(c, t0, t1, caja)][:n]
    items.append({"t": "trk", "f0": o0, "f1": o0 + n, "pos": pos, "grande": grande, "peq": peq, "lado": lado})
    print("seguimiento sobre recurso", grande, round(o0 / FPS, 1), "s; en pantalla", np.array(pos)[[0, -1]].round().tolist())

# ---- TRK sobre el PLANO PRINCIPAL: se colocó en la línea de voz, ANTES de pegar los BROLL. Con los recursos ya puestos,
# cada frame del rótulo tiene que enseñar SU clip y SU segundo. Si un recurso tapa el principio, el rótulo empieza cuando
# vuelve su plano (y se avisa: hay que medir la caja otra vez en ese segundo); si lo tapa por medio o entero, se para.
# Por qué (planto-estanque, 2026-11-17): «UN VISITANTE» entraba 1,07 s antes, sobre el recurso del abono, y la flecha
# señalaba al agua; nada lo comprobaba (el TRK de 8 campos, sobre recurso, sí).
def _ensena(f, c, t0, f0):
    v = next(v for v in vid if v["o"] <= f < v["o"] + v["n"])
    return (not v["b"]) and v["clip"] == c and abs((v["in"] + (f - v["o"]) * v["speed"]) / FPS - (t0 + (f - f0) / FPS)) < 0.06
for it, e, c, t0, caja in TRK_PRINCIPAL:
    ok = [_ensena(f, c, t0, it["f0"]) for f in range(it["f0"], it["f1"])]
    if not any(ok): raise SystemExit(f"rótulo {it['grande']}: su plano ({c} {t0} s) está tapado entero por un recurso: mueve el recurso o el rótulo")
    k = ok.index(True)
    if k:
        print(f"AVISO TRK: «{it['grande']}» empezaba {k / FPS:.2f} s antes de que se vea su plano (lo tapaba un recurso): recortado. "
              f"Mide la caja con rejilla.py en {c} {t0 + k / FPS:.2f} y pon ese t0 en plan.py")
        it["f0"] += k; it["pos"] = it["pos"][k:]; e["f0"] = it["f0"] - F(0.4); ok = ok[k:]
    if not all(ok): raise SystemExit(f"rótulo {it['grande']}: un recurso tapa su plano por medio (frame {it['f0'] + ok.index(False)}): mueve el recurso o acorta t1")

# ---- fails: el tramo en blanco y negro (y la voz saturada en paso5_audio.py) ----
# Lucas, 2026-11-17 (alimentacion, 20:08): «se baja la cámara, puedes poner en blanco y negro y saturar un poco la voz porque
# es un fail, hasta el "hemos vuelto", que ya recupera color». Es un efecto, no una corrección de color: el color del bruto
# sigue sin tocarse fuera del fail.
fallos = []
for a0, a1 in FALLOS:
    f0, f1 = pegar(L.ancla(a0)), pegar(L.ancla(a1)); cortar(f0); cortar(f1); fallos.append([f0, f1])
    for v in vid:
        if f0 <= v["o"] < f1: v["bn"] = 1
    print(f"fail en blanco y negro {f0 / FPS:.1f}-{f1 / FPS:.1f} s")
json.dump(fallos, open(f"{TRABAJO}/fallos.json", "w"))
# ---- ningún tramo de bruto sale dos veces (ni en el cuerpo ni dentro del tráiler) ----
# Lucas, 2026-11-17 (alimentacion): «22:55–23:03 repites el mismo clip dos veces» y «se repite el clip de la terrapene en
# la intro». Causa: un V(…) de acción (los grillos) y la frase de después eran el mismo trozo de bruto: el pista de T(…)
# venía de Whisper (103 s) y la frase empezaba de verdad en 95,9 s; y un recurso que repetía el plano principal de justo
# antes. La regla («no se repite un tramo») existía, pero nada lo medía. El tráiler sí puede repetir lo del cuerpo (sale
# de él), pero no repetirse a sí mismo. Lo que se repita a propósito va en REPETIR_OK = [(clip, segundo)].
_cuerpo = M.get("cuerpo", 0); _z = lambda f: "tráiler" if f < _cuerpo else "cuerpo"; _mm = lambda f: f"{int(f / FPS // 60)}:{f / FPS % 60:04.1f}"
_us = [(v["clip"], v["in"] / FPS, (v["in"] + v["n"] * v["speed"]) / FPS, v["o"], _z(v["o"]), v["b"]) for v in vid]
_rep = []
for i, (c, a, b, o, z, rb) in enumerate(_us):
    for c2, a2, b2, o2, z2, rb2 in _us[i + 1:]:
        if c == c2 and z == z2 and min(b, b2) - max(a, a2) > 0.3 and not any(cc == c and max(a, a2) - 1 <= tt <= min(b, b2) + 1 for cc, tt in REPETIR_OK):
            _rep.append(f"REPETIDO ({z}): {c} {max(a, a2):.1f}-{min(b, b2):.1f} s sale en {_mm(o)} ({'recurso' if rb else 'principal'}) y otra vez en {_mm(o2)} ({'recurso' if rb2 else 'principal'})")
def _libre(c, a, b, o):
    """Tramo libre más cercano del mismo bruto, de la misma duración (para cambiar un recurso que repite): segundo o None."""
    d = b - a; usados_ = [(a2, b2) for c2, a2, b2, o2, z2, _ in _us if c2 == c and z2 == "cuerpo" and o2 != o]
    for k in range(1, 121):
        for t in (a - 0.5 * k, a + 0.5 * k):
            if t >= 0 and all(t + d <= a2 - 0.3 or t >= b2 + 0.3 for a2, b2 in usados_): return round(t, 1)
for r_ in _rep: print(r_)
for c, a, b, o, z, rb in _us:
    if rb and z == "cuerpo" and any(f" {c} " in r_ and _mm(o) in r_ for r_ in _rep):
        t = _libre(c, a, b, o); print(f"  -> el recurso de {c} en {_mm(o)} ({a:.1f} s): tramo libre más cercano en {t} s (míralo con tira.py antes de usarlo)" if t is not None else f"  -> el recurso de {c} en {_mm(o)}: no hay tramo libre cerca: otro bruto")
if _rep: parar("Hay trozos de bruto que salen dos veces: cambia el recurso, recorta el V(…) o la frase en edl.py, o, si es a propósito, REPETIR_OK en plan.py")
# ---- tráiler-resumen: planos cortos y variados ----
# Lucas, 2026-11-17: «el primer clip se ve muy largo… si la intro es un recap, los clips tienen que ser llamativos para la
# retención». Un recurso del tráiler de más de 2,6 s se monta con varios planos (BROLL con lista).
_g = []
for v in vid:
    if v["o"] >= _cuerpo or not v["b"]: continue
    if _g and _g[-1][-1]["clip"] == v["clip"] and _g[-1][-1]["o"] + _g[-1][-1]["n"] == v["o"] and _g[-1][-1]["in"] + _g[-1][-1]["n"] == v["in"]: _g[-1].append(v)
    else: _g.append([v])
for pl in _g:
    n = sum(v["n"] for v in pl)
    if n > F(2.6): print(f"AVISO tráiler: el recurso de {pl[0]['clip']} en {_mm(pl[0]['o'])} dura {n / FPS:.1f} s: en el tráiler, 1,5–2,5 s por plano (BROLL con lista de varios animales o momentos llamativos)")

# ---- gráficos ----
if TITULO and "titulo" in M:
    items.append({"t": "titulo", "f0": M["titulo"], "f1": M["titulo"] + F(TITULO.get("dur", 4.0)), "arriba": TITULO.get("arriba", ""), "grande": TITULO["grande"], "abajo": TITULO.get("abajo", "")})
for s in L.secciones:
    items.append({"t": "seccion", "f0": s["o"] + F(0.12), "f1": s["o"] + F(3.12), "n": s["n"], "de": len(L.secciones), "titulo": s["titulo"], "sub": s["sub"],
                  **({} if ajuste("CONTADOR_CAPITULOS", False) else {"contador": False})})
for a, d, reg, nueva in MAPAS:
    f0 = L.ancla(a); items.append({"t": "mapa", "f0": f0, "f1": f0 + F(d), "reg": reg, "nueva": nueva})
for a, d, txt, *col in SUBS:
    f0 = L.ancla(a); items.append({"t": "sub", "f0": f0, "f1": f0 + F(d), "txt": txt, **({"color": col[0]} if col else {})})
if SUSCRIBE:
    f0 = L.ancla(SUSCRIBE[0]); items.append({"t": "suscribe", "f0": f0, "f1": f0 + F(2.8), "txt": SUSCRIBE[1]})
for a, n, *op in BOTONES:
    o = dict(op[0]) if op else {}; vel = float(o.pop("vel", 1)); base = f"b{n:02d}"; bj = f"{ESTUDIO}/public/botones/{base}.json"
    if not os.path.exists(bj): raise SystemExit(f"No existe el botón {n} ({bj}); los hay del 1 al 16")
    arch = f"{base}_{IDIOMA}" if IDIOMA and os.path.exists(f"{ESTUDIO}/public/botones/{base}_{IDIOMA}.webm") else base      # su versión en el idioma del vídeo, si la hay
    if IDIOMA and IDIOMA != "es" and arch == base:
        print(f"AVISO: el vídeo es en «{IDIOMA}» y el botón {n} no tiene versión en ese idioma: si lleva texto (base/recursos.md -> Botones), saldrá en español. El 2 se traduce con herramientas/boton_idioma.py")
    caja = json.load(open(bj)); f0 = L.ancla(a); o.setdefault("esc", BOTON_ESC)
    items.append({"t": "boton", "f0": f0, "f1": f0 + F(caja["dur"] / vel), "n": n, "arch": arch, "vel": vel, "caja": caja, "snd": [f"botones/{base}.mp3", 0.35, vel], **o})
# Cada gráfico propio recibe el idioma del vídeo y el logo de la marca en ese idioma (marca.json -> "logo", archivo de
# estudio/public/personal/<creador>/). Si el logo de ese idioma no está, va "" y se avisa: mejor sin logo que con el de otro canal.
_m = marca(); _logo = _m.get("logo")
if _logo and not os.path.exists(f"{ESTUDIO}/public/personal/{CREADOR}/{_logo}"):
    print(f"AVISO: falta el logo de la marca para «{IDIOMA}»: estudio/public/personal/{CREADOR}/{_logo}. Los gráficos propios que lo usan saldrán SIN logo. Pídeselo al creador.")
    _logo = ""
for a, d, tipo, *op in PROPIOS:
    f0 = L.ancla(a); items.append({"t": tipo, "f0": f0, "f1": f0 + F(d), "idioma": IDIOMA, **({} if _logo is None else {"logo": _logo}), **(op[0] if op else {})})
for i, e in enumerate(esp):
    if e["tipo"] != "dato": continue
    pl = [v for v in vid if v.get("esp") == i and not v["b"]]
    if not pl: print("AVISO: dato sin plano (tapado por recurso o sin sitio):", e["grande"]); continue
    v = pl[0]; x, y, mw = 0.5, 0.74, 0.4
    if v["cx"] is not None and v["z1"] > 1.2:   # cara a un lado -> la cifra, centrada en el hueco del otro
        w, h, cxr, cyr = encuadre(v["z1"], v["cx"], v["cy"], v["ax"], v["ay"]); xo = (v["cx"] * v["z1"] - cxr) / AW
        x, y = ((xo + 0.11 + 0.98) / 2 if xo < 0.5 else (xo - 0.11 + 0.02) / 2), 0.46; mw = (0.98 - xo - 0.11 if xo < 0.5 else xo - 0.11 - 0.02) * 0.92
    else: print("AVISO: dato sin cara, va abajo al centro:", e["grande"])
    items.append({"t": "dato", "f0": v["o"] + F(0.08), "f1": pl[-1]["o"] + pl[-1]["n"], "grande": e["grande"], "peq": e["peq"], "x": round(x, 3), "y": y, "mw": round(mw, 3)})
for a, d, txt, *op in GOLPES:      # (ancla, segundos, "TEXTO"[, {"y": 0.62}]): y = altura de la base si abajo tapa lo que se enseña
    f0 = L.ancla(a); items.append({"t": "golpe", "f0": f0, "f1": f0 + F(d), "txt": txt, **(op[0] if op else {})})
for a, ret, d, txt in NOTAS:
    f0 = L.ancla(a) + F(ret); items.append({"t": "nota", "f0": f0, "f1": f0 + F(d), "txt": txt})
# ---- ningún texto se va antes de que se haya DICHO entero y se pueda leer (comun.texto_dicho) ----
# Se alarga solo hasta medio segundo después de su última palabra (o hasta la pausa) y nunca menos que el tiempo de
# leerlo; sin pisar el texto siguiente. Imprime lo que alarga: si un texto crece mucho, mira si el ancla está bien.
_voz = {"golpe", "nota"} | {p[2] for p in PROPIOS}
_cortes = sorted({v["o"] for v in vid} | {L.total})
_tx = sorted([it for it in items if it["t"] in _voz and any(it.get(k) for k in ("txt", "grande", "sub"))], key=lambda x: x["f0"])
for it in _tx:
    txt = " ".join(str(it.get(k, "")) for k in ("txt", "grande", "sub") if it.get(k))
    fe = it["f0"] + F(getattr(plan, "RETARDO_TEXTO", {}).get(it["t"], 0))      # desde cuándo se puede LEER (una burbuja que asoma)
    fin, ult = texto_dicho(L.palabras, it.get("txt") or it.get("grande") or txt, fe, it["f1"])
    fin = max(fin, fe + max(F(1.2), F(0.6 + 0.3 * len(txt.split()))))
    if fin <= it["f1"]: continue
    sig = min((o["f0"] for o in items if o is not it and o["f0"] > it["f0"] and o["t"] not in ("trk", "boton", "suscribe") and o["f0"] < fin + F(0.8)), default=None)
    tope = sig - F(0.3) if sig is not None else L.total
    if tope < fin: print(f"AVISO: «{txt[:30]}» necesita hasta {fin / FPS:.1f} s para decirse y leerse, pero el texto siguiente entra en {sig / FPS:.1f} s: sepáralos en plan.py")
    nuevo = max(it["f1"], min(fin, tope))
    cs = [c for c in _cortes if nuevo - F(0.5) < c < nuevo and c - it["f0"] >= F(0.5)]      # sin colas: si cruza un corte, lo pisa medio segundo
    if cs and nuevo > it["f1"] and max(cs) + F(0.5) <= tope: nuevo = max(cs) + F(0.5)
    if nuevo > it["f1"]: print(f"texto alargado {(nuevo - it['f1']) / FPS:+.1f} s hasta que se dice y se lee: «{txt[:40]}»" + (f" (última palabra «{ult['w']}»)" if ult else "")); it["f1"] = nuevo
    it["_min"], it["_tope"] = nuevo, tope
# ---- los textos van con los cortes ----
# Un texto que acaba a unos fotogramas de un corte se ajusta a él, y uno que entra unos fotogramas antes de un corte entra
# EN el corte (Lucas, 2026-11-12: un texto que se cuela 2 fotogramas en el plano siguiente, o que se va 3 antes, se nota).
# Nunca se adelanta la entrada: un texto no sale antes de su palabra. Lo demás (que entre en SU palabra y aguante la
# frase) se decide en plan.py y se mide con timing_textos.py.
_cortes = sorted({v["o"] for v in vid} | {L.total})
_ajusta = {"golpe", "nota", "sub", "suscribe"} | {p[2] for p in PROPIOS}
for it in items:
    if it["t"] not in _ajusta: continue
    c1 = min(_cortes, key=lambda c: abs(c - it["f1"])); c0 = min((c for c in _cortes if c > it["f0"]), default=None)
    if 0 < abs(c1 - it["f1"]) <= F(0.24) and c1 - it["f0"] >= F(0.5):
        if c1 >= it.get("_min", 0): it["f1"] = c1
        elif c1 + F(0.5) <= it.get("_tope", 10 ** 9): it["f1"] = c1 + F(0.5)      # no se recorta lo que hace falta para decirlo y leerlo: pisa el plano siguiente medio segundo
    if c0 is not None and c0 - it["f0"] <= F(0.2) and it["f1"] - c0 >= F(0.5): it["f0"] = c0
for it in items: it.pop("_min", None); it.pop("_tope", None)
# ---- el botón de suscribir va SOLO en pantalla ----
# Lucas, 2026-11-14 (prueba-3): «se solapan el botón de suscribir y el texto de "soltar cable"». El botón se cuelga de
# «suscribiros» y el texto, de la frase de justo después: los dos caen abajo en el centro. Ningún texto ni gráfico comparte
# tiempo con el botón: el texto va a la repetición de su frase o a la siguiente, después del botón (o el botón a otra
# frase). No se renderiza con un choque.
_choques = [(b, it) for b in items if b["t"] in ("boton", "suscribe") for it in items
            if it is not b and it["t"] not in ("boton", "suscribe") and it["f0"] < b["f1"] and it["f1"] > b["f0"]]
for b, it in _choques:
    txt = " ".join(str(it.get(k, "")) for k in ("txt", "grande", "titulo", "sub") if it.get(k)) or it["t"]
    print(f"CHOQUE: «{txt[:40]}» ({it['t']}, {it['f0'] / FPS:.1f}-{it['f1'] / FPS:.1f} s) pisa el botón de suscribir ({b['f0'] / FPS:.1f}-{b['f1'] / FPS:.1f} s)")
if _choques: raise SystemExit("El botón de suscribir va solo: cuelga esos textos de después del botón (la repetición de su frase o la siguiente) o mueve el botón en plan.py")
# el botón acaba mientras él habla: si no, su final (el cuadrado rojo recogiéndose) se ve sobre lo que viene después de la
# voz (un negro, la intro, el outro, un clip sin voz). vaciamos-estanque (2026-11-19): 0,5 s sobre un negro; se arregló con
# "vel": 1.45. Seguir sobre otra pieza HABLADA (un corte dentro de lo que dice) es normal y no avisa.
for b in [it for it in items if it["t"] in ("boton", "suscribe")]:
    sobra = [p for p in P if p["k"] != "T" and p["o"] < b["f1"] and p["o"] + p["n"] > b["f0"]]
    fin = min([p["o"] for p in sobra] + [L.total])
    if b["f1"] > fin + F(0.1):
        que = f"{sobra[0]['clip']}" + (f" ({sobra[0]['tag']})" if sobra and sobra[0].get("tag") else "") if sobra else "el final del vídeo"
        print(f"AVISO BOTÓN: el botón ({b['f0'] / FPS:.1f}-{b['f1'] / FPS:.1f} s) sigue {(b['f1'] - fin) / FPS:.1f} s sobre {que}, que no es voz: "
              f"sube \"vel\" en BOTONES o adelanta su ancla")
# ---- dos gráficos nunca se pisan en pantalla ----
# (comun.caja_texto: dónde cae cada uno). La tarjeta de capítulo y el rótulo de la especie de su primera frase eran el
# caso típico: el rótulo se cuelga de DESPUÉS de la tarjeta (su f1 + 0,3 s: la siguiente vez que se nombra, o con un
# desplazamiento), o se sube con "y" / va a un lado con "lado".
_vis = [it for it in items if it["t"] not in ("boton", "suscribe")]
_pis = []
for i, x in enumerate(_vis):
    for y in _vis[i + 1:]:
        if not (x["f0"] < y["f1"] and y["f0"] < x["f1"]): continue
        if x["t"] in ("mapa", "titulo") and y["t"] in ("mapa", "titulo"): continue     # a pantalla completa: el segundo sustituye al primero (mapas encadenados)
        # los rótulos con flecha se mueven: se comparan instante a instante (5 muestras del tiempo en que coinciden)
        a0, a1 = max(x["f0"], y["f0"]), min(x["f1"], y["f1"])
        _ms = [a0 + (a1 - a0) * k // 4 for k in range(5)] if "trk" in (x["t"], y["t"]) else [None]
        if max(cruce(caja_texto(x, m), caja_texto(y, m)) for m in _ms) > 0.0015:
            nom = lambda it: (" ".join(str(it.get(k, "")) for k in ("txt", "grande", "titulo") if it.get(k)) or it["t"])[:30]
            _pis.append(f"PISA: «{nom(x)}» ({x['t']}, {x['f0'] / FPS:.1f}-{x['f1'] / FPS:.1f} s) y «{nom(y)}» ({y['t']}, {y['f0'] / FPS:.1f}-{y['f1'] / FPS:.1f} s) a la vez y en el mismo sitio")
for p_ in _pis: print(p_)
if _pis: parar("Dos gráficos se pisan: retrasa el segundo hasta que se vaya el primero (su ancla + segundos), súbelo (\"y\"), llévalo a un lado (\"lado\") o quítalo. Nunca se renderiza con un solape.")
# ---- ningún texto se sale del cuadro (Lucas, 2026-11-17: «los textos no se pueden salir de pantalla nunca, es un error muy
# grande»; en alimentacion v2, dos rótulos con lado="der" se cortaban por la derecha). Los componentes ya se encogen y se
# pegan al borde con margen; esto avisa si aun así algo queda fuera (texto larguísimo, x a mano, un gráfico propio nuevo).
_fue = [(it, fuera(caja_texto(it))) for it in items if it["t"] not in ("titulo", "mapa")]
_fue = [(it, d) for it, d in _fue if d > 0]
for it, d in _fue:
    nom = (" ".join(str(it.get(k, "")) for k in ("txt", "grande", "titulo") if it.get(k)) or it["t"])[:40]
    print(f"SE SALE: «{nom}» ({it['t']}, {it['f0'] / FPS:.1f} s) se sale del cuadro un {d * 100:.1f} %")
if _fue: raise SystemExit("Un texto se sale del cuadro: acórtalo (o pártelo en dos líneas con «|»), quita \"x\" a mano o cámbialo de lado. Nunca se renderiza con un texto cortado.")
items.sort(key=lambda x: x["f0"])
# rangos con gráfico (los que Remotion renderiza): se funden los que quedan a menos de medio segundo
rangos = []
for it in items:
    if rangos and it["f0"] <= rangos[-1][1] + F(0.48): rangos[-1][1] = max(rangos[-1][1], it["f1"])
    else: rangos.append([it["f0"], it["f1"]])
os.makedirs(os.path.dirname(CAPAS_JSON), exist_ok=True)
json.dump({"fps": FPS, "total": L.total, "ancho": AW, "alto": AH, "creador": CREADOR, "marca": marca(), "items": items, "rangos": rangos}, open(CAPAS_JSON, "w", encoding="utf-8"), ensure_ascii=False)
# ---- tramos de render: ~24 s o 12 planos, sin partir ningún gráfico ----
tramos = []; cur = []
libre = lambda fin: not any(r[0] < fin < r[1] for r in rangos)
for v in vid:
    cur.append(v); fin = v["o"] + v["n"]
    if (fin - cur[0]["o"] >= F(24) or len(cur) >= 12) and libre(fin): tramos.append(cur); cur = []
if cur: tramos.append(cur)
json.dump({"total": L.total, "tramos": tramos, "rangos": rangos}, open(f"{TRABAJO}/video.json", "w"))
dur = np.array([v["n"] / FPS for v in vid]); zs = [v for v in vid if v["z0"] != 1 or v["z1"] != 1]
print("planos de menos de 0,5 s:", [(v["o"], v["n"]) for v in vid if v["n"] < F(0.48)])
print(f"{len(vid)} planos, media {dur.mean():.2f} s, mediana {np.median(dur):.2f} s, {100 * (dur < 1).mean():.0f} % < 1 s, máx {dur.max():.1f} s; {len(vid) / (L.total / FPS / 60):.1f} cortes/min")
print(f"{len(zs)} planos con escala, {sum(1 for v in vid if v.get('t'))} animados, {sum(1 for v in vid if v['z1'] >= min(1.55, Z_FUERTE))} fuertes, {nb} recursos; máx planos por tramo {max(len(t) for t in tramos)}; {len(tramos)} tramos; {len(rangos)} rangos de gráficos = {sum(b - a for a, b in rangos) / FPS:.0f} s")
print("especiales:", [(e["tipo"], e["f0"], e["f1"]) for e in sorted(esp, key=lambda e: e["f0"]) if e["tipo"] in ("entra", "detalle", "fijo")])
print("planos > 5 s (¿falta un recurso o un corte de escala?):", [(round(v["o"] / FPS), round(v["n"] / FPS, 1), v["clip"], v["b"]) for v in vid if v["n"] > F(5)])
print("Antes de renderizar: timing_textos.py (cada texto frente a la voz y los cortes), hoja_recursos.py (mirar TODOS los recursos) y ver.py en los frames con texto o zoom.")
