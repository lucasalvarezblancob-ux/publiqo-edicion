#!/usr/bin/env python3
"""Deshace UN cambio global de la base solo para un creador (ver <skill>/base/CAMBIOS_GLOBALES.md).

Uso (desde la raíz de la carpeta de edición):
  PY herramientas/montaje/deshacer_cambio.py <creador> G001        deshace G001 para ese creador
  PY herramientas/montaje/deshacer_cambio.py <creador> G001 --volver   lo quita (vuelve a tener el cambio)
  PY herramientas/montaje/deshacer_cambio.py --lista               los cambios globales que hay

- tipo "ajuste": escribe `NOMBRE = <antes>  # Gxxx deshecho …` en personal/<creador>/ajustes.py (el creador manda
  sobre la base, así que vuelve a salir como antes).
- tipo "regla": añade a personal/<creador>/preferencias.md «Gxxx no aplica para este creador: <regla antigua>».
Las dos marcas llevan el id para poder quitarlas con --volver."""
import json, os, re, sys

RAIZ = os.getcwd()
CAMBIOS = next((p for p in (f"{RAIZ}/.claude/skills/edicion-horizontal/base/CAMBIOS_GLOBALES.md",
                            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "base", "CAMBIOS_GLOBALES.md"))
                if os.path.exists(p)), None)
if not CAMBIOS: raise SystemExit("No encuentro base/CAMBIOS_GLOBALES.md de la skill (lánzalo desde la carpeta de edición)")
txt = open(CAMBIOS, encoding="utf-8").read()
C = {c["id"]: c for c in (json.loads(b) for b in re.findall(r"```json\s*(\{.*?\})\s*```", txt, re.S))}

args = [x for x in sys.argv[1:] if not x.startswith("--")]
if "--lista" in sys.argv or not args:
    for c in C.values(): print(f"{c['id']}  {c['fecha']}  {c['tipo']:<6} {c.get('nombre', '')}  — {c['regla_antes']}")
    sys.exit(0)
if len(args) != 2: raise SystemExit(__doc__)
cre, gid = args; gid = gid.upper(); volver = "--volver" in sys.argv
if gid not in C: raise SystemExit(f"No existe {gid} (hay: {', '.join(C)})")
c = C[gid]; P = f"{RAIZ}/personal/{cre}"
if not os.path.isdir(P): raise SystemExit(f"No existe personal/{cre}/")
marca = f"# {gid} deshecho"

if c["tipo"] == "ajuste":      # uno ({"nombre", "antes"}) o varios ({"ajustes": {NOMBRE: antes, ...}})
    pares = c.get("ajustes") or {c["nombre"]: c["antes"]}
    f = f"{P}/ajustes.py"; t = open(f, encoding="utf-8").read() if os.path.exists(f) else ""
    lineas = [l for l in t.splitlines() if marca not in l]
    if volver:
        open(f, "w", encoding="utf-8").write("\n".join(lineas) + "\n"); print(f"✓ {cre}: quitado el rollback de {gid} ({', '.join(pares)} vuelve(n) al de la base)")
    else:
        for nom, antes in pares.items():
            if any(re.match(rf"\s*{re.escape(nom)}\s*=", l) for l in lineas):
                print(f"⚠️  {cre} ya define {nom} en su ajustes.py: manda lo suyo, no se toca."); continue
            if isinstance(antes, dict): antes = {k: tuple(v) if isinstance(v, list) else v for k, v in antes.items()}
            lineas.append(f"{nom} = {antes!r}   {marca} para este creador ({c['fecha']}): {c['regla_antes']}")
            print(f"✓ {cre}: {gid} deshecho → {nom} = {antes!r} en ajustes.py")
        open(f, "w", encoding="utf-8").write("\n".join(lineas) + "\n")
else:
    f = f"{P}/preferencias.md"; t = open(f, encoding="utf-8").read() if os.path.exists(f) else ""
    lineas = [l for l in t.splitlines() if f"**{gid} no aplica" not in l]
    if not volver: lineas.append(f"- **{gid} no aplica para este creador** ({c['fecha']}): {c['regla_antes']}")
    open(f, "w", encoding="utf-8").write("\n".join(lineas) + "\n")
    print(f"✓ {cre}: {'quitado el rollback de ' + gid if volver else gid + ' deshecho en preferencias.md'}")
