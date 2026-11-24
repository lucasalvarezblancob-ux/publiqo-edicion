#!/usr/bin/env bash
# Precálculo de una referencia: cortes, transcripción (idioma detectado), hojas de contactos, sonoridad (LUFS),
# voz/música (demucs, analizar_audio.py), candidatos de efectos de sonido (escuchar_sfx.py) y la intro FOTOGRAMA A
# FOTOGRAMA (hojas/intro_fot_NN.jpg, los primeros 30 s, 6 fotogramas por segundo de vídeo… a paso de 1 fotograma).
# Uso: herramientas/precalcular_ref.sh <video>.mp4 [carpeta de salida] [--ligero]
#   --ligero: sin demucs ni efectos (poca RAM). Cada paso se salta si su salida ya existe: se puede relanzar.
# Por defecto deja el análisis en refs/dinamicos/_analisis/<video>/; para un creador: personal/<creador>/refs/_analisis/<video>
# Además de la intro y el vídeo entero, saca los últimos 40 s cada 0,5 s (hojas/final_NN.jpg) para ver la outro y el cierre.
set -euo pipefail
LIGERO=0; ARGS=(); for x in "$@"; do [ "$x" = --ligero ] && LIGERO=1 || ARGS+=("$x"); done
V="${ARGS[0]}"; N=$(basename "$V" .mp4); D="${ARGS[1]:-refs/dinamicos/_analisis/$N}"; mkdir -p "$D/hojas" "$D/rotulos" "$D/detalle"
case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) PY=herramientas/.venv/Scripts/python.exe ;; *) PY=herramientas/.venv/bin/python ;; esac
[ -f "$D/cortes.json" ] || $PY herramientas/detectar_cortes.py "$V" "$D/cortes.json" >/dev/null
[ -f "$D/transcripcion.json" ] || PYTHONIOENCODING=utf-8 $PY herramientas/transcribir.py "$V" "$D/transcripcion.json" --idioma auto >/dev/null
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V" | tr -d '\r' | cut -d. -f1)
for i in 0 1 2 3 4 5 6 7; do o="$D/hojas/intro_0$i.jpg"; [ -f "$o" ] || bash herramientas/hoja_contactos.sh "$V" "$o" 0.25 $(awk -v i=$i 'BEGIN{print i*7.5}') 7.5 6 320 >/dev/null </dev/null; done
m=0; while [ $((m*60)) -lt "$DUR" ]; do o=$(printf "%s/hojas/min_%02d.jpg" "$D" $m); r=$((DUR-m*60)); [ $r -gt 60 ] && r=60
  [ -f "$o" ] || bash herramientas/hoja_contactos.sh "$V" "$o" 2 $((m*60)) $r 6 320 >/dev/null </dev/null; m=$((m+1)); done
for i in 0 1; do o="$D/hojas/final_0$i.jpg"; [ -f "$o" ] || bash herramientas/hoja_contactos.sh "$V" "$o" 0.5 $((DUR-40+i*20)) 20 8 320 >/dev/null </dev/null; done
# intro fotograma a fotograma (0–30 s): una hoja cada 2 s de vídeo, 6 columnas, a los fps del vídeo
FPSV=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$V" | tr -d '\r' | awk -F/ '{printf "%.4f", ($2?$1/$2:$1)}')
PASO=$(awk -v f="$FPSV" 'BEGIN{printf "%.5f", 1/f}')
for i in $(seq 0 14); do o=$(printf "%s/hojas/intro_fot_%02d.jpg" "$D" $i); [ -f "$o" ] || bash herramientas/hoja_contactos.sh "$V" "$o" "$PASO" $((i*2)) 2 10 256 >/dev/null </dev/null; done
# sonoridad integrada (LUFS) y pico
[ -f "$D/sonoridad.json" ] || ffmpeg -hide_banner -nostats -i "$V" -vn -af ebur128=peak=true -f null - 2>&1 | tr -d '\r' | awk '
  /I:/ {i=$2} /LRA:/ {l=$2} /Peak:/ {p=$2} END {printf "{\"lufs_integrado\": %s, \"rango_lra\": %s, \"pico_dbtp\": %s}\n", i, l, p}' > "$D/sonoridad.json"
if [ $LIGERO = 0 ]; then
  [ -f "$D/audio.json" ] || PYTHONIOENCODING=utf-8 $PY herramientas/analizar_audio.py "$V" "$D/audio.json" --cortes "$D/cortes.json" --stems "$D/stems" >/dev/null
  [ -f "$D/sfx.json" ] || PYTHONIOENCODING=utf-8 $PY herramientas/escuchar_sfx.py "$V" "$D/sfx.json" --stems "$D/stems" --cortes "$D/cortes.json" >/dev/null
fi
echo "$N listo: $(ls "$D/hojas" | wc -l) hojas$( [ -f "$D/sfx.json" ] && echo ', audio y efectos')"
