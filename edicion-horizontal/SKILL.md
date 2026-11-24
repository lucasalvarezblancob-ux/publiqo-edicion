---
name: edicion-horizontal
description: Edición de vídeo horizontal 16:9 para YouTube (vlogs, viajes, retos, visitas, días de entreno; 5–40 min) a partir de brutos largos — análisis y registro visual de los brutos, montaje por texto (EDL), dinamismo con cortes de escala y zooms, planos de recurso sobre la voz, intro con tráiler y título, capítulos, rótulos y cifras, mapas de satélite animados, música por ventanas, efectos, render 4K híbrido (ffmpeg + capas Remotion) y el paquete de YouTube al terminar: 5 parejas de título + miniatura para test A/B (con prompt para ChatGPT y fotograma de referencia), descripción, capítulos y etiquetas, en el idioma del vídeo. Úsala SIEMPRE que pidan editar un vídeo horizontal o largo de bruto/, hacer un vídeo de YouTube, corregir un edit, pedir títulos, miniaturas o la descripción de un vídeo, estudiar un canal de YouTube, añadir referencias, recursos o música, personalizar el estilo de un creador, o "que aprendas" de una corrección; también para instalarla o crear la carpeta de edición. No para reels verticales (esa es edicion-reels).
---

# Edición horizontal (YouTube 16:9)

Vídeo horizontal a la resolución del mejor bruto (normalmente 3840×2160) y a sus fps. La skill son **las bases**: cómo
se edita bien un vídeo largo (lo medido en referencias y lo que Lucas, su autor, ha ido corrigiendo). Encima, cada
creador pone **su personalización** en una carpeta local.

```
bases de la skill  →  personalización del creador (personal/)  →  lo que pida para un vídeo
(iguales para todos)   (local, manda sobre las bases)              (manda sobre todo)
```

## 0. Dónde está cada cosa y quién puede cambiar qué

- `<skill>` = la carpeta de esta skill (`.claude/skills/edicion-horizontal/`, enlace a `~/Projects/publiqo-edicion/edicion-horizontal`, dentro del
  repo público «Publiqo Edición», `github.com/lucasalvarezblancob-ux/publiqo-edicion`).
  **Solo lectura.** Lleva las bases: `base/preferencias.md`, `base/intros.md`, `base/recursos.md`,
  `base/titulos-miniaturas.md`, `base/descripciones.md`, `base/refs/<tipo>/` (fichas + `CONTEXTO.md`),
  `base/refs/_youtube/` (el estudio de títulos, miniaturas y descripciones de diez canales), `base/ejemplos/<slug>/` (código de edits hechos)
  `plantilla/` (de donde sale la carpeta de edición) y `creadores/<n>/` (personalizaciones ya hechas que vienen con la
  skill, p. ej. `reinoselva`: se instalan con `instalar.sh --creador <n>`; sus recursos están en su disco duro).
- **La carpeta de edición** = el directorio de trabajo, el que tiene `personal/<creador>/perfil.md`. Es local y de quien la usa.
- **`personal/` = la carpeta de PERSONALIZACIÓN.** Es local, no está en git y la skill nunca la pisa. Dentro hay **una
  carpeta por creador**, `personal/<creador>/` (lo normal es uno; si se edita para varios, cada uno la suya). Se crea
  con `PY herramientas/montaje/nuevo_creador.py <nombre>` desde la raíz. Ahí se adaptan las bases a su gusto (detalle
  en `personal/LEEME.md`):

  | Archivo | Qué personaliza |
  |---|---|
  | `perfil.md` | quién es: nombre, canal, idioma habitual, nicho, cámaras, de dónde saca la música |
  | `preferencias.md` | sus reglas de estilo, en palabras; cada corrección suya, con fecha y motivo |
  | `recursos.md` | sus recursos fijos (cabecera, cortinillas, logos, sonidos, música) y cuándo va cada uno |
  | `marca.json` | color de acento, canal, @, código y logo (lo leen los gráficos); con `"idiomas": {"en": {…}}` si su marca cambia con el idioma del vídeo |
  | `ajustes.py` | los números de la base: escalas y frecuencia de zooms, efectos de sonido, niveles de música, sonoridad |
  | `recursos/` | **todo su material, ordenado por carpetas** y con ficha en `INDICE.md`: `marca/` (sus archivos fijos ORIGINALES: intro, outro, logos, mascota, cortinillas), una carpeta por tema para sus clips de archivo y b-roll (`base/recursos.md` § 2), `creador/`, `fotos/`, `mapas/`, `sonidos/` y `musica/` (+ `CATALOGO.md`). Sus clips se usan en el EDL y en el plan como un bruto más |
  | `refs/` | vídeos suyos publicados y sus fichas: cómo edita él (§ 4) |

  También son del creador, fuera de `personal/` porque los necesita Remotion: sus **gráficos propios**
  (`estudio/src/personal/<creador>/Graficos.tsx`) y sus recursos **ya preparados** para superponer
  (`estudio/public/personal/<creador>/`: animaciones sin fondo en `.webm`, logos en `.png`). Y son locales las fuentes
  (`estudio/src/comun/marca.ts`) y las referencias por tipo (`refs/`). **No hay `recursos/` en la raíz**: todo recurso
  (clip de archivo, b-roll, foto, mapa, pista) es de un creador y va en su carpeta.
  Cada vídeo dice de quién es en `out/<slug>/proyecto.py`: `CREADOR = "<creador>"` (si solo hay uno, no hace falta).

**Cambios globales con rollback**: todo cambio de la base que cambia cómo salen los vídeos lleva un id en
`<skill>/base/CAMBIOS_GLOBALES.md` con lo que había antes. Si un creador dice «desde la actualización no me gusta X»,
se busca ahí y se deshace solo eso para él: `PY herramientas/montaje/deshacer_cambio.py <creador> G00x`.

**Base o personalización: decide antes de apuntar nada.** Vale para cualquier creador y cualquier vídeo (cómo se elige
un recurso, cómo se ordena, un fallo técnico) → base. Es de ESTE creador (sus recursos, su marca, su cabecera, su
gusto: «a mí los zooms más suaves») → `personal/`. Si no está claro, pregunta en una línea: «¿base para todos o solo
de este creador?». Los recursos y gustos de un creador **nunca** se apuntan en la skill.

**Si no hay carpeta de edición** (no existe `personal/LEEME.md`): ofrece instalarla con `<skill>/instalar.sh "<ruta>"`
(ver `<skill>/LEEME.md`). **Si hay carpeta pero ningún creador** (`personal/` solo tiene `_plantilla/`): créalo con
`nuevo_creador.py <nombre>` y rellena con él `personal/<creador>/perfil.md` y `marca.json` antes del primer edit.

**Modo** — compruébalo al empezar: `bash <skill>/modo.sh` imprime `autor` o `local`.
- `local` (quien no tenga permiso de escritura en el repo): **no edites nada dentro de `<skill>`**, aunque te lo pidan (un hook lo impide). Todo lo
  que cambien o corrijan va a `personal/` o a `refs/<tipo>/CONTEXTO.md` de la carpeta.
- `autor` (Lucas: una cuenta de `AUTORES` o con permiso de escritura en el repo): puede cambiar las bases. Ver § 3.
  Subirlas (`publicar.sh`) **solo cuando Lucas lo pida**.

**Orden de lectura antes de tocar nada** (lo de abajo manda sobre lo de arriba cuando choca):
1. `<skill>/base/preferencias.md` (bases) → `personal/<creador>/perfil.md`, `personal/<creador>/preferencias.md`, `personal/<creador>/recursos.md` y
   `personal/<creador>/ajustes.py` (lo del creador, manda).
   ⚠️ **Color: el del bruto, sin tocar.** ⚠️ **Idioma: el que se habla en el vídeo, detectado, nunca supuesto.**
2. `<skill>/base/refs/dinamicos/CONTEXTO.md` (números de ritmo, zooms, textos, mapas, música) y, si existe,
   `refs/dinamicos/CONTEXTO.md` de la carpeta (local, manda). Tipos: `dinamicos` (vlog, viaje, reto, visita: lo hecho
   hasta ahora) y `estudio` (a cámara en interior; aún sin referencias). Un tipo nuevo local = una carpeta en `refs/`.
   **Estilos** (vlog, viaje, reto, visita, entreno): capa OPCIONAL en `<skill>/base/refs/dinamicos/estilos/`. Solo se
   aplica si lo piden para ese vídeo o si el `perfil.md` del creador tiene `Estilo por defecto:`; si no, se edita
   exactamente como hasta ahora, con `CONTEXTO.md` y nada más. Nunca se deduce del bruto. Ver `estilos/LEEME.md`.
3. `<skill>/base/intros.md` (gancho, ráfaga, título, capítulos, cierre) y `<skill>/base/recursos.md` (registro visual,
   catálogo, música, mapas). Al entregar: `<skill>/base/titulos-miniaturas.md` y `<skill>/base/descripciones.md`.
4. `personal/<creador>/recursos/INDICE.md` y `…/recursos/musica/CATALOGO.md` (su material) y `out/REGISTRO.md`.
5. Un edit parecido para copiar estructura: `out/<slug>/` de la carpeta o `<skill>/base/ejemplos/ramon/`.

Si `<skill>/comprobar.sh` (lo lanza el hook al abrir la sesión) avisa de algo, atiéndelo antes de editar.

## 1. Estructura de la carpeta de edición (no la cambies sin preguntar)

```
<carpeta>/
├── personal/          PERSONALIZACIÓN (local): LEEME.md, _plantilla/ y una carpeta por creador
│   └── <creador>/     perfil.md, preferencias.md, recursos.md, marca.json, ajustes.py, refs/ y
│       └── recursos/  TODO su material, por carpetas, + INDICE.md: marca/ (intro, outro, logos, mascota), <tema>/
│                      (clips de archivo y b-roll), creador/, fotos/, mapas/, sonidos/, musica/ (+ CATALOGO.md)
├── bruto/             entrada: brutos pendientes (una carpeta por vídeo: bruto/<slug>/)
│   └── <slug>-analisis/   transcripcion/ (<clip>.json .txt .w.json) y visual/ (hojas/ + <clip>.json = registro visual)
├── bruto terminado/   brutos ya editados (para repasos)
├── refs/<tipo>/       referencias LOCALES + CONTEXTO.md (las de serie están en <skill>/base/refs/)
├── out/               vídeos terminados (AAAA-MM-DD_<slug>.mp4 y .txt) + REGISTRO.md
│   └── <slug>/        el montaje de cada vídeo: proyecto.py, edl.py, plan.py, trabajo/ (intermedios) y youtube/
│                      (el paquete: PAQUETE.md con títulos, prompts de miniatura y descripción + las referencias)
├── estudio/           proyecto Remotion, SOLO para las capas gráficas
│   ├── src/comun/     Graficos.tsx, MapaSatelite.tsx (de serie) y marca.ts (fuentes, local)
│   ├── src/personal/<creador>/   Graficos.tsx: gráficos propios del creador (local)
│   ├── src/videos/<slug>/   Capas.tsx + capas.json (lo escribe el paso 3)
│   ├── public/sonidos/      efectos de sonido de serie
│   ├── public/botones/      16 botones animados de YouTube, de serie (base/recursos.md § 9)
│   └── public/personal/<creador>/   recursos del creador ya preparados para superponer (local)
└── herramientas/      scripts de análisis y proxies, .venv de Python y montaje/ (los pasos, iguales para todos)
```

Python: siempre el de la venv — `herramientas/.venv/Scripts/python.exe` en Windows, `herramientas/.venv/bin/python` en
macOS (abajo, `PY`). En Windows todo se lanza con Git Bash. Los pasos se ejecutan **desde `out/<slug>/`**:
`PY ../../herramientas/montaje/pasoN_….py`.

## 2. Flujo de un vídeo

**Cómo funciona**: no se monta en una línea de tiempo a mano. Se escriben dos archivos de texto — `edl.py` (qué se dice
y en qué orden, eligiendo cada frase **por su texto literal** de la transcripción) y `plan.py` (recursos, zooms, textos,
mapas, música, **colgados de frases o marcas**, nunca de frames a mano) — y los pasos los convierten en vídeo. ffmpeg
monta la imagen desde los brutos; Remotion solo dibuja los gráficos, que van encima.

0. **Preparar** — `PY herramientas/montaje/nuevo_video.py <slug> "<carpeta de brutos>"` (desde la raíz; crea
   `out/<slug>/`, la composición de capas y elige lienzo y fps por el mejor bruto). **Lo primero, el vigilante**
   (obligatorio en todo vídeo, hasta la entrega): desde `out/<slug>/`, `PY vigilante.py` en SEGUNDO PLANO (cierra lo que
   se cuelgue, relanza el render si se para, libera memoria; cada 10 min) y un cron de la sesión cada 10 min
   (`CronCreate`) con `vigilante.py estado`: si cerró o relanzó algo, sigue desde ahí; si no hay nada en marcha y el
   vídeo no está entregado, sigue con el paso siguiente. Al entregar: `vigilante.py parar` y se borra el cron. Y toda
   orden que pueda tardar o quedarse esperando (Remotion, render, transcripción) va en segundo plano o con tope de
   tiempo, nunca en primer plano sin límite (preferencias → Lecciones técnicas: el parón de 2 h 40 min). Luego,
   `paso0_preparar.py`: ficha técnica de cada bruto, **transcripción con el idioma detectado** (ponlo en `IDIOMA` de
   `proyecto.py` tras comprobarlo), posición de la cara (para los zooms) y hojas densas (1 fotograma/s). Va **en
   paralelo** con el mismo resultado byte a byte: la transcripción por un lado y la imagen (caras + hojas) por otro,
   varios brutos a la vez según gráfica, núcleos y memoria (−35 % medido en Windows; `PASO0_WHISPER`/`PASO0_HILOS` lo fijan).
   Brutos HDR (iPhone): no se convierten enteros; tras el paso 4, `sdr.py` hace la copia SDR solo de los trozos que se
   usan y se comprueba el color (preferencias → COLOR).
   **Ventana de arranque** (con `paso0_preparar.py` ya en segundo plano, para no esperar): si `personal/<creador>/perfil.md`
   NO tiene línea `Arranque:` (o la tiene vacía), UNA `AskUserQuestion` con solo lo que no esté decidido (máx. 4 preguntas):
   1) **Estilo**: solo si el perfil no tiene `Estilo por defecto:` ni `Estilo de edición:` y hay algún estilo con reglas
   en `estilos/` (los «sin analizar» no se ofrecen; si no queda ninguno, no se pregunta). Primera opción: «Como siempre (sin estilo)».
   2) **Recursos que no salen en los brutos**, siempre en este orden: brutos del vídeo → su librería → stock
   (`base/recursos.md` § 5). Opciones según lo que haya: «Librería y stock» (stock solo si `personal/bancos.md` dice
   Shutterstock SÍ; ese «sí» es el permiso de descarga para todo el vídeo, § 5 bis), «Solo su librería», «Solo los brutos».
   Si su `recursos/` no se abre (disco sin conectar), se dice en la pregunta y se ofrece «Conecto el disco ahora»
   (`conectar_disco.sh`). Sin librería ni stock, no se pregunta.
   3) **Lo que el registro visual no puede saber** (multiSelect): segunda cámara o dron (→ `sincro.py`), partes leídas de
   teleprompter o notas (→ se tapan con recursos), brutos grabados solo como recurso, nada de eso. No sustituye al
   registro visual del paso 1: se hace igual, entero.
   4) **¿Lo guardo como lo de siempre para este creador?** «Solo este vídeo» / «Siempre así»: con «Siempre así», 1) y 2) se
   escriben en su `perfil.md` como `- **Arranque**: estilo <x|ninguno> · recursos: <…> (fecha)` y la ventana ya no sale.
   Las respuestas van a `out/<slug>/proyecto.py`: `ESTILO` (si hay) y una línea `# Arranque (fecha): recursos … · brutos …`.
   Con `Arranque:` en el perfil, sin respuesta o sin `AskUserQuestion` (modo no interactivo): no se pregunta y se edita
   como hasta ahora (estilo solo el del perfil; brutos → librería → stock con confirmación por tanda). Por qué: Lucas,
   2026-11-24, «basta con el sí, pero se prioriza si hay en recursos propios antes que stock».
1. **Estudiar los brutos a fondo (obligatorio)**:
   - Lee todas las transcripciones enteras.
   - **Registro visual**: un agente por bruto (los largos, por rangos de ~9 min) con
     `herramientas/montaje/ENCARGO_REGISTRO_VISUAL.md`, **en paralelo: hasta 4–5 a la vez en Mac**; de dos en dos en
     Windows con 16 GB de RAM. Resultado:
     `visual/<clip>.json` con qué se ve en cada tramo, los mejores recursos, lo que hay que evitar y los desplazamientos.
   - **Cronología**: brutos en orden de grabación, dónde está el creador en cada uno, de dónde viene y a dónde dice que
     va. Los planos de desplazamiento se quedan en su trayecto (preferencias → Orden y continuidad).
   - Lista lo que se nombra y **no** hay en imagen, las **matrículas legibles** (se difuminan siempre: `TAPAR`) y lo
     que el creador debe decidir (caras de terceros, menores, pantallas con datos).
2. **Guion de montaje → `edl.py`**: estructura (`base/intros.md`): tráiler en frío → ráfaga → título → cuerpo por
   capítulos `S(n, …)` → cierre. Cada frase, copiada literal de la transcripción con `T(…)` y **entera** (de donde
   empieza a donde acaba: nada de medias frases). Fuera retomas, arranques, ideas repetidas y tiempos muertos;
   **dentro todo lo que le da toque al vídeo** (humor, apartes al perro o a quien graba, reacciones, anécdotas,
   explicaciones, lo que siente) **y lo que pasa sin palabras**: el fallo o el susto en sí (se le cae algo al agua), con su sonido,
   delante de la frase que lo cuenta (los `momentos` del registro visual): ante la duda se deja, y la duración no es motivo para quitarlo (preferencias → Que el
   vídeo lo cuente todo).
   Enseña al creador la escaleta (capítulos y duración estimada) si es su primer vídeo o si lo pide.
3. **Línea y voz**: `paso1_alinear.py` (alineación forzada: bordes de cada frase y frame de cada palabra) →
   `frases.py` (**frases a medias**: cada pieza con lo que se dice justo antes y después; cada aviso se resuelve
   alargando hasta el borde de la frase, o se apunta en `OK_A_MEDIAS` del EDL por qué vale; y **la misma idea dos
   veces** (`REPITE`): la retoma se corta y se queda la toma buena, o se apunta en `OK_REPITE` por qué va) →
   `paso2_voz.py` → `comprobar_voz.py` (ratio ≥ 0,97 y ninguna palabra comida o repetida en un corte; si no, corrige
   el EDL; y cada `HUECO` —silencio de más de 1,5 s dentro de lo hablado: se corta o se enseña el gesto con su sonido— y
   cada `VOZ SIN TEXTO` —casi siempre quien graba dando indicaciones: fuera— se resuelve; y cada `AVISO ESTIRADA` de
   `paso1_alinear.py` —ahí suena algo que Whisper no transcribió, casi siempre una orden de rodaje—, con `retranscribir.py`).
4. **Plan → `plan.py`**: recursos sobre la voz (`BROLL`, elegidos del registro visual y **mirados** con `tira.py`; en
   el tráiler, varios planos cortos con una lista `(ancla, [(clip, s, dur), …])`; `(None, cx, cy)` lleva el corte de
   escala hacia el sujeto; nunca de la misma toma que la frase que tapan; la otra cámara sobre su voz, siempre `@sync` con `SINCRO` medido por `sincro.py`; si lee un teleprompter, su plano no se queda), fails (`FALLOS`: blanco y negro y voz
   saturada hasta que se recupera; preferencias → Audio),
   frases fuertes y zooms (`FUERTES`, `ENTRADAS`), cifras (`DATOS`), palabras-golpe (`GOLPES`), rótulos con seguimiento
   (`TRK`: el nombre de lo que se presenta o se enumera, con flecha, en su palabra; **la caja se mide con `rejilla.py` en
   el `t0` exacto, el primer segundo en que se ve ESE plano en el montaje, nunca con las fracciones del registro visual;
   medio lado ≈ medio tamaño del sujeto**: pájaro 60–80 px en 4K, perro 150–250), mapas (`MAPAS`), subtítulos solo donde se oye mal (`SUBS`), título (`TITULO`), petición de suscripción
   (`BOTONES`: siempre el botón animado de la skill, abajo en el centro, en el idioma del vídeo y **solo**: ningún texto a la vez), matrículas (`TAPAR`), personas del fondo (`TAPAR_PERSONAS`), palabrotas (`PITIDOS`: si el creador lo pide, TODAS; lista con `palabrotas.py`), voz de quien no quiere que se le reconozca (`VOZ_DISFRAZ`: tono arriba, solo si el creador lo pide; preferencias → Audio), resalte de algo importante que se pierde en el plano (`FOCOS`: blanco y negro todo menos el
   sujeto; con criterio, 1–2 por vídeo), gráficos propios del creador (`PROPIOS`) y música por ventanas
   (`PISTAS`, `VENTANAS`; pistas nuevas y planos que faltan: Shutterstock con Claude in Chrome si `personal/bancos.md`
   lo tiene —si no existe, se hace la prueba—, `base/recursos.md` § 5 bis). Los cortes de escala alternos los pone solo el motor (`dinamica.py`, con los números de
   `personal/<creador>/ajustes.py` si el creador los ha cambiado). **Aplica aquí lo del creador**: su
   `preferencias.md` y su `recursos.md` (intro, outro, mascota, tipo de música) — § 4.
   `paso3_plan.py` lo convierte en `trabajo/video.json` y `capas.json`, e imprime el ritmo (mediana de plano,
   cortes/min) y los avisos. **Se para** si un trozo de bruto sale dos veces (`REPETIDO`, con el tramo libre más cercano
   para cambiar el recurso) o si dos gráficos se pisan (`PISA`); se arregla en el plan, nunca se fuerza. Si hay `TAPAR`: después, `tapar.py seguir`, `tapar.py parches` y `tapar.py hoja` (mira
   TODAS las hojas: solo la matrícula borrosa, nada más tapado; y a tamaño real los momentos en que alguien pasa por
   delante y solo asoma una esquina: también se lee). Si hay `TAPAR_PERSONAS` (personas del fondo, `personas_fondo` del
   registro visual): `tapar_persona.py` y `tapar_persona.py hoja` (mira TODAS: la persona no se reconoce en ninguna y
   no se tapa nada más). Si hay `FOCOS`: `foco.py parches` y `foco.py hoja` (mira la
   hoja: el sujeto entero y en color en todos los fotogramas).
5. **Comprueba ANTES de renderizar** (obligatorio):
   - `timing_textos.py` → cada texto frente a la voz y a los cortes: entra EN su palabra (no al principio de la
     frase), aguanta la frase y sale con el corte; también los gráficos del creador que llevan texto (su mascota).
     Arregla en `plan.py` y repite (preferencias → Timing de los textos). Las colas de pocos fotogramas sobre un
     corte las ajusta solo `paso3_plan.py`, y también alarga solo cada texto hasta que se ha dicho entero y se
     puede leer (lo imprime; `CORTO` en `timing_textos.py` = el texto siguiente no le deja sitio).
   - `hoja_recursos.py` → mira TODAS las hojas: cada recurso enseña su sujeto desde el primer fotograma. Y
     `trabajo/trailer.jpg`: un fotograma de cada plano del tráiler; ningún animal ni momento sale dos veces.
   - `hoja_seguimiento.py` → mira cada `trabajo/trk_N.jpg`: 8 fotogramas del montaje por rótulo con flecha; en los 8,
     su plano (`principal`, o el recurso que toca si va sobre recurso) y el punto rojo **encima del sujeto**. Si no: `t0`
     al primer segundo en que se ve el plano y la caja medida otra vez con `rejilla.py` (preferencias → Textos).
   - `hoja_textos.py` → mira TODAS las hojas: cada texto sobre su plano, al entrar y al irse, con su caja. Ninguno tapa
     lo que se enseña en ese momento (el animal, las manos que hacen algo, los platos, una cara): si tapa, `lado`, `y`,
     la mascota al otro lado o una flecha que siga al sujeto (preferencias → Textos).
   - `planos_vacios.py` → planos principales sin cara sobre pared, techo, barrido o la cámara pegada al cuerpo, con
     lo que se dice encima (`trabajo/vacios.jpg`): cada uno fuera del EDL, tapado con un recurso de lo que se habla o
     apuntado en `VACIOS_OK` (preferencias → Paredes).
   - Si hay `VOZ_DISFRAZ` (o habla alguien más): `voces.py` → frases con pinta de ser de la otra persona y cuáles faltan
     por disfrazar; `paso5_audio.py` lo repite como `AVISO VOZ:` (preferencias → Audio).
   - `ver.py F …` en cada texto (frame anterior a la palabra: no está; frame de la palabra: está), cada cifra, cada zoom
     animado o a un sujeto (¿apunta bien?) y cada cambio de sección (¿el plano de antes y el de después tienen sentido?).
   - Cada gráfico propio o botón: `ver.py` en **cada plano que pisa** (los cortes de escala cambian el encuadre por debajo):
     no tapa la cara ni el sujeto, no pisa otro gráfico, y el clip superpuesto está limpio (sin fondo, sin halo, sin
     objetos raros).
   - El ritmo impreso frente al objetivo del CONTEXTO.
   - **Repaso de descartes**: `descartes.py` → lee `trabajo/descartes.md` ENTERO (lo hablado y lo mejor de la imagen
     que NO está en el vídeo). Lo interesante, bueno, gracioso o impactante que falte **se mete antes de renderizar**
     (si piensas «a lo mejor no se tenía que haber descartado», ya está decidido: dentro); a quien edita se le cuenta
     al entregar qué entró y qué se dejó fuera a propósito. **Se pregunta antes solo lo dudoso de verdad** (terceros,
     vida privada, promociones, cambios de estructura). (preferencias → Que el vídeo lo cuente todo)
6. **Render híbrido** — `paso4_render.py capas` (Remotion, solo los rangos con gráfico, ProRes con alfa) →
   `paso4_render.py tramos auto 2` (ffmpeg desde los brutos; NVENC si hay, si no x264) → audio: `paso5_audio.py` (voz +
   efectos, −14 LUFS) y, si hay música, `paso6_musica.py` (rellena solo los planos sin voz que quedaban sin música: `puente: …`) → `paso4_render.py unir ../AAAA-MM-DD_<slug>.mp4`.
   Es reanudable. Para retocar un vídeo ya entregado con una versión anterior de la skill, `paso3_plan.py --legado`
   (las comprobaciones nuevas de solapes y repeticiones avisan sin parar; un texto fuera del cuadro sí para).
   Si cambias el plan, se rehacen solo los tramos y capas que cambian: `rehacer.py guardar` antes de `paso3_plan.py` y
   `rehacer.py borrar` después; luego `paso3_plan.py && render_todo.py` con una salida nueva (`&&`, nunca `;`). Tiempo orientativo: ×2,7 la duración en 4K.
   **Todo seguido y en segundo plano**: `render_todo.py ../AAAA-MM-DD_<slug>.mp4` hace los cuatro pasos, retoma donde
   se quedó y reintenta con menos carga si algo falla.
   **Equipo con poca memoria o con límite de tiempo por orden** (16 GB, sesión con otras cosas abiertas): por tandas
   cortas, que se relanzan hasta que acaban — `sdr.py 240` y `CAPAS_HILOS=4 paso4_render.py capas 240` (salen con
   código 3 si queda algo) y `paso4_render.py tramos x264 2 <ids…>` de seis en seis tramos. Medido en `1311` (13,9 min,
   4K, i7-13700HX): capas 12 min, tramos 26 min (≈ 3 s por segundo de vídeo, de dos en dos).
   **Vigilancia**: el vigilante del paso 0 sigue en marcha (`render_todo.py` le deja dicho qué render es: si se muere o
   se cuelga, lo relanza solo, hasta 3 veces). El cron de la sesión mira `vigilante.py estado`; con `TERMINADO` o la
   salida hecha, sigue con el paso 7. `vigilar_render.py <salida>` vale para una pasada a mano. La vigilancia no cambia
   el resultado: el vídeo sale idéntico con ella o sin ella.
7. **Comprueba el archivo final** (obligatorio, no se entrega sin esto): ffprobe (resolución, fps, nº de frames,
   etiquetas bt709), sonoridad (`ebur128`), **color contra el bruto** (preferencias → COLOR) y **fotogramas sacados del
   archivo final** en cada gráfico, en cada recurso y en cada cambio de sección. **Matrículas**: recortes a tamaño
   real del archivo final, cada 2–3 fotogramas, en todo el tramo en que el vehículo está en plano (también cuando
   parece tapada: preferencias → Matrículas). Al entregar, di qué has comprobado y
   qué no puedes comprobar (movimiento y sonido: Claude no ve vídeo ni oye) y las decisiones abiertas.
8. **Entrega**: `out/AAAA-MM-DD_<slug>.mp4` + **el paquete de YouTube** + línea en `out/REGISTRO.md`. No se sube a
   ningún sitio. El paquete se hace SIEMPRE al acabar el render, sin que lo pidan, con todo lo que ya sabes del vídeo
   (EDL, registro visual, descartes), **en el idioma del vídeo** y siguiendo `base/titulos-miniaturas.md` (léelo
   entero antes; títulos en español § 4, en inglés § 5) y `base/descripciones.md`:
   - **5 parejas de título + miniatura** para test A/B, cada una con un ángulo distinto, su **prompt para ChatGPT** y la
     **imagen de referencia** que hay que adjuntarle: un fotograma limpio del bruto (`miniatura.py momentos` para
     elegir mirando → `miniatura.py sacar A <mm:ss> …` → mira la ráfaga → `miniatura.py hoja`) o una foto del creador
     (`miniatura.py fotos` / `foto`). Di cuáles tres probarías primero.
   - **Descripción** con capítulos (`capitulos.py`) y **etiquetas**.
   - Queda en `out/<slug>/youtube/` (`PAQUETE.md`, `A.jpg … E.jpg`, `hoja.jpg`) y, para pegar, en
     `out/AAAA-MM-DD_<slug>.txt`. Enseña en el chat los cinco títulos con el texto de su miniatura y la hoja.
   - Con la persona en la miniatura, `miniatura.py cara A2` (la cara grande, de referencia de identidad: se adjunta
     siempre) y una referencia con el mismo ángulo y mirada que pide la miniatura (titulos-miniaturas.md → la cara, fiel).
   - Cuando vuelvan las miniaturas generadas: `miniatura.py final A <imagen> …` y mira `youtube/prueba.jpg` (a 168 px)
     y `youtube/caras.jpg` (¿es su cara? si no, se rehace en un chat nuevo).
   - Si las ha generado Claude en ChatGPT: con todo guardado y comprobado, **borra esos chats** (solo los apuntados en
     `youtube/generadas/chats.md`; titulos-miniaturas.md → borrar los chats).
   - Lo que el creador elija y lo que gane el test se apunta (§ 3).
   - **Lista de lo que se ha quedado fuera** (SIEMPRE, junto al paquete, sin que la pidan), sacada de
     `trabajo/descartes.md` y de la cabecera del EDL, para que el creador diga si quiere añadir algo. Agrupada:
     1) gracioso o con su toque (frases literales con bruto y minuto; también lo que se VE: muecas, gestos, cantos,
     bailes, el perro); 2) imagen buena sin usar; 3) fuera a propósito y por qué, en una línea por tipo (dinero,
     llamadas, logística, retomas, lo que pidió quitar). Termina con lo que tú meterías. Lo que elija → `_v2` y se
     apunta en «Decisiones de Lucas sobre descartes» de `base/preferencias.md` (o en su `preferencias.md` si es gusto
     suyo). Por qué: Lucas, 2026-11-16 (`prueba-3`): «al acabar de editar el video, a parte de dar el packaging, da una
     lista de todo lo que se ha dejado fuera por si se quiere añadir».
9. **Correcciones**: arréglalo, vuelve a renderizar solo lo afectado, entrega como `_v2`, `_v3`… y **apúntalo** (§ 3).
10. **Cierre** (cuando el creador da el vídeo por terminado): brutos a `bruto terminado/` como
    `AAAA-MM-DD_<slug>_<nn>-<que-se-ve>.ext` (los que sirvan de recurso, a `personal/<creador>/recursos/<tema>/` con ficha), «Usado en» en el
    catálogo de música y en el índice, y borra las versiones intermedias solo si él lo dice.
11. **Limpieza automática**: a los **30 días** del render final se borran solos los intermedios de ese vídeo
    (`out/<slug>/trabajo/`, `estudio/public/<slug>/`): lo hace `herramientas/limpiar_renders.py`, lanzado por el hook
    `SessionStart`; queda en `herramientas/limpieza.log` (`--simular` para ver qué borraría). **Nunca se borran**:
    brutos, `personal/` (con los recursos de cada creador), `refs/`, los renders de `out/`, ni `proyecto.py`, `edl.py`, `plan.py` y
    `Capas.tsx` de cada vídeo (con ellos se puede rehacer todo).

Remotion: carga la skill `remotion-best-practices` antes de escribir componentes; mapas: `remotion-maps` (técnica de
mapa estático; el componente de serie es `MapaSatelite`). Vista previa de gráficos: `cd estudio && npx remotion studio`.

## 3. Aprender de las correcciones (obligatorio)

Cada vez que corrigen algo («más dinámico», «ese plano no va ahí», «no uses ese sonido»):
1. Arréglalo en el vídeo.
2. **Entiende por qué te equivocaste** (qué dato no miraste, qué supusiste) y escríbelo en la regla: una regla sin la
   causa del fallo se vuelve a incumplir.
3. **Apúntalo en el mismo turno**, donde toca:
   - **`local`** — todo en la carpeta, nunca en `<skill>`: regla general del creador → `personal/<creador>/preferencias.md`;
     recurso fijo → `personal/<creador>/recursos.md`; número de la base → `personal/<creador>/ajustes.py`; color o cuentas →
     `personal/<creador>/marca.json`; regla de un tipo de vídeo → `refs/<tipo>/CONTEXTO.md` → «Correcciones».
   - **`autor`** (Lucas) — decide: **base** (debería valer para todo el mundo) → `<skill>/base/preferencias.md`, el
     `CONTEXTO.md` del tipo, `intros.md`, `recursos.md`, `titulos-miniaturas.md` o `descripciones.md`, y si es de herramienta, el script de
     `<skill>/plantilla/` (y copia en la carpeta); **de un creador** → `personal/`, igual que en local. Si no está
     claro, pregúntalo en una línea.
   - Formato: `- AAAA-MM-DD — <regla en imperativo>. Por qué: <lo que dijo, literal>. (vídeo: <slug>)`.
4. Si contradice una regla anterior del mismo archivo, **sustituye** la vieja. Una regla de `personal/` tapa la base sin
   tocarla.
5. Cuando algo guste a la primera («dejamos este»), apúntalo también en «Lo que funciona».
6. Decisión de gusto sin regla: dos variantes cortas (un tramo renderizado de cada una) en vez de adivinar.

## 4. Personalizar para un creador

**Criterio (Lucas, 2026-11-12): lo del creador se AÑADE a las bases, no las sustituye.** Se usan *su* intro, *su* outro,
*su* estilo, *su* tipo de música, *sus* efectos y *su* mascota; los cortes, los zooms, la elección de recursos, los
rótulos y el título siguen siendo los de la skill, salvo en lo que él pida cambiar.

Cuando el creador (o Lucas, para un creador) traiga **sus recursos o su estilo** — cabecera, cierre, logo, mascota,
música habitual, sonidos, colores, vídeos suyos publicados:
1. **Créalo**: `PY herramientas/montaje/nuevo_creador.py <nombre>` (desde la raíz). Sus archivos originales, a
   `personal/<creador>/recursos/marca/`; sus vídeos publicados, a `personal/<creador>/refs/`. Su material de archivo (clips,
   b-roll, fotos, mapas, música) va en las demás carpetas de `recursos/`: **crea ya las de tema de su nicho** y apúntalas
   en su `INDICE.md` (`base/recursos.md` § 2, como en `edicion-reels`). Nada suelto y nada sin ficha.
2. **Estudia cómo edita él** (si hay vídeos suyos): un agente por vídeo con
   `herramientas/montaje/ENCARGO_CREADOR.md` (rellena antes sus huecos: quién es y qué recursos suyos hay que
   reconocer), **de dos en dos**. Sale una ficha `.json` + `.md` por vídeo en `personal/<creador>/refs/`: dónde van su
   intro y su outro y cuánto duran, cada aparición de su mascota (cuándo, cuánto, dónde, qué dice), rótulos, música
   (cuánta y a qué nivel), botones. Lo que **coincide** entre vídeos es la regla.
3. **Prepara lo que se superpone** y míralo: animaciones con fondo verde → `herramientas/quitar_fondo.py` (`.webm` con
   transparencia); logos o dibujos con fondo liso → `herramientas/quitar_fondo_imagen.py` (`.png`). Salida en
   `estudio/public/personal/<creador>/`. **Mira la hoja de prueba y una hoja con TODOS los fotogramas** de cada
   animación: nunca se superpone nada con fondo, halo u objetos raros (base/recursos.md § 10).
4. **Apunta las reglas** (con fecha y de dónde salen): estilo y estructura → `personal/<creador>/preferencias.md`;
   cada recurso fijo, con cómo se pide → `personal/<creador>/recursos.md`; color y canal → `marca.json`; números
   (niveles de música, zooms, efectos) → `ajustes.py`; quién es → `perfil.md`.
5. **Gráficos propios** (su mascota con burbuja, su logo sobre la intro): componentes en
   `estudio/src/personal/<creador>/Graficos.tsx`, que exporta `propios(it, f, dur)`. En el `Capas.tsx` del vídeo:
   `import { propios } from "../../personal/<creador>/Graficos"` y, en `extra`, `return propios(it, f, dur) ?? null`.
   En `plan.py` se piden con `PROPIOS = [(ancla, segundos, "tipo", {datos})]`; con `"snd": ["pop", 0.18]` llevan sonido.
   Cada uno recibe además `it.idioma` (el del vídeo) e `it.logo` (el logo de `marca.json` para ese idioma; `""` si
   el archivo no está: entonces no se pinta logo, **nunca el de otro idioma o canal**, y `paso3_plan.py` avisa).
   Sus clips fijos (intro, outro) van en el EDL como un bruto: `V("intro", 1.9, 6.7, vol=0, tag="intro")`.
6. **Nada de esto se escribe en `<skill>`**, tampoco en modo autor: es de ese creador. Lo que sí es de la skill: los
   botones de YouTube, los efectos de sonido de serie y las herramientas.
7. **Prueba de render** con todo lo suyo aplicado y fotogramas del archivo final en cada recurso suyo, antes de darlo
   por bueno. Di lo que no has podido comprobar (sus efectos de sonido, el movimiento).
8. **Sus títulos y miniaturas**: si tiene canal, estúdialo (`PY herramientas/canal_youtube.py @sucanal --salida
   personal/<creador>/refs/canal` y un agente con `<skill>/base/refs/_youtube/ENCARGO_CANAL.md`): qué moldes de título
   y qué miniaturas le funcionan A ÉL, su tono, su tipografía y color de texto → `personal/<creador>/preferencias.md` →
   «Títulos y miniaturas». Pídele un juego de **retratos para miniaturas** (`base/titulos-miniaturas.md` § 6) y
   guárdalos con ficha en `personal/<creador>/recursos/creador/`.

## 5. Analizar referencias (cuando añaden vídeos o enlaces a refs/)

Método completo y herramientas en `<skill>/base/refs/dinamicos/_analisis/METODO.md`; encargos para los agentes en
`ENCARGO_ESTILO.md` (el completo, para llenar un estilo: contexto e interés, intro fotograma a fotograma, motion
graphics, efectos confirmados, fuentes; desde 2026-11-24), `ENCARGO.md` (ficha general) y `ENCARGO_DINAMISMO.md`.
**Por tandas** (varios enlaces): `PY herramientas/cola_refs.py añadir --estilo <e> URL…` y `… avanzar` baja
(`bajar_ref.py`, 1080p) y precalcula de uno en uno, deja como mucho 2 «listos para ver» y, con `… hecho <id>` tras
escribir la ficha, **borra el vídeo**. En Windows, `herramientas/windows/instalar_vigilante.ps1` deja un vigilante
cada 5 min (RAM y procesos colgados, solo los nuestros). Efectos de sonido: `escuchar_sfx.py` (candidatos + hoja de
espectrogramas; se confirman mirando). Fuentes: `fuente_rotulo.py` (top-3 de Google Fonts). Por cada vídeo: cortes
(`detectar_cortes.py`), intro fotograma a fotograma, transcripción, audio (voz y música, `analizar_audio.py`), zooms
(`medir_zoom.py`), rótulos y gráficos → una **ficha JSON** en `refs/<tipo>/<creador>/` y los patrones, con números, en
el `CONTEXTO.md` del tipo. Agentes de dos en dos. No se juzga la calidad de imagen, solo la edición. Las referencias
nuevas son locales; en modo autor, si Lucas dice que son para la base, van a `<skill>/base/refs/<tipo>/`.

**Canales de YouTube (títulos, miniaturas, descripciones)**: otro método, `<skill>/base/refs/_youtube/METODO.md`.
`PY herramientas/canal_youtube.py @canal` baja el último año en versión original (títulos, descripciones, visitas,
miniaturas, hojas de contacto) y se analiza con un agente por canal (`ENCARGO_CANAL.md`), uno por idioma para los
títulos (`ENCARGO_TITULOS.md`) y uno para las descripciones; estos agentes son ligeros y pueden ir todos a la vez.
Lo ya estudiado (diez canales, 631 vídeos, 2026-11-13) está en `<skill>/base/refs/_youtube/`.

## 6. Recursos y música

**Al montar se mira el archivo del creador**: en el paso 1 (lo que se nombra y no se ve en los brutos) y en el paso 4
(cada `BROLL`), en `personal/<creador>/recursos/INDICE.md`: Temas para la frase, Momentos y Útil para el segundo exacto,
Vibe y Outfit para que case. **Dar de alta recursos** (los que trae el creador, un disco entero, los brutos que sirven de
recurso al cerrar un vídeo): `herramientas/inventario_recursos.py` → lotes → un agente por lote con
`herramientas/ENCARGO_RECURSOS.md` → `juntar` → `comprobar` (ninguna ficha pobre: `base/recursos.md` § 3–4).
Guía completa en `<skill>/base/recursos.md`: registro visual de los brutos, carpetas y fichas de `personal/<creador>/recursos/`, cómo
elegir un recurso, catálogo de música, mapas de satélite, **botones de YouTube** (§ 9: los únicos recursos que trae la
skill, con los efectos de sonido) y cómo quitar el fondo a animaciones y logos (§ 10). La skill no trae música.
**Música nueva y vídeo de stock: primero Shutterstock con Claude in Chrome** en ese ordenador (`base/recursos.md` § 5 bis):
la primera vez se prueba si hay sesión y se apunta en `personal/bancos.md`; Claude busca y propone, y descarga con una
confirmación por tanda. Nunca inicia sesión, ni compra, ni marca extras de pago, ni sube nada.

## 7. Otras skills y servicios

Lista en `<skill>/SKILLS.txt` (las instala `instalar.sh`, globales en `~/.claude/skills`): `remotion-best-practices`
y familia (`remotion-maps`, `remotion-captions`, `remotion-render`…), `hyperframes` (bloques de motion graphics) y
`media-use` (SFX, música e imágenes). **ElevenLabs es opcional** (voz IA, SFX o música generados): sin clave, todo el
flujo funciona con Whisper local, los sonidos de serie y la música del creador.

## 8. Instalar, actualizar, publicar

- `bash <skill>/instalar.sh "<ruta>"` — crea la carpeta de edición desde `plantilla/` (con `personal/_plantilla/`),
  enlaza la skill, instala lo que falte (`--adoptar` para una carpeta que ya existe; `--ligero` sin skills de apoyo,
  `.venv` ni `node_modules`). Detalle en `<skill>/LEEME.md`.
- La skill **se actualiza sola** al abrir sesión (hook `comprobar.sh` → `sincronizar.sh` del repo, como mucho cada 6 h):
  si hay versión nueva en GitHub y la copia está limpia, fast-forward, plantilla al día y el perfil de los creadores
  incluidos que haya cambiado el autor (en modo local se sobrescribe lo que el autor cambió). Si el hook dice que se actualizó, tenlo en cuenta (lee
  las novedades si afectan a lo que vas a hacer).
- `bash <skill>/actualizar.sh` — completo: además programas, skills de apoyo y dependencias. Pone al día herramientas y componentes de serie que no se hayan tocado en local.
  **Nunca pisa** `personal/` (con los recursos de cada creador), `refs/`, `out/`, `marca.ts`, `estudio/src/personal/` ni nada cambiado en
  local (lo lista).
- `bash <skill>/conectar_disco.sh <creador>` — enlaza `personal/<creador>/recursos` a su disco duro (lo busca en todas
  las unidades) y copia lo pesado de sus `refs/`. Para cuando cambia la letra del disco o se conecta por primera vez.
- `bash <skill>/publicar.sh "<mensaje>"` — **solo modo autor y solo cuando Lucas lo pida expresamente**: publica TODO
  el repo (todas las skills; antes copia a `creadores/<n>/` el perfil desde la carpeta de edición) como versión nueva
  (`vX.Y`, con Release). `--versiones` las lista; `--volver vX.Y` hace
  rollback para todos (publicado como versión nueva; no borra historial).
