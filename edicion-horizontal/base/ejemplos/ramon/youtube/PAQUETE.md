# Paquete de YouTube — `ramon` (RayWild, vídeo en inglés)

> ⚠️ Los prompts de miniatura de este ejemplo son del método anterior (transformar un fotograma). Desde el 2026-11-27
> (G010) todas las miniaturas se hacen desde cero con la cara del creador: `base/titulos-miniaturas.md` § 6, «Molde
> único». Los títulos, la segunda lectura y la elección de ángulos siguen valiendo.

Vídeo: `out/ramon/ramon_v7b.mp4` · 18:39 · idioma hablado: **inglés** (todo lo que se publica va en inglés) · canal
**RayWild** (@raywild10). Primera versión del 2026-11-13; **rehecho el 2026-11-14** con la guía nueva
(`base/titulos-miniaturas.md`, 15 canales). Qué cambió respecto a la primera versión, al final (§ 6).

## 1. De qué va y qué se vende

Ocho novedades del criadero en un vídeo: tres animales nuevos y cinco obras. **No se vende el resumen** («8 surprises»
no le dice nada a quien no conoce el canal): se vende un bloque fuerte por pareja. Canal **pequeño** y de **colección
propia**: nada de «My», nada que suponga conocer el canal (nombres de los animales, «otra vez»), Title Case limpio sin
palabras gritadas ni «!» (en los canales estudiados gritar no sube y en el canal pequeño resta: CC x0,76 frente a x1,17).

| Activo | Minuto (dura) | Lo dice el vídeo | Palanca |
|---|---|---|---|
| Tortuga rusa: «fácil» y muere mucho | 5:22–7:15 (1:53) | «they say it's an easy animal to keep but unfortunately many… died»; «their main problem is humidity» | **paradoja** + utilidad (quien tiene una) |
| Anubis, la tortuga más amenazada de África, en la palma | 1:02–2:51 (1:49) | «the most endangered tortoise in Africa» | superlativo con dueño **frente a** tamaño diminuto |
| La Várzea: una selva detrás de una puerta de casa | 9:34–12:09 (2:35), obras hasta 17:17 | «the four ecosystems of the South American continent» | **esconder con ancla** (¿cómo es por dentro?) |
| Crías de cuello de serpiente cazando grillos | 2:51–5:22 (2:31) | «they are eating like piranha»; «only a few weeks old… let's say a month» | ternura frente a ferocidad, el durante |
| Las casetas de las sulcatas se inundaron; casa nueva | 16:22–18:10 (1:48, al final) | «those houses that we built flooded» | suceso; la obra a medias |

Los dos primeros bloques duran algo menos de dos minutos (la guía los manda de recambio por debajo de dos): **pasan**
porque llegan pronto (minuto 1 y 5) y la promesa se cumple entera. El de la inundación, no: es el último.

Lo que **no** se vende: «NEW», «surprises», «update», «My», el número de episodio.

## 2. Las cinco parejas (de más a menos recomendada)

Cada prompt es **un mensaje nuevo en un chat nuevo de ChatGPT**, con las imágenes indicadas adjuntas (están en esta
carpeta). Lo que devuelva: `miniatura.py final A <imagen>` lo deja en 1920×1080 y saca la prueba a 168 px.

---

### A — La paradoja: la tortuga «fácil» que se muere

- **Título** (40): `The "Easy" Pet Tortoise That Keeps Dying`
- **Texto de la miniatura**: `RUSSIAN TORTOISE` (el nombre que el título calla: quien tiene una se reconoce).
- **Segunda lectura**: la imagen sola dice «un chico mira a su tortuga sana». Con el título dice «esa tortuga sana es la
  que la gente mata sin saberlo, y él lo sabe». Un solo paso, sin saber nada de fuera.
- **Pregunta abierta**: ¿por qué se mueren, y la mía? La causa (la humedad) no sale en ningún sitio: contestaría.
- **Referencias**: `A.jpg` (6:47 · C0247 542,4 s: la tortuga rusa en su recinto) + `A2.jpg` (6:42 · C0247 567,8 s:
  él mirando de reojo hacia abajo, a su derecha, preocupado y con la boca cerrada). Plantilla B (cara frente a sujeto).
- **Idea**: la tortuga grande y nítida a la izquierda, más cerca de la cámara; él a la derecha mirándola con la
  preocupación que ya tiene en A2 (la mirada es un vector hacia ella: la causa del gesto está en el cuadro). Instante:
  antes; todo está bien todavía. Sin el amarillo de la lámpara.

```
Create a YouTube thumbnail, 16:9 landscape. Keep everything important inside the central 16:9 area.
Attached: image 1 = a Russian tortoise on soil inside an enclosure, under a yellow heat lamp; image 2 = the same man glancing down to his right with a worried look.
KEEP EXACTLY: the man's face, beard, hair, build and grey sleeveless hoodie from image 2 (same person, do not beautify, do not change his age or features); the tortoise from image 1: exact same species and shell shape, low rounded shell, olive-tan scutes with dark brown blotches.
INSTANT: an ordinary, quiet moment; the tortoise looks healthy and nothing has happened yet.
COMPOSITION: the first thing the eye sees is the tortoise, in the left half, closer to the camera, about 45% of the frame width, tack sharp, its head turned toward the man. His face is the second thing the eye sees: right third, chest up, head about 30% of the frame height, a little behind the tortoise. Camera low, at tortoise height, wide-angle lens.
EXPRESSION AND GAZE: keep his expression from image 2 (worried, brows drawn together, mouth closed), looking down at the tortoise.
HANDS: relaxed, low or out of frame. No pointing.
BACKGROUND AND LIGHT: neutral daylight white balance, no yellow cast; plain pale soil; dark, blurred background. Soft light on his face. The shell is the only warm, saturated color besides the text.
TEXT: "RUSSIAN TORTOISE" in a bold condensed sans-serif, all caps, yellow (#FBBA1C) with a thick black outline, top left above the tortoise, two lines, each about 13% of the frame height.
STYLE: photorealistic, like a real phone photograph with a punchy YouTube color grade; not an illustration, no plastic AI skin.
DO NOT ADD: watermarks, channel logo, any logo or brand, any other text, arrows, circles, question marks, skulls, red crosses, a sick or dead animal, extra animals or people, anything small in the bottom-right corner.
```

Retoques: «The tortoise must be the one in image 1, same shell, not a different species.» · «Keep his face exactly as
in image 2, still looking down at the tortoise.» · «Remove the text.»

---

### B — Lo más raro de África, en una mano

- **Título** (50): `Africa's Most Endangered Tortoise Fits in One Hand`
- **Texto de la miniatura**: sin texto.
- **Segunda lectura**: la imagen sola dice «una tortuguita mona en un guante». Con el título dice «eso que cabe en una
  mano es de lo último que queda de su especie, y la tiene él». Superlativo con dueño delante (registro de FG) que
  choca con lo diminuto.
- **Pregunta abierta**: ¿cuál es, por qué está así y cómo es que él tiene una?
- **Referencias**: `B.jpg` (2:47 · C0246 231,5 s: la tortuga sobre el guante) + `B2.jpg` (2:12 · C0246 240,2 s: él con
  la tortuga, cejas arriba). Plantilla A (sujeto en la mano: suelo seguro).
- **Idea**: la mano morada ofreciendo la tortuga hacia la lente, en diagonal, enorme y nítida; él detrás, mirándola a
  ella (no a cámara), con asombro contenido. Morado del guante y amarillo del caparazón, complementarios, sobre fondo
  oscuro liso.

```
Create a YouTube thumbnail, 16:9 landscape. Keep everything important inside the central 16:9 area.
Attached: image 1 = close-up of a small tortoise resting on a hand in a purple nitrile glove; image 2 = the same man holding that tortoise.
KEEP EXACTLY: the man's face, beard, hair, build and grey sleeveless hoodie from image 2 (same person, do not beautify, do not change his age or features); the tortoise from image 1: exact same species, high domed shell, pale sand-yellow scutes with dark brown edges, same size relative to the hand.
INSTANT: he is offering it toward the viewer, mid-gesture.
COMPOSITION: wide-angle shot from very close. The first thing the eye sees is the tortoise: the open purple-gloved hand comes diagonally toward the lens from lower centre, the tortoise on the palm about 45% of the frame width, tack sharp, head facing the camera. His face is second: right third, chest up, head about 30% of the frame height, slightly soft.
EXPRESSION AND GAZE: quiet amazement, eyebrows raised, mouth closed (as in image 2), eyes looking down at the tortoise in his hand.
HANDS: one gloved hand offers the tortoise toward the lens, palm up. No pointing.
BACKGROUND AND LIGHT: replace the shelves with a plain, dark teal, blurred background. Soft light on his face, a warm key light on the shell.
TEXT: No text anywhere in the image.
STYLE: photorealistic, like a real phone photograph with a punchy YouTube color grade; not an illustration, no plastic AI skin.
DO NOT ADD: watermarks, channel logo, any logo or brand, text, arrows, circles, question marks, extra animals or people, extra fingers, anything small in the bottom-right corner.
```

Retoques: «Make the tortoise 20% larger and keep the shell pattern exactly as in image 1.» · «Keep his face exactly as
in image 2; if changing his gaze changes his face, let him look at the camera as in image 2.» · «Darker, plainer
background.»

---

### C — Una selva detrás de una puerta

- **Título** (45): `There's an Amazon Rainforest Behind This Door`
- **Texto de la miniatura**: sin texto.
- **Segunda lectura**: la imagen sola dice «un chico abre una puerta de cristal en una pared de casa; dentro hay
  plantas». Con el título dice «ahí dentro, en su casa, hay una selva amazónica entera». «This» tiene su referente a la
  vista (la puerta).
- **Pregunta abierta**: ¿cómo es por dentro y cuánto hay? Se ve solo una rendija con la cascada y el lagarto (esconder
  con ancla: la forma se ve, lo demás hay que entrar a verlo).
- **Referencias**: `C.jpg` (9:42 · C0251 17,8 s: él en la puerta de la Várzea) + `C2.jpg` (9:57 · C0251 29,7 s: el
  interior, cascada y lagarto caimán). Plantilla H (retrato + lugar con anomalía).
- **Idea**: la puerta entreabierta en el centro-izquierda y, por la rendija, la selva de C2 en verde saturado (la única
  mancha fría sobre la pared terracota); él a la derecha, con la mano tirando de la puerta y media sonrisa de quien sabe
  lo que hay detrás. Es el bloque más largo del vídeo: la promesa se cumple de sobra.

```
Create a YouTube thumbnail, 16:9 landscape. Keep everything important inside the central 16:9 area.
Attached: image 1 = a man standing at an open glass door in a terracotta wall; image 2 = what is inside that room: a rock wall with a waterfall, tropical plants and a green lizard on the rocks.
KEEP EXACTLY: the man's face, beard, hair, build and grey sleeveless hoodie from image 1 (same person, do not beautify, do not change his age or features); the lizard from image 2: exact same species, shape and colors; the rock wall, waterfall and plants of image 2.
INSTANT: he is pulling the door open; it is only half open, so we see a vertical slice of the room, not all of it.
COMPOSITION: the first thing the eye sees is the bright slice of jungle through the half-open door, centre-left, about 40% of the frame width: the waterfall and the lizard on the rock beside it, the lizard enlarged to about twice its size so it reads. His face is second: right third, chest up, head about 35% of the frame height, standing outside next to the door.
EXPRESSION AND GAZE: calm, knowing half smile, mouth closed, looking at the camera.
HANDS: his near hand grips the edge of the glass door, pulling it open. No pointing.
BACKGROUND AND LIGHT: flat warm terracotta wall outside; through the gap, lush saturated greens, wet rock, a soft beam of light on the waterfall. The green slice is the only cool, saturated color. Light on his face.
TEXT: No text anywhere in the image.
STYLE: photorealistic, like a real phone photograph with a punchy YouTube color grade; not an illustration, not a fantasy poster.
DO NOT ADD: watermarks, channel logo, any logo or brand, text, arrows, circles, question marks, other animals or people, a different lizard, a generic jungle, the whole room fully visible, anything small in the bottom-right corner.
```

Retoques: «The room must look like image 2, not a generic jungle.» · «Open the door less; show only a slice of the
room.» · «Keep his face exactly as in image 1» (si la media sonrisa le cambia la cara, mejor su gesto original).

---

### D — El bocado

- **Título** (43): `Baby Snake-Necked Turtles Eat Like Piranhas`
- **Texto de la miniatura**: `1 MONTH OLD` (dato que choca con «piranhas»; no repite ninguna palabra del título).
- **Segunda lectura**: la imagen sola dice «una tortuguita de cuello larguísimo, rara y tierna». Con el título y la
  edad dice «eso de un mes es una fiera». Depredadores en plural (CW 3/3 altos).
- **Pregunta abierta**: hay que verlas comer.
- **Referencia**: `D.jpg` (no está en el montaje con este encuadre: C0246 390,9 s, la cría entre los dedos con el
  cuello estirado), solo para la especie. Plantilla C (el instante, sin cara).
- **Idea**: el **durante**, que la primera versión no tenía (era la cría posando entre los dedos): macro a ras de agua,
  la cría lanzando el cuello con la boca abierta hacia un grillo que flota a unos centímetros. Los grillos los echa en el
  vídeo (bloque 2:51–5:22); bajo el agua no se distinguen a 168 px, por eso se recompone a ras de superficie. El grillo
  da la escala.

```
Create a YouTube thumbnail, 16:9 landscape. Keep everything important inside the central 16:9 area.
Attached: image 1 = a baby snake-necked turtle held between two gloved fingers above a tub of water.
KEEP EXACTLY: the turtle from image 1: exact same species, flat olive-brown shell, very long neck, small flat head, pale underside, same proportions.
INSTANT: the split second before the strike: the turtle is in shallow water, its long neck shooting forward, mouth just opening, a cricket floating on the surface a few centimetres in front of its mouth. Nothing has been eaten yet.
COMPOSITION: macro at water level. The first thing the eye sees is the turtle's head and neck, the turtle about 55% of the frame width, slightly left of centre, neck pointing right toward the cricket, eye tack sharp. The cricket is real size, which shows how tiny the turtle is. No person, no hands.
BACKGROUND AND LIGHT: dark, blurred, deep green-black water behind. Bright soft light on the turtle's wet skin; small ripples where the neck breaks the surface.
TEXT: "1 MONTH OLD" in a bold condensed sans-serif, all caps, yellow (#FBBA1C) with a thick black outline, top left, about 16% of the frame height, one line.
STYLE: photorealistic, like a real macro photograph with a punchy YouTube color grade; not an illustration.
DO NOT ADD: watermarks, any logo, any other text, arrows, circles, extra turtles, fish, teeth, blood, a different species, anything small in the bottom-right corner.
```

Retoques: «Do not change the turtle: same long neck and shell as in image 1.» · «The cricket smaller and closer to its
mouth.» · «Remove all text.»

---

### E — La inundación (recambio)

- **Título** (31): `Giant Tortoises' House Flooded…`
- **Texto de la miniatura**: sin texto.
- **Segunda lectura**: la imagen sola dice «una tortuga enorme sale de su caseta y él está de obra». Con el título dice
  «esa caseta se inundó con ella dentro (o casi) y la casa nueva es la respuesta».
- **Pregunta abierta**: ¿qué les pasó y cómo lo arregla?
- **Referencias**: `E.jpg` (16:47 · C0253 150,6 s: la sulcata saliendo de la caseta que se inundó) + `E2.jpg` (17:22 ·
  C0254 5,8 s: él en los cimientos de la casa nueva). Plantilla J (suceso), en el instante **bisagra**: la obra a medias.
- **Idea**: la sulcata en primer término saliendo de la caseta vieja; detrás, él de pie en los cimientos a medio hacer,
  agarrando la herramienta (no presentando con la mano, como en la primera versión); cielo cubierto. **Sin agua**: en el
  vídeo no hay plano de la inundación y no se inventa.
- **Por qué es de recambio**: es el bloque más corto y el último (1:48 al final); quien entra por este título espera 16
  minutos. Además es una desgracia ya ocurrida y el canal es de «consigo cosas»: ahí la pérdida no vende (CC x0,51 y x0,67).

```
Create a YouTube thumbnail, 16:9 landscape. Keep everything important inside the central 16:9 area.
Attached: image 1 = a large sulcata tortoise walking out of a low concrete shelter on bare ground; image 2 = the same man standing on half-built concrete-block foundations in a garden.
KEEP EXACTLY: the man's face, beard, hair, build, grey sleeveless hoodie and jeans from image 2 (same person, do not beautify, do not change his age or features); the tortoise from image 1: exact same species, tan-brown shell with raised growth rings, thick scaly front legs; the low grey concrete shelter with its small square entrance.
INSTANT: the new house is half-built: one row of concrete blocks, steel rods sticking up; nothing is finished.
COMPOSITION: low camera, almost at ground level. The first thing the eye sees is the tortoise, left foreground, about 40% of the frame width, sharp, coming out of the old shelter. His face is second: right third, standing on the half-built foundations, from the thighs up, head about 25% of the frame height.
EXPRESSION AND GAZE: serious, mouth closed, looking at the tortoise.
HANDS: one hand grips the handle of a shovel planted in the soil. No pointing, no presenting gesture.
BACKGROUND AND LIGHT: bare reddish soil, garden plants behind, heavy grey overcast sky. Warm light on the shell, soft light on his face.
TEXT: No text anywhere in the image.
STYLE: photorealistic, like a real phone photograph with a punchy YouTube color grade; not an illustration.
DO NOT ADD: water, puddles, rain, flooding, watermarks, any logo, text, arrows, circles, other animals or people, anything small in the bottom-right corner.
```

Retoques: «Remove any water or rain; the ground is dry.» · «Make the tortoise 20% larger.» · «Keep his face exactly
as in image 2.»

## 3. Qué probar primero

**A, B y C** en «Probar y comparar» de YouTube Studio (hasta tres; elige por tiempo de visualización, no por clics).
Tres palancas y tres imágenes distintas: paradoja con cara que mira al sujeto (A), lo raro en la mano hacia la lente
(B) y el sitio escondido tras una puerta (C). C promete el bloque más largo, así que es la que mejor retiene; A es la
que más puede traer por búsqueda (mucha gente tiene una tortuga rusa). Si el canal solo deja probar miniaturas, las
tres con el título de A.

**Recambio** si arranca flojo: D (la pareja entera) y estos títulos sueltos:
- `Meet Africa's Most Endangered Tortoise` (38) — para la miniatura B, si «Fits in One Hand» no convence.
- `Why Do So Many Russian Tortoises Die as Pets?` (45) — búsqueda pura, para la miniatura A.
- `Building Every South American Ecosystem for Reptiles` (52) — la ambición entera, para la miniatura C.

Si se cambia un título ya publicado, revisa el rótulo de su miniatura: puede quedarse sin ancla. Cuando haya resultado,
dímelo (cuál ganó y con qué porcentaje) y lo apunto en `personal/reinoselva/preferencias.md` → «Títulos y miniaturas»:
vale más que el estudio de otros canales.

## 4. Descripción, capítulos y etiquetas

```
Anubis is an Egyptian tortoise (Testudo kleinmanni), the most endangered tortoise in Africa, and he is small enough to sit in one hand. He is only the first of 8 surprises at RayWild…

Also new: baby snake-necked turtles from New Guinea (Chelodina siebenrocki), about a month old and already hunting crickets like piranhas, and a pair of Russian tortoises (Testudo horsfieldii). Why do so many Russian tortoises die as pets? How much water do baby snake-necked turtles need? Then the builds: the Asian pond is back, the Várzea biome opens up to the whole Amazon and the Guianas, a Gran Chaco aviary for Hillary and Cherry Head, an African zone, and a flood-proof house for our sulcatas Brutus and Gold Digger.

Chapters
0:00 8 surprises at RayWild
1:02 The rarest tortoise in Africa
2:51 Baby snake-necked turtles
5:22 The most trafficked tortoise
7:15 The Asian pond is back
9:34 Opening the Amazon biome
12:09 A Gran Chaco aviary
16:07 A whole African zone
17:17 A flood-proof tortoise house
18:10 See you in the next one

Subscribe to watch these ecosystems grow.

Instagram: [missing: Instagram]

#tortoise #turtles #reptiles
```

**Etiquetas**: `egyptian tortoise, Testudo kleinmanni, Kleinmann's tortoise, snake-necked turtle, Chelodina
siebenrocki, baby turtles eating, russian tortoise, Testudo horsfieldii, Horsfield's tortoise, russian tortoise care,
sulcata tortoise, Centrochelys sulcata, caiman lizard, red-footed tortoise, Phrynops hilarii, tortoise enclosure,
turtle pond, bioactive enclosure, RayWild, Ray Wild`

## 5. Comprobado y por confirmar

**Comprobado**
- Cada promesa está dicha en el vídeo (frases literales, minuto y duración, en la tabla del § 1). Los grillos de D los
  echa en el vídeo; el agua de E no sale y está en el `DO NOT ADD`.
- Nombres de especies: contra los rótulos del vídeo, no contra la transcripción.
- Capítulos: tiempos del archivo final.
- Las nueve referencias, miradas a tamaño de miniatura y a 168 px (`hoja.jpg`). B se entiende tal cual; A, C, D y E
  dependen de la recomposición del prompt.
- Títulos: todos de 50 caracteres o menos, sin «My», sin mayúsculas gritadas; ningún rótulo repite su título.
- Las cinco parejas, pasadas por las 24 preguntas del § 7 de la guía.

**Por confirmar (creador)**
- **Instagram** de RayWild: no está en su perfil. Sin él, se quita la línea.
- «**1 MONTH OLD**» (D): dice «a few weeks old, maybe let's say a month». Si prefiere, «WEEKS OLD».
- «**a pair** of Russian tortoises»: dice «we got two adults» y «at least a pair»; si no son macho y hembra, «two».
- «**Amazon Rainforest**» (C): la sala es una Várzea, el bosque inundable del Amazonas, que forma parte de la selva
  amazónica. Si le parece que exagera, `There's an Amazon Flooded Forest Behind This Door`.
- E: «two of our huge tortoises would be drowned» no deja claro si llegaron a estar en peligro; por eso el título no
  dice «Almost Drowned».
- **No hay fotos suyas** en `personal/reinoselva/recursos/creador/`: las caras salen de fotogramas, y cambiarles el
  gesto o la mirada arriesga el parecido (B y C lo piden: si sale otra cara, el retoque lo deshace). Con un juego de
  10–12 retratos (serio en calma, asombro con la boca cerrada, media sonrisa de quien sabe algo, mirando hacia arriba,
  de reojo a cada lado, palma abierta hacia arriba, ofreciendo algo a cámara con las dos manos, agarrando algo con
  fuerza, mueca de apuro; **ninguno señalando**), las miniaturas saldrán con su cara y el gesto que pida cada una.

**Lo que no puedo comprobar**: la miniatura final (la genera ChatGPT, no yo) y cuál gana: eso lo dice el test. El
estudio mide visitas frente a la mediana del canal, no el CTR.

## 6. Qué cambió respecto a la primera versión (13-nov)

- **El orden**: la paradoja de la tortuga rusa (antes E, de recambio) pasa a A. La inundación (antes D) baja a recambio.
- **Títulos**: fuera «My» (canal pequeño), las palabras en mayúsculas, el «!» y «(Here's Why)», que tranquilizaba.
  «Meet…» (verbo de presencia) pasa a «…Fits in One Hand» (choque entre lo más amenazado y lo diminuto). «Building the
  AMAZON, Asia & Africa for My Reptiles!!» pasa a «There's an Amazon Rainforest Behind This Door» (paradoja con su
  referente en la imagen; la ambición entera queda de recambio).
- **Miniaturas**: cada cara mira a la causa de su gesto, no a cámara (A con un fotograma nuevo, 6:42). La cría de D ya
  no posa: el instante es el ataque al grillo. C esconde la sala tras la puerta entreabierta. E pasa al instante
  bisagra (la obra a medias) y quita la mano que presentaba.
- **Prompts** con los bloques nuevos (instante, manos, «la primera parada del ojo») y el `DO NOT ADD` de la guía.
- Cada pareja lleva su segunda lectura en dos frases; hay tres títulos de recambio.
