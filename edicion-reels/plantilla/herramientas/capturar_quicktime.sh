#!/usr/bin/env bash
# Captura un instante de un vídeo tal como lo enseña QuickTime (con la gestión de color/HDR de Apple), para comparar
# bruto vs proxy/render. Solo Mac. Toma la pantalla unos segundos (avísalo).
# Uso: herramientas/capturar_quicktime.sh ARCHIVO SEGUNDO SALIDA.png
# Ojo: si la captura sale gris plano (≈ 49,51,51) o con otra ventana encima, QuickTime no llegó a pintar el vídeo
# (ordenador cargado) o había algo delante: repítela, no la uses para medir.
F="$1"; T="$2"; O="$3"
open -a "QuickTime Player"; sleep 2
osascript <<OSA
tell application "QuickTime Player"
  activate
  close every document saving no
  open POSIX file "$F"
  delay 8
  set d to front document
  set bounds of front window to {100, 60, 640, 1020}
  set current time of d to $T
  delay 1.5
end tell
OSA
screencapture -x -R100,90,540,930 "$O"
osascript -e 'tell application "QuickTime Player" to close every document saving no'
