"""Timing de los textos: cada texto del montaje frente a la voz y a los cortes, con avisos. Se mira ANTES de renderizar.

    PY ../../herramientas/montaje/timing_textos.py [tipo …] [--todo]      (desde out/<slug>/, después de paso3_plan.py)

Por cada texto (rótulos, cifras, palabras-golpe, comentarios, subtítulos, gráficos propios con texto): cuándo entra y
sale, las palabras que suenan alrededor con su desfase respecto a la ENTRADA del texto, y los planos que hay debajo.
Avisos (son pistas: decide mirando la línea, no a ciegas):
  ANTES     el texto se lee antes de que se diga su palabra (la primera palabra de la voz que coincide con el texto
            empieza más de 0,5 s después). Cuelga el ancla de ESA palabra, no del principio de la frase.
  2.ª ANTES lo mismo para la segunda línea de un rótulo (más de 1 s): retrásala (p. ej. `subEn`) o alarga el texto.
  A MEDIAS  el texto se va cuando a la frase le quedan una, dos o tres palabras: alárgalo hasta la pausa.
  CORTO     se va antes de que se haya dicho entero (+0,5 s tras su última palabra) o antes de poder leerlo
            (0,6 s + 0,3 s por palabra, mínimo 1,2 s). paso3_plan.py ya los alarga solo; si sale, es que el texto
            siguiente no le deja sitio: sepáralos.
  COLA      el texto se cuela unos fotogramas en el plano siguiente (o entra unos fotogramas antes de un corte):
            acábalo en el corte o deja que pise el plano siguiente al menos medio segundo.
  LECTURA   demasiadas palabras para el tiempo que está en pantalla (más de 4 palabras por segundo).
  PEGADO    entra menos de 0,3 s después de que se vaya otro texto, o coincide con otro: sepáralos.
Sin argumentos enseña solo los textos con aviso; `--todo`, todos; con tipos (`rotulo dato …`), solo esos.
En plan.py, `RETARDO_TEXTO = {"tipo": segundos}` dice cuánto tarda en poder LEERSE el texto de un gráfico desde que
empieza (una mascota que asoma y luego saca la burbuja: 0,5)."""
import json, re, sys
from comun import CAPAS_JSON, FPS, TRABAJO, ajuste, norm, texto_dicho
import plan as _plan

RET = getattr(_plan, "RETARDO_TEXTO", {})
SIN_VOZ = {"seccion", "mapa", "titulo", "logo_intro", "boton", "trk"}       # cuelgan de marcas o de la imagen, no de una palabra
args = [a for a in sys.argv[1:] if not a.startswith("--")]; todo = "--todo" in sys.argv or bool(args)
L = json.load(open(f"{TRABAJO}/linea.json", encoding="utf-8")); W = L["palabras"]
C = sorted(json.load(open(CAPAS_JSON, encoding="utf-8"))["items"], key=lambda i: i["f0"])
V = [v for t in json.load(open(f"{TRABAJO}/video.json"))["tramos"] for v in t]
cortes = sorted({v["o"] for v in V})
# G004: los rótulos de SITUACIÓN y ESTADO (dato, etiqueta partida, contador, marcador, barra) pueden cruzar cortes si no
# se mueven; los de énfasis (golpe, frases) siguen saliendo con el corte. Rollback: deshacer_cambio.py <creador> G004.
INFO = tuple(ajuste("TIPOS_CRUZAN_CORTES", ["dato", "partida", "contador", "marcador", "barra", "mapa"]))
s = lambda f: f / FPS
mmss = lambda f: f"{int(s(f) // 60)}:{s(f) % 60:05.2f}"

def claves(txt):
    """Palabras del texto que sirven para buscarlo en la voz: 5 letras o más (las cortas son artículos y preposiciones), o con cifras."""
    out = set()
    for p in re.split(r"[\s|/·:,.!?*'\"()+-]+", str(txt)):
        n = norm(p)
        if n and (len(n) >= 5 or any(ch.isdigit() for ch in n)): out.add(n)
    return out

def primera(ks, f0, f1, todas=()):
    """Primera palabra de la voz, entre 1 s antes de f0 y f1, que coincide con alguna del texto. Si lo que suena al
    entrar el texto ya es una palabra suya (aunque sea corta: «LIKE piranha»), va en su sitio."""
    for w in W:
        if abs(w["o0"] - f0) <= 0.3 * FPS and norm(w["w"]) in todas: return w
    for w in W:
        if f0 - FPS <= w["o0"] <= f1:
            n = norm(w["w"])
            if n and any(n == k or (len(n) >= 5 and len(k) >= 5 and (n.startswith(k[:5]) or k.startswith(n[:5]))) for k in ks): return w
    return None

textos = [it for it in C if it["t"] not in SIN_VOZ and any(it.get(k) for k in ("txt", "grande", "peq", "sub"))]
n_av = 0
for it in textos:
    if args and it["t"] not in args: continue
    f0, f1 = it["f0"], it["f1"]; ret = RET.get(it["t"], 0); fe = f0 + round(ret * FPS)      # fe: desde cuándo se LEE
    l1 = it.get("txt") or it.get("grande") or ""; l1 = " ".join(l1) if isinstance(l1, list) else l1
    l2 = it.get("sub") or it.get("peq") or ""
    av = []
    if it["t"] != "sub":                                                    # un subtítulo transcribe: va con la voz por definición
        k1 = claves(l1); pal1 = [norm(p) for p in re.split(r"[\s|/·:,.!?*'\"()+-]+", l1) if norm(p)]
        if len(pal1) > 6: k1 = set([p for p in pal1 if p in k1][:2])           # texto largo (una burbuja): manda su sujeto, que va al principio
        w1 = primera(k1, fe, f1, set(pal1))
        if w1 and s(w1["o0"] - fe) > 0.5: av.append(f"ANTES: «{w1['w']}» suena {s(w1['o0'] - fe):.1f} s después de que se lea el texto")
        if l2 and it["t"] != "dato":                                        # la línea pequeña de una cifra es su pie, va con ella
            fe2 = fe + round(float(it.get("subEn", 0)) * FPS); w2 = primera(claves(l2) - claves(l1), fe2, f1 + FPS)
            if w2 and s(w2["o0"] - fe2) > 1.0: av.append(f"2.ª ANTES: «{w2['w']}» suena {s(w2['o0'] - fe2):.1f} s después de que se lea la 2.ª línea")
            if w2 and w2["o0"] >= f1: av.append(f"2.ª línea: «{w2['w']}» se dice cuando el texto ya se ha ido (+{s(w2['o0'] - f1):.1f} s)")
    # ¿se va con la frase a medias?
    dentro = [w for w in W if w["o0"] < f1 <= w["o1"] + 0.3 * FPS]; sig = [w for w in W if w["o0"] >= f1]
    en_corte = any(abs(f1 - c) <= 4 for c in cortes)                         # acabar en un corte es a propósito
    if dentro and sig and not en_corte and sig[0]["o0"] - dentro[-1]["o1"] < 0.2 * FPS:
        k0 = k = W.index(sig[0]); fin = None
        while k + 1 < len(W) and k - k0 < 3 and W[k]["o1"] - f1 < 0.9 * FPS:
            if W[k + 1]["o0"] - W[k]["o1"] >= 0.4 * FPS or W[k + 1]["clip"] != W[k]["clip"]: fin = W[k]["o1"]; break
            k += 1
        if fin: av.append(f"A MEDIAS: a la frase le quedan {k - k0 + 1} palabras («…{W[k]['w']}»): la pausa llega {s(fin - f1):.1f} s después")
    if it["t"] not in ("sub", "dato"):
        nec, ult = texto_dicho(W, l1 or l2, fe, f1)
        if f1 < nec - 2: av.append(f"CORTO: se va {s(nec - f1):.1f} s antes de que se diga y se pueda leer" + (f" (su última palabra, «{ult['w']}», acaba en +{s(ult['o1'] - fe):.1f} s)" if ult else ""))
    # colas sobre un corte
    for c in cortes:
        if 0 < f1 - c <= 0.3 * FPS and c - f0 > 0.3 * FPS and it["t"] not in INFO: av.append(f"COLA: {f1 - c} fotogramas sobre el plano siguiente (corte en +{s(c - f0):.2f} s)")
        if 0 < c - f0 <= 0.2 * FPS and f1 - c > 0.3 * FPS and it["t"] not in INFO: av.append(f"COLA: entra {c - f0} fotogramas antes de un corte")
        if 0 < c - f1 <= 0.2 * FPS and it["t"] not in INFO: av.append(f"COLA: se va {c - f1} fotogramas antes del corte")
    # lectura
    np_ = len([p for p in re.split(r"[\s|]+", f"{l1} {l2}".strip()) if p]); vis = s(f1 - fe)
    if np_ >= 4 and np_ / max(vis, 0.1) > 4.0: av.append(f"LECTURA: {np_} palabras en {vis:.1f} s")
    # pegado a otro texto
    for o in textos:
        if o is it or {o["t"], it["t"]} <= {"trk", "sub"}: continue
        if "nota" in (o["t"], it["t"]): continue                              # un comentario del editor va pegado a lo que comenta
        if 0 <= f0 - o["f1"] < 0.3 * FPS: av.append(f"PEGADO: entra {s(f0 - o['f1']):.2f} s después de «{str(o.get('txt') or o.get('grande'))[:24]}»")
        elif o["f0"] <= f0 < o["f1"] and o["t"] != "sub" and it["t"] != "sub": av.append(f"PEGADO: coincide con «{str(o.get('txt') or o.get('grande'))[:24]}» ({o['t']})")
    n_av += bool(av)
    if not av and not todo: continue
    print(f"\n[{it['t']}] {mmss(f0)}–{mmss(f1)} ({s(f1 - f0):.1f} s{f', se lee a los {ret} s' if ret else ''}) f{f0}  «{l1[:60]}»" + (f" / «{l2[:40]}»" if l2 else ""))
    voz, pe, ps = [], False, False
    for w in W:
        if not f0 - 1.2 * FPS <= w["o0"] <= f1 + 0.8 * FPS: continue
        if not pe and w["o0"] >= fe: voz.append("▶"); pe = True
        if not ps and w["o0"] >= f1: voz.append("■"); ps = True
        voz.append(f"{w['w']}({s(w['o0'] - fe):+.1f})")
    print("   voz:    " + " ".join(voz))
    print("   planos: " + "  ".join(f"{'REC' if v['b'] else 'cam'} {v['clip']}@{v['in'] / FPS:.1f} x{v['z0']:.2f} [{s(max(v['o'], f0) - f0):+.1f}..{s(min(v['o'] + v['n'], f1) - f0):+.1f}]" for v in V if v["o"] < f1 and v["o"] + v["n"] > f0))
    for a in av: print("   ⚠ " + a)
print(f"\n{len(textos)} textos, {n_av} con aviso. ▶ = desde ahí se lee el texto, ■ = se va. Arregla en plan.py (ancla en la palabra, duración hasta la pausa o el corte) y repite.")
