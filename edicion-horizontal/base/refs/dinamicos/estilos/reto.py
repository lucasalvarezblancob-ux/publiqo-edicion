# Números del motor para el estilo «reto» (BORRADOR 2026-11-24, pendiente de visto bueno de Lucas/Mac).
# Mismos nombres que personal/<creador>/ajustes.py. Solo lo medido en las 7 referencias de reto.md
# (plex-30d, plex-7d, jjw-diamond, jjw-rhea, mrbeast-extremos, mrbeast-trap, fezz-21); lucas-survivor no cuenta.
# Lo que no está aquí se queda como en la base. Medido y sin cambio (por eso no va):
#   Z_FUERTE   mediana ×1,6 (plex-7d 2,0 · plex-30d 2,3 · jjw-diamond 1,65 máx. · jjw-rhea 1,6 · fezz-21 1,6)  ≈ base 1.65
#   Z_SIN_CARA 1.0 en 6 de 7 (jjw-diamond empuja despacio sobre objetos, nunca de golpe)                    = base 1.0
#   LUFS       mediana −13,2 (−15,8 a −6,7); YouTube normaliza a −14                                        = base -14
#   MUSICA_NIVELES TRAILER: intro 6,4 dB bajo la voz de mediana (1,2–13) → ≈ −15 con la calibración de abajo  ≈ base -16
# No se pudo medir: CARA_Y (null en las 7 fichas).

# ---------- Ritmo y zooms (dinamica.py) ----------
# Vuelta a ×1,0 entre cada golpe en 4 de 4 referencias con punch (plex-30d, plex-7d, jjw-diamond, jjw-rhea).
# Valores: jjw-diamond mediana ×1,29 (1,18–1,65) · jjw-rhea cortes de escala ×1,15–1,25 · Plex ×1,3–1,5 (capado a
# ×1,5 por el límite 4K → 4K que piden las dos fichas de Plex). Son los valores de la base, intercalados con 1,0.
# Base: [1.0, 1.3, 1.0, 1.45, 1.15, 1.0, 1.35, 1.12, 1.5, 1.0, 1.25] (encadena 1.45 → 1.15 y 1.35 → 1.12 → 1.5).
ESCALAS = [1.0, 1.3, 1.0, 1.5, 1.0, 1.2, 1.0, 1.45, 1.0, 1.25]

# Mediana de las propuestas de las 7 fichas: mínimos 1,2–2,0 (mediana 1,7), máximos 2,2–5,0 (mediana 3,2).
# Plano mediano real de las 7: 1,4–2,2 s (mediana 2,0). Con 1 cámara (Plex) 1,7–5,0; multicámara 1,2–3,3.
# Base: (2.48, 4.48).
CAMBIO_CADA = (1.7, 3.2)

# ---------- Efectos de sonido (paso5_audio.py) ----------
# dato: cifras, contadores y marcadores entran mudos en 5 de 7 (jjw-diamond, jjw-rhea, mrbeast-extremos,
#       mrbeast-trap, fezz-21); el sonido va en la consecuencia (casilla, vida, plaza), que se pone a mano con "snd".
#       Base: ("pop", 0.2).
# golpe: textos de énfasis y punch mudos en 6 de 7 (solo jjw-diamond pone golpe en 2 reacciones). Base: ("whoosh-short", 0.16).
# trk: rótulos y etiquetas pegados al sujeto mudos en las 3 que los tienen (jjw-rhea, mrbeast-trap, mrbeast-extremos).
#       Base: ("pop", 0.25).
# seccion: cartela o cambio de bloque con impacto en 3 de 5 que suenan (jjw-diamond +1,7 dB, mrbeast-trap +5,4,
#       fezz-21 +8,7 respecto a la voz); jjw-rhea soplido, plex-7d jingle. Ganancia sin medir: la del «titulo» de la
#       base. A decidir. Base: ("whoosh-short", 0.22).
SFX = {"dato": None, "golpe": None, "trk": None, "seccion": ("impact-bass-1", 0.30)}

# ---------- Música (paso6_musica.py) ----------
# Las fichas miden distancia voz − música; el motor usa dB sobre la pista normalizada. Calibración supuesta: la base
# (BASE −24) suena ≈ 15,5 dB bajo la voz (CONTEXTO.md, ramon v2: 14–17). Comprobar en el primer render. A decidir.
# BASE: voz − música 9,1 dB de mediana con las 7 (3,6–12,0) y 11,1 sin las dos con público o narrador gritando
#       (mrbeast-trap 3,6, fezz-21 5,8) → ≈ 10,5 dB bajo la voz → −24 + 5 = −19. Base: -24.
# SINVOZ: sin voz la música va 1,5 dB bajo la voz de mediana (−5,2 a +1: jjw-rhea −5,2, mrbeast-extremos −5,0,
#       fezz-21 ≈ −2, plex-30d −1,5, mrbeast-trap +0,1, plex-7d ≈ +1, jjw-diamond ≈ +1) → −10. Base: -13.
# SECCION: cartela sin voz encima, música 0 a +7 dB sobre la voz (jjw-diamond 0, plex-30d +2, mrbeast-trap +2,7,
#       jjw-rhea +3 a +8; mediana ≈ +2,4) → −6. Solo vale si el rótulo va sin voz encima. Base: -15.
# MAPA y CIERRE no van: las referencias no coinciden (mapa −12,9 a +2,7 dB; cierre con música en 4 de 7, sin ella en 3).
MUSICA_NIVELES = {"BASE": -19.0, "SINVOZ": -10.0, "SECCION": -6.0}
