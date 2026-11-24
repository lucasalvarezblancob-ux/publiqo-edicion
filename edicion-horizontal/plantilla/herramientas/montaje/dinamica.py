"""Motor de dinamismo: convierte la línea de voz en planos con juego de escala (cortes de escala y zooms).
Números medidos en refs/dinamicos (YoSoyPlex, TheGrefg, elxokas) y corregidos por Lucas en `ramon` (2026-11-11):
- al hablar, un cambio visual cada 2,5-4,5 s: corte de escala DE GOLPE en un límite de frase (sin quitar fotogramas);
- escalas alternas x1,0 / x1,12-1,5; frase fuerte x1,65 mientras dura la frase y vuelta por corte;
- el punch-in se centra en la cara (YuNet, herramientas/caras.py) y la CONTIENE durante todo el plano; si no cabe, cierra menos;
- pocos zooms animados (entrada rápida con frenada; zoom-out al abrir sección); nada de zoom lento sostenido a cámara;
- "dato": plano x1,3 con la cara a un tercio para dejar sitio a la cifra al otro lado.
Todas las coordenadas van en píxeles del LIENZO (ANCHO x ALTO de proyecto.py)."""
import json
import numpy as np
from comun import ALTO as AH, ANCHO as AW, F, FPS, ajuste, norm

# Lo que lleva ajuste(...) se puede cambiar en personal/<creador>/ajustes.py (gusto del creador) sin tocar este archivo.
NIVELES = ajuste("ESCALAS", [1.0, 1.3, 1.0, 1.45, 1.0, 1.15, 1.0, 1.35, 1.0, 1.5, 1.0, 1.25])   # G002: vuelta a ×1,0 entre escalas (13 de 13 refs)
VUELTA = ajuste("ESCALAS_VUELTA", True)
Z_FUERTE = ajuste("Z_FUERTE", 1.65)
SEG_MIN, SEG_MAX = (F(s) for s in ajuste("CAMBIO_CADA", (2.48, 4.48)))   # segundos entre cambios de escala
CARA_Y = ajuste("CARA_Y", 0.38)                         # la cara queda al 38 % del alto
PAUSA = round(0.14 * FPS, 3)         # pausa entre palabras (en frames) que vale como límite de frase
CARA_MAX = 1150 / 3840                # la cara no pasa del ~30 % del ancho del cuadro
# Plano SIN cara (de espaldas, manos, el recinto): sin corte de escala. Centrado a ciegas, el zoom acaba en un hombro o en
# una pared (Lucas, prueba-3 v2, 10:25 y 10:35: «está zoomeado a su hombro, mejor ahí no tener zoom»). Si hay un sujeto
# que merece acercarse, se hace con su centro (BROLL con (zoom, cx, cy), DETALLE, ENTRADAS sobre la cara).
Z_SIN_CARA = ajuste("Z_SIN_CARA", 1.0)


class Caras:
    def __init__(self, carpeta):
        self.c, self.carpeta = {}, carpeta

    def en(self, clip, f_in, n):
        """Cara en [f_in, f_in+n) del bruto: mediana y recorrido, en px del lienzo; None si no hay cara fiable."""
        if clip not in self.c:
            try: self.c[clip] = json.load(open(f"{self.carpeta}/caras_{clip}.json"))
            except FileNotFoundError: self.c[clip] = None
        d = self.c[clip]
        if not d: return None
        a, b = max(0, int(f_in / FPS / d["paso"])), int((f_in + n) / FPS / d["paso"]) + 2
        m = d["caras"][a:b]; ok = np.array([x for x in m if x], float)
        if not m or len(ok) / len(m) < 0.6: return None
        ok = ok * (AW / d.get("ancho", AW))        # el bruto puede tener otra resolución que el lienzo
        # mediana, y el recorrido de la cara en el plano (para que el encuadre la contenga entera todo el rato)
        return {"cx": float(np.median(ok[:, 0])), "cy": float(np.median(ok[:, 1])), "w": float(np.median(ok[:, 2])), "wmax": float(ok[:, 2].max()),
                "x0": float(ok[:, 0].min()), "x1": float(ok[:, 0].max()), "y0": float(ok[:, 1].min()), "y1": float(ok[:, 1].max()), "cob": len(ok) / len(m)}


def contener(v, c):
    """Ajusta escala y centro del plano para que la cabeza quepa en el recorte en TODO su recorrido (no solo en la mediana).
    Lección de ramon v2 (4:18): centrar en la mediana de una cara que se mueve acaba en un zoom a la pared."""
    z = max(v["z0"], v["z1"])
    if z <= 1: return
    mx, arriba, abajo = 0.95 * c["wmax"], 1.15 * c["wmax"], 1.5 * c["wmax"]       # margen lateral, pelo, barbilla y cuello
    z = min(z, AW * 0.94 / (c["x1"] - c["x0"] + 2 * mx), AH * 0.94 / (c["y1"] - c["y0"] + arriba + abajo))
    if c["cob"] < 0.85: z = min(z, 1.2)                                           # detección floja: se cierra poco
    z = max(1.0, round(z, 3))
    v["z0"], v["z1"] = (z, z) if v["z0"] == v["z1"] else ((1.0, z) if v["z1"] > v["z0"] else (z, 1.0))
    if z <= 1.001: v["z0"] = v["z1"] = 1.0; v["t"] = 0; return
    aw, ah = AW / z, AH / z
    xs = min(max(c["cx"] - v["ax"] * aw, c["x1"] + mx - aw), c["x0"] - mx); v["cx"] = xs + v["ax"] * aw
    ys = min(max(c["cy"] - v["ay"] * ah, c["y1"] + abajo - ah), c["y0"] - arriba); v["cy"] = ys + v["ay"] * ah


def encuadre(z, cx, cy, ax=0.5, ay=CARA_Y):
    """Tamaño escalado y esquina del recorte ANCHO x ALTO para una escala fija."""
    w, h = 2 * round(AW / 2 * z), 2 * round(AH / 2 * z)
    x = (w - AW) / 2 if cx is None else min(max(cx * z - ax * AW, 0), w - AW)
    y = (h - AH) * 0.4 if cy is None else min(max(cy * z - ay * AH, 0), h - AH)
    return w, h, 2 * int(x / 2), 2 * int(y / 2)


def planos_de_voz(P, W, caras, esp, secciones, sin_escala=()):
    """P: piezas de la línea; W: palabras con o0/o1 (frames de salida).
    esp: especiales [{f0, f1, tipo: 'fuerte'|'dato'|'entra'|'detalle'|'fijo', z, ax}] en frames de salida.
    Devuelve los planos de vídeo; cada plano especial lleva 'esp' = índice en la lista."""
    ini_seccion = {s["o"] for s in secciones}
    vid = []; k = 0
    for p in P:
        base = {"clip": p["clip"], "speed": p["speed"], "b": 0, "t": 0, "cx": None, "cy": None, "ax": 0.5, "ay": CARA_Y}
        if p["k"] != "T" or id(p) in sin_escala:
            vid.append({**base, "in": p["in"], "n": p["n"], "o": p["o"], "z0": 1.0, "z1": 1.0}); continue
        f0, f1 = p["o"], p["o"] + p["n"]
        ws = [w for w in W if f0 <= w["o0"] < f1 and w["clip"] == p["clip"]]
        cand = [int(w["o0"]) - F(0.08) for a, w in zip(ws, ws[1:]) if w["o0"] - a["o1"] >= PAUSA]     # pausa >= 0,14 s
        todas = [int(w["o0"]) - F(0.08) for w in ws[1:]]
        mios = [(i, e) for i, e in enumerate(esp) if e["f0"] < f1 - F(0.32) and e["f1"] > f0 + F(0.32)]
        obl = sorted({f for _, e in mios for f in (e["f0"], e["f1"]) if f0 + F(0.32) < f < f1 - F(0.32)})
        cortes = [f0]
        while True:
            u = cortes[-1]
            sig = next((f for f in obl if f > u), None)
            c = next((f for f in cand if u + SEG_MIN <= f <= f1 - F(0.8)), None)
            if c is None or c > u + SEG_MAX: c = next((f for f in todas if u + F(3.2) <= f <= f1 - F(0.8)), None)
            if sig is not None and (c is None or sig <= c or sig - c < F(0.8)): c = sig
            if c is None: break
            cortes.append(c)
        cortes.append(f1)
        for a, b in zip(cortes, cortes[1:]):
            cara = caras.en(p["clip"], p["in"] + a - f0, b - a)
            e = next(((i, e) for i, e in mios if min(b, e["f1"]) - max(a, e["f0"]) >= 0.7 * (b - a)), None)
            v = {**base, "in": p["in"] + a - f0, "n": b - a, "o": a, "z0": 1.0, "z1": 1.0}
            if e: v["esp"] = e[0]
            dado = bool(e and "cx" in e[1])
            if dado: cara = {"cx": e[1]["cx"], "cy": e[1]["cy"], "w": AW * 0.15625}; v["ay"] = 0.5      # centro dado (animal seguido)
            tope = max(1.0, min(1.8, CARA_MAX * AW / max(cara["w"], 1))) if cara else Z_SIN_CARA     # sin cara: sin zoom (ver Z_SIN_CARA)
            if cara: v["cx"], v["cy"] = cara["cx"], cara["cy"]
            if e and e[1]["tipo"] == "fijo": pass
            elif e and e[1]["tipo"] in ("entra", "detalle"): v.update(z0=1.0, z1=min(e[1]["z"], tope), t=e[1].get("t", F(0.32)))
            elif e: v.update(z0=min(e[1]["z"], tope), z1=min(e[1]["z"], tope), ax=e[1].get("ax", 0.5))
            elif cara and a in ini_seccion and b - a > F(1.2): v.update(z0=min(1.4, tope), z1=1.0, t=F(0.48))   # abre la sección
            else:
                k += 1; z = min(NIVELES[k % len(NIVELES)], tope)
                if vid and vid[-1]["clip"] == p["clip"] and abs(vid[-1]["z1"] - z) < 0.08: k += 1; z = min(NIVELES[k % len(NIVELES)], tope)
                # G002: nunca dos escalas seguidas en la misma toma; tras un plano ampliado (rotación, golpe o detalle) se
                # vuelve a ×1,0. Rollback con deshacer_cambio.py (escribe ESCALAS antiguas y ESCALAS_VUELTA = False).
                if VUELTA and z > 1.0 and vid and vid[-1]["clip"] == p["clip"] and vid[-1]["z1"] > 1.01: z = 1.0
                v.update(z0=z, z1=z)
            if cara and not dado: contener(v, cara)
            vid.append(v)
    if VUELTA:      # G002: un plano de la rotación justo antes de un golpe o detalle del plan (misma toma) va a ×1,0
        for x, y in zip(vid, vid[1:]):
            if "esp" not in x and not x.get("t") and x["z1"] > 1.01 and x["clip"] == y["clip"] and y["z1"] > 1.01 and "esp" in y:
                x.update(z0=1.0, z1=1.0)
    return vid


# Fuente que no es 16:9 (stock DCI 4096x2160, vertical): se recorta al centro a la proporción del lienzo ANTES de escalar.
# Con una fuente 16:9 no hace nada. Lo usan filtro_zoom y las hojas (ver.py, hoja_recursos.py, hoja_textos.py).
RECORTE_169 = f"crop=w='2*trunc(min(iw,ih*{AW}/{AH})/2)':h='2*trunc(min(ih,iw*{AH}/{AW})/2)',"


def filtro_zoom(v):
    """Filtro ffmpeg (tras fps=FPS) para la escala y el encuadre de un plano. Siempre deja la imagen en ANCHO x ALTO."""
    z0, z1, t, n = v["z0"], v["z1"], v.get("t", 0), v["n"]
    # fuente que no es 16:9 (stock DCI 4096x2160, vertical): primero se recorta al centro a la proporción del lienzo; con una
    # fuente 16:9 no hace nada (min(iw, ih*16/9) = iw). Sin esto, scale a ANCHO x ALTO la deformaba (vaciamos-estanque-2,
    # 2026-11-19). En un vertical el centro casi nunca es el sujeto: ahí, mejor una copia _h recortada a mano a su altura.
    pre = RECORTE_169
    if z0 == 1 and z1 == 1 and not v.get("anim"): return pre + f"scale={AW}:{AH}:flags=bicubic,"
    cx, cy, ax, ay = v.get("cx"), v.get("cy"), v.get("ax", 0.5), v.get("ay", CARA_Y)
    an = v.get("anim")
    if an and t == 0 and z0 == z1:      # vaivén / rampa hacia un remate (paso3: VAIVENES, ZOOM_REMATE), sobre la escala del plano
        u = f"(t-{an['desde'] / FPS:.4f})"
        if an["tipo"] == "vaiven":
            e, h_, s = an["ent"] / FPS, an["aguanta"] / FPS, an["sal"] / FPS
            env = (f"if(lt({u},0),0,if(lt({u},{e:.4f}),1-pow(1-{u}/{e:.4f},3),if(lt({u},{e + h_:.4f}),1,"
                   f"if(lt({u},{e + h_ + s:.4f}),0.5+0.5*cos(PI*({u}-{e + h_:.4f})/{s:.4f}),0))))")
            Z = f"({z1}*(1+{an['z'] - 1:.4f}*{env}))"
        else:
            Z = f"({z1}*(1+{an['vel']:.4f}*min(max({u},0),{(an['hasta'] - an['desde']) / FPS:.4f})))"
        xs = f"({AW}*{Z}-{AW})/2" if cx is None else f"min(max({cx:.0f}*{Z}-{ax * AW:.0f},0),max({AW}*{Z}-{AW + 2},0))"
        ys = f"({AH}*{Z}-{AH})/2" if cy is None else f"min(max({cy:.0f}*{Z}-{ay * AH:.0f},0),max({AH}*{Z}-{AH + 2},0))"
        return pre + f"scale=w='2*trunc({AW // 2}*{Z}+0.01)':h='2*trunc({AH // 2}*{Z}+0.01)':eval=frame:flags=bicubic,crop=w={AW}:h={AH}:x='{xs}':y='{ys}',"
    if t == 0 and z0 == z1:
        w, h, x, y = encuadre(z1, cx, cy, ax, ay)
        return pre + f"scale={w}:{h}:flags=bicubic,crop={AW}:{AH}:{x}:{y},"
    if t:   # animado con frenada (ease-out cúbico) en t frames, luego se queda
        Z = f"({z1}+({z0 - z1:.4f})*pow(max(0,1-t/{t / FPS:.3f}),3))"
    else:   # lento, lineal en todo el plano (solo para imágenes fijas, paisajes y rótulos)
        Z = f"({z0}+{(z1 - z0) / (n / FPS):.5f}*t)"
    # OJO: en crop, iw/ih se quedan con el tamaño del PRIMER fotograma aunque scale cambie de tamaño en cada uno
    # (ramon v2: todos los zooms animados recortaban desde la esquina). Por eso el recorte se calcula con Z(t), no con iw.
    xs = f"({AW}*{Z}-{AW})/2" if cx is None else f"min(max({cx:.0f}*{Z}-{ax * AW:.0f},0),max({AW}*{Z}-{AW + 2},0))"
    ys = f"({AH}*{Z}-{AH})/2" if cy is None else f"min(max({cy:.0f}*{Z}-{ay * AH:.0f},0),max({AH}*{Z}-{AH + 2},0))"
    return pre + f"scale=w='2*trunc({AW // 2}*{Z}+0.01)':h='2*trunc({AH // 2}*{Z}+0.01)':eval=frame:flags=bicubic,crop=w={AW}:h={AH}:x='{xs}':y='{ys}',"
