# Propuestas para la base, sacadas del estudio de reto

Borrador (2026-11-24). Sale de las 7 referencias de `reto.md` (ids y fichas, allí). Aquí solo lo que valdría para
CUALQUIER vídeo, no solo retos. Cada punto: lo medido, cuántas referencias lo hacen, lo que hace hoy la base y la
propuesta. Todo es **A decidir (Lucas/Mac)**: nada de esto está aplicado.

## Para cualquier vídeo

### 1. Silencio de música como remate, con vuelta en el corte
- **Medido**: la música se corta en seco 0,5–5 s justo antes del remate o la frase clave, la frase va con sonido directo
  y la música vuelve con un golpe en el fotograma del corte siguiente. **7 de 7.** Frecuencia 0,4–2,3 por minuto
  (mrbeast-extremos 2,3; jjw-rhea 1,7; jjw-diamond 1,1 de ≥ 2 s; plex-30d 0,73; mrbeast-trap 0,68; fezz-21 0,39;
  plex-7d 0,37). Ejemplos: mrbeast-trap 0:05.2–0:06.90; jjw-diamond 3:56–3:59.75; plex-30d 8:43.0–8:46.9.
- **Base hoy**: `CONTEXTO.md` §2.4 dice que la música «se quita a propósito» en lo serio y en los chistes, sin cifra.
  `paso6_musica.py` trabaja por ventanas con fundidos; no hay forma de cortar 1–3 s en seco y volver en un corte.
- **Propuesta**: una marca en el plan («hueco» en una frase) que corte la música en seco N décimas antes y la devuelva en
  el corte siguiente. Objetivo: ≈ 1 por minuto en vídeo hablado.

### 2. El sonido va en la consecuencia, no en la entrada
- **Medido**: los marcadores, listas, contadores y subtítulos entran mudos (**5 de 7**); suena lo que cambia: casilla
  marcada (jjw-rhea, 12 dings a −11/−22 dB respecto a la voz), vida perdida (jjw-diamond 11:02.80), plaza conseguida
  (mrbeast-trap 9:25.70). Un sonido fijo por tipo de gráfico (**4 de 7**). SFX totales 0–1,45/min (mediana 0,85).
- **Base hoy**: `paso5_audio.py` pone un efecto a cada gráfico al entrar (`dato` pop, `trk` pop, `golpe` whoosh,
  `seccion` whoosh…). `CONTEXTO.md` §2.8: RH 3–5/min estimado.
- **Propuesta**: en la base, `dato` y `trk` mudos por defecto y el efecto en el instante del cambio (campo `snd` del
  ítem, que ya existe). Mantener un sonido por tipo. Riesgo: Reino Selva se edita con la base; revisar con su perfil.

### 3. Material fuera de su sitio, siempre marcado
- **Medido**: todo plano que no es de ese momento lleva etiqueta o marco: «COMING UP:» con viñeta, «EARLIER…» desaturado
  con la música cortada, archivo ajeno dentro de una página de YouTube, recuerdo en B/N entre dos destellos. **4 de 7**
  (jjw-diamond, jjw-rhea, mrbeast-extremos, mrbeast-trap).
- **Base hoy**: nada. `CONTEXTO.md` §4 recoge «LATER IN THIS VIDEO» y «PREVIOUSLY» de Paul Cuffaro, sin regla.
- **Propuesta**: regla de la base: un adelanto o un recuerdo nunca se cuela sin marca. Componente Remotion de etiqueta
  de esquina (adelanto) y filtro B/N + etiqueta (recuerdo).

### 4. El destello blanco puntúa gráficos y no cuenta como transición
- **Medido**: destellos a blanco de 4–8 f para entrar o salir de un gráfico, un mapa o un recuerdo; nunca dentro de la
  acción. **5 de 7** (mrbeast-trap 43, ninguno en juego; jjw-rhea ≈ 30; fezz-21 15 en el sorteo; mrbeast-extremos y
  jjw-diamond en la intro). El cuerpo sigue a corte seco (≈ 95–97 %).
- **Base hoy**: `CONTEXTO.md` §2.2, «≤ 5 transiciones construidas por vídeo».
- **Propuesta**: aclarar que el tope de 5 es para transiciones entre escenas; los destellos que puntúan gráficos van aparte.

### 5. Se alarga la espera, no el golpe
- **Medido**: antes del momento clave, 1,4–9,6 s sin voz (y a veces sin música); el resultado se enseña en < 1 s o se
  repite desde 4–5 ángulos. **4 de 7** (mrbeast-trap 29:56.0–30:05.6; fezz-21 17:00.2–17:03.8; jjw-diamond 18:39–18:44.15;
  mrbeast-extremos 12:56.0–12:59.0). En el pico se habla menos: **3 de 7** (mrbeast-extremos 120–144 palabras/min
  frente a 187; mrbeast-trap 45 frente a 166–203).
- **Base hoy**: `CONTEXTO.md` §2.5, «los momentos fuertes se sostienen en plano largo (20–85 s)».
- **Propuesta**: sustituir por «la preparación se sostiene; el golpe es corto». Choca con «nunca un plano sin voz sin
  música» (`MUSICA_HUECO_MAX` 1,0): permitir el vacío solo justo antes de un golpe marcado. A decidir.

### 6. Un gráfico en capa puede cruzar cortes
- **Medido**: la lista, el contador o el subtítulo se quedan quietos sobre 1–3 cortes y el montaje de debajo no se
  frena. **4 de 7** (jjw-rhea 18:50.0, 3,0 s sobre 3 planos; fezz-21 contador sobre los insertos; mrbeast-extremos
  subtítulos que cruzan 12:33.7; mrbeast-trap contador fijo).
- **Base hoy**: `timing_textos.py` hace que el texto «salga con el corte» (memoria: «Timing de textos, medido»).
- **Propuesta**: excepción para piezas de estado (contador, lista, marcador): pueden cruzar cortes si no se mueven.

### 7. Elipsis con un número que salta
- **Medido**: el tiempo quitado se ve en una cifra que salta en el corte (contador de repeticiones, reloj, km), sin
  cámara rápida ni rótulo de «X después». **3 de 7** con contador (jjw-diamond 735 → 1.152 en 16 s, 5:36–5:52;
  fezz-21 3 → 21 en 5:32.5; jjw-rhea de 2 a 10 dentro de un destello). «X horas después»: **0 de 7**.
- **Base hoy**: `CONTEXTO.md` §4, «elipsis por corte seco al paso ya hecho» (Paul Cuffaro).
- **Propuesta**: añadir la variante: si hay algo que se cuenta, el número que salta es la elipsis.

### 8. Una plantilla por función, siempre igual
- **Medido**: cada tipo de gráfico tiene una plantilla, una esquina y un sonido, y no cambia en todo el vídeo. **4 de 7**
  lo llevan al extremo (jjw-rhea 3 plantillas, 49 apariciones; plex-7d 13 paneles de 3 tipos con 3 sonidos;
  mrbeast-trap; fezz-21 con 4 ingredientes para 18 tipos).
- **Base hoy**: `Graficos.tsx` tiene piezas (`Titulo`, `Dato`, `Golpe`, `Sub`, `Clip`), sin regla de sistema.
- **Propuesta**: regla corta en la base: el mismo gráfico para la misma función, misma esquina, mismo sonido.

### 9. Marcador de progreso más frecuente
- **Medido**: una actualización de estado cada 48–70 s. **4 de 7** (mrbeast-trap 48 s de media; mrbeast-extremos 49 s
  de mediana; jjw-rhea 54 s; jjw-diamond ≈ 55 s).
- **Base hoy**: `CONTEXTO.md` §3, RH: lista o mapa de niveles cada ≈ 2,5 min.
- **Propuesta**: para vídeos con progreso (viaje, entreno, reto), objetivo de 1–2 min entre actualizaciones, cada una
  disparada por la frase que da la cifra. En vlog puro puede no aplicar: A decidir.

## Solo de reto (no proponer a la base)

- Ritmo de 20–34 cortes/min y plano mediano de 2,0 s (depende de multicámara y del número de participantes).
- Voz − música 9–12 dB y música el 75–100 % del vídeo.
- Intro explicativa de 21–108 s sin cabecera.
- Contador fijo, vidas, X de eliminado, códigos de color de equipo, cartela VS, ráfaga de reparto.
- Subida (riser) antes de cada disparo o resultado.
- Retirar el marcador en el último 23 %.
- Cuenta atrás con pitido por cifra.

## Lo que ya coincide con la base (no cambia nada)

- Corte seco en el cuerpo (≈ 95–97 %), no montar a ritmo (19–39 % en pulso), subtítulos solo puntuales (7 de 7),
  `Z_SIN_CARA` 1,0 (6 de 7), `Z_FUERTE` ≈ ×1,6 (mediana), música desde el segundo 0 (7 de 7), habla desde el fotograma 0
  (7 de 7), nunca un plano sin voz sin música (7 de 7, con el matiz del punto 5), un plano por idea en la intro,
  rótulo con seguimiento pegado al sujeto, LUFS −14.
