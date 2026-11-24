# Números del motor para el estilo «vlog» (y viaje, que es el mismo) (BORRADOR 2026-11-24, pendiente de visto bueno
# de Lucas/Mac). Mismos nombres que personal/<creador>/ajustes.py. Solo lo medido en las 15 referencias de vlog.md:
# alessio-vuelta, alessio-capri, alessio-24h, nil-tomorrowland, nil-f1, nil-sagrada, nil-restaurante, bycalitos,
# luisito, rh-hotel, rh-titanic, rh-avispas, plex-viaje, plex-coche, plex-gane. Las fichas viejas no cuentan.
# Lo que no está aquí se queda como en la base. Medido y sin cambio (por eso no va):
#   Z_FUERTE   golpe ×1,60–1,70 en Plex (plex-viaje 1,60 · plex-coche 1,67 · plex-gane 1,70), nil-restaurante 1,5–1,6,
#              nil-sagrada 1,43–1,52, rh-avispas 1,75 → ≈ 1,6–1,67                                        ≈ base 1.65
#   Z_SIN_CARA 1.0 en 9 de 9 que lo miden (sin cara, sin zoom; solo las fotos fijas empujan +2,5–7,5 %/s)  = base 1.0
#   CARA_Y     0,38 de mediana (plex-gane 0,30 · plex-coche 0,33 · plex-viaje 0,38 · rh-hotel 0,40 a ojo ·
#              nil-sagrada 0,43 del detector)                                                               = base 0.38
#   LUFS       mediana −15,6 (−20,9 a −11,8); 12 de 15 pasan de 0 dBTP; YouTube normaliza a −14          = base -14
#   MUSICA_NIVELES CIERRE: con voz, 11,4 dB bajo la voz de mediana (5,7–22) → ≈ −20 con la calibración   = base -20
# No se pone (no coinciden o no se pudo medir):
#   MUSICA_NIVELES TRAILER: depende del tipo de intro. Corta y sin voz (alessio ×3): música a nivel de la voz o encima
#       (+1 a +10 dB). Explicativa con voz: ≈ 12 dB bajo la voz (nil-f1 10–19, nil-sagrada 9–12, bycalitos 10,9,
#       rh-hotel 13,2, rh-avispas 11). Base: -16.
#   MUSICA_NIVELES MAPA: sin subida en 4 de 5 con mapa y música (nil-f1, nil-sagrada, luisito, bycalitos 11 dB bajo la
#       voz); nil-restaurante sin música. Base: -19 (sube). Muestra pequeña: se deja.
#   MUSICA_HUECO_MAX, VOZ_DISFRAZ_TONO: sin dato en las fichas.
# Viaje frente a día a día (11 frente a 3): música 51 % frente a 34 %, voz − música 13,2 frente a 9,5 dB, cortes/min
#   24,9 frente a 21. No es bastante para otro archivo (ver vlog.md). Si se separa: día a día BASE ≈ −18 (9,5 dB).

# ---------- Ritmo y zooms (dinamica.py) ----------
# Vuelta a ×1,0 entre cada golpe en 9 de 9 referencias con punch; ninguna encadena dos escalas (plex-gane: 13 cambios
# pequeños frente a 61 jump cuts y 44 golpes). Saltos por corte medidos con operador o trípode: nil-f1 mediana ×1,17
# (×1,08–1,32; p75 ×1,24), rh-titanic ×1,22 (×1,2–1,35). Los golpes ×1,4–1,9 son Z_FUERTE, no escalas.
# Con selfie gran angular (6 de 15: alessio ×3, luisito, bycalitos, nil-tomorrowland) no hay zoom digital sobre quien
# habla: para esos creadores, ESCALAS = [1.0] en su ajustes.py.
# Base: [1.0, 1.3, 1.0, 1.45, 1.15, 1.0, 1.35, 1.12, 1.5, 1.0, 1.25] (encadena 1.45 → 1.15 y 1.35 → 1.12 → 1.5).
ESCALAS = [1.0, 1.2, 1.0, 1.3, 1.0, 1.15, 1.0, 1.25]

# Mediana de las propuestas de las 15 fichas: mínimos 1,2–9 (mediana 2,2), máximos 2,2–40 (mediana 5,0). Sin
# alessio-24h (9, 40: tomas largas de rutina) sale casi igual: 2,0 y 4,9. Plano mediano real ≈ 2,0 s (1,3–3,8): ese
# ritmo sale de los jump cuts del EDL, no de este número. Base: (2.48, 4.48).
CAMBIO_CADA = (2.2, 5.0)

# ---------- Efectos de sonido (paso5_audio.py) ----------
# golpe: zooms y punch-in mudos en 9 de 9 (plex-gane 44 de 44; nil-f1 solo un impacto grave cada ≈ 7 min, a mano).
#        Base: ("whoosh-short", 0.16).
# trk: etiquetas pegadas al sujeto mudas en 2 de 3 (nil-sagrada, rh-titanic). Base: ("pop", 0.25).
# titulo: título o cabecera con impacto en 0 de 9 que la tienen (clic o pop por palabra alessio ×2; jingle propio
#        rh-titanic, rh-avispas, bycalitos; papel rh-hotel; nada alessio-capri, luisito, nil-tomorrowland). A decidir
#        qué poner; mientras, sin efecto. Base: ("impact-bass-1", 0.30).
# dato no se toca: el dinero suena en 7 de 7 que rotulan precios (caja o ding, −5 a −13 dB bajo la voz) y los datos
#        que no son dinero van mudos en 5 (plex-coche, plex-gane, rh ×3) y con pop o ding en 4 (nil-restaurante,
#        nil-sagrada, alessio-24h, alessio-vuelta). Base: ("pop", 0.2). No hay «caja» en estudio/public/sonidos.
# seccion, mapa, suscribe no se tocan: sin un sonido común (mapa: ding nil-f1 y nil-restaurante, whoosh bycalitos,
#        nada en 3).
SFX = {"golpe": None, "trk": None, "titulo": None}

# ---------- Música (paso6_musica.py) ----------
# Las fichas miden distancia voz − música; el motor usa dB sobre la pista normalizada. Calibración supuesta (la de
# reto.py): la base (BASE −24) suena ≈ 15,5 dB bajo la voz → la voz está en ≈ −8,5. Comprobar en el primer render.
# BASE: voz − música 12,5 dB de mediana con las 15 (6,1–17,4); 13,7 solo con las 11 en español; Alessio (inglés)
#       7–9,5 → −8,5 − 12,5 = −21. Base: -24.
# SINVOZ: sin voz la música va a nivel de la voz de mediana (−7 a +10: Plex +5 a +9, alessio-vuelta +10, nil-sagrada
#       +2,6 a +6,7; nil-restaurante, bycalitos, luisito, alessio-24h 1,4–2 bajo; rh-hotel −7) → −8,5. Base: -13.
MUSICA_NIVELES = {"BASE": -21.0, "SINVOZ": -8.5}
