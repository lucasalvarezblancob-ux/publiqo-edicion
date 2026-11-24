# Propuestas para la base, sacadas del estudio de vlog

Borrador (2026-11-24). Sale de las 15 referencias de `vlog.md` (ids y fichas, allí). Aquí solo lo que valdría para
CUALQUIER vídeo, no solo vlogs. Cada punto: lo medido, cuántas referencias lo hacen, lo que hace hoy la base y la
propuesta. Se compara con `PROPUESTAS_BASE_reto.md`: **[reto N]** = la misma propuesta sale también allí (confirmada por
dos estilos, 22 referencias en total: la más fuerte). Todo es **A decidir (Lucas/Mac)**: nada de esto está aplicado.

## Confirmadas por reto y vlog

### 1. Silencio de música como remate, con vuelta en el corte **[reto 1]**
- **Medido**: la música se quita en seco 0,7–6 s antes del remate o la revelación y vuelve de golpe en el corte siguiente.
  **8 de 15** (plex-gane 0,7 s, 3:25.57; nil-f1 1–3 s, 0:17.9 → 0:21.42; plex-viaje 5–6 s, 0:30–0:36; bycalitos 5,6 s,
  12:19.6–12:25.2; nil-tomorrowland 4,3 s, 0:27.0–0:31.3; plex-coche corte en seco al aparte B/N; alessio-vuelta;
  luisito). La música entra de golpe en un corte en **12 de 15**. Reto: 7 de 7.
- **Base hoy**: `CONTEXTO.md` §2.4, «se quita a propósito», sin cifra. `paso6_musica.py` funde 0,48 s de entrada y 3,0 s
  de salida (`ENT`, `SAL`); no corta en seco.
- **Propuesta**: la de reto (marca «hueco» en el plan) y además **entrada y salida en seco en un corte** como opción de
  ventana. En vlog, ≈ 0,3–1 por minuto (menos que en reto).

### 2. Suena lo que cuenta, no lo que entra **[reto 2]**
- **Medido**: zooms y punch-in mudos en **9 de 9** con punch (plex-gane 44 de 44). Textos, subtítulos y cartelas mudos en
  5 de 15 (Plex ×2, RH ×3). Suena el dinero (**7 de 7** que rotulan precios: caja o ding, −5 a −13 dB bajo la voz), el
  logro (rh-titanic, ding + destello verde) y el aparte (plex-viaje 13 de 13 efectos). SFX 0,16–2,1/min, mediana 0,48.
  Reto: 5 de 7 mudos, mediana 0,85/min.
- **Base hoy**: un efecto por gráfico al entrar (`paso5_audio.py`); `CONTEXTO.md` §2.8, RH 3–5/min.
- **Propuesta**: la de reto (`dato`, `trk`, `golpe` mudos por defecto; el efecto, con `snd`, en el instante del cambio),
  con una excepción nueva: **el dinero suena siempre**. Objetivo total ≈ 0,5–1/min, más en la intro. Riesgo, el mismo
  que en reto: Reino Selva se edita con la base.

### 3. Material fuera de su sitio, siempre marcado **[reto 3]**
- **Medido**: **6 de 15** (bycalitos look de recuerdo con aberración y viñeta; plex-coche media saturación con swell 5–10 f
  antes; luisito tarjeta de YouTube 9 veces; rh-hotel captura del reproductor 10:33; plex-viaje archivo con «To Be
  Continued»; alessio-capri captura del perfil al nombrar a alguien). Reto: 4 de 7.
- **Base hoy**: nada.
- **Propuesta**: la de reto. Añadir la variante «vídeo pasado del canal → tarjeta de reproductor» (3 de 15).

### 4. Un gráfico de información puede cruzar cortes **[reto 6]**
- **Medido**: **6 de 15** (alessio ×3, etiqueta «sitio | hora» 1,7–2,3 s sobre jump cuts; nil-tomorrowland tarjeta de datos
  sobre 3 cortes, 9:11.47; nil-restaurante cartela de pase sobre 1–2; rh-titanic barra de viaje 11–12 s). Reto: 4 de 7.
- **Base hoy**: `timing_textos.py` hace salir el texto con el corte.
- **Propuesta**: la de reto, ampliada: piezas de estado **y de situación** (lugar, hora, dato del sitio, barra de viaje)
  pueden cruzar cortes si no se mueven. Los textos de énfasis siguen saliendo con el corte.

### 5. Una plantilla por función, siempre igual **[reto 8]**
- **Medido**: **8 de 15** (alessio ×3 un solo rótulo para todo; nil-sagrada un fondo y un pie para 23 tarjetas;
  nil-restaurante un ding para todo dato; bycalitos un sistema temático y flash + whoosh 19 de 19; alessio-24h el mismo pop
  a −25 dBFS; plex-coche una familia, dos colores). Reto: 4 de 7.
- **Base hoy**: piezas en `Graficos.tsx`, sin regla.
- **Propuesta**: la de reto.

### 6. El destello corto puntúa gráficos y no cuenta como transición **[reto 4]**
- **Medido**: destello de 2 f para entrar o salir de un gráfico, un mapa o un cambio de plano en un montaje. **5 de 15**
  (bycalitos 19, con whoosh; luisito en el mapa 3:58.58; alessio-24h ≤ 4 dentro de montajes; alessio-vuelta y -capri en la
  cartela de día). Más corto que en reto (4–8 f). Corte seco en el cuerpo 93–99 %.
- **Base hoy**: `CONTEXTO.md` §2.2, ≤ 5 transiciones construidas.
- **Propuesta**: la de reto. Duración: 2–8 f según el estilo (vlog 2 f, reto 4–8 f).

### 7. Elipsis con un número, sin «X horas después» **[reto 7]**
- **Medido**: «X horas después» grande en **0 de 15** (reto 0 de 7). El tiempo se cuenta con una cifra: hora del día como
  rótulo (alessio ×3), cifra de tiempo en voz en off o en texto (rh-titanic «28 horas» 29:04; rh-hotel «10 horas»; rh-avispas
  «3 horas»), barra que se llena (rh-titanic 29:06–29:17). Cámara rápida 1 de 15 (nil-tomorrowland, 2022).
- **Base hoy**: `CONTEXTO.md` §4, corte seco al paso ya hecho.
- **Propuesta**: la de reto, con la variante «la cifra es de tiempo»: hora, horas de viaje, día.

## Solo de vlog, pero valdrían para cualquier vídeo

### 8. El punch vuelve siempre a ×1,0; nunca dos escalas seguidas
- **Medido**: **9 de 9** con punch (plex-gane: 13 cambios pequeños frente a 61 jump cuts y 44 golpes, «o mismo encuadre o
  golpe grande»). Reto: 4 de 4 con punch (está en `reto.py`, no en sus propuestas).
- **Base hoy**: `ESCALAS` = [1.0, 1.3, 1.0, 1.45, 1.15, 1.0, 1.35, 1.12, 1.5, 1.0, 1.25]: encadena 1.45 → 1.15 y
  1.35 → 1.12 → 1.5.
- **Propuesta**: intercalar 1.0 entre cada escala en la base (como `reto.py` y `vlog.py`). **13 de 13** referencias entre
  los dos estudios: es la más segura de todas.

### 9. Texto en el fotograma de su palabra, ± 2–3 f
- **Medido**: **11 de 15** lo miden (rh-avispas 0–2 f; nil-f1 ± 2 f, 8 de 8; nil-sagrada ± 3 f; rh-hotel 0–3 f antes;
  alessio-24h en el mismo fotograma).
- **Base hoy**: ya es la regla (`timing_textos.py`, memoria «Timing de textos, medido»). No cambia nada: **confirma** la
  regla con cifra. Propuesta: fijar la tolerancia en ± 3 f.

### 10. El clímax se prepara quitando la música 30–56 s antes
- **Medido**: **4 de 15** (rh-avispas 44 s, 12:39–13:23; rh-hotel ≈ 50 s; luisito 56 s, 24:08–25:04; alessio-vuelta 45 s
  antes de 7:36.35), con voz encima: no es un hueco sin voz. En el pico la música entra de golpe, a veces por encima de la
  voz (2 de 15). Reto no lo mide (allí la música es casi continua).
- **Base hoy**: nada.
- **Propuesta**: para vídeos con un clímax claro, ventana sin música de 30–45 s antes con la voz encima y entrada de golpe
  en el pico. No choca con «nunca un plano sin voz sin música» porque hay voz.

### 11. La promesa vuelve en el desenlace, con el mismo gráfico
- **Medido**: **6 de 15** (rh-avispas precios verdes 0:09.41 → «total: 2.750€» 22:51.0; nil-tomorrowland Garrix 0:25.0 →
  foto final; alessio-capri maletas 0:58 → 21:30; rh-hotel misión completada; rh-titanic misiones; alessio-24h). En reto es
  el marcador (no está en sus propuestas como tal).
- **Base hoy**: §2.1 habla de la intro, no del desenlace.
- **Propuesta**: si la intro promete algo con un gráfico, el desenlace lo cierra con ese mismo gráfico.

### 12. Mano que tapa el objetivo como elipsis
- **Medido**: **7 de 15** (nil-tomorrowland 7 en 21,7 s; rh-titanic 9:14.4, 20:36.4; bycalitos 18:07.4; luisito 3:26.1;
  plex-coche 5:50.17; alessio-vuelta; nil-f1). Va con swoosh o música nueva 0,2 s después (bycalitos).
- **Base hoy**: §2.2 la contaría como transición construida.
- **Propuesta**: no cuenta para el tope de 5 (como el destello, punto 6): es un gesto grabado.

### 13. El detector de cortes pierde el 15–35 % en selfie
- **Medido**: recuentos a ojo en 7 fichas (nil-restaurante ≈ 66 % visto; plex-viaje ×1,54; plex-coche 20 %; nil-sagrada
  hasta 43 % andando; bycalitos; luisito; rh-titanic de 16,9 a 19,9 cortes/min). Es método, no edición.
- **Base hoy**: `CONTEXTO.md` §1 da los números de RH del detector solo (14–17 cortes/min); con jump cuts serían ≈ 18–20.
- **Propuesta**: en el método de fichas, recuento a ojo de 2–3 minutos obligatorio para cortes/min; marcar en §1 que sus
  cifras son mínimos. Y en «Dinamismo medido en cada versión», medir la v2 con el mismo método que la v1.

## A decidir antes de proponer (chocan con preferencias de Lucas)

- **Huecos sin voz solo con el sonido del sitio** (4 de 15: nil-restaurante, plex-coche, luisito, nil-tomorrowland) frente
  a «nunca un plano sin voz sin música». Reto: 7 de 7 cumplen la regla. Con dos estilos, la excepción solo sale en vlog:
  si se acepta, va en `vlog.md`, no en la base.
- **Zoom lento sostenido sobre quien habla** (2 de 15) frente a la receta 5 de la base. Reto: Lucas lo dejó solo «hacia un
  remate» (decisión 3). Coinciden en que no es general: no se propone a la base.
- **Zoom de vaivén** (1 de 15, plex-viaje). Una sola referencia: no basta.
- **Texto que crece** (preferencia de Lucas) frente a texto quieto (nil-sagrada ×1,000–1,007; alessio, plex-coche). Ni vlog
  ni reto miden crecimiento continuo en el texto. No es propuesta: es una duda sobre la preferencia.

## No es para la base (se contradice con reto)

- **«Se alarga la espera, no el golpe» [reto 5]**: en vlog el pico se **sostiene** en plano largo (7 de 15: luisito 49,8 s;
  rh-avispas 57,5 s; nil-restaurante ≈ 10 s; plex-coche 34,5 s; plex-gane baja a 13 cortes/min). Lo que coincide es la
  preparación (punto 10). La base (§2.5, plano largo) vale para vlog; la propuesta de reto vale para reto. Que se quede
  cada una en su estilo.
- **Marcador de progreso más frecuente [reto 9]**: en vlog lo llevan 4 de 15. No para la base.

## Solo de vlog (no proponer a la base)

- Jump cut a la misma escala en selfie gran angular, sin zoom digital (6 de 15).
- Intro explicativa cuando hay un sitio que justificar (5 de 11 viajes).
- Música el 51 % del vídeo, 12,5 dB bajo la voz; sin voz, a nivel de la voz.
- Montaje de llegada sin voz de 2–18 s (7 de 11 viajes), separador de zona, rótulo de parada, mapas, precios con
  conversión doble, cartela de salto de día.
- Voz en off (solo RH, 14–16 %).

## Lo que ya coincide con la base (no cambia nada)

- No montar a ritmo (15 de 15; reto 7 de 7), corte seco en el cuerpo (93–99 %), subtítulos solo puntuales (13 de 15) con
  color por hablante (9 de 12), `Z_SIN_CARA` 1,0 (9 de 9; reto 6 de 7), `Z_FUERTE` ≈ ×1,6–1,67 (reto ×1,6), `CARA_Y` 0,38,
  habla y música desde el segundo 0 (12 de 15; reto 7 de 7), botón de suscribir animado abajo al centro y solo (3 de 3 que
  lo usan), sin zoom en el gráfico ni rebote (0 de 15 con rebote), música del cierre ≈ 11,4 dB bajo la voz (`CIERRE` −20),
  LUFS −14.
