# Cambios globales de la base (con rollback por creador)

Cada cambio de la base que **cambia cómo salen los vídeos de todos** (números del motor o reglas de estilo) lleva un id
y lo que había antes, para que un creador pueda **deshacer solo ese cambio** sin quedarse sin el resto:

    PY herramientas/montaje/deshacer_cambio.py <creador> G00x        (desde la raíz de la carpeta de edición)

- Si es un número del motor, escribe el valor antiguo en `personal/<creador>/ajustes.py` (lo del creador manda).
- Si es una regla de texto, la escribe en su `preferencias.md` como «Gxxx no aplica para este creador: <regla antigua>».
- `--volver` quita el rollback (el creador vuelve a tener el cambio).
- Cuando un creador diga «desde la actualización no me gusta X», se busca aquí y se deshace solo eso.

Los cambios que no tocan el resultado (herramientas nuevas, encargos, documentación, arreglos de fallos) no van aquí.
Formato: un bloque por cambio con su JSON (lo lee `deshacer_cambio.py`).

## G001 — Capítulos sin contador «1/7» ni casillas (2026-11-24)
Lucas: «eso no me gusta». El rótulo de capítulo queda en título + subtítulo.
```json
{"id": "G001", "fecha": "2026-11-24", "tipo": "ajuste", "nombre": "CONTADOR_CAPITULOS", "antes": true, "ahora": false,
 "regla_antes": "El rótulo de capítulo lleva número/total («1/7») y casillas de progreso."}
```

## G002 — Las escalas vuelven a ×1,0 entre saltos (2026-11-24)
Estudio de estilos: 13 de 13 referencias con saltos de escala vuelven a ×1,0 entre cada uno. Nunca dos escalas distintas
seguidas en la misma toma (antes la base encadenaba ×1,45 → ×1,15 y ×1,35 → ×1,12 → ×1,5). Un plano de la rotación justo
antes de un golpe o detalle del plan también queda a ×1,0.
```json
{"id": "G002", "fecha": "2026-11-24", "tipo": "ajuste", "nombre": "ESCALAS",
 "ajustes": {"ESCALAS": [1.0, 1.3, 1.0, 1.45, 1.15, 1.0, 1.35, 1.12, 1.5, 1.0, 1.25], "ESCALAS_VUELTA": false},
 "regla_antes": "Escalas encadenadas sin volver a ×1,0 (1,45 → 1,15; 1,35 → 1,12 → 1,5)."}
```

## G003 — Suena la consecuencia, no la entrada; el dinero suena siempre (2026-11-24)
Estudio de estilos: zooms y punch mudos en 9 de 9 vlogs; cifras y etiquetas mudas en 5 de 7 retos; el dinero suena en
7 de 7 que rotulan precios. Etiquetas (`trk`), cifras (`dato`) y golpes de zoom (`golpe`) entran mudos; el efecto va
con `"snd"` en el instante del cambio (casilla, logro, plaza). Un texto con €, $, «euros», «dólares», «pesos»… suena
(`dinero`: caja registradora corta; la larga, con `"snd"`, para un total). Alimentación: de 29 efectos (1,3/min) a 11 (0,5/min); las referencias, 0,16–2,1/min (mediana 0,5).
```json
{"id": "G003", "fecha": "2026-11-24", "tipo": "ajuste", "nombre": "SFX",
 "antes": {"trk": ["pop", 0.25], "dato": ["pop", 0.2], "golpe": ["whoosh-short", 0.16], "dinero": null},
 "regla_antes": "Cada etiqueta, cifra y golpe de zoom suena al entrar (pop / whoosh)."}
```

## G004 — Los rótulos de situación y estado pueden cruzar cortes (2026-11-24)
Estudio de estilos: 6 de 15 vlogs y 4 de 7 retos dejan la etiqueta de sitio/hora, la tarjeta de datos, el marcador o la
barra de viaje sobre varios cortes si no se mueve. `timing_textos.py` ya no avisa «COLA» en esos tipos
(`TIPOS_CRUZAN_CORTES`: dato, partida, contador, marcador, barra, mapa). Los de énfasis (golpe, frases) siguen saliendo
con el corte.
```json
{"id": "G004", "fecha": "2026-11-24", "tipo": "ajuste", "nombre": "TIPOS_CRUZAN_CORTES", "antes": ["dato"],
 "regla_antes": "Todo texto sale con el corte (timing_textos.py avisa de cualquier texto que cruce un corte)."}
```

## G005 — Música que corta en seco y silencio como remate (2026-11-24)
Estudio de estilos: la música se quita en seco 0,7–6 s antes del remate y vuelve de golpe en el corte siguiente (8 de 15
vlogs, 7 de 7 retos); entra de golpe en un corte en 12 de 15. Son **opciones del plan** (`HUECOS_MUSICA`, ventana con
`{"seco": True}` en `paso6_musica.py`): un vídeo que no las pide suena igual que antes, así que no hay nada que deshacer.
Se apunta para que se sepa de dónde sale.
```json
{"id": "G005", "fecha": "2026-11-24", "tipo": "regla", "nombre": "HUECOS_MUSICA",
 "regla_antes": "La música siempre funde al entrar (0,48 s) y al salir (3 s); no hay silencio de remate."}
```

## G006 — Reglas de criterio del estudio de estilos (2026-11-24)
En `CONTEXTO.md` § «Reglas del estudio de estilos (G006)»: material fuera de su sitio marcado; una plantilla por función;
el destello corto y la mano que tapa el objetivo no cuentan como transición; elipsis con una cifra (sin «X horas
después»); quitar la música 30–45 s antes del clímax con la voz encima; la promesa vuelve en el desenlace con el mismo
gráfico; texto en el fotograma de su palabra (±3 f).
```json
{"id": "G006", "fecha": "2026-11-24", "tipo": "regla", "nombre": "REGLAS_ESTUDIO",
 "regla_antes": "Sin estas reglas: transiciones construidas ≤ 5 contando destellos y manos; sin regla de material fuera de sitio, plantillas, elipsis, clímax ni promesa."}
```
