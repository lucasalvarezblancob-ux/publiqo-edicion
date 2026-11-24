# Método de análisis de una referencia (probado con `cazar-avispas-asesinas`, 2026-11-11)

Se analiza **solo la edición**, nunca la calidad de imagen (son copias a 720p/1080p de YouTube).
Todo se lanza desde la raíz de la carpeta de edición con Git Bash. Python: `herramientas/.venv/Scripts/python`
(macOS: `herramientas/.venv/bin/python`).

## Flujo por tandas (desde 2026-11-24)
`cola_refs.py añadir --estilo <e> URL…` → `cola_refs.py avanzar` (baja con `bajar_ref.py` a 1080p y lanza
`precalcular_ref.sh`; como mucho 2 vídeos «listos para ver» a la vez; se para si falta RAM o disco) → un agente por
vídeo con `ENCARGO_ESTILO.md` → `cola_refs.py hecho <id>` (borra el mp4 y los stems; quedan hojas y JSON).
En Windows, antes: `powershell -ExecutionPolicy Bypass -File herramientas\windows\instalar_vigilante.ps1 -Carpeta <carpeta>`.

## Ya calculado por vídeo en `refs/dinamicos/_analisis/<video>/`
- `hojas/intro_fot_NN.jpg`: los primeros 30 s FOTOGRAMA A FOTOGRAMA (una hoja cada 2 s, 10 columnas).
- `sonoridad.json`: LUFS integrado, rango (LRA) y pico.
- `sfx.json` + `sfx_hoja_NN.jpg` (`escuchar_sfx.py`): candidatos a efecto de sonido con una pista de tipo (CLAP) y su
  espectrograma + fotograma. NO están confirmados: se confirman mirando (firmas en `ENCARGO_ESTILO.md` § G).
- Fuentes: `herramientas/fuente_rotulo.py <recorte>` da el top-3 de Google Fonts (acierta familia; el peso, a veces).
- `cortes.json`: cada corte (`t`, `score`, `tipo` seco|transicion), duración de planos y resumen por minuto.
  Fiable en cortes secos (comprobado contra fotogramas). NO ve transiciones encadenadas (whip/zoom a mapa) ni
  jump cuts con encuadre casi idéntico: esos se cuentan a ojo en las hojas.
- `audio.json`: tramos de música (batería+bajo aislados con demucs), nivel de voz y de música, diferencia
  voz−música en dB, cambios de pista, acentos de sonido (posibles SFX) y cuántos caen sobre un corte.
  `por_segundo.voz_db / resto_db / ritmo_db` = curva segundo a segundo.
- `transcripcion.json` + `.txt`: frases con tiempo y confianza, palabras con tiempo.
- `hojas/intro_00..07.jpg`: primeros 60 s, una celda cada 0,25 s (6×5, 7,5 s por hoja, tiempo impreso).
- `hojas/min_MM.jpg`: todo el vídeo, una celda cada 2 s (una hoja por minuto).

## Herramientas para mirar más de cerca
- `bash herramientas/hoja_contactos.sh VIDEO SALIDA.jpg CADA_S INICIO DUR [COLS=6] [ANCHO=320]`
  (p. ej. cada 0.1 s alrededor de una transición; ANCHO 640 con COLS 3 para leer rótulos).
- Fotograma suelto a tamaño completo: `ffmpeg -v error -y -ss T -i VIDEO -frames:v 1 SALIDA.jpg`;
  recorte de un rótulo: añade `-vf crop=w:h:x:y`. Guarda los recortes en `<video>/rotulos/`.
- `python herramientas/medir_zoom.py VIDEO INI FIN`: escala acumulada dentro de un plano (1.08 = +8 %).
- Las imágenes se miran con la herramienta Read. Escribe temporales solo dentro de `<video>/`.

## Qué apuntar (los 11 puntos + subtítulos)
1. Cortes y ritmo: s/plano por parte (intro, desarrollo, momentos fuertes, cierre); jump cuts al hablar;
   J/L cuts (compara tiempos de palabra con el corte); match cuts.
2. Intro (0–60 s, cada 0,25 s): cold open, recap/tráiler de lo que viene (qué planos, de qué minuto del vídeo
   salen, cuánto dura cada uno, qué frase los acompaña), título/cabecera (cuándo y cómo), motion graphics,
   cuándo entra la música.
3. B-roll mientras se habla: origen (mismo vídeo antes/después, recursos aparte, stock/archivo), duración,
   cómo vuelve a cámara. Proporción aproximada de tiempo de voz cubierto por b-roll.
4. Voz en off: cuándo sustituye a hablar a cámara, cómo está escrita, cómo se mezcla.
5. Transiciones: tipos, frecuencia (nº por 10 min) y dónde.
6. Zooms y dinamismo: punch-ins (escala, duración), zooms lentos (% por segundo), cámara virtual, estabilización.
   Mide al menos 8 con `medir_zoom.py`.
7. Tipografía y rótulos: cada tipo (título, lower third, dato, capítulo, subtítulo): fuente más parecida de
   Google Fonts, tamaño (alto de mayúscula / alto de pantalla), posición, color, borde/sombra, animación de
   entrada y salida y duración. Recorta ejemplos.
8. Motion graphics: mapas, contadores, flechas, recortes, pantallas: cómo entran, cuánto duran, estilo.
9. Música: entradas, cambios y cortes; nivel respecto a la voz; cambio por secciones; ¿a ritmo de los cortes?
10. Efectos de sonido: cuáles, cuántos por minuto, dónde. Candidatos en `sfx.json`/`sfx_hoja_*.jpg`; solo cuentan los confirmados mirando.
11. Estructura: capítulos, tensión/clímax, cierre, CTA, pantalla final.
12. Subtítulos: ¿subtitulan tramos con ruido / voz lejana / otro idioma? Estilo y posición.

Cada afirmación con su tiempo (mm:ss) y, si se puede, con número. Si algo no se puede saber, dilo.
