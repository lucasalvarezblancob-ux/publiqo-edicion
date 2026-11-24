#!/usr/bin/env bash
# Trae la última versión del estándar sin tocar lo local.
#   actualizar.sh ["<carpeta de edición>"]   (por defecto, la carpeta actual)
set -uo pipefail
source "$(dirname "$0")/lib.sh"
DEST="${1:-${CLAUDE_PROJECT_DIR:-$PWD}}"; DEST="$(cd "$DEST" && pwd -P)"
[ -f "$DEST/personal/LEEME.md" ] || { echo "$DEST no es una carpeta de edición (falta personal/LEEME.md)."; exit 1; }

if [ -z "${EDICION_HORIZONTAL_SIN_PULL:-}" ] && git -C "$REPO_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "→ Skill (git pull de $GH_REPO)"
  git -C "$REPO_DIR" pull -q --ff-only --autostash origin main || echo "⚠️  No se pudo hacer pull (¿cambios locales en el repo de skills?). Sigo con lo que hay."
fi

# RAPIDO (actualización automática al abrir sesión): solo la plantilla; lo lento se deja para un actualizar.sh normal.
RAPIDO="${EDICION_HORIZONTAL_RAPIDO:-}"
if [ -z "$RAPIDO" ]; then
  echo "→ Referencias estándar"; bajar_refs || echo "⚠️  No se pudieron bajar todas las referencias."
  echo "→ Programas"; instalar_programas || echo "⚠️  Faltan programas (mira arriba)."
  echo "→ Skills de apoyo"; instalar_skills "$DEST"
  echo "→ Python y Remotion"; instalar_pesados "$DEST" || echo "⚠️  Revisa lo de arriba."
fi
enlazar_skill "$DEST" || true

echo "→ Plantilla (herramientas, componentes, config)"
MAN="$DEST/$MANIFIESTO_REL"; mkdir -p "$(dirname "$MAN")"; touch "$MAN"; NUEVO="$(mktemp)"; tocados=(); respaldados=(); cambio_pkg=0; cambio_req=0
RESPALDO="$DEST/herramientas/.respaldo_local/$(date +%Y-%m-%d_%H%M%S)"
while IFS= read -r f; do
  nuevo="$(sha "$SKILL/plantilla/$f")"; d="$DEST/$f"
  viejo="$(limpia < "$MAN" | awk -v f="$f" 'substr($0,67)==f {print substr($0,1,64)}')"
  if [ ! -e "$d" ]; then
    # nuevo en la plantilla → se añade; si ya estaba en el manifiesto, lo borraste tú: no se repone
    if [ -z "$viejo" ]; then mkdir -p "$(dirname "$d")"; cp -p "$SKILL/plantilla/$f" "$d"; echo "  + $f"; viejo="$nuevo"; fi
  else
    local_h="$(sha "$d")"
    if [ "$local_h" = "$nuevo" ]; then viejo="$nuevo"                       # ya al día
    elif [ "$local_h" = "$viejo" ]; then                                    # sin tocar en local → se actualiza
      cp -p "$SKILL/plantilla/$f" "$d"; echo "  ↻ $f"; viejo="$nuevo"
      case "$f" in estudio/package*.json) cambio_pkg=1;; herramientas/requirements.txt) cambio_req=1;; esac
    elif [ "$nuevo" != "$viejo" ]; then                                     # cambiado en local y hay versión nueva
      case "$f" in
        herramientas/*|estudio/src/comun/*)
          # Código del MOTOR: lo de cada creador va en personal/ y ajustes.py, no aquí. Si se quedara la copia local, ese
          # equipo se perdería todas las mejoras sin enterarse (Windows de Lucas, 2026-11-24: 19 herramientas de las pruebas
          # del 13–15 nov paradas en la versión vieja). Se guarda la local y se pone la nueva.
          mkdir -p "$(dirname "$RESPALDO/$f")"; cp -p "$d" "$RESPALDO/$f"; cp -p "$SKILL/plantilla/$f" "$d"; viejo="$nuevo"; respaldados+=("$f")
          case "$f" in herramientas/requirements.txt) cambio_req=1;; esac ;;
        *) tocados+=("$f") ;;
      esac
    fi
  fi
  echo "${viejo:-$nuevo}  $f" >> "$NUEVO"
done < <(archivos_plantilla)
mv "$NUEVO" "$MAN"
if [ -n "$RAPIDO" ] && [ $((cambio_pkg + cambio_req)) -gt 0 ]; then
  echo "  La versión nueva cambia dependencias (npm/pip): lanza bash .claude/skills/$NOMBRE/actualizar.sh antes de renderizar."
else
  [ $cambio_pkg = 1 ] && (cd "$DEST/estudio" && npm install --no-audit --no-fund -q)
  [ $cambio_req = 1 ] && "$(py_venv "$DEST")" -m pip install -q -r "$DEST/herramientas/requirements.txt"
fi
if [ ${#respaldados[@]} -gt 0 ]; then
  echo "⚠️  ${#respaldados[@]} archivo(s) del motor estaban cambiados en local y se quedaban sin las mejoras. Puesta la versión"
  echo "   nueva; tu copia está en ${RESPALDO#$DEST/}/ (lo de cada creador va en personal/ y ajustes.py):"
  printf '  · %s\n' "${respaldados[@]}"
fi
if [ ${#tocados[@]} -gt 0 ]; then
  echo "Hay versión nueva de estos archivos, pero los has cambiado en local y no los toco:"
  printf '  · %s\n' "${tocados[@]}"; echo "  (la versión estándar está en .claude/skills/$NOMBRE/plantilla/<ruta>: compárala y decide)"
fi
echo "✓ Al día. Lo tuyo (personal/ con tus recursos, refs/, out/, marca.ts, Root.tsx) no se ha tocado."
