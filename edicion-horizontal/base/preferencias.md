# Preferencias ESTÁNDAR — las bases de edición (valen para todos los vídeos horizontales)

**Estándar mínimo de `edicion-horizontal`.** Son las bases: salen de las referencias medidas y de las correcciones de
Lucas, autor de la skill, y solo él las cambia. Donde una regla dice «Lucas», léelo como **el creador que edita en esta
carpeta**. **Lo que el creador tenga en su carpeta de personalización (`personal/`) manda sobre estas reglas** cuando
chocan, salvo COLOR (que el bruto no se toque es el estándar; si quiere otra cosa, la pide en ese vídeo; el Log se revela
siempre con su LUT y el look creativo se elige en la ventana de arranque: G009).

Los números de ritmo, zooms, textos y mapas, con su origen, están en `base/refs/dinamicos/CONTEXTO.md`; aquí va la regla.
`ramon` = el primer edit de prueba (23 min, 11 brutos Sony 4K 25 fps, hablado en inglés); su código está en
`base/ejemplos/ramon/` (sin media).

Formato: `- AAAA-MM-DD — regla. Por qué. (vídeo)`. Si una regla nueva contradice otra, sustituye la vieja.

## ⚠️ COLOR — regla fija (heredada de reels; manda sobre todo lo demás)
- **El color del bruto NO se toca nunca, salvo que el creador lo pida expresamente en ese vídeo.** Prohibido por
  defecto: etalonado, gamma, curvas, contraste, brillo, saturación, viñeta, LUT creativas y «mejorar» por iniciativa
  propia. Por qué: «que se mantenga, nada de tocarlo a no ser que te lo diga».
- **Bruto SDR (Sony y la mayoría de cámaras): no pasa por ningún proxy.** El paso 4 monta desde el archivo original con
  ffmpeg, sin filtros de color, y etiqueta la salida bt709 limitado. Medido en `ramon`: 0,3–0,7 niveles de diferencia
  media con el bruto.
- **Bruto HDR (iPhone HLG/PQ): se convierten a SDR SOLO los trozos que usa el montaje**, con
  `herramientas/montaje/sdr.py` (desde `out/<slug>/`, después de `paso3_plan.py`; `paso4_render.py tramos` lo llama
  solo si falta algo). Deja `trabajo/sdr/<clip>/<a>_<b>.mp4` (libplacebo, x264 CRF 14, a los fps del proyecto) y todos
  los pasos leen la imagen con `comun.fuente()`, que elige el original (SDR) o la copia (HDR); el sonido sale siempre
  del original. Vale igual para los clips de archivo del creador que sean HDR. **Nunca `zscale` + `tonemap` a mano**
  (sale ~20 niveles más claro y cálido). Por qué por trozos: convertir los brutos enteros cuesta ~2 s por segundo de
  bruto en 4K; en `1311` (83 min de iPhone 4K 60 fps) habrían sido unas 3 h y se convirtieron 151 trozos (24 GB) en
  una fracción. `herramientas/proxy.sh` (el bruto entero; en macOS, avconvert + `hdr-pantalla.cube`) queda para
  cuando se quiere un archivo SDR suelto. Medido en `1311`: +0,3 a +1,2 niveles las copias y +0,8 a +1,1 el render.
- **Bruto en LOG (DJI D-Log M, Apple Log, S-Log3, V-Log, C-Log, F-Log…): se REVELA siempre con el LUT de conversión
  de su perfil, sin preguntar** (G009, 2026-11-26). Revelar no es «tocar el color»: el Log está hecho para eso y sin LUT
  sale gris y lavado (Lucas: «si está grabado en logarítmico, obviamente se le pondrá un LUT, porque si no el vídeo sale
  muy gris»; en `casa-creadores` v1 los clips de la Osmo Action 5 Pro en D-Log M salieron grises y la revisión no lo vio).
  Va como el HDR: `comun.revelado()` lo detecta (metadatos → seguro; si no, 10 bits o cámara de Log + imagen con negros
  levantados, sin altas luces y poco saturada → probable) y `sdr.py` revela solo los trozos que se usan, con el `.cube`
  de `herramientas/luts/` (los oficiales del fabricante; `herramientas/color_log.py luts` dice cuáles faltan y de dónde
  bajarlos; los del creador, en `personal/<creador>/recursos/luts/`, mandan). Si el LUT se pasa, `LUT_INTENSIDAD` (0–1)
  en su `ajustes.py`. Un «probable» se confirma con `color_log.py comparar BRUTO <s> antes_despues.jpg`; si no es Log,
  `LOG_CLIPS = {"<clip>": None}` en `proyecto.py`. Sin el LUT del perfil, el render se para y dice cuál falta.
- **LOOK creativo: por defecto NINGUNO** (directo, el color de la cámara). Se pregunta UNA vez en la ventana de arranque
  (fila COLOR) y se guarda en `personal/<creador>/ajustes.py` (`LOOK`); «solo este vídeo» → `proyecto.py`. Hay tres
  de la casa, suaves y que respetan la piel (`natural`, `calido`, `cine`, generados por `color_log.py`, sin licencias
  de terceros) y los `.cube` del creador en `personal/<creador>/recursos/luts/` (packs gratis buenos para eso: los
  creativos oficiales de Sony y Panasonic, FreeVisuals —libre para uso comercial—; mira siempre la licencia).
  `LOOK_INTENSIDAD` (0–1). Va encima de todo el vídeo, por debajo de los gráficos (el acento no cambia). Si cambia el
  LUT, su intensidad o el look, `paso4_render.py tramos` rehace solo los tramos afectados (los parches de `foco.py` y
  `tapar.py` de esos planos, a mano).
- **Comprobación obligatoria, dos veces**: una copia SDR de cada bruto HDR contra el bruto antes de montar
  (`comparar_color.sh BRUTO trabajo/sdr/<clip>/<a>_<b>.mp4 "<t>" <a / FPS>`), y el render contra el bruto antes
  de entregar. macOS: QuickTime en el mismo instante + captura. Windows/Linux: `herramientas/comparar_color.sh` (mpv,
  `winget install shinchiro.mpv`). Diferencia media ≤ 5 niveles en zonas sin texto ni movimiento. Un fotograma sacado
  con ffmpeg de un bruto HDR no vale como referencia. Di el resultado al entregar.
- **Etiquetas**: todo lo que sale va `bt709/bt709/bt709`, rango `tv`, `yuv420p`. Si un bruto viene etiquetado
  `iec61966-2-4` (xvYCC, lo hace la Sony), el concat sin recodificar hereda la etiqueta: el paso `unir` la corrige con
  `-bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1`. Comprueba el archivo final con ffprobe.
- Las capas de Remotion se renderizan aparte (ProRes 4444 con alfa, `remotion.capas.config.ts`) y solo llevan gráficos:
  el vídeo nunca pasa por Chrome, así que Remotion no puede cambiarle el color.
- Plano muy claro con texto encima que no se lee → sombra más fuerte en el texto o moverlo; bajar la exposición de ese
  plano solo si el creador lo pide.

## Marca y estilo
- Acento, canal y @: `personal/<creador>/marca.json`; fuentes: `estudio/src/comun/marca.ts` (todo local). De serie: amarillo-lima
  `#E6EC52`, **Unbounded 900** para todo lo grande, **Lexend** para lo pequeño. Nada de rosa. Un solo acento y una
  familia grande por vídeo.
- **Color por función**: acento = dato, número, énfasis; blanco = información; blanco en minúsculas entre *asteriscos* =
  comentario del editor. Contorno negro + sombra corta; sin cajas ni pastillas.
- **Idioma: el del vídeo, SIEMPRE detectado del audio** (`paso0_preparar.py` lo imprime por bruto), nunca supuesto por el
  nombre del creador, el país ni el idioma en que te escriben. Transcripción, rótulos, título, capítulos y descripción
  van en ese idioma. Por qué: «ten en cuenta el idioma del vídeo siempre» (el primer bruto estaba en inglés y Lucas
  escribe en español). (ramon)

## Ritmo, cortes y zooms
- 2026-11-11 — **Dinamismo con juego de escala.** A cámara, un cambio visual cada 2,5–4,5 s: corte de escala DE GOLPE en
  un límite de frase, escalas alternas ×1,0 ↔ ×1,12–1,5; frase fuerte ×1,65 mientras dura (1–2 por minuto); pocos zooms
  animados (entrada rápida con frenada). **Nada de zoom lento sostenido.** Lo hace `dinamica.py`; lo elegido a mano va en
  `FUERTES` y `ENTRADAS` de `plan.py`; el gusto de cada creador, en `personal/<creador>/ajustes.py`. Objetivo en vídeo hablado:
  mediana de plano ~2,2 s y 22–27 cambios/min. Por qué: «no me parecen lo suficientemente dinámicos, falta algo de juego
  con zooms y cortes» (refs: Plex, Grefg, Xokas, Lucas Valero). (ramon v1 → v2)
- 2026-11-11 — **Los zooms tienen que apuntar bien.** Un punch-in contiene la cara durante TODO el plano (no vale centrar
  en la mediana si la persona se mueve); si no cabe, se cierra menos. Con detección de cara floja (< 85 % de muestras),
  máximo ×1,2 y centrado. Un zoom a un objeto o animal lleva su centro a mano (`(zoom, cx, cy)`) y se comprueba con
  `ver.py`. Por qué: había zooms que acababan en una pared. (ramon v2)
- 2026-11-15 — **Sin cara en el plano, sin cortes de escala.** El juego de escala es para cuando se le ve hablando. En
  un plano principal sin cara (él de espaldas, la cámara andando, buscando el interruptor) un ×1,15 no se lee como
  ritmo: se lee como un zoom a su hombro o a una pared. `dinamica.py` lo deja a ×1,0 (`Z_SIN_CARA`); el ritmo de esos
  tramos se da con recursos de lo que se habla, no con zoom. Por qué: Lucas, prueba-3 v2, «está zoomeado a su hombro,
  mejor sin zoom» y «hay un zoom a una pared». (vídeo: prueba-3)
- **Se corta por el texto, no por tiempos.** El EDL elige cada frase por su texto literal en la transcripción y
  `paso1_alinear.py` afina los bordes con alineación forzada (los tiempos de Whisper van ~0,17 s adelantados, hasta
  0,8 s). Después `comprobar_voz.py`: ratio ≥ 0,97 y ninguna palabra comida o repetida en un borde.
- 2026-11-14 — **Las frases, ENTERAS: no se corta a media frase.** Una pieza `T(…)` empieza donde empieza la frase (con
  su sujeto, su «hay que…», su «vamos a…») y acaba donde acaba (con su remate, su verbo, su «porque…» si lo lleva).
  El fallo típico es copiar de la transcripción solo el trozo «bueno» y dejar fuera dos palabras de delante o la
  coletilla de detrás: en el vídeo suena cortado («…que mirar que no haya nadie» por «hay que mirar…»; «a meter aquí
  la pala» por «vamos a meter…»; «porque no va a invadir…» sin lo que explica; una frase que acaba en «para que»).
  Se comprueba SIEMPRE con `frases.py` (después de `paso1_alinear.py`): enseña cada pieza con lo que se dice justo
  antes y justo después en el bruto y si hay pausa real en el corte, y avisa de las que arrancan con una palabra que
  cuelga de lo anterior (porque, que, y, además, a…) o terminan en una que pide continuación (que, para, de, y…).
  Cada aviso se lee y se resuelve: **alargar hasta el borde de la frase** (lo normal), dejarlo si lo de fuera es
  muletilla o retoma y lo de dentro se entiende solo (se apunta en `OK_A_MEDIAS` del `edl.py` con el porqué), o quitar
  la pieza. Solo valen golpes sueltos en el **tráiler**, y aun así cada uno tiene que entenderse solo. Tampoco se
  empalman dos mitades de frases distintas para «fabricar» una. Si el creador se interrumpe él mismo (le corta el
  perro, se le cae algo), eso no es un corte: es el momento, y se deja con lo que pasa después.
  Por qué: Lucas, «y hay veces que cortas frases a medias» (v1 de `1311`: de 113 piezas de habla, una docena
  empezaban o acababan a media frase). (vídeo: 1311)
- 2026-11-17 — **La misma idea dicha dos veces es una retoma, aunque la primera toma tenga gracia: se queda la buena.**
  Se corta: la frase repetida dentro de la misma pieza («porque lleva pienso para tortugas, porque lleva un poco de pienso
  para tortugas vegetarianas» → solo la segunda), la toma que el creador repite porque quien graba se lo pide («ahora
  vamos a la várzea… vámonos a la várzea»: suena la segunda y nada de en medio) y la primera presentación que vuelve a
  hacer entera justo después («las Tortugas Ninja son… ¿qué falta?» y luego, del tirón, «…Donatello, Rafael,
  Michelangelo y Leonardo» → solo la buena, sin el olvido). Una retoma con un tropiezo gracioso solo se queda si el
  tropiezo ES el momento y se quita la otra toma; nunca las dos. Lo mide `frases.py` (sección «La misma idea dos veces»:
  grupos de palabras que suenan dos veces en la pieza o en las tres siguientes, y la retoma pegada); cada aviso se
  resuelve en el EDL o se apunta en `OK_REPITE` con el porqué (un estribillo, «baila las congas, baila las congas»).
  Por qué: Lucas, alimentacion v1, «se repite dos veces… yo quitaba el primero», «lo repite dos veces y se oye al cámara
  decirle que lo diga», «repite el plano dos veces, pon solo el bueno, si no se hace repetitivo». **Causa:** criterio y
  herramienta. Al aplicar «lo que le da toque se queda» metí la primera toma por el olvido gracioso y no vi que la
  segunda repetía lo mismo; y `frases.py` solo miraba los bordes de cada pieza, no lo que se dice dentro ni en la de al
  lado. La voz de quien graba pidiendo la retoma no sale en la transcripción (Whisper no la oye): `comprobar_voz.py`
  avisa ahora de `VOZ SIN TEXTO` y de `HUECO` (silencios de más de 1,5 s dentro de lo hablado). (vídeo: alimentacion)
- 2026-11-17 — **Fuera lo que, suelto, se puede sacar de contexto o invita a criticar al creador.** Sobre todo en un canal
  de animales: frases que, sin lo de alrededor, suenan a que los animales mueren, sufren o están descuidados («aguanta,
  mosca… es que se están muriendo»), escenas que alguien puede leer como maltrato o descuido aunque no lo sean (pedir que
  se lleven al perro y amenazar con encerrarlo: «pilla al perro… si no lo voy a meter en la habitación y que se espere»),
  peleas o riñas, quejas que dejan mal a terceros. La regla del toque **no** cubre esto: ante la duda, fuera, y se cuenta
  al entregar en la lista de lo que se ha quedado fuera. Pregúntate con cada aparte: «¿alguien podría recortar este
  trozo y usarlo contra él?». Por qué: Lucas, «eso sácalo porque no se sabe el contexto y se puede sacar de contexto» y
  «bórralo, no queremos a gente criticando la escena». **Causa:** criterio. La regla de «apartes al perro, se quedan»
  (1311) se aplicó sin el filtro de cómo se ve fuera de contexto. (vídeo: alimentacion)
- Fuera: retomas, muletillas largas, esperas, colocar la cámara. Dentro: reacciones, risas y los silencios que cuentan,
  y **todo lo que le da toque al vídeo** (ver «Que el vídeo lo cuente todo»).
- Límite de calidad: con bruto y salida a la misma resolución todo punch es ampliación. Hasta ×1,3–1,4 no se nota;
  ×1,6–1,7 solo en golpes cortos; más de ×2 solo para un detalle que lo merezca.
- No se monta a ritmo de la música, salvo ráfagas y montajes sin voz.
- 2026-11-14 — **Vídeos lo más dinámicos posible, SIEMPRE, y una versión nueva nunca menos dinámica que la anterior.**
  Al alargar un montaje (más frases, más toque) el dinamismo no se diluye: se mide y se iguala o se supera, antes de
  renderizar, con `paso3_plan.py` y `video.json` frente a la versión anterior (o, en un vídeo nuevo, frente a los
  objetivos de aquí):
  - cortes por minuto (≥ 22–27) y mediana de plano (≤ ~2,2 s);
  - **% del tiempo con texto o gráfico en pantalla** (rangos de gráficos ÷ duración; en Reino Selva, ≥ 20 %);
  - planos de archivo por minuto sobre las menciones (especie, recinto, el pasado, el perro…);
  - **huecos sin ningún texto de más de ~25 s**: se buscan (rangos de `video.json`) y en cada uno se rotula lo que da
    juego en ese tramo (una salida graciosa, una reacción, la idea del momento, un aparte al perro), con su timing medido.
  Por qué: Lucas, al pedir la v2 de `1311`, «la v2 tiene que ser igual de dinámica a ser posible, eso siempre, vídeos
  lo más dinámicos posibles». La v2 (22 min, con todo el toque) cortaba igual que la v1 (27,7 frente a 26,8 cortes/min),
  pero tenía texto solo el 14 % del tiempo frente al 20 % de la v1, con huecos de hasta 94 s sin nada: se añadieron 45
  textos y 3 planos de archivo hasta el 20,1 %. (vídeo: 1311)

## Orden y continuidad
- 2026-11-12 — **Un plano de desplazamiento (andar, bajar escaleras, entrar, conducir) va en el momento del vídeo en que
  ocurre ese desplazamiento**, nunca como «transición genérica» en otro cambio de sección. Un clip sin habla se sitúa por
  **orden de grabación** (número de archivo y hora) y por lo último que se dijo antes de él: si el bruto anterior acaba
  en «vamos a la várzea» y el siguiente empieza ya en la várzea, el clip de en medio ES la bajada a la várzea. Por qué:
  «cuando baja las escaleras va justo en el momento que baja a la várzea, no después… lo has pasado al punto 6». El
  fallo: se trató el clip como un «paseo» suelto y se colocó en el siguiente cambio de sección. (ramon v3 → v4)
- **Antes de escribir el EDL, la cronología**: lista de brutos en orden de grabación con dónde está el creador en cada
  uno, de dónde viene y a dónde dice que va (`paso0_preparar.py` da la tabla; el registro visual, el campo
  `desplazamiento`). Si se cambia el orden de las secciones respecto al rodaje, los desplazamientos se quedan con SU
  trayecto o no se usan.
- **Continuidad**: un recurso o un plano de acción no puede enseñar un sitio, una ropa o una luz que contradiga el
  momento en que se pone (el creador aparece en un sitio al que aún no ha llegado).
- Al mover una pieza del EDL, revisa todo lo que cuelga de su marca (ventanas de música, recursos, rótulos).

## Que el vídeo lo cuente todo (repaso de descartes)
- 2026-11-12 — **Antes de dar un montaje por bueno, repasa TODO lo que se ha quedado fuera.** Al escribir el EDL se
  eligen frases y se descarta más de la mitad del bruto; ahí se pierden cosas buenas sin darse cuenta. Después de
  `paso3_plan.py`: `descartes.py` → `trabajo/descartes.md` (cada tramo de habla que no suena en el vídeo, marcado
  NUEVO si no se parece a nada de lo que sí suena, y cada «mejor recurso» del registro visual que no sale). **Se lee
  entero**, y cada NUEVO se mira con su contexto (qué se dice justo antes y después).
- **Qué se busca** (lista viva: se afina con cada «sí» y cada «no» de quien edita, abajo):
  - el **porqué** de algo que el vídeo afirma sin explicar (la causa, el mecanismo, «porque…»);
  - una **anécdota** o historia con principio y final (cómo pasó algo, un error, un susto);
  - un **chiste**, una salida graciosa o un momento con un animal o una persona que hace gracia, y su plano;
  - una **frase con fuerza** (rotunda, emocionante, que valdría para el tráiler);
  - un **ejemplo concreto**: el nombre de una especie, un sitio, una cifra, una comparación;
  - **qué va a pasar**: planes, lo próximo que hará, el vídeo que anuncia;
  - un momento **sincero** (lo que cuesta, lo que sale mal, una confesión);
  - **imagen**: un «mejor recurso» sin usar, un animal haciendo algo, una acción que abre o cierra una escena.
  No es recuperable: retomas y la misma idea dicha otra vez, arranques, instrucciones al cámara o al editor, y lo que
  se dice sin que se vea nada que lo sostenga.
- 2026-11-14 — **Lo que le da TOQUE al vídeo se queda, desde el primer EDL.** El toque es la personalidad del creador:
  el humor y las salidas, lo que le dice al perro, al animal o a quien graba, las reacciones (un «¡guau!», un susto,
  un «pobrecilla»), las anécdotas, las explicaciones y los porqués, lo que siente por lo que hace (le sabe mal
  estropear una planta, se alegra de salvarla), las manías y las frases con gracia aunque «no hagan avanzar» el
  vídeo. **Eso no es relleno ni charla de rodaje: es el vídeo.** Solo se corta: la retoma, el arranque, la misma idea
  dicha otra vez, el tiempo muerto, las instrucciones a quien graba o edita y lo privado (terceros con nombre,
  llamadas, datos personales). **La duración no es motivo** para quitar nada de lo otro, ni hay que apretar hacia un
  vídeo corto: se monta con lo que hay de bueno y sale lo que salga (dentro de lo que publica el creador).
  Regla de mano al escribir el EDL: ante la duda entre dejar una frase con gracia o quitarla, **se deja**.
- **El repaso de descartes es para cazar lo que se escapó, no para aplazar decisiones.** Si al leer
  `trabajo/descartes.md` algo «a lo mejor no se tenía que haber descartado», ya está decidido: **se mete antes de
  renderizar** y no se le presenta a quien edita como «descarte». Al entregar se le cuenta qué entró en ese repaso y,
  **junto al paquete de YouTube, la lista de TODO lo que se ha quedado fuera** para que diga si quiere añadir algo
  (SKILL.md § 2, paso 8). **Se pregunta antes solo lo de verdad dudoso**: lo que
  toca a terceros o a su vida privada, promociones, lo que deja mal al creador, o lo que cambia la estructura del
  vídeo. Él dice sí o no; entonces se aplica.
  Por qué: Lucas, tras la v1 de `1311` (13:55, un tercio de lo hablado; en la lista de descartes iban cuatro momentos
  que yo mismo marcaba como buenos): «añade todo lo que has descartado, y no descartes tanta cosa, que son cosas
  interesantes, que le dan su toque a los vídeos; está bien descartar, pero tienes que aprender que lo que le da toque
  al vídeo tiene que quedarse; de hecho me lo has presentado como "descarte" ya sabiendo que a lo mejor no se tenía
  que haber descartado». El fallo fue triple: montar apretando hacia un vídeo corto, tratar la personalidad como
  relleno, y escudarse en «no meter nada sin preguntar» con cosas que ya se sabía que valían. Esta regla sustituye a
  la de 2026-11-12 («lo que falte no se mete por cuenta propia»), que queda solo para lo dudoso. (vídeo: 1311)
- 2026-11-14 — **Sin pasarse al otro lado: lo que sí sobra, sobra.** Meter el toque no es meterlo todo. Se siguen
  cortando la **narración de colocación** («esta la voy a poner aquí… no, aquí»), la **logística** (ir a por la pala,
  buscar la manguera), la **misma idea dicha otra vez** y las retomas, aunque estén enteras y bien dichas. Orientación,
  no tope: un vídeo del creador que pasa de unos 13 min a 28 por meter el toque se ha pasado; lo que queda sin logística
  ni repeticiones ronda los 20–22 min (de 83 min de bruto en `1311`). Si al meter el toque la duración se dobla, se
  repasa el EDL buscando colocación, logística y repeticiones antes de enseñarlo.
  Por qué: Lucas, al ver la versión intermedia de la v2 de `1311`: «¿cómo ha pasado la v2 de 13 min a 28? ¿No es
  demasiado?». Se dejó en 22:20 quitando eso, sin tocar humor, reacciones ni explicaciones. (vídeo: 1311)
- 2026-11-15 — **Lo que PASA va en el vídeo, no solo lo que se dice de ello.** Un fallo, una caída, un susto o lo que
  hace el animal (se le cae el micro al agua, resbala, el perro le roba algo) se monta **en el momento en que ocurre,
  con su sonido** (`V(…)`), y la frase que lo cuenta va detrás («se me ha caído el micro»). Aunque el plano sea movido o
  feo: aquí manda lo que pasa, no la calidad del plano. Al escribir el EDL, cada frase que cuenta algo que acaba de
  pasar («se me ha caído», «me he mojado», «casi me mato», «mira lo que ha hecho») obliga a mirar con `tira.py` los
  10–20 s de antes y meter el momento. El registro visual los apunta aparte (`momentos`) y `descartes.py` los saca los
  primeros como **MOMENTO sin usar**. **Los detalles pequeños cuentan**: un fail de 3 s es de lo que más gracia hace
  del vídeo y es lo primero que echa en falta quien lo ve.
  Por qué: Lucas, en la v3 de `1311`: «en el 5:52 dice que le ha caído el micro, pero deberías incluir el momento en el
  que se le cae al agua también, ya que es gracioso el fail… para que la skill aprenda que hay cosas que no hay que
  dejarse y entienda que hay que darle importancia a cosas pequeñas también». Causa: el EDL se elige por frases de la
  transcripción y la caída no tiene palabras; el registro visual solo puntuaba planos como recurso (uno movido saca 0)
  y por eso `descartes.py` nunca la enseñó. Se metió la frase que lo cuenta y no lo que pasó. (vídeo: 1311)
- **Cada decisión se apunta** (aquí si vale para todos; en `personal/<creador>/preferencias.md` si es de su gusto), con
  el tipo de momento y el porqué, para detectar mejor la próxima vez.
  Por qué: Lucas, «revisa siempre que el vídeo cuente todo lo importante, que no quede nada eliminado de tomas… y si
  detectas que falta algo, me dices antes de ponerlo, para yo decirte si sí o si no, y así lo aplicamos a la skill
  general, que sepa mejor detectar todas las partes interesantes, buenas, graciosas, impactantes». Y por qué hacía
  falta: en `ramon` se usó el 45–65 % de lo hablado de cada bruto y nadie había repasado el resto. (vídeo: ramon)
- **Decisiones de Lucas sobre descartes** (para aprender qué entra y qué no):
  - 2026-11-12 (`ramon` v6 → v7; lista de 17, alargó el vídeo de 16:46 a ~18:40 y no le importó: **la duración no
    es motivo para dejar fuera algo bueno**). Literal: «añade todo menos el 11, el 12, 13, 14. Apunta qué tipo de
    cosas no hay que excluir… el 16 y 17 los quiero dentro».
  - **SÍ entra (no lo vuelvas a excluir):**
    - la **frase rotunda** que abre un bloque («…once it is built, there's no way back»);
    - el **chiste con un animal** y SU plano (el perro mirando a las tortugas: «he's also not having the fun that
      tortoises have»): sin el plano no hay chiste, van juntos;
    - la **anécdota de cómo pasó algo** (las medakas entraron con una planta que cambió de estanque);
    - el **porqué** de una afirmación que el vídeo dejaba sin explicar (por qué la tortuga rusa acabará siendo rara:
      las crían cogiendo huevos del campo);
    - **planes y vídeos anunciados** (va a criar grillos y lo enseñará) y **lo que significa en concreto** una
      decisión (qué especies caben al abrir el bioma, qué peces podrá meter);
    - el **ejemplo concreto** de especie al explicar algo general (la rana de ojos rojos al hablar del Chocó);
    - el **plan para el animal protagonista** de un capítulo (qué será de él en verano);
    - una **curiosidad breve aunque no haya imagen** (las ranas se han enterrado hasta el año que viene): si son 5–8 s
      y cierran una idea, entran a cámara;
    - la **salida graciosa** sobre un nombre («we called it bunker… it's not a bunker, it's a den»);
    - la **acción que abre una escena** (abre con llave la puerta del bioma antes de «I've got good news»);
    - los **«mejores recursos» sin usar**, para tapar voz que ya estaba (16 y 17 «los quiero dentro»).
  - 2026-11-14 (`1311` v1 → v2; el vídeo pasó de 13:55 a bastante más y era lo que quería). Literal, arriba. **SÍ
    entra, y desde el principio** (todo esto se había quedado fuera en la v1):
    - los **apartes al perro o al animal** que se mete en medio («déjame, pesado», «Ragnar, stop», «deja la tortuga,
      tío», «¿las vas a destrozar o no?») y lo que pasa con él a lo largo del día (le roba un calcetín, hay que
      quitárselo para que no se lo trague): es el **hilo cómico** del vídeo, se sigue entero;
    - el **cuidado por los animales y las plantas** («hay que mirar siempre, cuidar bien con los animales», «me sabe
      mal fastidiar plantas que ya están enraizando», «a esta la hemos salvado», «pobrecilla», «reanimación»);
    - la **explicación completa** de algo que el vídeo dejaba a medias (la luna creciente y decreciente cada quince
      días, después de nombrar el calendario biodinámico);
    - las **frases con gracia o de carácter** («eficiencia pura», «¿por qué? porque sí», «como ya tengo una edad», «con
      esto te pones fuerte», «a por el gordo, el gordo de Navidad», «el que mejor se lo pasa aquí es el que me graba,
      que le gusta verme sufrir»);
    - las **reacciones** a lo que sale bien o mal («toda de una, ¡guau!», «no había ni enraizado, sorprendente», «no
      entiendo nada») con su imagen;
    - los **consejos y avisos** de pasada («con estos zapatos no recomiendo que hagáis nada», «lo pondré veinte
      minutos a regar», «echarle ese abono») y lo que **anuncia** que hará o explicará;
    - las **pequeñas derrotas** («un pequeño fallo, la voy a intentar rescatar», «no me quiero mojar los pies otra vez»).
    Fuera se quedó solo lo privado: una pregunta sobre el examen de un familiar y una llamada de teléfono.
  - 2026-11-16 (`prueba-3` v3 → v4). Lucas: «creo que omites partes graciosas en los videos, y yo creo que a parte de
    valor hay que dejar partes graciosas». **SÍ entra:** cuando el creador **canta, baila o hace el payaso mientras
    trabaja** (taladrando de espaldas canta «Shot me down!… ¡Halalalala!… Se acabó»), aunque no diga nada útil y no se
    le vea la cara: va entero, con su sonido, y el ritmo lo dan palabras-golpe de lo que canta (sin cara no hay corte
    de escala). Una canción o un tarareo no son «tiempo muerto»: en el texto de la transcripción parecen ruido
    («¡Halalalala!»), así que al leer `descartes.md` cuenta lo que se oye, no lo que se dice.
  - **NO entra** (los cuatro que quitó en `ramon`; el motivo no lo dijo, la lectura es mía):
    - hablar del **dinero** que le cuesta («a lot of money that I am putting in here»);
    - hablar de su **poca audiencia** o de cómo va el canal («I don't have much audience in English»);
    - **promoción** de otro canal y **calendario** de episodios («check my Spanish channel», «every week»): eso va en
      la descripción, no en el montaje;
    - una **explicación en la que duda o no recuerda el dato** (la diferencia entre dos especies cuyo nombre no le
      sale): resta autoridad y no enseña nada.
    Mi lectura: fuera lo que habla del canal y del negocio en vez del tema, y lo que deja al creador en mal lugar.
    Si en otro vídeo dice que sí a algo de esto, corrige esta lista.
- 2026-11-19 — **Fuera las órdenes de rodaje** («corta», «ven», «graba», «para», «otra vez», «¿ya?»), aunque estén en
  mitad de una frase buena: se parte el `T()` en dos. Whisper casi nunca las transcribe (con su filtro de silencios) y
  la alineación forzada estira las palabras de al lado por encima, así que `comprobar_voz.py` no ve ningún hueco: salen
  como `AVISO ESTIRADA` en `paso1_alinear.py` (una palabra que dura más de 1 s, 1,5 s si es una cifra) y se confirman con
  `retranscribir.py <clip> <t0> <t1> --prompt "Corta. Ven."` (sin VAD; con `--escribir` corrige el `.w.json`). Por qué:
  Reino Selva, «11:00 digo "corta" eso sobra»: «Ven, corta.» quedó dentro de «…2026 cero kills. El único animal herido…»
  («2026» duraba 4,3 s y «kills» 2 s en la línea). (vídeo: vaciamos-estanque v2)
- 2026-11-19 — **Un comentario de quien graba que solo aporta una palabrota o un juicio** («en mi puta vida me imaginé
  que iba a estar grabando una cosa así») va fuera del EDL, no pitado. Si aporta algo (una pregunta, un aviso, humor), se
  queda con su pitido (Audio → Palabrotas). (vídeo: vaciamos-estanque v3)
- 2026-11-19 — **Tomas falsas solo si son buenas de verdad**: graciosas o con algo que pasa (un susto, el perro, una
  caída). Equivocarse leyendo o repetir una frase no lo es. Ante la duda, fuera, y se dice al entregar en «lo que se ha
  quedado fuera». Por qué: Reino Selva, «quita esas tomas falsas, no son buenas» (dos tropiezos leyendo el guion con un
  rótulo «TOMAS FALSAS» al final). (vídeo: vaciamos-estanque-2 v2)

## Planos de recurso (sobre la voz)
- 2026-11-11 — **Un recurso tiene que enseñar aquello de lo que se habla desde su primer fotograma.** Nada de paredes,
  barridos de cámara, arranques de plano ni el sujeto diminuto. Por qué: «elige los planos de recurso con criterio» (en
  la v2 había recursos donde solo se veía pared). (ramon v2 → v3)
- 2026-11-15 — **Paredes: tampoco en el plano PRINCIPAL.** Cuando quien graba cambia de sitio, de ángulo o de foco
  (se acerca al acuario, le pasa la cámara, se moja el micro, va a por algo) el plano principal se queda en pared,
  techo, suelo, un barrido o pegado al cuerpo mientras sigue sonando la voz. Eso no se deja nunca. Después de
  `paso3_plan.py`, **`planos_vacios.py`**: lista los planos principales sin cara que el registro visual describe así,
  con lo que se dice encima, y hace `trabajo/vacios.jpg`. Cada uno se decide mirando la hoja:
  - no se dice nada que importe (reencuadres, «ahora sí», el micro mojado, «no sé si va») → **fuera del EDL**;
  - se dice algo → **`BROLL` de aquello de lo que habla** («esto se está muriendo» → la planta que se muere; «se fue»,
    «mira el medaka» → el pez; «estaba aquí» → donde estaba), de los mismos brutos (`mejores_recursos`, otra cámara)
    o del archivo del creador; si no hay nada de eso, un plano bonito del sitio;
  - **«mira X» y X está grabado en algún bruto** (otra cámara, la subacuática, otro momento) → ese plano, aunque el
    principal valga;
  - es un desplazamiento con sentido (va al cuadro eléctrico) → se queda, corto y sin zoom;
  - **el reencuadre al coger la cámara** (entre dos frases: él coge la cámara, se ve la pared, vuelve a encuadrar) se
    corta, aunque eso parta la pieza en dos.
  Lo que se deje a propósito (él trabajando de espaldas: hay acción) se apunta en `VACIOS_OK` de `plan.py`.
  Por qué: Lucas, prueba-3 v2: siete de sus diez correcciones eran esto («se ve la pared», «pon un plano de lo que se
  muere», «pon el medaka o algo relacionado, de los brutos o de los recursos», «poner recursos de la várzea o algún
  plano»). (vídeo: prueba-3)
- **Antes de montar, registro visual de TODOS los brutos** (qué se ve en cada segundo): hojas densas del paso 0 + un
  agente por bruto con `herramientas/montaje/ENCARGO_REGISTRO_VISUAL.md`, **hasta 4–5 a la vez en Mac** (de dos en dos
  en Windows con 16 GB de RAM). Sin
  registro no se eligen recursos. Por qué: «estudia a fondo los brutos».
- Se eligen de `mejores_recursos` del registro, **se miran** (`tira.py`) y, con el plan hecho, **se revisan todos** con
  `hoja_recursos.py` antes de renderizar. Si el sujeto queda pequeño, zoom al sujeto; si no hay imagen de algo que se
  nombra, **no se inventa**: se queda el plano a cámara (con texto o zoom) y se le dice al creador qué falta (foto de
  banco, grabación suya).
- Duración 1,5–4 s; si pasa de ~3 s, corte de escala a la mitad. No se repite un tramo en el mismo vídeo.
- 2026-11-17 — **Ningún trozo de bruto sale dos veces, y un recurso de la MISMA toma que la frase que tapa no es un
  recurso.** La regla de arriba («no se repite un tramo») no la medía nada y en alimentacion v1 había 31 repeticiones:
  Lucas vio dos («22:55–23:03 repites el mismo clip dos veces», «se repite el clip de la terrapene en la intro»). Tres
  causas, las tres arregladas en las herramientas:
  1. recursos sacados del mismo bruto unos segundos antes o después de la frase (el «mejor recurso» del registro está
     en la misma toma en que habla): el recurso enseña algo que el plano principal vuelve a enseñar enseguida. Si lo que
     se quiere enseñar es justo lo que pasa mientras habla, no hace falta recurso: se deja el principal (o un zoom);
  2. un `V(…)` de acción elegido por el registro visual que se solapaba con la frase de después (la pista de `T(…)` es
     de Whisper, que puede ir 7 s desfasado: la frase empezaba en 95,9 s y el V iba de 97,5 a 102);
  3. la alineación forzada «se comía» hacia atrás las últimas palabras de la pieza anterior del EDL (`paso1_alinear.py`
     ya no deja que una pieza empiece antes de donde acaba, montada, la palabra que la precede).
  `paso3_plan.py` se para con `REPETIDO` (y propone el tramo libre más cercano del mismo bruto, que se mira con
  `tira.py`); lo repetido a propósito va en `REPETIR_OK`. El tráiler puede repetir planos del cuerpo (sale de él), pero
  no repetirse a sí mismo. Al quitar un recurso, `planos_vacios.py` otra vez: lo que tapaba puede ser una pared. (vídeo: alimentacion)
- 2026-11-17 — **El corte de escala de un recurso largo va hacia el SUJETO, no al centro.** Un recurso de más de 3,2 s se
  parte en ×1,0 → ×1,25; si el sujeto no está en el centro (la tortuga abajo, en las manos), el ×1,25 lo saca de cuadro o
  lo deja donde caen los rótulos. En `BROLL`, `(None, cx, cy)` lleva el ×1,25 hacia ese punto. Por qué: Lucas, «el zoom a
  lo mejor un poco más centrado en la tortuga». (vídeo: alimentacion)
- 2026-11-17 — **Un gesto que se hace callado se enseña, más cerca y con su sonido, y la frase siguiente entra por encima.**
  Un silencio de un par de segundos dentro de lo hablado (echa el agua, coloca el plato) no se tapa con un recurso mudo
  de otra cosa: se corta, o se enseña el gesto con zoom (`BROLL` del mismo instante con `(zoom, cx, cy)`, que sustituye
  al principal sin repetirlo) mientras empieza la frase de después. Por qué: Lucas, «en el 1:50… hay como un segundo
  muerto en el que pone el agua y está muteado el audio, yo pondría como pone el agua algo zoomeado y el principio de lo
  que dice después por encima». **Causa:** el EDL se lee como texto: el silencio no estaba en ninguna parte. Ahora
  `comprobar_voz.py` lista los `HUECO`. (vídeo: alimentacion)
- 2026-11-12 — **Lo que se nombra y no está en los brutos del día se tapa con archivo, cuando lo haya.** El pasado
  («cuando empezamos a construir…»), otra época del año, una especie, un sitio, una planta: si en sus `recursos/` hay un
  clip clasificado de eso, va sobre su voz en el momento en que lo nombra (1,5–4 s, como cualquier recurso), aunque
  haya plano a cámara que valga. Da ritmo y enseña lo que se cuenta. Cómo se busca y qué hacer si no lo hay:
  `base/recursos.md` § 5. Por qué: Lucas, «habla del pasado de cuando empezaron la construcción…, de los peces, de
  la várzea, de plantas… en un futuro en recursos habrá vídeos de todo eso clasificados, para que puedas ir poniendo
  planos de vez en cuando cuando los menciona, con su voz de fondo, para que sea también más dinámico». (vídeo: ramon)
- 2026-11-13 — **Todo recurso es de un creador**: sus fijos, sus clips de archivo y b-roll, fotos, mapas y música van
  en `personal/<creador>/recursos/`, **ordenados por carpetas de tema como en `edicion-reels`** (nada suelto, todo con
  ficha en su `INDICE.md`); no hay `recursos/` en la raíz. Por qué: Lucas, «los recursos tienen que ir ligados a la
  personalización; recursos estará dentro del perfil de creador» y «se tienen que ordenar por carpetas como hacíamos
  en los recursos de la skill de reels».
- Material de `personal/<creador>/recursos/`: cómo catalogarlo y elegirlo, en `base/recursos.md`. Los recursos fijos del
  creador (cabecera, cortinillas, logos) y cuándo van: `personal/<creador>/recursos.md`.
- 2026-11-19 — **Si el creador lee** (teleprompter o notas: `mirada: fuera_lee` en el registro visual durante frases
  seguidas), **su plano no se queda**, aunque la voz sea buena. Por orden:
  1. la otra cámara, si en ella mira al objetivo, SINCRONIZADA (`@sync`, abajo);
  2. recursos de lo que nombra, uno por frase, empezando en la palabra que lo nombra (o lo que hace: «se lanzan sobre
     sus presas» → el martín pescador lanzándose);
  3. si no hay, stock de lo que nombra (`base/recursos.md` § 5 bis), de la especie exacta.
  Una ficha gráfica encima no basta: debajo sigue viéndose que lee. Por qué: Reino Selva, «4:04 - 6:40: no miro a
  cámara, porque estoy leyendo teleprompter, usar shutterstock sobre los distintos pájaros» y «10:53: intenta pillar
  tomas de la otra cámara con el audio de la otra cámara». El registro visual decía «mira fuera de cámara» y no se usó.
  (vídeo: vaciamos-estanque-2 v2)
- 2026-11-19 — **Un plano de otra cámara sobre la voz se saca del MISMO instante**: el desfase se mide por correlación
  del audio (`sincro.py <clip voz> <clip otra>` → `SINCRO` en `proyecto.py`) y el plano se pide con
  `(ancla, "@sync:<clip>", duración | None, zoom)` en `BROLL`: el segundo sale del montaje y no pasa del final de la
  pieza de voz. Nunca de otra toma de la misma frase ni a ojo; `paso3_plan.py` avisa con `AVISO LABIOS` de los que no
  cuadran. Si no hay toma sincronizable, que no se le vean los labios (plano de lejos o de espaldas). La voz sigue siendo
  la del micro bueno; solo cambia la imagen. Por qué: Reino Selva, «11:34 hay lag con mi voz y mis labios» (la Sony
  puesta a ojo iba 0,47 s adelantada; otros dos planos eran de otra toma de la misma frase). (vídeo: vaciamos-estanque-2 v2)
- 2026-11-19 — **Cada `AVISO ANCLA` de `paso3_plan.py` se mira**: ¿el minuto elegido es el de la escaleta? Una frase
  corta casi siempre está dentro de otra y las frases del tráiler suenan dos veces (`n=0` es la del tráiler, `-1` la del
  cuerpo). Tras `paso3`, comprueba con `ver.py` en el minuto real cada recurso que nombra algo concreto. Por qué (lo vi
  al revisar el archivo, antes de entregar): la garza salía bajo la ficha del cormorán porque «es un ave grande»
  casaba antes con «el cormorán es un ave grande»; el plano de la garza con el koi caía en el tráiler; y un
  `VOZ_DISFRAZ` con «un mes», n=0, disfrazó al creador en vez de a quien grababa (era n=1). (vídeo: vaciamos-estanque-2)

## Textos y gráficos
- 2026-11-11 — **Guía: Plex y Xokas.** Una familia ancha y negra para lo grande; entran de golpe (pop en 5–6 f) y salen
  por corte; pocos y con función. Tipos de serie (`estudio/src/comun/Graficos.tsx`): título, capítulo (título y subtítulo, sin «n/total» ni casillas: Lucas, 2026-11-24; `CONTADOR_CAPITULOS = True` lo vuelve a poner), cifra
  junto a la cara, palabra-golpe, nota del editor, rótulo con seguimiento, subtítulo. La suscripción no es un rótulo:
  es un botón animado (abajo, «Clips y gráficos superpuestos»).
- 2026-11-11 — **Texto que crece: zoom continuo y suave, nunca a escalones.** Pop de entrada y luego ×1 → ×1,22 con
  frenada. Por qué: «se zumea a trozos, no es suave». (ramon v2)
  - 2026-11-14 — **La escala de un texto nunca baja: ni rebote al entrar ni pasarse de tamaño.** El pop de entrada va de
    ×0,86 a ×1 frenando hasta parar (`pop()` en `Graficos.tsx`) y por encima solo sigue el crecimiento continuo. Por qué:
    Lucas, «los textos grandes aún parece que rebotan un poco al aparecer: aparecen, se encogen un poco y luego se
    zoomean». Causa: el pop antiguo (×0,8 → ×1,06 → ×1) se multiplicaba por el crecimiento, que en esos 6 fotogramas sube
    un 1 %: el texto se encogía un 5 % justo después de aparecer. Al arreglar lo de los escalones se miró el crecimiento y
    no la entrada. Cualquier animación de escala nueva (también en los gráficos de un creador): monótona. (vídeo: 1311)
- 2026-11-15 — **Ningún texto de relleno: cada rótulo tiene que añadir algo.** Se rotula una idea clave, un dato, una
  especie, un nombre, una frase con gracia o con fuerza. **No** se rotula una acción trivial que ya se ve y se oye
  («FUERA CALCETINES» mientras se los quita, «VAMOS ALLÁ», «A PLANTAR»): no aporta y le quita peso a los rótulos que sí
  importan. El % de tiempo con texto y los «huecos sin texto» del CONTEXTO son una alarma para buscar qué rotular,
  **nunca** una cuota: si en un hueco no hay nada que merezca texto, se llena con recursos, zooms o archivo, no con
  un rótulo. Al repasar el plan, cada `R(…)` pasa la pregunta «¿qué sabe o siente quien lo ve que no sabría sin él?»;
  si la respuesta es nada, fuera.
  Por qué: Lucas, en la v3 de `1311`: «en el minuto 6:45 el texto "fuera calcetines" sobra». Causa: salió de la pasada
  de dinamismo de la v2, que buscaba frases para tapar huecos de 25–94 s sin texto: se rotuló por llenar el hueco, no
  porque la frase lo pidiera. (vídeo: 1311)
- 2026-11-17 — **Dos gráficos NUNCA se pisan.** Ni la tarjeta del capítulo con el rótulo de la especie que se nombra
  en su primera frase, ni un rótulo con una palabra-golpe, ni nada con nada. `paso3_plan.py` calcula dónde cae cada
  gráfico (`comun.caja_texto`) y se para con `PISA:` si dos coinciden en tiempo y sitio. Se arregla retrasando el
  segundo hasta que se va el primero (`("@s7", 3.4)`: después de la tarjeta), subiéndolo (`y`), llevándolo a un lado
  (`lado`) o quitándolo si repite lo que ya dice el otro (la tarjeta «Testudo marginata y Testudo graeca» y un rótulo
  con lo mismo). Por qué: Lucas, alimentacion v1, «en el punto 2/7 se solapan dos textos, esto no puede pasar nunca» y
  «21:56 vuelven a sobreponerse textos, NO PUEDE PASAR». **Causa:** herramienta y método. Solo se comprobaba el choque
  con el botón de suscribir; la tarjeta de capítulo la pone el motor y los rótulos el creador, y nadie los comparaba.
  En la v1 vi un solape (UROMASTYX sobre la tarjeta del 6), lo arreglé a mano y no busqué los demás: **cuando aparece un
  fallo, se busca en todo el vídeo y se arregla la causa, no el caso**. (vídeo: alimentacion)
- 2026-11-17 — **El rótulo con flecha (`TRK`) entra con SU plano, nunca sobre el recurso de antes, y la flecha señala
  al sujeto durante todo el tramo**: caja medida con `rejilla.py` en el primer fotograma de ese plano (no con el
  registro visual) y comprobada con `hoja_seguimiento.py` (8 fotogramas, el punto rojo sobre el sujeto en todos).
  `paso3_plan.py` ya recorta el rótulo si un recurso tapa el principio de su plano (y se para si lo tapa por medio),
  avisa si el punto se mueve demasiado para un sujeto pequeño, y el seguimiento ya no se va con lo que pasa por
  delante (una mano, alguien que cruza): se queda quieto y recupera al sujeto cuando vuelve a verse. Por qué: Reino
  (planto-estanque, 15:24), «el texto de un visitante sale antes de tiempo… empieza antes de poner el plano del
  pájaro… la flecha no está apuntando bien a este». **Causa:** el `TRK` sobre plano principal se colocaba en la línea de
  voz ANTES de pegar los recursos y nadie lo volvía a mirar (salía 1,07 s sobre el recurso del abono); la caja salió de
  las fracciones del registro visual, a 250 px del pájaro, y siguió a las hojas; `hoja_textos.py` enseña 2 fotogramas a
  640 px, donde no se ve. En alimentacion pasó lo mismo con «HIBISCUS»: un guante pasó por delante y la flecha se fue
  con la mano. (vídeos: planto-estanque, alimentacion)
- 2026-11-17 — **Ningún texto se sale del cuadro. Nunca.** Es de los errores más graves: se ve cortado y parece hecho
  sin mirar. En alimentacion v2 se cortaban por la derecha «ASTROCHELYS RADIATA» y «AGUA DE ÓSMOSIS» (y había otros 12
  rótulos con `lado` a punto). **Causa:** al llevar un rótulo a un lado (`lado="der"`) se centraba en el 72 % del ancho
  pero conservaba el tamaño pensado para ir centrado (70 % del ancho): con un nombre largo, la mitad sobresalía. La
  comprobación de solapes medía la caja con la misma cuenta equivocada y la hoja de textos dibuja una estimación, no el
  texto real, así que nada lo vio; y al moverlos de sitio en la v2 solo se miró que no taparan al sujeto. **Arreglo:**
  con `lado`, el rótulo va pegado a ese borde con un margen del 4 % y su tamaño es el que cabe en el 58 % del ancho
  (contando el crecimiento); las flechas cambian solas de lado si por el suyo no cabe el nombre; las cifras se meten
  dentro; y `paso3_plan.py` se para con `SE SALE` si una caja queda fuera. **Y al cambiar un texto de sitio, se mira con
  `ver.py` en su fotograma de máximo tamaño (el último), no solo con la hoja de textos.** Un gráfico propio nuevo de un
  creador tiene que seguir la misma regla (margen y tamaño que quepa) y su caja ir en `comun.caja_texto`. Por qué:
  Lucas, «aquí el texto se sale del vídeo, esto no puede pasar» y «los textos no se pueden salir de pantalla nunca, es
  un error muy grande». (vídeo: alimentacion)
- 2026-11-17 — **Un texto no tapa lo que se está enseñando en ese momento** (el animal comiendo, la tortuga en las manos,
  los platos, la rosa de la que habla). Se mira SIEMPRE con `hoja_textos.py` después de `paso3_plan.py`: cada texto
  sobre su plano, al entrar y al irse, con su caja dibujada. Si tapa: `lado`, `y` (rótulos y palabras-golpe:
  `{"y": 0.62}`), otro sitio para la mascota (`"lado": "izq"`), o —si el sujeto se mueve— un rótulo con FLECHA que lo
  sigue (`TRK`) en vez de un texto fijo («¡CAZADO! un caracol vivo» señalando la boca de la terrapene). Por qué: Lucas,
  «el texto tapa a la tortuga, que es el foco del clip… tiene que tener en cuenta que el texto no tape lo importante en
  el momento que aparece» y «"¡cazado!" tapa cómo come el caracol: ahí una flecha con el texto trackeando». **Causa:**
  método. La regla («nada tapa la cara ni el sujeto») ya estaba, pero había 46 rótulos y con `ver.py` (un fotograma
  cada vez, lento) solo miré las burbujas y los botones. La hoja los enseña todos en segundos; en la v2 salieron 18
  textos que tapaban algo y se movieron. (vídeo: alimentacion)
- 2026-11-17 — **Cuando el creador nombra varias cosas que se ven («flores de hibiscus, Mazuri y variado de lechugas»),
  una flecha con el nombre a cada una, que aparece cuando la dice.** Tres `TRK` con su segundo de entrada cada uno; las
  coordenadas, de `rejilla.py`. Lo mismo con un animal o personaje que se presenta y está en plano: su nombre con
  flecha (y su apodo si el creador tiene uno: `personal/<creador>/preferencias.md`). Por qué: Lucas, «lo ideal es que
  pongas una flecha con el nombre señalando a cada una de las 3 cosas que nombra… para que el espectador sepa qué es
  cada una» y «le ponía una flecha con el nombre para resaltarlo». **Causa:** el `TRK` se quedó sin usar en todo el vídeo
  porque había que calcular la caja a ojo; `rejilla.py` da las coordenadas en píxeles del lienzo. (vídeo: alimentacion)
- **Nunca un texto antes de que se diga.** Todo cuelga de anclas (frase o marca), no de frames a mano; compruébalo con
  `timing_textos.py` (abajo, «Timing de los textos») y con `ver.py` en el frame anterior y en el de la palabra.
- **Subtítulos solo donde se oye mal** (ruido, viento, voz lejana, otro idioma): abajo, una línea, 3–6 palabras, de
  golpe. Nunca continuos. Los tramos se proponen con la transcripción (palabras con poca confianza, frases que Whisper
  no entiende) y, como Claude no oye, **se confirman con el creador**.
- **Nombres, cifras y especies: literales.** Lo que no salga en la transcripción o no te lo haya dicho el creador
  (nombres científicos, datos) va marcado como pendiente de validar. Las **notas del editor** son propuestas: se le
  enseñan antes de darlas por buenas.
- Nada tapa la cara ni el sujeto. En los últimos 20 s deja libres las zonas de las tarjetas de YouTube si hay pantalla final.

### Timing de los textos (cuándo entra y cuándo se va cada uno)
- 2026-11-12 — **Cada texto entra EN su palabra, aguanta la frase que resume y sale con el corte.** Se mide, no se
  estima: después de `paso3_plan.py`, `timing_textos.py` (desde `out/<slug>/`) enseña cada texto frente a la voz (el
  desfase de cada palabra respecto a la entrada del texto) y a los planos que tiene debajo, con avisos. Se arregla en
  `plan.py` y se repite hasta que los avisos que queden sean a propósito.
  - **Entra en la palabra que escribe**, no al principio de la frase: el ancla es ESA palabra (`"siebenrocki"`, no
    `"the name is siebenrocki"`; `"iberian pond"`, no `"an iberian pond"`). Una décima no se nota; medio segundo antes,
    sí, y además le pisa el remate a quien habla. Un nombre que no se dice (el científico) entra con el nombre común.
  - **La segunda línea, cuando se dice.** Si la línea pequeña repite algo que él dice un par de segundos después
    («FLOODED» … «after very heavy rains»), entra con su propio retraso (en el rótulo de un creador, p. ej. `subEn`) y
    el texto aguanta hasta que acaba de decirlo. Si es solo el pie de un nombre (nombre común), entra con él.
  - **Aguanta la frase.** Si al irse el texto a la frase le quedan una, dos o tres palabras, se alarga hasta la pausa.
    Y no se va antes de que se diga algo que lleva escrito («…or a whole life» se iba justo al decir «life»).
  - 2026-11-14 — **Ningún texto se va antes de que se haya DICHO entero y se pueda leer.** Aguanta hasta 0,5 s después
    de su última palabra (o hasta la pausa) y nunca menos que el tiempo de leerlo: 0,6 s + 0,3 s por palabra, mínimo
    1,2 s. Lo hace solo `paso3_plan.py` (`comun.texto_dicho`: casa las palabras del texto con la voz, en orden) e
    imprime lo que alarga; `timing_textos.py` avisa con `CORTO` si el texto siguiente no le deja sitio. Por qué: Lucas,
    «aparecen en buen timing pero desaparecen antes de que la persona acabe de decirlo, por lo que no te da tiempo ni a
    leerlo». Causa: la duración de cada texto se ponía a ojo en `plan.py` (0,8–1,6 s para un golpe) y la comprobación
    solo miraba la entrada y si a la frase le quedaban 1–3 palabras, no si el propio texto ya se había dicho. En la v3
    de `1311` hubo que alargar 64 de los 103 textos (de +0,1 a +2 s). (vídeo: 1311)
  - **Con los cortes.** Un texto acaba en un corte o pisa el plano siguiente medio segundo o más; nunca 1–7 fotogramas
    de cola, ni se va 3 fotogramas antes del corte (esto lo ajusta solo `paso3_plan.py`). Y no se queda encima de un
    recurso que enseña OTRA cosa (los nombres de dos tortugas sobre un plano de obra): se acorta o se mueve el recurso.
  - **Cifra junto a la cara:** su plano corta en el número («three eggs per season»), no en la muletilla de antes
    («up to…»): el corte de escala en la cifra es el golpe.
  - **Comentario del editor: DESPUÉS de lo que comenta.** Es una reacción; si sale antes del remate, lo destripa
    («*humans: not thriving*» salía 0,9 s antes de que dijera «humans»).
  - **Gráficos que tardan en leerse** (una mascota que asoma y luego saca la burbuja): lo que tiene que caer en la
    palabra es el momento en que el texto SE LEE, no el arranque de la animación. En `plan.py`,
    `RETARDO_TEXTO = {"tipo": segundos}` para que la herramienta lo cuente.
  - **Tiempo de lectura:** como mucho 4 palabras por segundo en pantalla. Si no cabe, se acorta el texto; no se pone
    más rápido ni se alarga sobre otra idea.
  - **Un gráfico grande se mira en TODOS los planos que pisa:** los cortes de escala cambian el encuadre por debajo
    (una burbuja que con el plano general caía en el pecho, en el corte a ×1,45 le tapaba la boca).
  Por qué: Lucas, «aprovecha para revisar el timing de los textos, a ver si se puede mejorar un poco alguno», «al
  revisar textos, ¿has revisado también el timing de aparición de la tortuga que va apareciendo hablando?» y «el tema
  de los timings, aprende y apúntalo en la skill general». **Por qué fallaba:** cada texto se colgaba de la frase tal
  cual estaba copiada en el EDL (o sea, de su primera palabra), las duraciones se ponían a ojo y `ver.py` solo enseña
  un fotograma: nada medía el texto contra la voz ni contra los cortes. Y las burbujas las di por buenas sin medirlas
  hasta que preguntó. En `ramon` v6 se retocaron 36 de sus 49 textos: «IBERIAN POND» 0,6 s antes de la palabra,
  dos burbujas 2–3 s antes de nombrar al animal, cinco textos con 1–7 fotogramas de cola. (vídeo: ramon v6 → v7)

### Resaltar algo importante dentro del plano (foco)
- 2026-11-12 — **Cuando lo importante se pierde en el plano, se resalta**: todo el cuadro en **blanco y negro (y algo
  más oscuro) menos el sujeto**, que se queda en color dentro de una elipse de borde suave que lo sigue
  (`FOCOS` en `plan.py` + `herramientas/montaje/foco.py`), y/o un **rótulo con flecha** pegado a él (`TRK`). Sirve para
  cualquier cosa importante que el espectador no sabría dónde mirar: un animal pequeño haciendo algo, un detalle, un
  objeto, una persona entre varias, el resultado de algo. Referencia: la intro de «la isla de los monos» de Rubén
  Holgado (`refs/dinamicos/CONTEXTO.md` → gráficos con seguimiento).
  **Con criterio y sin abusar**: uno o dos por vídeo (tres en uno largo), 2–5 s cada uno, y solo donde de verdad no se
  ve; si el sujeto ya llena el plano o basta un corte de escala, no hace falta. Nunca sobre la cara del creador
  hablando, ni dos seguidos, ni como adorno.
  Receta: corte de escala hacia el sujeto (`BROLL` con zoom, partiendo el recurso en abierto → cerrado → abierto) +
  `FOCOS` durante el plano cerrado + `TRK` de 2–3 palabras si hay que decir qué pasa. Con `"en": ancla` el foco sale
  solo en ese plano (el mismo trozo de bruto suele estar también en el tráiler y en la ráfaga). Después de
  `paso3_plan.py`: `foco.py parches` y `foco.py hoja`, y **mira la hoja**: el sujeto entero y en color en todos los
  fotogramas. El color del sujeto no se toca (regla de COLOR): solo se apaga lo de alrededor.
  Por qué: Lucas, «se podría poner una flecha o algo que resalte un poco más al animal comiendo, o blanco y negro todo
  menos la tortuga comiendo… como la intro de Rubén Holgado de los monos (esto último se puede usar en la skill en
  general a lo mejor, con criterio y sin abusar)» y «eso del resalte es para resaltar cosas importantes en general a
  veces, no aplicado solo a una tortuga comiendo». (vídeo: ramon, v6)
- 2026-11-15 — **Lo pequeño que el creador enseña o nombra («mira las raíces»), con flecha (`TRK`).** Si lo que señala
  ocupa poco del cuadro o se confunde con el fondo, un rótulo de 1–2 palabras con flecha que lo sigue mientras habla
  de ello; el `FOCO` en B/N, si además se pierde entre más cosas. Se comprueba con `ver.py` que la flecha toca el
  sujeto en todo el plano. Por qué: Lucas, prueba-3 v2, «las raíces de la yuca: una flecha o un círculo para
  señalarlas». (vídeo: prueba-3)

### Clips y gráficos superpuestos (botones, mascotas, logos)
- 2026-11-12 — **Nunca se superpone un clip con su fondo, con halo del fondo o con objetos raros.** Los botones y las
  mascotas vienen sobre verde y los logos sobre un color liso: se les quita con `quitar_fondo.py` /
  `quitar_fondo_imagen.py` y se **mira** la hoja de prueba sobre oscuro y sobre claro. Las animaciones generadas traen
  sorpresas (en `ramon`, la tortuga botaba un balón a mitad del clip): mira una hoja con **todos** los fotogramas del
  tramo que vas a usar, no seis sueltos. Por qué: se vio en la prueba de render, no en la hoja de seis fotogramas.
- 2026-11-12 — Un gráfico superpuesto **no tapa la cara ni el sujeto y no pisa otro gráfico** (rótulo, cifra, mapa).
  Compruébalo con `ver.py` en dos momentos: por debajo hay cortes de escala y el encuadre cambia. Si tapa, al otro lado
  (`lado`), más pequeño (`tam`) o un segundo más tarde. Por qué: la burbuja tapaba la boca en un plano con la cara a la derecha.
- 2026-11-12 — **Pedir suscripción, me gusta o campana = botón ANIMADO de la skill, abajo en el CENTRO.** Siempre que
  el creador lo pide con la voz va uno de los 16 botones (`BOTONES` en `plan.py`; catálogo y encaje con la voz:
  `base/recursos.md` § 9), en su sitio de serie. Nunca a un lado, y nunca un texto o un botón dibujado en su lugar.
  Por qué: Lucas, «no seguiste la norma de suscribir, al final pone subscribe en texto en vez de usar lo que te dije» y
  «cuando se ponga suscribir, lo ponemos abajo en medio con las animaciones estas, no en un lado». (vídeo: ramon, v5)
- 2026-11-14 — **El botón de suscribir va solo en pantalla: ningún texto ni gráfico comparte tiempo con él.** El texto
  que caería encima se cuelga de después del botón (la repetición de su frase o la frase siguiente), o el botón se cuelga
  de otra frase. `paso3_plan.py` se para con `CHOQUE: …` si coinciden. Por qué: Lucas, en 8:51 de `prueba-3`, «se
  solapan el botón de suscribir y el texto de "soltar cable"». Causa: el botón se cuelga ~4 s antes de «suscribiros» y
  dura ~8 s, así que pisa la frase de después; el rótulo de esa frase («Soltar cable es mi deporte preferido») cayó
  dentro, los dos abajo en el centro, y nada comparaba los tiempos del botón con los de los textos. (vídeo: prueba-3)
- 2026-11-17 — **El botón de suscribir, a un tercio del ancho** (`esc` 0,34 de serie, antes 0,5). Por qué: Lucas, «en
  todos los vídeos… la animación de suscribirse es muy grande, hazla algo más pequeña». (vídeo: alimentacion)
- 2026-11-12 — **El texto de un botón o de una burbuja va en el idioma del vídeo.** Los 16 botones de serie están en
  español: en un vídeo en otro idioma va la versión traducida del botón (`herramientas/boton_idioma.py`; el 2 en inglés
  ya está), no el español ni un texto dibujado. Lo que afirme un texto añadido (un dato de la
  mascota, una nota del editor) tiene que ser **cierto** —se busca o se sabe, y se comprueba— y tiene que ver con **lo
  que se está diciendo en ese momento** o se acaba de decir, no con otra parte del vídeo. Por qué: Lucas, «tienen que
  ver con lo que habla en el momento que lo pone».

## Mapas
- 2026-11-11 — **Mapa de satélite animado** cuando se nombran regiones, países o rutas: la cámara vuela a la zona, el
  borde se dibuja, llega el relleno y salta la etiqueta; las regiones anteriores quedan encendidas más tenues. Nada de
  mapa vectorial plano con fundidos. Por qué: «la animación del mapa no me gusta» (v1) → el de satélite gustó y «va a la
  skill». Base con `herramientas/mapa_satelite.py` (NASA Blue Marble, dominio público) → `personal/<creador>/recursos/mapas/`; componente
  `estudio/src/comun/MapaSatelite.tsx`; ejemplo en `base/ejemplos/ramon/Capas.tsx`. 3–6 s, solo cuando sitúa.

## Audio
- **La voz del bruto es el audio.** Proceso mínimo: paso alto suave y ganancia; sin compresión fuerte ni reducción de
  ruido que la deje enlatada. Fundido de 8 ms en cada corte.
- **Mezcla final −14 LUFS integrados, pico real ≤ −1,5 dB**, en dos pasadas (`paso5_audio.py`). Mide el archivo final.
- 2026-11-11 — **Música solo cuando toca**, no cama continua: gancho + título + arranque, entrada de cada sección (rótulo
  + ~10–14 s), secuencias de planos sin voz, mapas, la frase emotiva y el cierre. Orientación: **30–40 % del vídeo,
  14–17 dB bajo la voz**, entrada rápida y salida de 3 s; en planos sin voz sube. Por qué: «no hace falta que la pongas
  en cada momento, solo cuando toque, a veces poniendo planos». (ramon v2)
- **La música la descarga el creador** de su banco con licencia y la deja en `personal/<creador>/recursos/musica/` (catálogo en
  `CATALOGO.md`). Claude no descarga nada de un banco sin confirmación pista a pista y **no puede escucharla**: elige por
  ficha (BPM, etiquetas) y lo dice; el creador confirma de oído.
- **Efectos de sonido «a veces»**: uno suave pegado a cada gráfico (título, capítulo, rótulo, mapa, cifra), nunca en cada
  corte. Se cambian o quitan con `SFX` en `plan.py` (un vídeo) o en `personal/<creador>/ajustes.py` (todos los del creador).
- 2026-11-14 — **Quien no quiere que se le reconozca (quien graba, un tercero que lo pide): voz disfrazada y fuera de
  imagen.** Su voz, en `VOZ_DISFRAZ = [(clip, "frase literal", n), …]` de `plan.py`: `paso5_audio.py` sube el tono de
  esas frases sin cambiar la duración (voz de pitufo; cuánto: `VOZ_DISFRAZ_TONO` en `ajustes.py`, 1,45 de serie). Su
  imagen: cara pixelada o el plano fuera; si solo asoma (una mano, un brazo), se tapa con un recurso. Para encontrarlo:
  el registro visual anota cada vez que asoma alguien que no es el creador, y la voz de quien graba se distingue por el
  texto (le pregunta, le pide cosas, el creador le contesta) y porque llega más baja y lejana al micro del creador.
  Claude no oye: al entregar se dice qué frases se han disfrazado y cuáles quedan en duda.
  **La herramienta es general; usarla o no es del creador**: solo se disfraza la voz de quien su `preferencias.md` lo
  pida (en Reino Selva, el cámara siempre). Sin `VOZ_DISFRAZ` en el plan no se toca ninguna voz.
  2026-11-15 — **Se escapan si se buscan solo por el texto.** Lo que dice quien graba se cuela también ENTRE las palabras
  de una pieza aunque no esté en el texto del EDL («pero no me metas», «¿qué ha pasado?»). Por eso: `voces.py` (desde
  `out/<slug>/`, tras `paso2_voz.py`) transcribe lo que suena en `voz.wav` y marca como candidata cada frase con otro
  tono (≥ 1,38 × el del creador; `TONO_OTRA`) y más baja (≤ −2,5 dB; `DB_OTRA`), diciendo cuáles faltan en
  `VOZ_DISFRAZ`; las candidatas se confirman por el sentido (¿le contesta, le habla de tú?). `paso5_audio.py` busca cada
  frase en lo que suena (bordes reales del audio, no los de la línea) y avisa con `AVISO VOZ:` de las candidatas que
  queden sin disfrazar. Por qué: Lucas, prueba-3 v2, «se te han escapado bastantes partes en las que habla el cámara y no
  le pones voz de pitufo». Por qué (lo primero): Lucas, «cuando
  habla el cámara (señor misterio) […] distorsiona un poco la voz para que no se le reconozca, puede ser como una voz de
  pitufo; […] no debe de salir en los vídeos, o se le pixela la cara o se elimina cuando salga». Quién es ese tercero,
  en `personal/<creador>/preferencias.md`. (vídeo: prueba-3)
  2026-11-19 — **`voces.py` no basta, y la otra voz puede ser MÁS GRAVE.** Ahora mira las dos direcciones (más aguda,
  `TONO_OTRA`; más grave, `TONO_GRAVE` ÷1,15 y al menos 6 dB más baja, `DB_GRAVE`) y lista aparte las DUDOSAS (≥ 12 dB
  por debajo del creador, `DB_LEJOS`; casi siempre él hablando bajo). Con una voz que sube y baja mucho salen frases del
  creador entre las candidatas (en alimentacion, 21): por eso además se lee `voz.json` entero buscando lo que dice la
  otra persona por el SENTIDO:
  - réplicas a lo que dice el creador;
  - frases de tú a tú («lo cuidaste»);
  - quejas de quien sostiene la cámara («me rompes el móvil», el perro le muerde);
  - comentarios del fondo.
  Las dudosas se preguntan. Cada línea `voz disfrazada` de `paso5_audio.py` dice lo que suena ahí: comprueba que es de la
  otra persona (si la frase suena dos veces, la `n` decide cuál se disfraza). Por qué: Reino Selva, «distorsionar voz de
  fondo pitufo», «voz pitufo en todo lo que dice la otra persona»: quien grababa iba a ~95 Hz, más grave que el creador
  (~116 Hz), y a −40/−51 dB; `voces.py` solo buscaba voces más agudas y encontró 1 de 5. (vídeo: vaciamos-estanque v2)
- 2026-11-19 — **Palabrotas.** Si el creador pide pitar una palabrota, se pitan TODAS las del vídeo, las suyas y las de
  quien graba, todas las veces que suenan: `palabrotas.py` (las del texto del EDL, listas para pegar) y, además,
  `trabajo/voz.json` leído buscándolas (lo que dice quien graba entre frases). Van todas en
  `PITIDOS = [(clip, "palabra", n), …]` de `plan.py` antes de renderizar: `paso5_audio.py` pone encima un pitido de
  1 kHz al nivel de la voz, de principio a fin de la palabra, sin clic. Se apunta en su `preferencias.md` para que en los
  siguientes vídeos se haga sin que lo pida. Por qué: Reino Selva, «digo "jodido" poner un pitido o algo en cada
  ocasión» y, en la corrección siguiente, «pita también los hostia y cojones y demás palabrotas»: se aplicó literal (solo
  «jodido») en vez de generalizar. (vídeo: vaciamos-estanque v2–v3)
- 2026-11-17 — **Un fail (se cae la cámara, se va la luz, se le cae algo) se marca: blanco y negro y la voz algo saturada,
  hasta que se recupera.** `FALLOS = [(ancla_inicio, ancla_fin)]` en `plan.py`: `paso4_render.py` pone ese tramo en
  blanco y negro y `paso5_audio.py` satura la voz (como una radio rota) con fundidos cortos; al volver («¡hemos
  vuelto!») recupera el color. Es un efecto pedido, no una corrección de color: fuera del fail el color no se toca.
  **Con subtítulos** (`SUBS`) de lo que se dice mientras dura: la voz saturada se entiende peor. Sin que pisen la
  palabra-golpe de la vuelta.
  Con criterio: uno o dos por vídeo, solo en un fallo de verdad. Por qué: Lucas, «en el 20:08 que se baja la cámara,
  puedes poner en blanco y negro y saturar un poco la voz porque es un fail, hasta el "hemos vuelto" que ya recupera
  color». (vídeo: alimentacion)
- Nunca huecos mudos: un plano sin voz lleva su sonido original bajo o música.
  - 2026-11-14 — **Ningún plano sin voz se queda sin música** (él andando, mirando, un recurso sin habla): los respiros
    de música entre ventanas solo caen donde se habla, y en todo rato de más de 1,5 s sin palabras la música sube
    (nivel `SINVOZ`). Lo hace solo `paso6_musica.py`: si un hueco de más de 1 s queda sin voz y sin música, adelanta la
    ventana siguiente (la canción nueva entra con el plano sin voz) o alarga la anterior, e imprime `puente: …`. Por qué:
    Lucas, en 1:46 de `1311` v2, «cuando dice "vámonos" hay un plano en el que sale caminando y no habla ni nada y no
    hay música; ponle música a eso». Causa: las ventanas acababan a −3,5/−4 s fijos de cada capítulo para dejar un
    respiro antes del rótulo, sin mirar si ahí se hablaba, y la subida «sin voz» solo se aplicaba a los recursos, no a
    un plano suyo en el que no habla. Pasaba en dos cambios de capítulo. (vídeo: 1311)

## Entrega
- **Horizontal 16:9, H.264, a la mejor resolución que haya en los brutos** (3840×2160, 2560×1440 o 1920×1080; nunca se
  amplía por encima del mejor bruto ni se entrega por debajo) y a los fps del bruto principal (Sony 25, iPhone 30). No
  se mezclan fps: el lienzo manda y lo demás se convierte.
- Salida: `out/AAAA-MM-DD_<slug>.mp4` (bt709, `faststart`) + línea en `out/REGISTRO.md`. Peso orientativo: 4K a calidad
  alta ≈ 350 MB/min; si el creador necesita menos, se recodifica al final, no se baja la calidad del montaje.
- **Antes de entregar**: duración y número de frames (ffprobe), color contra el bruto, sonoridad, y fotogramas del archivo
  final en cada gráfico y en cada plano de recurso. Di qué se ha comprobado y qué no (Claude no ve el movimiento ni oye).
- 2026-11-12 — **Matrículas: SIEMPRE difuminadas, y solo la matrícula.** Toda matrícula que se pueda leer en el
  vídeo final (coche aparcado al fondo incluido) se difumina con `herramientas/montaje/tapar.py` (`TAPAR` en
  `plan.py`): el borrón va **ajustado a la matrícula** fotograma a fotograma y no tapa nada más (ni el coche, ni lo que
  pase por delante: una mano, un retrovisor). Se buscan al hacer el registro visual y se comprueban en el archivo
  final. Por qué: Lucas, «las matrículas difuminadas siempre, y ajustado solo a la matrícula». Un rectángulo fijo
  grande no vale: tapaba el retrovisor y el brazo. (vídeo: ramon)
  - 2026-11-12 — **También cuando solo asoma una esquina.** Si alguien pasa por delante y la tapa casi entera, lo que
    asoma (la banda azul y la primera cifra) se lee igual y también va borroso; `tapar.py` lo hace con una segunda
    pasada (sigue lo que rodea a la matrícula y busca su esquina). **Se comprueba en el archivo final, a tamaño real y
    cada 2–3 fotogramas, en TODO el tramo en que el coche está en plano**, no solo donde la matrícula se ve entera: las
    entradas y salidas detrás de un hombro son donde falla. Por qué: Lucas preguntó «¿has ocultado la matrícula en el
    último vídeo?» y en la v7 asomaban la banda y el «1» durante 1,8 s (3:40–3:42). Causa del fallo: el seguimiento
    solo reconocía trozos grandes de la matrícula, la daba por tapada, y la hoja de comprobación enseñaba esos
    fotogramas en pequeño y con el recorte donde la matrícula había estado antes, así que se dieron por buenos sin
    verla. (vídeo: ramon)
  - 2026-11-14 — **Buscarlas: cualquier coche en una muestra = el plano entero a tamaño real.** Una muestra cada
    ~2,5 s en hoja pequeña no basta para saber si la matrícula se lee: con la cámara en movimiento el coche cruza el
    cuadro en menos de un segundo. Si en una muestra hay un coche (aunque sea un trozo, un techo, una rueda), se saca
    ese plano en el archivo, a tamaño real y fotograma a fotograma en la zona del coche. Por qué: en la v2 de `1311` la
    muestra cogía el todoterreno entrando, de techo, y en la hoja no se veía nada; 0,7 s después se leía la matrícula
    entera (se vio en el repaso final, y hubo que tapar y rehacer el tramo). Descubierto en el repaso; no lo pidió Lucas. (vídeo: 1311)
- 2026-11-19 — **Nadie reconocible al fondo sin permiso.** Cualquier persona que no sea el creador y no participe en el
  vídeo (un operario, alguien que pasa), aunque esté lejos o de espaldas o solo asome por un borde, se difumina todo el
  tiempo que esté en plano (`TAPAR_PERSONAS` en `plan.py` + `tapar_persona.py` y `tapar_persona.py hoja`; caja a mano en
  fotogramas clave cada 0,125 s, medida con `rejilla.py`), o se cambia el plano. Se miran TODAS las hojas
  `persona_N.jpg`. El registro visual las anota en `personas_fondo`. Un tercero que sí participa (habla con él, sale a
  propósito) es de la regla de abajo: se pregunta. Por qué: Reino Selva, «13:16 blur a la persona que sale de fondo, no
  puede saberse quien es»: un operario entre las plantas, 2,5 s detrás del creador; en el registro visual solo se habían
  anotado las personas en primer plano. (vídeo: vaciamos-estanque v2)
- **Avisa de lo que el creador debe decidir**: caras de terceros, menores, pantallas con datos, marcas. Eso no se tapa
  ni se publica por iniciativa propia.
- Con el vídeo, siempre, el **paquete de YouTube**: 5 parejas de título + miniatura para test A/B (cada una con su
  prompt para ChatGPT y su fotograma de referencia), descripción, capítulos y etiquetas, en el idioma del vídeo
  (`base/titulos-miniaturas.md`, `base/descripciones.md`).
- **No se sube nada a ningún sitio** (YouTube, nubes, repos) salvo que el creador lo pida en ese momento.
- Cierre y limpieza a los 30 días: `SKILL.md` § 2.

## Lecciones técnicas (para no repetirlas)
- **Render híbrido**: todo en Remotion a 4K tarda ×14 la duración; capas en Remotion + vídeo con ffmpeg, ×2,7 (medido en
  i7-13700HX, 16 GB). Por eso Remotion solo hace gráficos.
- **ffmpeg, zoom animado**: `crop` no actualiza `iw/ih` cuando `scale` cambia de tamaño en cada fotograma
  (`eval=frame`). El recorte se calcula con la misma expresión Z(t) que la escala, no con `iw`. Ya está en `filtro_zoom`.
- **NVENC** (`h264_nvenc`) acelera los tramos en Windows con NVIDIA; ffmpeg 8 exige controlador ≥ 610. `auto` lo prueba
  y, si no va, usa x264. No actualices controladores sin permiso. `videotoolbox` (macOS) está escrito pero sin probar:
  compara un tramo con x264 antes de fiarte.
- 2026-11-17 — **Durante TODA la edición hay un vigilante aparte, no solo en el render.** Al empezar el vídeo se lanza
  `vigilante.py` en segundo plano (y un cron de la sesión cada 10 min con `vigilante.py estado`). Cada 10 minutos: cierra
  lo que lleve 10 min vivo sin gastar CPU (Remotion, esbuild, ffmpeg, un paso de `herramientas/` colgado) con todo lo que
  cuelga de él, relanza el render si se ha muerto o colgado (`render_todo.py` deja `trabajo/render_pedido.json`; como
  mucho 3 veces) y libera memoria (navegadores de Remotion y servicios de esbuild huérfanos; en Windows con poca memoria,
  recorta lo que no es de la edición). Nunca cierra nada del usuario ni toca un render que avanza. Por qué: Lucas, «sobre
  el parón de casi 3 h, quiero que cuando estés editando un vídeo haya un agente que cada 10 min revise si hay algún
  proceso parado y lo relance… y de paso, que libere algo de RAM». **Causa del parón:** una orden de Remotion lanzada en
  PRIMER PLANO se colgó (el servicio de esbuild se quedó con la salida abierta) y la herramienta Bash esperó 2 h 40 min;
  con la sesión ocupada no salta ningún cron, y la vigilancia que había (`vigilar_render.py`) solo existía durante el
  render. Por eso el vigilante es un proceso aparte: al cerrar lo colgado, la orden vuelve y la sesión sigue sola. Y
  además: **toda orden que pueda tardar o quedarse esperando (Remotion, render, transcripción) va en segundo plano o con
  tope de tiempo** (`ver.py` corta a los 4 min). Al encontrarlo había un navegador de Remotion huérfano desde hacía 4 h 30.
  `vigilar_render.py` sigue valiendo para una pasada a mano (memoria y estado del render).
  **«Colgado» se mide proceso a proceso, nunca con la suma del grupo** (el mismo día, en la primera prueba, el vigilante
  cerró el render BUENO en el tramo 46: el render lanza un ffmpeg nuevo por tramo y, al acabar uno y empezar otro, la
  CPU sumada del grupo BAJA aunque avance). Ahora cuenta la CPU gastada por cada proceso desde la pasada anterior (uno
  nuevo cuenta entero) y, si es el render, que su registro se haya movido en los últimos 10 min. Lo relanzó solo y
  retomó donde iba (2 min perdidos), pero un vigilante que mata lo que funciona es peor que no tenerlo: **un cambio en
  el vigilante se prueba con `vigilante.py estado` contra un render en marcha antes de dejarlo actuar.**
- **Filtros largos**: pásalos por archivo (`-/filter_complex archivo`), no por la línea de comandos (límite de Windows).
- **`-nostdin`** en todo ffmpeg lanzado desde un bucle o un script.
- **Git Bash en Windows**: un comando con un heredoc largo puede fallar («unexpected EOF»): escribe el script o el
  documento en un archivo. Rutas con `/`. Python: `herramientas/.venv/Scripts/python.exe` (macOS: `.venv/bin/python`).
- **Listas de archivos** (`VIDEOS.txt`, `SKILLS.txt`): se leen quitando el retorno de carro (`tr -d '\r'`); la skill fija
  `eol=lf` en `.gitattributes`.
- **`drawtext` de ffmpeg** no vale para rótulos (sin fuentes de marca, escapes frágiles): los textos van en Remotion.
- **Música en casi todo el vídeo** (creadores que la llevan seguida): una ventana por capítulo; si la ventana es más
  larga que la canción, `paso6_musica.py` vuelve al compás 8 con un cruce de medio segundo. La base sigue siendo «solo
  donde toca»; la música seguida es una preferencia de creador (`personal/<creador>/preferencias.md`).
- **Vídeo con transparencia en Remotion**: `.webm` VP9 `yuva420p` con `<OffthreadVideo transparent>` (componente `Clip`
  de `Graficos.tsx`); comprobado en el render de capas ProRes 4444. Para leerlo con ffmpeg hay que forzar
  `-c:v libvpx-vp9` antes de `-i` (el decodificador nativo pierde el alfa).
- 2026-11-16 — **Registro visual en Mac: hasta 4–5 agentes en paralelo**, no de dos en dos. Por qué: Lucas, «el
  registro visual en mac se puede hacer con más de dos agentes en paralelo, hasta 4-5». El de dos en dos queda para
  Windows con 16 GB. En Mac, mira la memoria libre antes de la tanda (`memory_pressure`) y baja si va justa.
- **16 GB de RAM (Windows)**: agentes de dos en dos; no lances demucs, whisper y un render a la vez. Si el sistema mata un proceso
  en segundo plano por memoria, no lo relances sin preguntar.
- **Claude in Chrome**: si hay varios navegadores conectados, elige el del equipo del creador antes de abrir pestañas.
- MapLibre dentro de Remotion no cargó en render (timeout de `delayRender`): mapas con imagen estática + SVG.
- 2026-11-19 — **`paso3_plan.py && render_todo.py …`, nunca con `;`.** Si paso3 se para, no se renderiza. Por qué: paso3
  se paró con `REPETIDO` sin reescribir `video.json` y `render_todo.py`, encadenado con `;`, empezó a renderizar el plan
  anterior. Ahora `render_todo.py` se niega si `plan.py` o `edl.py` son más nuevos que `trabajo/video.json`.
  (vídeo: vaciamos-estanque)
- 2026-11-19 — **Retoques: `rehacer.py guardar` antes de paso3 y `rehacer.py borrar` después**, y `render_todo.py` con
  una salida nueva (`_v2`): solo se rehacen los tramos y las capas que cambian. Lo que no ve (parches de `tapar.py`,
  `tapar_persona.py` o `foco.py` rehechos; un `.tsx` cambiado) se borra a mano.
- 2026-11-19 — **Recursos de stock que no son 16:9** (DCI 4096×2160, verticales): el render los recorta al centro a 16:9
  antes de escalar (`dinamica.RECORTE_169`; antes se deformaban) y `hoja_recursos.py` avisa con `AVISO PROPORCIÓN`. En
  un vertical el centro casi nunca es el sujeto: copia `_h` recortada a mano a su altura
  (`ffmpeg -i in.mp4 -vf "crop=2160:1215:0:Y,scale=3840:2160:flags=lanczos,format=yuv420p" -c:v libx264 -crf 16 -an in_h.mp4`).
- 2026-11-19 — **El botón de suscribir acaba mientras él habla** (`AVISO BOTÓN` en `paso3_plan.py`): si no, su final
  (el cuadrado rojo recogiéndose) se ve sobre lo que viene después de la voz (un negro, el outro, un clip sin voz). Se arregla subiendo `"vel"` en `BOTONES` (1,45 lo dejó en 7,0 s) o adelantando
  su ancla. (vídeo: vaciamos-estanque)

## Lo que funciona (aprobado)
- 2026-11-11 — El mapa de satélite animado de `ramon` («va a la skill»).
- 2026-11-12 — Primer visto bueno de Lucas a la base de edición tras `ramon` v3.
