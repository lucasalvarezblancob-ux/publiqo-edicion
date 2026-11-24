# Encargo: estudiar a fondo UN vídeo de referencia para un ESTILO (vlog, reto, viaje…) — 2026-11-24

Eres editor de vídeo profesional y guionista de YouTube. Este vídeo es una referencia que Lucas ha elegido para el
estilo **<ESTILO>** (`base/refs/dinamicos/estilos/<estilo>.md`). Hay que entender **cómo está editado y por qué
funciona**, fijándose al milímetro: cada efecto, zoom, sonido, fuente, transición, motion graphic, la intro entera
plano a plano, el ritmo, el contexto y lo que lo hace interesante. Salen **hechos con tiempo (mm:ss.cc o fotograma)
y número**, nunca opiniones sueltas. Une y amplía `ENCARGO.md` y `ENCARGO_DINAMISMO.md`. No juzgues la calidad de imagen.

Trabaja desde la raíz de la carpeta de edición (en Windows, con Git Bash). Python: `herramientas/.venv/Scripts/python.exe`
(macOS: `herramientas/.venv/bin/python`). Mira las imágenes con Read. No descargues, no uses git, no lances demucs ni
whisper (ya está hecho): solo herramientas ligeras (`hoja_contactos.sh`, `ffmpeg -ss T -frames:v 1`, `medir_zoom.py`,
`fuente_rotulo.py`). No modifiques nada fuera de la carpeta de análisis del vídeo y de la ficha.

## Lo que ya está calculado (carpeta `refs/dinamicos/_analisis/<video>/`)
- `cortes.json` (cortes, s/plano, tramos), `transcripcion.json/.txt` (idioma detectado), `sonoridad.json` (LUFS).
- `audio.json`: voz vs música por segundo, tramos de música, voz−música en dB, cambios de pista, acentos.
- `sfx.json` + `sfx_hoja_NN.jpg`: **candidatos** a efecto de sonido (NO confirmados; ver «Efectos de sonido»).
- Hojas: `hojas/intro_fot_NN.jpg` (0–30 s **fotograma a fotograma**, una hoja cada 2 s), `hojas/intro_NN.jpg`
  (0–60 s cada 0,25 s), `hojas/min_MM.jpg` (todo, cada 2 s), `hojas/final_NN.jpg` (últimos 40 s cada 0,5 s).

## Cómo mirar
1. `transcripcion.txt` entera y los resúmenes de `cortes.json`, `audio.json`, `sonoridad.json` y `sfx.json`.
2. **Todas** las hojas `intro_fot_*`, `intro_*`, `min_*` y `final_*`.
3. Al menos **8 tramos de 10–15 s a 0,1 s** (`hoja_contactos.sh VIDEO SALIDA.jpg 0.1 INI DUR 10 256` → `detalle/`):
   2 del principio, 2 del medio, 2 del final, 1 momento de acción/pico y 1 chiste/reacción. Y **a 1 fotograma**
   (paso = 1/fps) cada transición construida, cada motion graphic y cada entrada de texto que veas.
4. Cada tipo de rótulo: un fotograma completo a resolución del vídeo (1080p) y un recorte ajustado al texto en
   `rotulos/`. Pásale `fuente_rotulo.py <recorte> [--texto "…"] --color "#FFFFFF"` (el color de las letras: sin él, con
   texto sobre vídeo el fondo se mezcla y la puntuación baja) y apunta el top-3 con su puntuación (< 0,5 = no fiable).
   Si la intro tiene micro-flash o estroboscopio (planos de 2–5 f), cuenta sus cortes con
   `detectar_cortes.py VIDEO <carpeta>/cortes_rafagas.json --rafagas` (el `cortes.json` normal los junta en uno).
5. `medir_zoom.py VIDEO INI FIN` en ≥ 8 planos; en cámara en mano, a ojo por el tamaño de la cara (final ÷ inicial).
6. Cruza siempre imagen + transcripción + audio: qué palabra dispara cada zoom, texto, efecto o corte.

## Qué hay que sacar
**A. Contexto e interés** (Lucas: «cuanto más contexto, mejor»)
- Quién sale, dónde, qué se propone y qué está en juego (en 3–5 frases). Tono (humor, épico, íntimo, didáctico).
- **Por qué engancha**: gancho de los primeros 5 s y de los primeros 30 s (qué promete), preguntas abiertas que deja
  (y cuándo las cierra), giros, recompensas, personajes secundarios, humor, tensión, momentos «wow».
- **Curva de energía**: por cada minuto, 1–5 con el motivo (qué pasa, ritmo de cortes, música). Dónde están los picos
  y cómo se preparan (música que sube, ralentí, silencio, cuenta atrás).
- Ritmo de información: cada cuántos segundos pasa algo nuevo (lugar, persona, dato, giro). Qué se recorta (esperas,
  trayectos) y cómo se resume (montaje rápido, cámara rápida, texto «3 HORAS DESPUÉS»).

**B. Intro, plano a plano** (lo más importante del estilo; las de Alessio Pierucci son la referencia estrella)
- Línea de tiempo de 0 a donde acabe la intro: por cada plano, inicio–fin en **fotogramas**, qué se ve, de dónde sale
  (del propio vídeo, grabado aparte, archivo), movimiento de cámara, zoom/velocidad, texto, motion graphic, efecto de
  sonido, música (entra, cae, golpe) y qué se dice.
- Cold open / tráiler / pregunta / título / cabecera animada / logo / saludo: cuáles hay, en qué orden y cuánto dura cada uno.
- El **título o cabecera**: cómo se construye fotograma a fotograma (máscaras, revelado, cinética, partículas, 3D),
  fuente, color, duración, sonido. ¿Se hizo con plantilla o a mano? ¿Motion graphics o tipografía simple?
- Primer corte a la persona hablando: en qué segundo y con qué frase.

**C. Motion graphics y animaciones** (catálogo)
- Cada tipo: qué es (mapa, lista, cifra, lower third, flecha, círculo, sticker, emoji, interfaz de móvil, captura,
  contador, barra, transición gráfica, recorte de persona, rotoscopia, 3D, partículas), entrada y salida en fotogramas,
  curva (lineal, ease, rebote, golpe), posición, tamaño (alto ÷ alto de pantalla), color en hex aproximado, fuente,
  sonido que lo acompaña, qué lo dispara, cuántas veces por minuto, 3 ejemplos con tiempo. Cuándo SÍ y cuándo NO los usan.

**D. Cortes y ritmo**: s/plano por parte; % < 1 s; ráfagas (≥ 3 cortes en 2 s) por minuto y con qué material; jump cuts
al hablar (cada cuántas palabras); J/L cuts; match cuts; insertos de 0,2–0,6 s (memes, reacciones, repeticiones);
cámara rápida/lenta, congelados, rebobinados, speed ramps.

**E. Zooms**: por TIPO (punch-in en corte, snap zoom, zoom lento, zoom-out, zoom + temblor, reencuadre, cámara virtual,
pantalla partida): escala inicial→final, duración en fotogramas, curva, centro, disparador, extras (blur, temblor,
sonido), por minuto, 3 ejemplos.

**F. Textos y títulos**: cada tipo (título, capítulo, lugar, persona, dato/precio, comentario del editor, texto-chiste,
subtítulos, cuenta atrás, listas, «día N»): fuente (top-3 de `fuente_rotulo.py` + tu juicio), peso, mayúsculas,
color, borde/sombra/caja, tamaño, posición, entrada y salida en fotogramas, duración, por minuto, disparador,
3 ejemplos, recorte. ¿Subtitulan todo, solo a otros, solo frases sueltas? ¿Cómo marcan el énfasis (color, tamaño)?

**G. Efectos de sonido** — Claude no oye: `sfx.json` propone candidatos con una pista de tipo y `sfx_hoja_*.jpg`
enseña el espectrograma (línea cian = el instante) y el fotograma. **Confirma cada uno** mirando la hoja y el vídeo:
- Firmas: whoosh = mancha de ruido ancha que sube o baja (acompaña a una transición, un zoom o un texto que entra);
  pop/click = raya vertical finísima (con un texto o sticker que aparece); impacto = mancha fuerte en los graves que se
  apaga (con un corte duro, un título o un golpe); ding/ping = rayas horizontales que se apagan; riser = mancha que
  sube hacia el instante (antes de un pico o un corte a negro). Un golpe de la música se repite a compás en celdas vecinas.
- En la ficha, SOLO los confirmados (tipo, tiempo, a qué acompañan, nivel respecto a la voz). Si no se puede
  confirmar, va a `dudas`. Da efectos por minuto (confirmados) y qué eventos visuales llevan efecto casi siempre.

**H. Música y sonido**: tramos y cambios de pista (por sección, por momento emocional), voz−música en dB
(`audio.json`), silencios a propósito (cuándo y para qué), música a ritmo de cortes (sí/no y dónde), LUFS
(`sonoridad.json`), sonido directo vs música en la acción.

**I. B-roll, voz en off y transiciones**: proporción de b-roll sobre voz, de dónde sale, duración típica, vuelta a
cámara; voz en off (guionada o en directo, mezcla); transiciones construidas (tipo, duración en fotogramas, cuántas,
dónde) frente a corte seco.

**J. Cierre**: cómo acaba, CTA (suscribirse, siguiente vídeo, merch, código), pantalla final y su duración.

**K. Para la skill**
- `para_el_estilo`: lo que este vídeo hace DISTINTO de `base/refs/dinamicos/CONTEXTO.md`, con números, como reglas
  programables («punch-in ×1,25 de golpe en la palabra fuerte, 1 cada 6–8 s»). Y lo de `CONTEXTO.md` que este estilo
  NO hace (para «Qué NO se hereda»).
- `para_la_base`: lo que vale para cualquier vídeo dinámico (aunque no sea de este estilo), con números.
- `para_el_motor`: valores para `estilos/<estilo>.py` con los nombres de `ajustes.py` (ESCALAS, CAMBIO_CADA, Z_FUERTE,
  SFX, MUSICA_NIVELES…) cuando se puedan medir.

## Entrega
Ficha JSON (UTF-8, español) en `base/refs/dinamicos/<creador>/AAAA-MM-DD_<slug>.json` (en la rama de trabajo) con:
`video` {archivo, creador, canal, url, titulo, duracion, publicado, estilo}, `resumen` (6–10 frases),
`contexto` {quien, donde, objetivo, tono, gancho_5s, gancho_30s, preguntas_abiertas, giros, recompensas},
`curva_energia` [{minuto, nivel, motivo}], `ritmo_informacion`, `estructura` [{desde, hasta, parte, que_pasa}],
`intro` {duracion_s, orden, linea_de_tiempo [{f0, f1, t, que_se_ve, origen, camara, zoom_velocidad, texto,
motion_graphic, sfx, musica, voz}], titulo_cabecera {como_se_construye, fuente, color, duracion_f, sonido},
primer_plano_hablando_s}, `motion_graphics` [...], `cortes` {...}, `zooms` [...], `textos` [...], `subtitulos`,
`sfx` {confirmados [{t, tipo, acompaña_a, respecto_voz_db}], por_minuto, reglas, candidatos_descartados},
`musica` {...}, `broll`, `voz_en_off`, `transiciones` [...], `cierre`, `para_el_estilo` [...], `para_la_base` [...],
`para_el_motor` {...}, `dudas` [...].
Respuesta final: 20–30 líneas con lo más llamativo, los números clave y las 5 reglas más copiables.
