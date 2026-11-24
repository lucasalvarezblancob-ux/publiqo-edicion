#!/usr/bin/env python3
"""Detecta cortes de un vídeo (referencia o bruto) y mide el ritmo.

Uso: detectar_cortes.py VIDEO SALIDA.json [--umbral 10] [--tramo 60]
  1) ffmpeg scdet a 480 px puntúa cada fotograma (0-100) -> <salida>.scd.txt (se reutiliza si existe)
  2) corte = pico local con puntuación >= umbral y al menos 3x la mediana de su vecindario (±12 f)
     -> descarta movimiento de cámara y flashes sostenidos
  3) escribe cortes, duración de cada plano y estadísticas por tramo de --tramo segundos
Los fundidos y whips salen como varios picos seguidos: se agrupan (<0,2 s) y se marcan "transicion".
--rafagas: para intros con micro-flash o estroboscopio (planos de 2-5 fotogramas). El vecindario se mide con el
  percentil 25 en vez de la mediana (si no, una ráfaga entera se descarta como «flash sostenido») y un grupo de >= 3
  picos separados >= 2 fotogramas, con la imagen quieta entre ellos, se cuenta como otros tantos cortes ("rafaga"), no
  como una transición (la cámara rápida, que cambia en todos los fotogramas, no cuenta). Con --hasta S, solo en los
  primeros S segundos (la intro): una cámara rápida muy brusca más adelante también daría picos seguidos.
  Sin --rafagas, el resultado es el de siempre (comparable con las fichas antiguas).
"""
import argparse, json, re, statistics as st, subprocess, sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("salida")
ap.add_argument("--umbral", type=float, default=10.0)
ap.add_argument("--tramo", type=float, default=60.0)
ap.add_argument("--rafagas", action="store_true")
ap.add_argument("--hasta", type=float, help="con --rafagas: solo hasta este segundo (la intro); después, como siempre")
a = ap.parse_args()

sal = Path(a.salida); scd = sal.with_suffix(".scd.txt")
if not scd.exists():
    scd.parent.mkdir(parents=True, exist_ok=True)
    # ffmpeg se lanza dentro de la carpeta de salida: así el nombre no lleva "C:" (rompe el filtro en Windows)
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(Path(a.video).resolve()), "-vf",
                    f"scale=480:-2,scdet=threshold=6:sc_pass=0,metadata=mode=print:key=lavfi.scd.score:file={scd.name}",
                    "-an", "-f", "null", "-"], check=True, cwd=scd.parent)
t, s = [], []
for ln in scd.read_text().splitlines():
    m = re.search(r"pts_time:([\d.]+)", ln)
    if m: t.append(float(m.group(1))); continue
    m = re.search(r"score=([\d.]+)", ln)
    if m: s.append(float(m.group(1)))
n = min(len(t), len(s)); t, s = t[:n], s[:n]
dur = t[-1]

picos = []
for i in range(1, n - 1):
    if s[i] < a.umbral or s[i] < s[i - 1] or s[i] < s[i + 1]: continue
    vec = s[max(0, i - 12):i - 1] + s[i + 2:i + 13]
    raf = a.rafagas and (a.hasta is None or t[i] <= a.hasta + 1)
    base = (sorted(vec)[len(vec) // 4] if raf else st.median(vec)) if vec else 0
    if s[i] >= 3 * max(base, 0.5):
        picos.append((t[i], s[i]))
# agrupar picos pegados (transición con duración: fundido, whip, flash)
cortes = []
for tt, sc in picos:
    if cortes and tt - cortes[-1]["fin"] < 0.2:
        c = cortes[-1]; c["fin"] = tt; c["tipo"] = "transicion"; c["score"] = max(c["score"], sc); c["_p"].append((tt, sc))
    else:
        cortes.append({"t": round(tt, 3), "fin": tt, "score": round(sc, 1), "tipo": "seco", "_p": [(tt, sc)]})
if a.rafagas:      # un grupo de >= 3 picos separados >= 2 fotogramas = una ráfaga de planos cortísimos, no un fundido
    paso = (t[-1] - t[0]) / max(1, n - 1)
    nuevos = []
    for c in cortes:
        ps = c["_p"]
        # y entre pico y pico la imagen tiene que estar QUIETA (cada micro-plano es estable). En cámara rápida o un
        # trayecto acelerado todos los fotogramas cambian: eso no es una ráfaga de cortes.
        i0 = min(range(n), key=lambda k: abs(t[k] - ps[0][0])); i1 = min(range(n), key=lambda k: abs(t[k] - ps[-1][0]))
        pk = {min(range(i0, i1 + 1), key=lambda k: abs(t[k] - pt)) for pt, _ in ps}
        entre = [s[k] for k in range(i0, i1 + 1) if k not in pk and k - 1 not in pk and k + 1 not in pk] or \
                [s[k] for k in range(i0, i1 + 1) if k not in pk]
        quieto = (st.median(entre) if entre else 0) < 0.25 * st.median([x for _, x in ps])
        dentro = a.hasta is None or ps[0][0] <= a.hasta
        if dentro and len(ps) >= 3 and quieto and min(b_[0] - a_[0] for a_, b_ in zip(ps, ps[1:])) >= 1.5 * paso:
            nuevos += [{"t": round(pt, 3), "fin": pt, "score": round(ps_, 1), "tipo": "rafaga", "_p": []} for pt, ps_ in ps]
        else: nuevos.append(c)
    cortes = nuevos
for c in cortes: c["dur_transicion"] = round(c.pop("fin") - c["t"], 3); c.pop("_p", None)

bordes = [0.0] + [c["t"] for c in cortes] + [dur]
planos = [round(b - a_, 3) for a_, b in zip(bordes, bordes[1:])]

def resumen(v):
    if not v: return {}
    v = sorted(v)
    q = lambda p: round(v[min(len(v) - 1, int(p * len(v)))], 2)
    return {"planos": len(v), "media": round(st.mean(v), 2), "mediana": q(.5), "p10": q(.1), "p90": q(.9),
            "max": round(v[-1], 2), "menos_de_1s": round(sum(x < 1 for x in v) / len(v), 2),
            "mas_de_5s": round(sum(x > 5 for x in v) / len(v), 2)}

tramos = []
k = 0.0
while k < dur:
    v = [p for b, p in zip(bordes, planos) if k <= b < k + a.tramo]
    tramos.append({"desde": k, "hasta": min(k + a.tramo, dur), **resumen(v)})
    k += a.tramo

out = {"video": a.video, "duracion": round(dur, 2), "umbral": a.umbral, "n_cortes": len(cortes),
       "cortes_por_minuto": round(len(cortes) / dur * 60, 1),
       "transiciones_con_duracion": sum(c["tipo"] == "transicion" for c in cortes),
       "cortes_en_rafaga": sum(c["tipo"] == "rafaga" for c in cortes), "modo_rafagas": a.rafagas,
       "global": resumen(planos), "tramos": tramos, "cortes": cortes}
sal.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: out[k] for k in ("duracion", "n_cortes", "cortes_por_minuto", "transiciones_con_duracion", "global")}, ensure_ascii=False))
for tr in tramos: print(f'{int(tr["desde"]//60):02d}:00  planos={tr.get("planos",0):3d}  mediana={tr.get("mediana","-")}  media={tr.get("media","-")}')
