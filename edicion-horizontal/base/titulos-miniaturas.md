# Títulos y miniaturas de YouTube — ESTÁNDAR

> Estándar de `edicion-horizontal`. Sale de mirar, vídeo a vídeo, unos 850 vídeos largos de quince canales (la mayoría,
> lo publicado en 1–2 años), con título y descripción en versión original y la miniatura original. Datos bajados el
> 2026-11-13 y el 2026-11-14; estudio al detalle del 2026-11-14 (19 informes cruzados regla a regla). Abreviaturas:
> - **Español (5)**: **RH** Rubén Holgado (viaje extremo) · **HC** HiClavero (viaje-reportaje) · **NO** Nil Ojeda
>   (series de lujo y reto) · **NV** Nico Villa (viaje por país, rioplatense) · **BC** byCalitos (lujo y estilo de vida).
> - **Inglés (10)**: **MB** MrBeast y **SM** Sidemen (retos) · **PC** Paul Cuffaro, **CW** Chandler's Wild Life, **BW**
>   Brave Wilderness, **FG** Forrest Galante y **CC** Colson's Critters (animales; CC es un canal pequeño, 82 k) ·
>   **BM** Ben Morris (viaje en solitario) · **BB** Back to Basics (supervivencia, pesca y caza) · **BZ** biaheza
>   (dinero y coches).
> - **Títulos de animales (5 más, 2026-11-14)**: **GB** La Granja del Borrego (español de Colombia: granja, cuidar fauna) ·
>   **FD** Field Days en español (supervivencia y caza, traducido del inglés) · **AC** AntsCanada (recintos-ecosistema en
>   casa) · **WW** Wickens Wicked Reptiles (reptiles en cautividad, listas) · **JF** Jacob Feder (zoo en el patio y
>   rescates). Solo el título y su encaje con la miniatura: `base/refs/_youtube/animales_titulos_2026-11-14.md`.
>
> Análisis, recuentos y hojas: `base/refs/_youtube/` (`CONTEXTO.md` dice qué hay). El cruce completo, con los apoyos y
> los contraejemplos de cada regla: `base/refs/_youtube/SINTESIS_2026-11-14.md` (léelo cuando dudes; aquí va lo que se
> aplica). Lo del creador (`personal/<creador>/preferencias.md` → «Títulos y miniaturas») manda sobre esto.
>
> **Cómo leer las cifras**: «x2,4» = ese vídeo tuvo 2,4 veces las visitas normales de SU canal. No es el CTR. En los 15
> canales el ratio lo explica antes el tema, la serie, el invitado o la época que el empaquetado: las cifras de aquí
> comparan dentro de lo comparable (mismo tema o serie; corregido por época cuando el canal crece o se apaga, y por la
> caída normal de cada episodio en una serie) y son indicios con recuento, no leyes. En 11 canales los éxitos tienen
> menos «me gusta» por visita: vienen de gente que no sigue el canal, que es justo a quien convence el empaquetado.
> «12 →» = 12 casos con esa mediana; «8/10» = en 8 de las 10 mejores. Si una regla choca con lo que el creador sabe de
> su público, gana él.

Con cada vídeo terminado y renderizado se entrega un **paquete de YouTube** (§ 8): **5 parejas de título + miniatura**
para probar (cada una con su prompt para ChatGPT y la imagen que hay que adjuntarle), la descripción con capítulos
(`base/descripciones.md`) y las etiquetas. Todo **en el idioma hablado del vídeo** (`IDIOMA` de `proyecto.py`, detectado),
no en el idioma en que te escriben. Claude no sube ni publica nada, y no genera la imagen: da el prompt y la referencia.

## 1. Qué decide el clic (léelo antes de escribir nada)

> **2026-11-17 — Las cinco parejas venden EL MISMO vídeo.** Cada título dice qué ES el vídeo (su promesa central: «doy
> de comer a todos mis animales», «visito el zoo X», «me paso el juego Y») y cambia solo el gancho que se añade (la
> cifra, el animal que no se fía, un detalle curioso entre paréntesis). Un momento de 30 s del vídeo (los caracoles, la
> señal de salud, las Tortugas Ninja) va como gancho DENTRO de la promesa, nunca como el tema del título: quien entra
> por «La señal de que tu tortuga está sana» espera un vídeo de salud, se encuentra 23 min de comidas y se va (y la
> prueba A/B compara vídeos distintos, no envoltorios). Prueba: tapa el vídeo y lee solo el título; ¿alguien sabría
> de qué van los 20 minutos? Si no, no vale. Las palancas distintas (pregunta 24) son ganchos distintos sobre la
> misma promesa, no temas distintos. Por qué: Lucas, alimentacion, «es un vídeo de alimentación de animales; los dos
> primeros títulos están muy bien, pero los otros tres tienen relación con el vídeo, pero no acaban de decir lo que
> realmente es el vídeo». **Causa:** criterio. Leí «cinco parejas con palancas distintas» como cinco temas distintos y
> convertí tres detalles del vídeo (C caracoles, D uratos, E Tortugas Ninja) en su tema; las dos buenas (A y B) eran
> justo las que mantenían «Doy de comer a +100 animales». (vídeo: alimentacion)
>
> **Cómo se lee el contexto antes de titular** (el método que dio los títulos buenos; Lucas: «ahora sí que me parecen
> buenos títulos»):
> 1. **La promesa sale de la escaleta, no de los momentos.** Mira los capítulos `S(…)` del EDL y la frase con que el
>    creador abre el vídeo, y escribe en UNA frase qué hace durante los 20 minutos y a qué escala: «doy de comer a los
>    +100 animales, recinto a recinto». Eso es lo que tiene que entender quien solo lee el título.
> 2. **Los momentos son ganchos, en otra lista.** La tabla de activos (frase literal, imagen, palanca) es de dónde salen
>    los paréntesis y los sujetos de la miniatura; ninguno es el tema.
> 3. **Cada título = la promesa (o una variante que diga lo mismo) + UN gancho distinto.** Variantes de la promesa:
>    «Doy de comer a +100 animales…», «Doy de comer a TODOS mis animales…», «Qué come cada uno de mis +100 animales».
>    Ganchos: la cifra, el animal que no se fía, «algunos comen caracoles vivos», «hasta a las Tortugas Ninja».
> 4. **La miniatura enseña la promesa EN ACCIÓN** (él dando de comer, los platos, los animales comiendo) con el gancho
>    como sujeto principal; no el gancho suelto fuera de su contexto.
> 5. **Prueba del tapado** antes de entregar: cada título, solo, ¿dice de qué van los 20 minutos?
> El paquete aprobado de alimentacion: A «Doy de Comer a TODOS Mis Animales (Más de 100)», B «Doy de Comer a +100
> Animales (y el Lagarto Caimán No Se Fía)», C «Doy de Comer a +100 Animales (Algunos Comen Caracoles Vivos)», D «Qué
> Come Cada Uno de Mis +100 Animales», E «Doy de Comer a Todos Mis Animales (Hasta a las Tortugas Ninja)».

1. **El tema pesa más que el diseño** (los 15). Quién sale, de qué va, la serie y el episodio, si la idea es nueva, el
   invitado y el destino explican más que la tipografía (NO: el peor episodio de su serie de lujo supera al mejor de las
   otras dos; BZ primer vídeo de cada idea x2,98 frente a secuelas x0,98). Pregunta antes qué apetece de verdad ver de
   este vídeo: si la respuesta es floja, ninguna miniatura lo arregla.
2. **Título y miniatura son UNA pieza** (abajo, «El encaje»). Ilustrar el título hunde cuando la imagen no añade
   **prueba ni nada en juego**: alguien posando junto a algo hecho, la postal, la cosa quieta que el título ya nombró
   (HC eco 11 → x0,59; BM 6/6 bajo x1; RH, BB). Ilustrar vale si la imagen **es** el morbo o la prueba de que es verdad
   y grande: el dolor en curso, el acceso envidiable, el famoso (BW «Bitten by…» con el bicho mordiendo x1,43). Lo
   mejor: que la imagen traiga una segunda cosa que el título no nombra (HC 8 → x1,51; BZ 9 → x2,02).
3. **La imagen nunca enseña el final** (9 canales: MB «después» 7 → x0,70 frente a «durante» 25 → x1,16; NV imagen que
   responde 10 → x0,66). El título sí puede contarlo si lo que queda es el **camino** (método, obra, compra, consecuencia
   sin decir el culpable) y la imagen se para antes: «I Bought a Failed Business and Turned it Around» (BZ x4,46).
4. **Se esconde el qué, nunca a la persona ni la cosa que se vende sin nada al lado.** Esconder sin ancla apaga (PC
   siluetas 0/16 por encima de x1,26; BW «WHAT IS IT?» x0,66; BZ pixelado x0,24). Se puede esconder **qué es** si (a)
   se ve la forma o la clase (silueta que dice «serpiente» pero no cuál; cifra pixelada con su signo y su orden: BZ 8 →
   x1,64), (b) hay un ancla de precio, riesgo o destinatario (etiqueta, arma que apunta, flecha al peligro: CC x7,11;
   BB la presa como sombra con el arpón apuntando x4,83), o (c) lo tapado es un juego que se puede adivinar (SM «GUESS
   THE…» x3,24). Nunca un «?» sobre algo que ya se ve. El dónde y el interior de un recipiente entero, sí se callan.
5. **Concreto = una propiedad que se ve o una paradoja**, no por fuerza un nombre propio. El nombre raro sirve si suena
   a criatura imposible y la foto lo confirma («Forest Lobster», BW x24,5, es un apodo de dos cosas incompatibles; con
   foto corriente, «Cave Alien» x0,66); si suena a catálogo, di lo que hace («Fish That Walk on Land» x2,44 frente a
   «FIDDLER CRABS» x0,73, CC). Lo vago hunde: «Ciudad» + adjetivo (HC 12 → x0,84), «NEW», «EXOTIC», «Rarest» (FG x0,35).
6. **Vende el bloque más fuerte, no el resumen**, o la promesa de totalidad («ALL of My… in ONE Video», PC x4,6; una vez
   al año). Listas, recopilaciones y «mejores momentos», lo peor en 7 canales (FG listas 16 → x0,62; BB «MOVIE» 7 →
   x0,74). Una recopilación solo se salva una vez y como reto con plazo terminado (CC «I Built… in 100 days!!» x5,8).
7. **La tensión la pide el género.** Aventura, retos y animales: peligro, esfuerzo, contacto. Lujo, estilo de vida,
   alojamiento o transporte: **deseo** («quiero estar ahí»), sin peligro (NO lujo 19/19 ≥ x1,66; BM tren-cama 4/4 ≥
   x3,68). Hunde siempre lo **resuelto con alguien posando** (MB 7 → x0,54) y el dinero como **coste para quien mira**;
   vende como espectáculo ajeno, regalo al creador, pérdida de alguien conocido (BC «-6000€» x3,23), objeto roto (BZ
   x5,54) o ganga imposible (RH «gratis» x2,69). Lo barato, como objeto (un coco, un hotel), no presupuesto (BM x0,66).
8. **Se promete lo que el vídeo cumple.**
   - **Norma de la casa** (no se discute con cifras): no se promete nada que el vídeo no tenga, y **nunca un famoso, un
     animal o un suceso que no esté en el vídeo**. Se exagera lo que hay: escala, color, nitidez, abundancia, juntar en
     una imagen cosas que pasan en momentos distintos.
   - **Lo que dicen los datos** (aparte, como dato): exagerar o inventar el decorado o el símbolo que hace literal lo que
     el vídeo cumple no se castiga en el ratio (12 canales: HC objeto inventado 16 → x1,34; BB generadas x1,39 frente a
     foto tal cual x1,02); inventar el suceso, la emoción, el animal, un peligro que el título no nombra o una estética
     de terror o fantasía, sí (BW escena que no ocurre ≤ x0,95 en 7; FG criatura inventada x0,30–0,70; BM famoso que no
     está x0,36). Cumplir la norma no cuesta clics; y aunque los costara, se queda.

### El encaje título + miniatura (lo más fuerte del estudio)

- **Busca la segunda lectura** (11 canales): la imagen sola dice una cosa; con el título, otra que **sube lo que está
  en juego**. Escribe las dos frases («la imagen sola dice…», «con el título dice…»); si son la misma, no la hay. El ojo
  da la imagen por entendida, el título la desmiente y hay que abrir para comprobar (BM 8 → x4,49; FG 8 → x2,43; HC 10 →
  x1,61; BB 9 → x3,77; NV sube 7 → x2,14 frente a explica 3 → x0,40). Ejemplo: un chico en una valla con sol y «2:17
  am» (BM x6,88). Dos condiciones: **en un solo paso**, sin saber nada de fuera (si pide contexto, BM 6 → x0,59), y **sin
  dejar al creador de verdugo** («We Shot an Antelope for Conservation.», BW x0,22).
- **Polos opuestos** (4): el título quita (privación, pérdida, «Failed») y la imagen da (abundancia, éxito, abrigo), o
  al revés (BB «…(No Food, No Water, No Shelter)» + pez enorme x14,91; BZ «Failed/Crashed» + lujo 6 → x4,52; BC «(me ha
  dejado)» bajo dos caras sonriendo x3,01).
- **Reparte** (4): lo grande en el título, lo exacto en la imagen; cada cifra en un solo sitio (BZ cifra solo en la
  imagen x5,62 frente a en los dos x1,31; MB dinero en 26/49 títulos y 0 cifras en la imagen).
- **Uno de los dos abre el hueco**: título nominal o de formato → la imagen carga con la curiosidad; título que lo cuenta
  todo + imagen que ilustra = nada (SM postal del formato 10 → x0,86).
- **Lo que el título nombra se ve, y nada lo desmiente ni lo delata** (5): ni monumento ni bandera si el título calla el
  sitio (RH 6/8 peores lo delatan; BM torre Eiffel x0,28), ni objeto moderno en un náufrago (BB 8 → x0,65), ni sonrisa
  bajo un «I Regret…» (BZ x0,65). Si se contradicen, gana la imagen.
- **Calla lo pequeño y nombra lo famoso** (7 y 5 canales, los dos idiomas). El topónimo, el dueño, el caso o el invitado
  que nadie conoce se cambian por su rasgo, estatus o arquetipo («de un multimillonario», «una isla remota»: BB
  arquetipo 8/8 ≥ x2,5 frente a topónimo 8 → x0,79; FG 0 nombres propios en 41). El país conocido, el suceso mundial y
  la persona que tira se nombran (HC actualidad mundial 5 → x1,99; BC famoso 7 → x1,99). «Este lugar» no es un rasgo
  (NV «Esta Ciudad…» x0,23).
- **Empaqueta para el desconocido** (6): nada que suponga ver el canal: nombres de casa, la mascota, compañeros fijos,
  «otra vez», «my tide pool» (CC 10 → x0,78; BM coprotagonista 6 → x0,39).

**Huecos de curiosidad que funcionan** (elige uno por pareja y dilo en una línea al proponerla):

| Hueco | El título da | La miniatura da | Queda sin decir |
|---|---|---|---|
| ¿Lo consigue? | la regla, el premio, el plazo | alguien que aún puede perder. Si el título da el plazo, el desgaste (cuerpo agotado, reloj de madrugada: SM «4:00» x1,31); si no, un día grande y no redondo («DAY 201»). Nunca la unidad del título («30 Days» → «DAY 29»: MB 6 → x0,91) | quién gana, si aguanta |
| ¿Qué le pasa? | el animal o el riesgo, con su nombre | el contacto, la marca en la piel (BW 11 → x2,24); si el público sabe que el daño llega, el durante | cuánto duele, cómo sale |
| ¿Qué es eso? | una propiedad imposible o un apodo | la cosa entera y nítida, sin el rasgo que permite nombrarla (envuelta, de espaldas: FG x3,43 frente a x0,82) | si es real, qué hace |
| ¿Cómo es por dentro? | de quién es, que es privado | con animales, el sitio lleno y ordenado (PC 23 → x1,42); con objetos, el continente por fuera + una pieza (BC yate x2,87) | la pieza estrella |
| ¿Cómo acabó así? | la consecuencia («…Sent Me to the Hospital») | la causa o el durante, con el daño a la vista (BW 3 → x4,01); nunca un final feliz | el camino |
| ¿Cuál gana? | los dos lados («Cheapest vs Most Expensive…») | solo el peldaño más alto, o una persona en cada mundo en una escena continua, una disfrutando a costa de la otra (SM x1,72). Las dos cifras, en el título o en la imagen (BM «$2»/«$2,000» x3,46) | el veredicto |
| ¿De verdad es tan…? | el veredicto («Japón es OTRO PLANETA») | una rareza que el título no nombra (NV x6,37); solo si hay prejuicio o fama que desmentir | las pruebas |
| ¿De nada a esto? | la privación o el fracaso («No Food, No Water…», «Failed») | la abundancia, el éxito, el abrigo | el cómo |
| Enséñamelo | el hallazgo, si contradice algo famoso o un récord («Qatar 4 Años Después del Mundial (no hay nadie)», HC x2,6) | el sitio; nunca un rótulo «no hay nadie» sobre el vacío (RH x0,48; vacío a secas, BM x0,17–0,41) | verlo |
| ¿Qué pasará ahora? (animales) | lo que ha metido, soltado o conectado en el recinto («I Added a PYTHON into…», «I Released Birds Into…») | el instante antes de la consecuencia: la jaula abierta con los pájaros dentro, el depredador entero junto a lo que se puede comer (AC 3,70 y 2,56) | qué hace dentro, qué se come |

### Animales: qué se vende (léelo antes de titular un vídeo de animales)

Once canales de animales (PC, CW, BW, FG, CC, BB y los cinco del 2026-11-14). Hasta esa fecha los títulos de animales de
la skill se desviaban: cogían la gramática del viajero o del reto («Me Di 1 Hora para…», «Dormí 24h en la Jaula de…»,
«Intenté Salvar Plantas de…») y ponían de protagonista la hazaña del creador, un animal pequeño o vago, o ningún animal.
Detalle y cifras: `base/refs/_youtube/animales_titulos_2026-11-14.md`.

1. **El producto son los animales, no la hazaña del creador.** El «yo» rinde solo haciendo algo **con un animal grande
   que se nombra** (GB «CUIDANDO LEONES RECIEN NACIDOS POR 1 DIA» 2,95); el «yo» con una condición inventada y sin animal
   delante, por debajo (JF «I + verbo» 0,79 frente a «My [animal] + suceso» 1,58; WW «I/My» 0,72 frente a nominal 1,17).
   Ninguna condición artificial («en 1 hora», «con 10 €») si el vídeo no es un reto de verdad.
2. **En un vídeo de animales, el título lleva un animal** (o la colección, o el recinto que los aloja). Obra, jardín o
   plantas sin destinatario, por debajo (AC «Forming The Trees…» 0,49; JF obras 0,67). **Matiz (Lucas, 2026-11-14): en un
   vídeo de obra o de arreglos de un canal de animales, el animal va en el título solo si sale de verdad en el vídeo y
   forma parte de lo que está en juego** (Safira estorbando la obra de su propia selva; el recinto de sus animales sin
   luz). Si solo se nombra o apenas sale, **manda el gancho propio del vídeo** (el plazo, el obstáculo, la paradoja) y el
   título no se alarga con un destinatario de relleno («…el Estanque de Mis Peces» con peces diminutos que no cuentan
   nada). Por qué: al rehacer `1311` y `prueba-3` apliqué esta regla de forma mecánica; dos de los títulos quedaron peor
   que los de antes (más largos, perdían lo que estaba en juego) y otros dos dependían de unas tortugas que no salían en
   el vídeo, lo que choca con el § 1.8.
   **Y siempre, el título dice de qué va el vídeo** (Lucas, 2026-11-14: «si no, la persona va a entrar y el vídeo no
   tiene nada que ver»): la obra, el arreglo o el tema que ocupa la mayor parte del vídeo se reconoce en el título (las
   luces, el estanque, el recinto). El animal se **suma** como gancho a ese tema («Mi Lagarto Caimán No Me Deja Arreglar
   las Luces»), nunca lo **sustituye** («Mi Lagarto Caimán se Ha Quedado sin Luz» desplaza el vídeo hacia el lagarto; «Un
   Pájaro Salvaje Estrenó Mi Estanque» vende 7 segundos de un vídeo de plantar). Prueba: quien entra por el título, ¿se
   encuentra en el primer minuto lo que esperaba?
3. **El animal grande o peligroso se nombra por su nombre** (pitón, jaguar, oso, cocodrilo, sulcata gigante): «a PYTHON»
   2,56 frente a «a Green Predator» 0,72, mismo molde (AC); «el oso» 1,73 frente a «el pájaro» 0,76, mismo molde (GB).
   «Pájaro», «bicho», «criatura» a secas, no. El genérico solo si promete **totalidad** («Todos Mis Animales», «ANIMALES
   SALVAJES»: GB 1,28) o si la imagen lo concreta de cerca (JF «BLOOD SUCKING CREATURES» x9,26). Nunca callado en el
   título **y** en la imagen (AC 0,59).
4. **El animal pequeño no es el gancho del título** salvo que la miniatura lo agrande (AC araña y termita de montaje
   2,40 y 2,03; a escala real, «Fighting Rhino Beetles» con tanque vacío 0,40). Invertebrados, ratas, peces comunes y
   pájaros pequeños rinden menos en cuatro canales.
5. **Lo que más vende, por este orden de fuerza** (cada uno con su condición, en los moldes del § 4–5): la **colección
   entera** una vez (JF 4,00 local en 8 casos; WW x6,86; PC x4,6); **el nacimiento**, primer capítulo (JF x3,99–4,82; GB
   crías 1,72); **la pérdida en la colección sin decir cuál** (JF «…We Lost Animals !» x6,20; WW «I Euthanized My Snakes.
   Heartbroken!» x9,24); **el depredador que entra en el recinto** (AC); **la obra con superlativo cierto o desproporción
   para un animal** (AC 6/6 ≥ 1,7; GB «…PARA MI EJERCITO DE RANAS» 2,11; JF tobogán para el jaguar x3,06); **el rescate
   con la emoción en el título y la víctima en la imagen** (JF x12,7); **el cuidador por un día** de un animal grande (GB);
   **la ventana documental** «Así Viven los [X] en [lugar con noticia]» (GB 3,99); en canales de cría, **el veredicto que
   salva de un error** a quien quiere tener uno (WW «Top 5 WORST Beginner Reptiles | Get These Instead!» x4,02).
6. **Abajo**: la rutina (dar de comer, dormir, «UPDATE»: WW 0,47, AC 0,68), la rareza o «nunca has oído hablar de…» (WW
   0,81; FG «Rarest» x0,35), la compra o la llegada a secas (JF x0,44), el zoo o el acuario ajeno (JF x0,32, AC 0,42), el
   rescate ya resuelto («How I Stopped…», «Here's How We Saved Him!»: AC 0,76) y el final contado («NO PUDE ATRAPAR…»,
   «(we got stung)», «Successfully»). «Por Fin» / «FINALLY» sí, cuando cierra una espera que el público siguió y la imagen
   pone el durante (JF 8 → 1,43).
7. **El reparto con la miniatura**: el título pone la causa o el marco (lo que metió, el plazo, el lugar, la tragedia) y la
   miniatura el animal **grande, entero y en el instante anterior a la consecuencia**, o el incidente que el título calla
   (la herida, la boca abierta con su mano dentro, el pez enorme bajo «sin comida»). Título, rótulo e imagen diciendo lo
   mismo es lo que más se repite en las peores (GB 6/10, JF 5/10, WW 5/10). **El animal que nombra el título sale en la
   imagen siempre** (AC 5/5 en las mejores, 0/6 en las peores: en una tarrina o pequeño).
8. **Palabras de fuera del nicho**: «playa», «selva», «río», «en casa», no la jerga del aficionado («vivario»,
   «ecosistema», «várzea», «paludario»): AC «Giant Indoor Lagoon Beach» 2,28 frente a «Giant Lagoon Ecosystem Vivarium» 1,14
   con la misma obra.

## 2. Método (en este orden)

1. **Reúne lo que sabes del vídeo**: el `edl.py` entero (qué se dice y en qué orden), el registro visual,
   `trabajo/descartes.md`, los capítulos (`capitulos.py`), el perfil y las preferencias del creador y, si lo hay, el
   estudio de SU canal (§ 9). Comprueba el idioma (`IDIOMA`).
2. **Mira dónde cae el vídeo en el canal**: sus últimos ~10 títulos y miniaturas, para no repetir la sorpresa, el molde
   ganador ni la paleta (la segunda vez rinde la mitad: PC x4,6 → x1,97); si abre una idea, un país o una serie (el
   primero rinde más, BZ x2,98: ahí va el empaquetado más fuerte) o es una secuela (§ 3); qué tipo de canal es (§ 5).
3. **Haz la lista de activos** (6–10): cada hecho fuerte con (a) la frase literal en que se dice, (b) si hay imagen que
   lo pruebe y en qué minuto, (c) qué palanca toca:
   - tensión o asombro: extremo, riesgo, rareza, reto, suceso, transformación, totalidad, acceso a lo vedado;
   - deseo: abrigo o lujo que apetece (BM tren x5,01; BZ refugio x4,99), lujo ajeno que le dejan al creador (NO «Me
     Invita» x3,97), dinero como espectáculo ajeno o ganga imposible;
   - otras: «lo pruebo por ti» (BM 18 → x1,64), la vida de otros mejor que la propia (HC 7 → x1,51 frente a 5 → x0,84),
     el espejo con el país del público (NV), la relación entre dos personas conocidas (BC), el regodeo y la complicidad
     (SM), el tabú alimentario (BB), la ternura.
   Lo que no tiene imagen propia puede ir al título, no a la miniatura.
4. **Elige 5 ángulos DISTINTOS** (no cinco redacciones de la misma idea): cada pareja tira de una palanca diferente o
   vende un bloque diferente. Así el test enseña qué le importa al público (una plantilla fija aplana: NO x0,78–1,32).
5. **Escribe cada pareja a la vez**: título + qué se ve y en qué instante + texto de la miniatura (si lleva) + **las dos
   frases de la segunda lectura** + la pregunta que deja abierta. Pásale la prueba del § 7.
6. **Prepara la cara** (molde único, § 6; G010): UN retrato limpio del creador, de frente, mirando a la lente, ojos
   abiertos y boca cerrada. Primero `recursos/creador/` (`miniatura.py fotos` / `foto`); si no hay, el fotograma más
   limpio así (`miniatura.py momentos` → `miniatura.py sacar A <mm:ss> …` → mira `A_rafaga.jpg`) o una miniatura suya
   publicada en la que salga así. Luego `miniatura.py cara A` (el recorte grande, ≥ 1024 px). La misma pareja de
   imágenes vale para las cinco miniaturas. Del vídeo **no** se adjunta la escena.
   - **Una imagen más, solo si algo tiene que ser EL real**: su perro, su animal con nombre, un objeto o producto
     concreto que es el gancho. Sácalo de cerca con `miniatura.py sacar` (el mejor primer plano puede no estar en el
     montaje: búscalo en el registro visual, `recurso: 3`, y sácalo con `CLIP@segundos`).
   - **Lo que no se entiende en un segundo a 168 px no es miniatura**, por fuerte que sea en el vídeo: elige otro
     activo o haz literal el gancho con un objeto (regla 26).
7. **Escribe el prompt** de cada miniatura (§ 6, «El prompt»): una escena nueva que cuenta el gancho, con el esqueleto.
8. **Descripción, capítulos y etiquetas** (`base/descripciones.md`).
9. **Entrega** (§ 8): di cuáles tres probarías primero y por qué, y deja 2–3 títulos de recambio por si el vídeo arranca
   flojo (CC retitula 19 de 45; BM, BZ y MB también cambian títulos publicados).

## 3. Títulos: lo que vale en los dos idiomas

| Regla | Por qué y evidencia |
|---|---|
| **El gancho entero, en los primeros ~50 caracteres.** Detrás, lo que añade (regla, magnitud, paréntesis, «\| Ciudad»). Falla poner delante la etiqueta de episodio o el sitio y el gancho al final | lo largo no se castiga (BB > 60 car. 12 → x1,26, su mejor tiene 92; FG 6 de sus 10 mejores pasan de 55); en moldes de golpe, corto (BW ≤ 35 car. x1,18) |
| **Empieza por un marco que se reconozca** (fórmula, país, nombre famoso); nunca por algo desconocido ni por una etiqueta de serie. El gatillo suele cerrar («…(no hay nadie)», «…de 1 Metro² en Japón») | HC «Kensington: …» x0,89; «Así es…» y «Por qué…?» de arranque, NV 0/12 mejores y 5/8 peores |
| **El verbo promete una acción con resultado, coste o cuerpo**: Gasté, Sobreviví, Dormí, He Comprado, I Bought, I Stayed. Nunca una presencia o un proceso: Visité, Busqué, Aprendí, I Visited, I Tried, Living, Catching. En retos, verbos de padecer, no de dar | 8 canales: BM verbo de cuerpo 9 → x3,68 frente a turista 18 → x0,93; RH «Gasté» x1,89, «Aprendí» x0,57; MB y SM, verbos de dar en 0/12 mejores y 4/8 peores |
| **El experimento necesita condición**: «…with $0», «as a Complete Beginner», «for 24 Hours» | sin ella, «lo probé» no promete nada: BZ «I Tried» a secas 6 → x0,39; «(Complete Beginner)» x5,62 |
| **Una paradoja dentro del título**: cosa humilde + superlativo, dos términos que chocan, un apodo imposible, un estatus roto junto a lo caro (Failed, Crashed, de Carretera) | no se resuelve sin ver (6 canales): «El Hotel de Carretera más lujoso de España.» (BC x3,33); «I Visited the World's Biggest City Nobody's Heard Of» (BM x3,47) frente a «Secret Island Nobody's Heard of» (x0,3); BZ estatus roto 6 → x4,52 |
| **Superlativo solo de algo que se ve** (tamaño, peligro con contacto, condición física de la gente), y cuanto mayor el mundo del récord, mejor. Nunca de belleza, opinión, rareza genérica, ausencia ni sensación propia | CC «World's Largest» x7,11 > «America's Largest» x2,90 > «THIS HUGE» x1,81; BW genéricos 14 → x0,69; BM «Emptiest» x0,17 |
| **Una sola idea.** «y» de consecuencia o escalada, sí; lista de actividades o temas, no | «…and Turned it Around» x4,46; «King Cobras & Crocodile EAT Pythons!» x2,94; «(Catch, Clean & Cook)» x0,43; «NERVIOS, CAOS y TENSIÓN…» x0,17 |
| **La cifra mide lo que está en juego** (plazo con resultado, tamaño, desproporción «ONE Giant Fish / Entire Village», algo que se imagina con el cuerpo), nunca cuánto contenido hay. Siempre con dígitos. Que haya premio cuenta; su tamaño, no | «71 Days» BB x1,96; «1 Metro²» HC x2,27; «5 Animals…» FG 17 → x0,59; «N Days Living…» BB 20 → x0,72; MB $1,000,000 5 → x0,80 |
| **Sin hashtags.** Emojis y «\|» no aportan; el «\|», solo como cola de búsqueda tras el gancho en series por país | 0 hashtags en los 15; NV «\| Ciudad» x1,49 frente a x0,96 |
| **Qué puede adelantarse**: que algo sale mal o un **hecho** que da la vuelta a la imagen. Nunca una valoración, quién gana ni cómo termina | «(I Regret This)» PC x4,1; «(me ha dejado)» BC x3,01; «(mala idea)» NO x0,53 |
| **Series**: el número de episodio, fuera del título o al final; el episodio con gancho propio, como vídeo suelto. «More», «Part 2», «THE MOVIE» bajan; el regreso, solo si el formato ya gustó («IS BACK»). Delante, solo una etiqueta de género que ya es la promesa («SURVIVAL CHALLENGE:») o la marca de un grupo que ya vende | 6 canales: BC «- Episodio N» 15 → x1,00 frente a sueltos x1,36; BB «[EP:n]» delante x0,94; FG «More» 3/3 ≤ x0,51; SM regreso 9 → x1,31; BB etiqueta 9/9 ≥ x1,75. Sobre el número en la miniatura no hay datos |
| **Una fórmula ganadora rinde la mitad la segunda vez**: repite el molde con un sustantivo nuevo, nunca la sorpresa; un giro ganador, una vez por tanda | 7 canales: PC x4,6 → x1,97; NV «te va a volar la mente» x2,68 → x1,31 |
| **Que se entienda sin la miniatura**: con la categoría (Porsche, casa, cárcel) o un nombre que tire; «este» o «así», solo con su referente en la imagen. TODO EN MAYÚSCULAS ni suma ni resta (es marca). Ni minúsculas como norma ni tono de comunicado | «¿Comprarías Este Porsche 911?» BC 4 → x1,74; «The YouTube Hamster Wheel» BZ x0,39; BZ minúsculas x0,27; «We Shot an Antelope for Conservation.» BW x0,22 |

**Si el creador da el título**, se respeta tal cual y se trabaja la miniatura para ese título.

## 4. Títulos en ESPAÑOL

Por defecto, español de España; si el creador es de América o habla a ese público, su variante (abajo). Detalle y
plantillas: `base/refs/_youtube/titulos_es.md` (primera tanda: sus frecuencias no dicen qué rinde; si choca, manda esto).

**Cómo suena natural**
- **Verbo en primera persona, en pasado y sin sujeto**: «Fui», «Gasté», «Sobreviví», «Dormí». Nunca «Yo fui…». Decide
  el verbo (§ 3): «Visité», «Busqué», «Participé» son lo más plano (HC 9 → x0,82). El perfecto para una compra o una
  noticia personal reciente («He Comprado Mi Primer Porsche 911», BC x1,42). En lujo y estilo de vida, mejor el título
  **nominal**, que admite punto: «Esta es Mi Casa Definitiva.» (BC con punto 9 → x1,78 frente a x1,10).
- **El país conocido, de sujeto de un verbo fuerte** («Japón es OTRO PLANETA», «China YA VIVE…»; NV país delante 23 →
  x1,34 frente a x0,80). El sitio desconocido, de complemento de un verbo con resultado (HC «La Ciudad donde…» sin verbo
  7 → x0,77; con «Visité/Investigué» delante, x1,37).
- **Superlativo con artículo y detrás** («el/la [SUSTANTIVO] Más [ADJETIVO] del Mundo»), solo si **choca** con su
  sustantivo o es una condición visible de la gente (HC «más Pobre» x1,65 frente a «más Peligroso» x0,59). A secas es el
  más usado y no rinde (RH 27 → x0,91; HC x0,85; NO x0,88).
- **Las contracciones cuentan**: «Fui al…», «Fui a la…», «Sobreviví al…». Sin ellas suena a errata.
- **Calla el topónimo pequeño y di su rasgo** («el País que te Paga por Visitarlo»; RH: 8 de sus 10 mejores no nombran
  el sitio); nombra el marco famoso (§ 1). El nombre, en la primera línea de la descripción o en la miniatura.
- **Giros que ya son molde, con su condición**: «Así es Vivir en…» solo con la vida de otros en una condición extrema o
  una cifra imposible (HC 5/5 ≥ x1,4), nunca «Así es [ciudad]» (NV 6 → x0,57); «…No Es Como [Me Contaron]» solo con un
  prejuicio fuerte (sin él, NV x0,96); «te va a volar la mente» se gasta; «¿Real o Trampa?» (HC x1,83, un caso).
- **Tuteo** siempre que se hable al que mira («que te Paga», «¿Comprarías…?»).

**Ortografía y forma**
- **Mayúscula en Cada Palabra, a la española**: sustantivos, adjetivos, verbos y adverbios con mayúscula; en minúscula
  «de, del, la, el, los, en, a, al, con, por, que, y, un, una, te, se». «Fui al País que te Paga por Visitarlo».
  Poner mayúscula también a «Un», «Es», «Lo» es calco del inglés.
- **Una o dos palabras en MAYÚSCULAS** solo si es el estilo del creador, y sobre el **predicado o el veredicto** («OTRO
  PLANETA», «SE HUNDE»), nunca sobre el país ni el sustantivo del tema (NV; su Title Case plano: 6/6 ≤ x0,74).
- **Paréntesis en minúscula** que añade un **hecho** que da la vuelta («(me ha dejado)»; «(no hay nadie)» tras un sitio
  famoso). Nunca una valoración, un aviso vago ni lo que ya dice el título (HC 5 → x0,86; «(Pero CUIDADO)» x0,13).
- **Tildes todas. Pregunta con «¿…?»**. Sin «¡!» en España: norma de corrección, no de rendimiento (en rioplatense y en
  el registro de NO no resta: NV #17 x4,79). El punto final, como marca de estilo o en título nominal.
- **Cifras**: símbolo detrás y pegado («1000€», «25.400€», «60.000$»), punto de millar, «24h/50h».
- **Lo que suena traducido**: gerundio inicial («Comprando Peces para Mi Estanque»; además anuncia proceso: en BC
  ninguno pasa de x1,15), «Yo…», «vs» (0 de 279: el contraste va con «el Mejor y el Peor…» o con dos vídeos gemelos),
  inglés sin necesidad («Tour», «Outfit»). «Billonario» es calco, pero no resta en su público (NV x4,71; NO x2,99).
- **América** (NV, argentino; un canal): presente («Visito», «Exploro», x1,42), voseo, «acá», «$1 DÓLAR» con el símbolo
  delante, «!» sin daño. Estructura (país delante x1,34; «| Ciudad» de cola x1,49 frente a x0,96):
  `[PAÍS] + verbo en presente + GATILLO EN MAYÚSCULAS + bandera + coletilla + | Ciudad`.

**Moldes que mejor salen, con su condición** (rellena el hueco con lo del vídeo)

| Molde | Ejemplo real | Cuándo |
|---|---|---|
| `Fui al [País / Pueblo] que [HECHO QUE TE AFECTA]` | «Fui al País que te Paga por Visitarlo» (x2,69) | un hecho comprobable que parece imposible (sustantivo que se contradice: RH x1,54–2,69 frente a descriptivos x0,48–0,90) |
| `[Fui a / Visité] [el/la SITIO] Más [ADJETIVO] del Mundo` | «Fui al Pueblo Más Peligroso del Mundo» (x2,39) | solo si el superlativo choca o es de condición visible; a secas, mediana x0,91 (RH) |
| `[Visité / Investigué] [el SITIO] donde [HECHO INSÓLITO]` | «Investigué la Ciudad donde Escapan de Corea Del Norte» (x1,96) | el hecho se agarra a algo que todos conocen (HC 7 → x1,37; curiosidad local x0,77) |
| `Sobreviví [N]h [GERUNDIO] Solo [CONDICIÓN]` | «Sobreviví 50h Comiendo Solo lo que Pesco» (x1,95) | reto con regla de cuatro palabras y plazo |
| `[N] Días [Entre / Con] [X]` | «21 Días Entre Millonarios» (x3,78) | solo si [X] es un mundo deseado o un récord; la estancia a secas es el suelo (RH x0,73) |
| `[PAÍS] es [METÁFORA DE DOS PALABRAS]` | «Japón es OTRO PLANETA» (x6,37) | una idea lo resume todo |
| `[SITIO] No Es Como [Me Contaron]` | «El Salvador NO ES como ME CONTARON» (x2,69) | solo con prejuicio previo fuerte |
| `Así es Vivir en [SITIO] de [DATO IMPOSIBLE]` | «Así es Vivir en un Cibercafé de 1 Metro² en Japón» (x2,27) | la vida de otros en una condición extrema, con alguien de allí en la imagen |
| `[SITIO CONOCIDO] [N] Años Después de [HECHO] ([lo que hay])` | «Qatar 4 Años Después del Mundial (no hay nadie)» (x2,6) | el hecho fue noticia para todos (en clave personal, BC x0,91) |
| `El Mundo Privado de [X]` · `Detrás del Mundo de [X]` | «Detrás del Mundo de los Barcos de Lujo.» (x2,87) | [X] lo conoce todo el mundo y la imagen no tapa lo prometido (de nicho y tapado, x0,87) |
| `[RICO] Me Invita a [SU LUJO]` · `La Lujosa Vida de [FAMOSO]` | «Niño Millonario Me Invita a Su Avión Privado» (x3,97); «La Lujosa Vida de Coscu en Argentina» (x4,26) | lujo prestado: permiso para entrar; el dueño con nombre o estatus (sin él, x0,59 y x0,44) |
| `Gasté [N]€ en [SITIO DONDE NO SABES QUÉ TE LLEVAS]` | «Gasté 1000€ en Trasteros Abandonados» (x1,89) | compra con sorpresa: el lado barato, o lo que pierde alguien conocido (BC «-6000€» x3,23) |
| `Fui a [Pescar / Buscar / Cazar] [ANIMAL CON APODO]` | «Fui a Pescar Monstruos de Río» (x2,44) | el animal tiene un apodo que ya asombra |
| `[PLAN] con [FAMOSO] ([giro personal])` | «Un Día de Compras con Leto (me ha dejado)» (x3,01) | el peso lo lleva el nombre (sin famoso, x0,88–1,12); el giro puede ir en la miniatura |

**Animales, recintos y proyectos en español.** Lee antes «Animales: qué se vende» (§ 1). En español hay dos canales de
animales en la muestra, ninguno de España: GB (Colombia; con recuento propio) y FD (traducción literal del inglés; sirve
sobre todo para ver qué delata el calco). Lo demás son los moldes en inglés del § 5, **pasados a gramática española, no
calcados** (adaptación sin recuento propio: márcalo así).

| Molde en español | De dónde sale | Cuándo |
|---|---|---|
| «24 Horas Cuidando [ANIMAL GRANDE o CRÍAS] ([giro corto])» · «Un Día Cuidando [ANIMALES]» | GB «CUIDANDO LEONES RECIEN NACIDOS POR 1 DIA (COMEN BORREGOS)» 2,95; «PASO 24 HORAS CUIDANDO ANIMALES SILVESTRES» 2,42 | un día en un papel con un animal que impone; el giro, un hecho (no el final); la miniatura, el incidente (herida, ataque) |
| «Así Viven los [ANIMALES] en [LUGAR QUE YA ES NOTICIA]» | GB «ASÍ VIVEN LOS HIPOPÓTAMOS EN COLOMBIA» 3,99 (con acuario corriente, 0,87) | la especie fuera de su sitio o el lugar remoto; el creador no es el sujeto; el peligro lo pone la imagen |
| «Encontré el [ANIMAL IMPONENTE] Más Grande de [REGIÓN]» | GB oso 1,73 frente a «pájaro» 0,76, mismo molde | solo si el superlativo es cierto y el animal tiene nombre fuerte |
| «¡Ha Roto el Huevo! (así nace el [ANIMAL POR SU RASGO] más [X] del mundo)» · «Mi [ANIMAL] Está a Punto de Parir» · «Por Fin Ha Parido Mi [ANIMAL]» | GB 1,85; JF parto x3,99–4,50 | nacimientos: el primer capítulo; los hitos siguientes, con su propio gancho |
| «Construí un [OBRA] para Mi Ejército de [ANIMALES]» · «Le Construí un [OBRA DESPROPORCIONADA] a Mi [ANIMAL]» | GB ranas 2,11 (cifra «+100 MIL» en la imagen) frente a abejas 0,68 (imagen que repite) | la desproporción se ve y se cuenta; la imagen trae la cifra o la escala, no ilustra el título |
| «Construí la [Selva / Playa / Laguna] Más Grande que He Hecho en Casa» | AC obra superlativa 6/6 ≥ 1,7 (adaptación) | obra nueva con superlativo cierto; la miniatura enseña los animales que vivirán dentro |
| «Metí una [ESPECIE CON NOMBRE FUERTE] en Mi [Selva / Estanque] Gigante» | AC «I Added a PYTHON into…» 2,56 (adaptación) | entra un animal grande o depredador; la miniatura, el segundo antes de soltarlo |
| «Se Inundó Mi [RECINTO]… Hemos Perdido Animales» | JF x6,20; CW x2,06 (adaptación) | suceso real en la colección; la imagen, la crisis, nunca cuál murió |
| «Todos Mis [ANIMALES] en un Solo Vídeo» · «Doy de Comer a Todos Mis Animales» | JF x9,15, PC x4,6 (adaptación) | la colección entera, una vez; miniatura-catálogo ordenada con un animal grande en contacto |
| «El Rescate Más Triste que He Hecho» | JF x12,7 (adaptación) | el título calla el animal; la miniatura lo enseña herido (y mejor con crías) con el creador al lado |
| «Las 5 Peores [Tortugas / Serpientes] para Empezar (y Cuáles Tener)» | WW x4,02; callar la alternativa x3,65 frente a nombrarla x0,79 (adaptación) | canales de cría: el veredicto que salva de un error, categoría amplia |
| «Cazo un [ANIMAL GRANDE] con [HERRAMIENTA QUE NO LE PEGA]» · «Si No lo Pesco, No Como» | FD arco + cangrejo 5,67; la regla 3,06 frente a la crónica 0,60 | supervivencia, pesca, caza: cómo lo caza, no cómo se lo come |
| «[DEPREDADORES] se Comen [PRESA]» | CW (adaptación) | en plural, o con un segundo depredador |
| «Me Mordió [ANIMAL]» | BW (adaptación) | el presentador recibe el daño |
| «Dentro del [SITIO] Privado de un Multimillonario» | FG, PC (adaptación) | acceso a lo vedado, dueño con estatus |

**Cómo suena en España en un título de animales** (GB y FD: lo que delata otra variante o el calco):
- «¡» de apertura si hay «!»; tildes también en mayúsculas («ASÍ», «MÁS», «DÍA»).
- **Perfecto para lo que acaba de pasar en la colección** («Me Han Robado la Vaca», «Se Me Ha Escapado la Pitón», «Mi
  Sulcata Ha Puesto Huevos»); indefinido para la hazaña terminada («Construí», «Metí», «Encontré»).
- Léxico de aquí: león marino, cebo, hoguera, reto, acampada, madre, animales salvajes (no lobo marino, carnada, fogata,
  desafío, camping, mamá, silvestres).
- Calcos de animales y campo: «Atrapando y cocinando…» / «Atrapé y cociné» (*catch and cook*: «Pesco y cocino…»),
  «hambriento y sediento», «…y esto pasó» («…y pasó esto»), «Viviendo de la tierra», «(crudo y sin editar)» («sin
  cortes»), «vivario» («terrario», «mi selva»).

## 5. Títulos en INGLÉS

Detalle: `base/refs/_youtube/titulos_en.md` (primera tanda, con moldes y plantillas) y `titulos_en_2.md` (FG, BM, BB,
CC, BZ). En inglés, cómo suena un título depende más del **género** que del idioma.

**Cómo suena natural**
- **Animales y concursos: telegráfico**, sin sujeto, auxiliar ni artículos («BITTEN by a Vampire Bat!», no «I Was
  Bitten By A Vampire Bat»). **Experiencia propia** (viaje, prueba, compra-reventa): **«I» + pasado con un verbo de
  compromiso** (BM 28/36 empiezan por «I», x1,11 frente a x0,49; BZ sus 10 mejores). Decide el verbo («I Spent…» x1,53,
  «I Built» x0,48, MB).
- **Gerundio inicial solo de un suceso o de algo que cambia** («Feeding…», CW 9 → x1,34; «Rescuing…» con cifra); nunca
  de rutina o estancia («Living», «Camping», «Catching»: CW 9 → x0,75; BB «Living» 12 → x0,78).
- **Pasiva sin sujeto** para lo que te pasa («BITTEN by…», «STUNG by…», «CAUGHT in…»: BW 8 → x1,36) y **participio
  de catástrofe** («Shipwrecked», «Castaway», «Plane Crash»: BB 6 → x3,69).
- **Retos**: el gatillo es el obstáculo, justo tras el verbo; el premio, coletilla (con «$» x1,12, sin él x0,83 en MB;
  su tamaño no cuenta). «I Spent / I Survived [N] Days» solo con una condición de privación (sin ella, BB 20 → x0,72).
- **«My…»** solo si el mundo del creador ya es conocido (PC, canal grande; en CC «my» 19 → x0,73 frente a x1,26). Más
  fuerte: el **genitivo de un dueño-tipo ajeno** («an Indian Billionaire's…», «Florida's $1M…»: FG en 7 de sus 10
  mejores, 0 de las 10 peores).
- **Superlativo delante y con dueño** («World's…», «Australia's Most Controversial Shipwreck», BB x14,91), con las
  condiciones del § 3. «…on Earth», «…EVER» solo tras un superlativo físico (el genérico «Weirdest Bugs on Earth», BW x0,65).
- **Adjetivos delante y apilados sin preposiciones** («Indian Billionaire's Private Wildlife Rescue Center»); el lugar o
  el dueño, al final. **«The» + nombre único** gana a «a/an» + genérico («Inside The Pyramids» x1,53 frente a «In An
  Ancient Temple» x0,82; indicio de MB).

**Ortografía y forma**
- **Title Case limpio por defecto.** Palabras EN MAYÚSCULAS solo si son el estilo del creador: FG, BM y BZ no gritan
  ninguna en 118 de 119 títulos; CC con mayúsculas x0,76 frente a limpio x1,17; en ninguna tanda gritar sube.
- **El «!» es estilo de casa, no del género**: FG (animales) 0 de 41, BM 0 de 36; CW sin «!» x1,44; BW sin él baja.
  «!!» en todos deja de ser énfasis (PC 125 de 140, misma mediana). **«…»** solo tras una mala noticia.
- **Paréntesis final** que añade una regla (mejor en tríada negativa: «(No Food, No Water, No Shelter)»), una magnitud
  («(750,000 Gallons)», PC x3,91), una consecuencia («(I Regret This)»), un nivel («(Complete Beginner)») o un aviso que
  sube el riesgo («(Do Not Attempt)», BW 3 → x2,58). Nunca el menú, el formato, la parte ni algo que tranquilice
  («(Pt. N)», «(Finally)», «(No Budget)»: PC ~27 → x0,95).
- **Cifras**: signo delante, coma de millar, unidades pegadas («6ft», «65lbs»). Abreviar vale («$1M», FG x2,53): cuenta
  que la cifra esté y sea desproporcionada. «vs» abreviado, «Pt. 2», «ft.».
- **Lo que suena traducido**: artículos y sujetos de más («I Am Buying Some New Fish For My Pond»), «of the world» (es
  «in the World» o «World's…»), «250.000 $», «versus», «Part 2», «featuring», «with Prime Minister of UK». El registro
  documental (FG) conserva artículos sin daño.
- **Relleno que no sube**: «NEW» pegado al ejemplar comprado (PC 28 → x0,92; pegado a un sitio nuevo no estorba: «My NEW
  Freshwater STINGRAY Pond», CC x5,66), «(Finally)», «for My POND» en todos, «You won't BELIEVE…» (CW x0,52), «THIS» sin
  sustantivo (vale con uno paradójico que la miniatura enseña: «…Cross this Invisible Line», FG x4,21).

**Moldes** (los de animales, recintos y proyectos primero: es lo más cercano a un vlog de naturaleza)

| Molde | Ejemplo real | Cuándo |
|---|---|---|
| `ALL of My [THINGS] in ONE Video!!` | «ALL of My EXOTIC ANIMALS in ONE video!!» (x4,6) | repaso completo; una vez al año y con algo nuevo delante (la segunda vez, x1,97) |
| `FEEDING MY EXOTIC ANIMALS !` · `I BUILT a ZOO In My BACKYARD… Now I'm Giving You the Full Tour!` | JF x9,15 y x6,59 | la colección entera es lo que más vende en un zoo en casa; miniatura-catálogo con un depredador en contacto. Solo la propia (el zoo ajeno, x0,32) |
| `I [Added / Released] a [SPECIES WITH A STRONG NAME] Into My Giant [HABITAT]` | «I Added a PYTHON into My Giant Rainforest Vivarium» (AC 2,56); «I Released Birds Into…» (3,70) | entra un animal carismático o un depredador; la especie, nunca un rasgo («a Green Predator» 0,72); la imagen, el segundo antes de soltarlo |
| `My [ANIMAL] is ABOUT TO GIVE BIRTH!!` · `My [ANIMAL] FINALLY GAVE BIRTH!!` | JF x3,99 y x4,50 | el primer capítulo de un parto; el rótulo, el durante («SHE'S GIVING BIRTH!») |
| `[Saving My PLACE From DISASTER]… We Lost Animals` | «Saving My ZOO From FLOODING… We Lost Animals !» (JF x6,20) | pérdida real en la colección, sin decir cuál; la secuela cae (x0,97) |
| `This Was the [SADDEST] RESCUE I've Ever Done…` | JF x12,7 | el título calla el animal; la imagen, la víctima (mejor con crías) y el creador al lado; muy de vez en cuando |
| `Building the [Ultimate / Largest… I've Ever Made] [HABITAT]` · `The World's Largest [THING] - [N] YRS Later` | AC 3,55; 3,85 | obra nueva o revisión con un superlativo cierto; sin él, «[THING]: 1 YR Later» (1,57), nunca «UPDATE on…» (0,68) |
| `I [MILESTONE] and It Changed Everything` | AC x10,47 (final de temporada) | una vez, en un hito real; copiado, 1,07 |
| `Top 5 WORST [BROAD GROUP] \| Get These Instead!` · `5 [ANIMALS] You THINK You Want But Definitely DON'T!` | WW x4,02; x5,85 | canales de cría o consejo: salvar de un error; categoría amplia; callar la alternativa |
| `[APODO DE DOS COSAS INCOMPATIBLES] CAUGHT…!` | «Forest Lobster CAUGHT in the Amazon Rainforest!» (x24,5, atípico) | el apodo suena imposible y la foto lo confirma; el lugar no vende (BW 7 → x0,60) |
| `BITTEN / STUNG by a [EXACT ANIMAL]!` | «Bitten by an Assassin Hawk Bug!» (x8,9) | el presentador recibe el daño; sin cola de sitio ni aclaración (puro, ≤ 33 car.: 5/5 ≥ x1,18) |
| `Feeding My [SUPERLATIVE] [ANIMALS]!` | «Feeding My CRAZIEST ANIMALS!» (x3,43) | el grado en el título, la lista en la imagen («FEEDING ALL MY ZOO ANIMALS!» x0,99) |
| `[PREDATORS] EAT [BIG PREY]!` | «King Cobras & Crocodile EAT Pythons!» (x2,94) | en plural o con un segundo depredador (CW plural 3/3 altos, singular 2/2 bajos) |
| `Inside [an OWNER-TYPE's / COUNTRY's MOST SECRET] [PLACE]!!` | «Private Tour of India's MOST SECRET AQUARIUM!!» (x3,63) | acceso a lo vedado (PC «Private» ~x2,2; FG «Private Tour» 13 → x1,42, ninguno bajo) |
| `Exploring [PLACE] FULL of [CATEGORY]!!` | «Exploring Indoor ZOO Full of EXOTIC ANIMALS!!» (x3,42) | solo con dueño de estatus o cifra y un presentador con crédito (la copia literal de CC, x0,88) |
| `I Built [THING] in [N] Days!!` · `Building EMERGENCY [THING]…` | «Building EMERGENCY POND for FISH & TURTLES in My Backyard!!» (x3,59) | la obra vende en pasado con plazo (CC «I Built… in 100 days!!» x5,8) o con urgencia; a secas, PC 23 → x0,90 |
| `My [PLACE / ANIMAL] [WHAT HAPPENED]…` | «My Wildlife Park Flooded…» (x2,06) | el suceso con su sustantivo; en canales de «consigo cosas», la pérdida no vende (CC x0,51 y x0,67) |
| `[Camping Overnight / 24 Hours] in [UNLIKELY PLACE]!! (I Regret This)` | «Camping Overnight in My BABY OTTER Enclosure!! (I Regret This)» (x4,1) | reto corto en solitario; la imagen, el durante, nunca feliz |
| `[Modern Day / Real Life] [IMPOSSIBLE THING]?!` | «Modern day Saber-Toothed Tiger?!» (x3,17) | una hipérbole con un animal real delante (un caso) |
| `[GENRE TAG]: [ARCHETYPE PLACE] ([No X, No Y, No Z])` | «SURVIVAL CHALLENGE: Australia's Most Controversial Shipwreck (No Food, No Water, No Shelter)» (x14,91) | la etiqueta ya es la promesa; arquetipo en vez de topónimo; tríada de privación |
| `I Bought a [FAILED / CRASHED THING] and [RESULT]` | «I Bought a Failed Business and Turned it Around» (x4,46) | estatus roto + consecuencia; la imagen, el objeto de lujo o el antes |
| `[Do the Obstacle], Win $[PRIZE]` · `Last To [Leave X] Wins $[N]` | «Eat Everything In A Grocery Store, Win $1,000,000» (x1,88) | reto con premio; el obstáculo concreto es el gatillo |
| `I Spent [N] Hours Inside [THE FAMOUS PLACE]!` | «I Spent 100 Hours Inside The Pyramids!» (x1,53) | «The» + un sitio que todos conocen |
| `Cheapest vs Most Expensive [THING] in [PLACE]` · `$[A] vs $[B] [THING]` | «I Stayed at Cheapest vs Most Expensive Hotel in Bali» (x3,46, con «$2»/«$2,000» en la imagen) | el orden no decide (SM pone el caro primero, MB el barato); las dos cifras, en el título o en la imagen; el número pequeño tiene que dar risa |

**Español frente a inglés: lo que de verdad es de idioma**

| | Español | Inglés |
|---|---|---|
| Mayúsculas | Cada Palabra, artículos y preposiciones en minúscula | Title Case limpio; palabras gritadas solo como marca de casa |
| Signos | tildes, «¿…?»; sin «¡!» en España (corrección, no rendimiento) | «!» de casa o nada; «?!» en algún molde; «…» tras mala noticia |
| Superlativo | con artículo y detrás: «el Hotel… más lujoso» | delante y con dueño: «World's…», «Australia's Most…» |
| Dinero | «1000€», símbolo detrás y pegado | «$1,000», signo delante; «$1M» vale |
| Gramática | 1.ª persona sin sujeto («Gasté»); el gerundio inicial es calco | «I» delante en experiencia propia; gerundio y pasiva en animales y concursos |
| Contraste | «el Mejor y el Peor», vídeos gemelos (sin «vs») | «Cheapest vs Most Expensive», «$2 vs $2,000» |
| Calcos | «Yo…», «Tour»; «Billonario» suena traducido pero no resta | artículos de más, «of the world», «versus», «Part 2» |

Lo demás (callar el sitio, el «!», la longitud, la palanca) es del tipo de canal: los viajeros en inglés (BM, BZ)
escriben como los viajeros en español. Un título no se traduce: se vuelve a escribir con el molde del otro idioma.

**Lo que cambia por tipo de canal** (títulos y miniaturas; detalle en la síntesis, § C)

| Tipo | Qué cambia respecto a la base |
|---|---|
| **Viaje** (HC, RH, NV, BM) | Calla el topónimo pequeño, nombra el marco famoso. Plantilla H (HC 16 → x1,33). La vida de otros rinde más que la propia. Postal sola, lo peor (salvo el primer vídeo de cada país en NV: 15 → x1,25). Lo barato, como objeto. Asombro contenido. Dato que contradice la foto. BM: noche y abrigo antes que cielo azul |
| **Lujo y estilo de vida** (BC; serie de lujo de NO) | Deseo sin tensión: calma, media sonrisa. El famoso nombrado lleva el peso (BC 7 → x1,99). Título nominal con punto. Cara grande si es el gancho. El continente por fuera + una pieza. Lujo prestado o que pierde alguien conocido. Sin «Episodio N» en el título |
| **Retos y concursos** (MB, SM) | Cara grande normal (45–75 % en 16/20 y 17/20). Alguien que aún puede perder; el creador participa (MB 6/6). El premio en el título, nunca en la imagen. Versus con dos personas o solo el lado caro. El regreso del formato, declarado (SM x1,31). Montajes imposibles casi siempre (46/49, ~40/50) |
| **Animales** (PC, CW, BW, FG, CC, GB, AC, WW, JF) | Lee «Animales: qué se vende» (§ 1). El tema manda más que en ningún otro. Los animales son el producto, no la hazaña del creador. Animal entero y haciendo algo, y el que nombra el título, siempre en la imagen. Esconder con ancla sí, silueta sobre la rutina no. Calma ante lo enorme. Color al límite sin cambiar la especie. Dueño de estatus en las visitas. Cinco registros: **dolor** (BW: contacto, durante, pasiva, ≤ 35 car., «!»), **documental** (FG; GB «Así Viven…»: sobrio, sin «!» ni nombres propios, genitivo ajeno), **colección propia o recinto** (PC, CW, CC, AC, JF: la colección entera, el nacimiento, la pérdida, el animal que entra, la obra con superlativo; «My» solo en canal grande), **cuidador o rescatador** (GB, JF: un papel con un animal grande; la emoción en el título y la víctima en la imagen) y **consejo al que quiere tener uno** (WW: veredicto amplio que salva de un error). Listas de curiosidades y recopilaciones, lo peor; las listas de veredicto para el comprador, no |
| **Supervivencia, pesca y caza** (BB; un canal) | Etiqueta de género delante (9/9 ≥ x1,75). Casi nunca texto (52/59; las 10 mejores sin él). La tensión en el título y el trofeo sonriente en la imagen (25 → x1,87): polos opuestos. Arquetipo, no topónimo. Participio de catástrofe, tríada negativa. Objeto hacia la lente. La presa como sombra con el arma apuntando. Títulos largos |
| **Dinero y negocios** (BZ; un canal) | «I» + pasado. La cifra comparada, nunca sola (7/10 mejores). Tapar el valor dejando la forma. Estatus roto. El primero de cada idea (x2,98). Documento + cara grande (x1,50). Quitar decoración. Experimento con condición |
| **Canal pequeño** (CC, 82 k; un canal) | Varianza enorme (tres picos, 32 % de las visitas): lo genérico es arriesgado pero ahí están los picos. «My» resta. Empaqueta para el desconocido. Un regalo a un creador conocido es suelo seguro (5 casos ≥ x1,15). La pérdida no vende. Retitula sin miedo |

## 6. Miniaturas

### Molde único: desde cero, con la cara (Lucas, 2026-11-27; G010)

**Todas las miniaturas se hacen así**, también las de un vídeo editado. Por qué: Lucas, «quiero que todas las miniaturas
sean como las que me has generado desde cero, solo con una foto de la cara… que mantengas la cara y sepas lo que quieres
mostrar en la miniatura y lo resaltes muchísimo», y de las hechas sobre fotogramas: «sí que resaltas la realidad con IA,
pero no son tan limpias como las que generas prácticamente desde cero, manteniendo solo la cara». **Causa:** partíamos del
fotograma (la regla 24 antigua) y la IA conserva lo que ve: el fondo real con su desorden (manguera, marco azul de la
piscina, cubos, pared de ladrillo), la luz plana de un día nublado, la cara pequeña y de lado y el gesto del momento.
Salía la realidad un poco mejor, no una miniatura. Comparado: tres paquetes publicados de Reino Selva («Lo Que Le Pasó al
Cometa Negro», «Vaciamos Mi Estanque Más Profundo…», «Intenté Trasplantar un Estanque… en 1 Hora») frente a 50 hechas
desde cero con la cara de Lucas, todas aprobadas.

- **Del vídeo sale QUÉ se enseña, no la imagen.** El EDL, el registro visual y los descartes dicen el gancho (el sitio, la
  prueba, la comida, el animal, la cifra, lo que le pasa). La miniatura es una escena nueva que lo cuenta en un segundo.
- **Adjuntos: solo la cara**: un retrato limpio de frente, mirando a la lente (`recursos/creador/` o el fotograma más
  limpio así), más su recorte grande (`miniatura.py cara`). Una imagen más **solo** si algo concreto tiene que ser EL real
  porque es el gancho o el público lo conoce (su perro, su koi negro, su bici, el producto de una marca): «keep the exact
  same <thing>; ignore the man and the background in image 2». **El fotograma nunca es la base de la escena.**
- **Cómo son las 50** (lo que se repite):
  1. **La cara de frente, mirando a la lente**, ~25–35 % del alto, centrada o en un tercio, seria y en calma, con los ojos
     abiertos y la boca cerrada. Plano de pecho hacia arriba; de cuerpo entero solo si la postura es la historia
     (flexiones, paracaídas).
  2. **Un protagonista enorme que dice el título**, pegado a la cara o empujado hacia la lente: la guindilla, la pizza de
     1 metro, la hamburguesa de 5 kilos, el helado de diez bolas, el tiburón ballena, el jaguar, el castillo de piezas. A
     menudo, **dos objetos que juntos cuentan la historia, uno en cada mano**: el clip y las llaves de la casa, la cartera
     vacía y el onigiri, el detector y el meteorito.
  3. **El sitio llevado a postal**: atardecer u hora dorada (la mayoría), aurora, noche de neón con lluvia, velas y luna
     azul; un detalle que dice dónde (el Coliseo, los globos de Capadocia, la pagoda). Nítido de punta a punta, colores
     saturados y **fondo limpio**: ni cubos, ni mangueras, ni trastos, ni gente.
  4. **Vestido de la escena** (esmoquin en el tren de lujo, parka en el hielo, uniforme de piloto, delantal de pizzero) y
     con **huellas de lo vivido** (sudor, barro, ropa rota, pintura en la cara, escarcha en las cejas).
  5. En aventura, **selfie con el brazo** en primer plano (la isla, la cascada helada, la cueva, el tiburón).
  6. **Sin texto.**
- **Lo que no cambia: se promete lo que el vídeo cumple** (§ 1.8). El decorado, la luz, la ropa, el tamaño y la abundancia
  se inventan o se exageran todo lo que haga falta; lo que pasa, el animal y la persona tienen que estar en el vídeo.
- **El resto del § 6 sirve para decidir QUÉ enseñar** (el instante, el sujeto primero, las manos, el color, el texto si el
  creador lo lleva). Lo que hable de partir del fotograma, de «foto de móvil», «luz natural» o fondo desenfocado queda
  sustituido por este molde, y las plantillas (A–K) valen como idea de composición, siempre dentro de él. El gesto, por
  defecto el de las 50; otro, solo si lo pide el creador (su `preferencias.md`).
- Esqueleto del prompt: «El prompt», abajo (uno solo). Si un creador no lo quiere: `deshacer_cambio.py <creador> G010`.

**Reglas** (detalle por canal en `base/refs/_youtube/canales/`; el cruce, en la síntesis)

*Escena y sujeto*
1. **En un segundo se siente algo sin descifrar nada** (la anomalía, el apuro, el abrigo); entenderlo del todo puede
   esperar al título si le da la vuelta en un paso. Lo que hay que leer o descifrar falla (HC: 10 de las 11 que no se
   entienden solas ≤ x1,37; BC chat x0,21). El límite no es el número de cosas, sino que cada una tenga su sitio y todas
   digan lo mismo (las 10 mejores de SM llevan 3–6 bloques; una multitud uniforme cuenta como uno).
2. **La primera parada del ojo es el sujeto, no la cara** (MB sujeto primero 20 → x1,12 frente a cara primero 28 →
   x0,81; HC, RH). Lo prometido es la cosa; la cara, la reacción a la cosa.
3. **Cada sujeto haciendo algo, nunca posando** (5 canales: CW posado 11 → x0,64 y cuatro animales haciendo algo hacia
   el creador x3,43; NV figurantes que hacen lo que dice el título en 9/12 mejores y 0–1/8 peores).
4. **El creador puede ser pequeño cuando algo manda** (el animal, un sitio que es la amenaza, un número, un fenómeno) y
   su figura hace algo hacia ello o da escala (8 canales: BM ≤ 30 % 13 → x3,46; BB a 4 % x4,06). Lo que falla es el plano
   general **sin nada raro**, la postal (HC x0,4–0,7; BM con acompañante 6 → x0,39; FG animal solo en su hábitat x0,27).
5. **Varias cosas, con orden; muchas del mismo tipo se leen como una** (10 canales: CW ordenado x3,43 frente a amontonado
   x0,99; FG una especie repetida hasta el horizonte x2,53 frente a surtido x0,69; CC escaparate de un tipo x7,11 frente
   a collage x0,31). La mezcla de tipos obliga a descifrar.
6. **Escala con algo cuyo tamaño ya sabes**: una persona o un coche diminutos junto a lo enorme (MB 5/24 arriba, 0/16
   abajo); el animal junto a la cara, ~50 % más alto que la cabeza. Con objetos, el continente por fuera + una pieza, no
   el interior lleno (BC yate x2,87 frente a interior x0,54), y un objeto con historia, con el daño girado a cámara.

*El instante*
7. **Nunca el después**: lo resuelto, cocinado, terminado, alguien posando junto a la obra (9 canales: MB 7 → x0,70,
   inauguración x0,48; NO desgracia ya ocurrida 8 → x0,70; BB cocinado x0,35).
8. **Antes o durante, según lo que el público ya sabe** (8 canales). *Antes* si el desenlace es incierto y el riesgo se
   ve, con alguien que aún puede perder (RH 15 → x1,42; FG 9 → x1,49). *Durante* si el formato promete que el daño llega
   o el animal actúa (BW 8 → x1,45 frente a «a punto» 7 → x0,71; MB 25 → x1,16).
9. **Instantes que rinden**: el **bisagra**, que parte el antes del después (la presa capturada aún cruda, el fuego
    recién encendido, la obra a medias: BB 25 → x1,87); **la amenaza que el protagonista no ha visto** (FG x4,24; PC
    x2,68); **el fallo de la barrera** (cristal roto, guante que no basta: FG 5 → x1,99 frente a cristal entero x1,33);
    **la consecuencia fuera de cuadro**, con el durante a la vista (BW 3 → x4,01).

*Cara y gesto*
10. **La cara casi siempre, ni gigante tapando la escena ni un punto** (HC ≥ 60 % x0,56; MB > 50 % 28 → x0,84 frente a
    x1,12; NV sus 10 mejores, 17–37 % del alto). Si hay sujeto, la cara es la segunda parada y no lo tapa. Si la cara
    **es** el gancho (persona conocida, pareja, grupo, reacción a un documento), puede ocupar media imagen (BC ≥ 45 % 14
    → x1,36; BZ documento + cara x1,50). Sin cara: el macro que lo dice todo (BW 5 → ≥ x1,18), o cuando el título
    nombra al invitado y él sale (NO x3,3).
11. **La expresión tiene su causa dentro del cuadro**, mejor tocando al creador; sin causa a la vista, calma (6 canales:
    BW la misma mueca con contacto x2,14, sin él x0,52; FG susto ante algo quieto 7 → x0,48; NV boca en «o» sin causa
    4 → x0,20). Ninguna expresión es buena o mala en sí: la «o» con su causa funciona (BB, la pinza a un palmo, x3,62).
12. **Calma ante lo enorme o letal** (5: BM cara serena 10 → x3,82 frente a la que reacciona 23 → x0,99; BW calma x1,10
    frente a grito x0,74). Lo peor, la cara seria sin motivo en canales de personaje (SM 8 → x0,84).
13. **La cara la pide el género**: reportaje y aventura, asombro contenido con la boca cerrada (RH y HC, 0 sonrisas);
    lujo, media sonrisa o calma satisfecha (BC sonríe en 9 de sus 10 mejores); concurso, la media sonrisa de quien sabe
    algo (SM 5 → x1,20); aguante, agotamiento; inquietud, contenida y con las manos en las correas o la cara (FG x4,24).
14. **La mirada es un vector**: al objeto raro del cuadro, hacia arriba a lo que tiene encima (HC 5 → x1,99), o fuera
    del cuadro si se vende «hay más»; nunca a la nada (HC reojo a nada x0,37–0,65).
15. **Dos caras, dos gestos distintos** (una disfruta y otra sufre; una sabe y otra no: SM x1,45 frente a x0,68; BC
    x3,01). Como mucho dos caras grandes: una fila de caras iguales no es una escena (MB 3+ en 0/12 mejores y 3/8 peores).
16. **Que se le reconozca y que participe**: sin gafas de sol, casco ni sombra de sombrero en la cara (SM gafas 0/12
    mejores; BB x0,51); vestido de la prueba y dentro del duelo, no de anfitrión ni árbitro (MB 6/6 → x1,35 frente a
    árbitro x0,90).

*Manos y objeto*
17. **Manos que agarran, sufren u ofrecen; nunca el brazo que señala** (HC señalar 5/5 < x0,9 frente a palma abierta
    x1,41; en MB y SM la mano que presenta solo sale en las peores). El dedo a un palmo de algo peligroso, sí (FG x3,28).
18. **El objeto en la mano da un suelo, no los éxitos** (HC 10 → x1,40; BB 17 → x2,52; pero PC 64 → x1,00). Rinde si
    es raro o deseable, se valora a la vista, duele, cuesta o delata; va **hacia la lente**, en diagonal y con gran
    angular (BB x4,73 frente a hacia los lados x0,53), se ofrece al espectador y, mejor, a medio proceso. Nunca el
    atrezo del papel ni el objeto fijo de la serie (SM x0,80; NO x0,95).

*Dinero, cifras y flechas*
19. **Una cifra sola no levanta** (RH «300$» x0,63; PC 41 etiquetas → x0,88). Rinde si **choca** con algo que se ve:
    otra cifra (BZ cifra comparada en 7/10 mejores y 0/10 peores; CC precios comparables 7 → x1,81), un objeto que vale
    mucho más o menos, un signo menos sobre alguien conocido, lo imposible («0 €»). El bulto de billetes es neutro (BZ
    8 → x1,10): vale como abundancia que el espectador querría. El premio del reto, nunca en la imagen (MB 0/49).
20. **Nunca una flecha o un círculo que señala lo que ya se ve** (CW x1,01 frente a x1,28 sin ella; NV 8 → x0,61). Sí la
    raya o flecha que **une** dos cosas y de esa unión sale la pregunta (la etiqueta → su objeto, lo tapado → lo que le
    espera, una cifra → otra, la causa → el efecto: BZ x5,62; CC x5,66; BW x4,01), y el trazo que dibuja algo invisible
    (FG línea roja x4,21). El círculo de aumento, solo sobre lo pequeño de verdad (el mosquito).

*Color y parrilla*
21. **Una sola mancha saturada de temperatura contraria** a todo lo demás, y que sea el sujeto o el creador (RH ~15 →
    x1,42; HC gorra azul en una imagen dorada x2,6). Luz en la cara. En viajes, contraste con luz: la noche o el interior
    cálido con frío fuera ganan al cielo azul y al agua turquesa (BM noche 8/8 ≥ x1,19 frente a día azul 28 → x0,76).
22. **Rompe la parrilla**: ni la paleta ni la plantilla de la semana anterior (BB repetir x4,83 → x0,84; romper el color
    4/6 > x1,8). Quitar decoración rinde: contornos, flechas de adorno, pixelado, logo del canal (BZ; SM logo 9 → x0,83).
23. **Abajo a la derecha** (ahí va la duración) no va lo único importante ni nada pequeño que leer; un secundario
    grande, sí (PC 5 de sus 6 mejores).

*Realidad*
24. **Rehecha, no retocada** (2026-11-27, G010; antes decía «parte de una foto real del vídeo y rehazla»): del momento
    real sale qué se cuenta; la imagen se genera desde cero con la cara del creador (molde único, arriba). El fotograma
    tal cual rinde poco (BC 5 → x0,91; BM reales x0,99 frente a rehechas x1,31), y retocado arrastra su fondo y su luz.
    Fotorrealista, como una foto de verdad: nunca un póster de terror o fantasía (RH x0,61), una ilustración en lugar
    del animal (BW x0,41 frente a foto x2,77), ni la cara del creador hecha personaje o idealizada (CW real x1,84 frente
    a IA x1,03; indicio): la cara es la suya, tal cual. Siempre dentro del § 1.8.
25. **Cada animal, su especie exacta** (norma: quien sigue un canal de animales la nota). El color y la escala se pueden
    llevar al límite (BW saltamontes dorado x24,5; FG cobra naranja x3,28); la especie, la forma y el dibujo, no.

*Invención* (gusto de un creador, 2026-11-14; aún sin CTR que lo confirme)
26. **Lo inventado traduce el gancho en un objeto que se entiende en un segundo**, y la IA está para eso: un reloj de
    arena para «en 1 hora», un martillo neumático para «tierra de cemento», un cojín de joyero o un maletín esposado
    para «la más amenazada», un globo con animales para «de África», una puerta corriente que se abre a una selva para
    «detrás de esta puerta», dos terrarios (uno empapado, otro seco) para «se le muere». Un objeto protagonista
    grande, fondo limpio y saturado (vale un liso de color), la cara mirando a la lente con calma o asombro y la boca
    cerrada. **No entra** el gag que no dice el gancho (cajas de regalo, manuales, un sillón, una mascarilla de
    oxígeno, una hoja de paraguas) ni lo raro que hay que descifrar (un bloque de cemento en primer plano, raíces de
    dos metros, una torre de cajas). En la exploración de Reino Selva (40 pruebas, 3 niveles de invención) el creador
    eligió 25: los tres niveles por igual (decorado 13/18, real exagerado 5/8, montaje fuerte 8/14), así que lo que
    decide no es cuánto se inventa sino que lo inventado diga el título. La 2.ª tanda, afinada por título con esta
    regla (cara al ~30 % mirando a la lente, un objeto protagonista grande, la especie nombrada), pasó casi entera: 14
    de 17. Solo cayó de verdad la **imagen partida** (medio y medio), que no mejoró al afinarla; las otras dos que
    quedaron fuera lo hicieron por cómo salieron (un animal deforme) o porque había otra mejor para el mismo título.
    Una 3.ª prueba con 30 paquetes inventados (animales, viajes, aventuras) gustó 29/30: el molde no es solo de
    animales. Al generar, la IA falla siempre en lo mismo y hay que pedirlo explícito: **lo diminuto lo finge con
    perspectiva** (di que está a la misma distancia que la persona y dale una medida del cuerpo: «el techo le llega a la
    cadera»); **la profundidad o la altura no se ven** si la cámara no se pone encima o debajo (pide el punto de vista y
    una escala lejana: la luz de otro espeleólogo al fondo); **dos cosas que se tocan se funden** en una forma
    (separa: «el tronco, un metro por encima del agua; los cocodrilos, aparte»); y en los planos abiertos **la cara se
    queda pequeña** aunque el prompt diga 30 %: pide «plano cercano» y, si sale lejos, corrígelo en el mismo chat.
    Y **que el suelo no corte el cuerpo**: la única descartada de las 30 tenía al creador de pie con el césped a la
    altura de la cintura, como enterrado. Si está de pie, que se vea hasta el suelo o que lo corte el borde del
    encuadre; si no, agachado, sentado o detrás de algo que tape con sentido (una mesa, el borde de la cesta).
27. **Molde de postal** (Lucas, 2026-11-16: «métele a la skill el molde»). Es la forma de la regla 26 en que la IA
    pone casi todo, y **desde el 2026-11-27 es el molde de todas las miniaturas** (arriba). **De referencia, solo la cara** del creador (un retrato limpio de frente) **y el animal real si
    sale** (una captura suya, con «ignore the man in image 2»). El escenario se inventa: espectacular, como una postal
    de viaje, con luz de cine (hora dorada, rayos entre la niebla, luna azul, tormenta con rayo) y la ropa propia de
    esa escena (vadeadores en el estanque, chubasquero en la tormenta, parka en el hielo). El animal o el objeto que
    dice el título va **enorme y pegado a la cara**. La cara ocupa ~30 % del alto, mira a la lente en calma, con los
    ojos abiertos y la boca cerrada. Sin texto. En Reino Selva, 20 de 20 vídeos de animales hechos desde cero
    gustaron. En los reworks de sus paquetes ganó lo inventado cuando era **un objeto que cuenta el título** (el
    fluorescente con su propio chubasquero, una carretilla convertida en estanque, el perro junto a un hoyo perfecto
    en tierra de cemento). Perdió cuando el escenario inventado envolvía a **su animal real** en una escena que no
    pudo pasar: su perro en un jardín japonés de fantasía cayó en las tres versiones, y un pajarito tirándose de un
    trampolín también. Con su animal real, mejor una escena que pudo pasar exagerada (24) que una de fantasía. El
    sufijo fijo lleva siempre dos cosas, porque sin ellas la IA falla: **ANATOMY** (los dos brazos unidos a los
    hombros, manos de cinco dedos, nada que flote; un brazo «volando» tiró una miniatura) y **ni personas ni animales
    que no se describan** (sin esto metió un jaguar que no se había pedido). Esqueleto en «El prompt», abajo.

*Texto*: llevarlo o no es estilo del canal, no palanca (MB x0,99 con y x0,97 sin; NV lo lleva el 85 %, BB casi
nunca). Lo que separa es **qué dice**. Hasta 4 palabras, legibles de un golpe a 168 px.

| | Qué | Evidencia |
|---|---|---|
| **Bien** | un dato nuevo que **choca con la foto**, mejor la lectura de un instrumento (hora, temperatura, contador) o una cifra imposible | «2:17 am» sobre un paisaje con sol (BM x6,88); «9AM», «0 €» (HC x1,62, x1,83); «VIVEN EN 2087» bajo «Japón es OTRO PLANETA» (NV x6,37); «-6000€» sobre alguien conocido (BC x3,23) |
| **Bien** | el nombre de la cosa que el título calla (un animal, no un sitio); texto de suceso, no de tarea; el marcador que el título no tiene | «MAMMOTH MICE» (BW x2,77); «ATTACKED!», «ESCAPED» (CW 8 → x1,46 frente a tarea 12 → x0,76); «HOUR 10» (PC 3/3 > x1,9) |
| **Mal** | lo mismo que el título, con sus palabras **o con otras** (si lo borras, el título no pierde nada); la respuesta; una conclusión o una negación; el topónimo; una pregunta sin su referente a la vista | BZ eco 14 → x0,86; BM 6 ecos sin palabras compartidas, todos bajo x1; NV respuesta 10 → x0,66; «CUIDADO» x0,13; NV topónimo 17 → x0,79 frente a concepto x1,29; FG dudas 6 → x0,41. Contestar «no se sabe» sí abre (FG x1,11) |
| **Repetir vale** | (a) el formato o el evento, que clasifica el vídeo para quien no conoce el canal; (b) las dos cifras del versus, cada una en su mundo; (c) la pregunta del título en 3–4 palabras con un giro; (d) un sinónimo más fuerte con la prueba en la imagen | SM repiten 8 → x1,40; CC «REPTILE SHOW!» 4/4 ≥ x1,8; FG. Una pregunta, solo con su referente: «¿POR QUÉ VAN ASÍ?» con ellos en la foto (NV x6,06) |
| **Dónde** | decide lo que dice, no dónde está. De escena: un tercero que confirma (cartel de aviso), un aparato que mide (reloj, termómetro), una etiqueta a mano colgada de su objeto; nunca lo que ya se ve ni lo que hay que leer para entender. Rótulo: sobre la escena o la piel, detrás de la cabeza del sujeto o arriba sobre el cielo. Con forma de interfaz (reseña, verificado), parece una prueba encontrada | FG carteles x1,42–3,28; SM relojes x1,18; CC etiquetas en 4/10 mejores, 0/10 peores; MB rótulos de decorado 5 → x0,54; BW rotulador en la piel x2,58; HC arriba 7/7; BC reseña x3,33 |

**Plantillas** (elige la que pida el ángulo; recetas en los análisis de canal)

| Plantilla | Cómo es | Para qué |
|---|---|---|
| **A. Sujeto en la mano** | gran angular muy cerca; el animal u objeto empujado hacia la lente en diagonal, 50–75 % del ancho, ojo nítido; la cara detrás, a un lado; el pez largo, en vertical junto al cuerpo o en diagonal a la lente (BB) | un animal o un objeto que es la noticia; suelo seguro, no techo (regla 18) |
| **B. Cara frente a sujeto** | creador a un lado (2/5), sujeto al otro (3/5), más cerca de cámara y ~50 % más alto que su cabeza; la expresión con su causa; fondo desenfocado solo si el fondo no es el contenido | riesgo, tamaño, «¿le muerde?» |
| **C. El instante, sin cara** | macro: el sujeto llena el cuadro, una mano o un dedo de escala, fondo de un color; o la caza en suspenso (la presa como sombra, el arma apuntando: BB x4,83) | contacto, detalle, rareza |
| **D. Recinto lleno** | animales del mismo tipo, cada uno haciendo algo (mejor hacia el creador), ordenados sin taparse; o una sola especie repetida hasta el fondo; nunca con objetos de colección; sin texto | totalidad, variedad, visita |
| **E. El sitio manda** | picado o gran angular; el sitio ocupa dos tercios; el creador pequeño, haciendo algo hacia él; una persona o un vehículo diminuto de testigo de escala | obra terminada, sitio imposible |
| **F. Dos mundos** | los dos en una escena continua, unidos por una línea guía, con una persona en cada lado (o el cielo que cambia); la línea divisoria, solo para el antes/después de la misma persona (SM); dos animales en espejo con una parte del cuerpo en el eje (BW x4,31) | versus, contraste, transformación |
| **G. El punto de la historia** | foto de aspecto real a media prueba; el marcador no comparte unidad con el título: el desgaste, la hora de madrugada en un reloj, o «DAY 201» si el título no da plazo | reto con plazo |
| **H. Retrato + lugar con anomalía** | busto a un lado, el lugar detrás, nítido de punta a punta, con un detalle que no cuadra; si el título calla el sitio, ni monumento ni bandera que lo delate | viaje, sitio raro |
| **I. Selfie con gente** | selfie gran angular; los figurantes **hacen lo que dice el título** (si no, fuera); con alguien conocido, dos caras juntas y nada más; el texto arriba | viaje con personas, invitado |
| **J. Suceso** | creador con la ropa del suceso (mojado, embarrado), dos tercios para el lugar transformado; el cielo pone el ánimo | inundación, emergencia, rescate |
| **K. Abrigo** | dentro, quieto, cálido y a gusto (una lámpara, boca cerrada); fuera, por la ventana, frío u hostil; sin texto (BM tren-cama 4/4 ≥ x3,68) | alojamiento, transporte, refugio |

### El prompt (para ChatGPT; vale para otras IA de imagen)

La miniatura la genera quien edita en ChatGPT (o Claude, con Claude in Chrome), **adjuntando solo la cara**: el retrato
de frente (`youtube/A.jpg`) y su recorte (`youtube/A_cara.jpg`), más una imagen del animal u objeto real si hace falta
(molde único, arriba). El prompt describe una **escena nueva**; nunca «transforma esta foto». Sin la cara, la IA inventa
una persona que no es el creador.
- 2026-11-27 — **Probado**: tres paquetes publicados de Reino Selva, rehechos desde cero con una sola miniatura suya de
  frente como referencia de cara (10 imágenes, una por chat, ~1 min cada una). Lucas: «He visto que lo has entendido».

- **Idioma**: el prompt, **en inglés** (lo que mejor entienden las IA de imagen); encima, una línea en español con la
  idea para quien lo pega. **El texto de la miniatura, literal y en el idioma del vídeo**, entre comillas.
- **Un prompt, una imagen**: cada variante es un mensaje nuevo en un chat nuevo, con su referencia adjunta.
- 2026-11-17 — **Si las miniaturas las genera Claude en ChatGPT (Claude in Chrome), al acabar se borran sus chats.**
  Al abrir cada chat se apunta su URL en `youtube/generadas/chats.md` (letra, versión, URL). Cuando TODAS las imágenes
  están guardadas en `youtube/generadas/`, pasadas por `miniatura.py final` y comprobadas (`prueba.jpg`, `caras.jpg`),
  se borran esos chats y solo esos (menú del chat → Eliminar), también los de intentos descartados; nunca otro chat de
  la cuenta, aunque se llame igual. Antes de borrar, la imagen de cada chat tiene que estar guardada en local (borrar
  en ChatGPT no se deshace). Si alguno no se puede borrar o no se encuentra, se dice al entregar con su URL. Pedir que
  se generen las miniaturas ya incluye este borrado. Por qué: Lucas, alimentacion, «cuando se le diga que genere las
  miniaturas, borre las conversaciones en ChatGPT de las miniaturas una vez acabadas».
- **El título del vídeo NO va en el prompt** (ni como «contexto»): ChatGPT lo escribe en la imagen aunque el prompt diga
  «No text anywhere». Visto en alimentacion C y E, 2026-11-17 (dos de tres salieron con el título rotulado y hubo que
  pedir quitarlo). Lo que el título promete se describe como escena; el texto, solo si la miniatura lo lleva (bloque 8).
- **La cara va desde el primer mensaje** (el retrato y su recorte, nombrados en el prompt: «image 1 is the man; image 2
  is a close-up of his face»). Sin ella, la IA inventa una cara. Y no lo arregles después en el mismo chat pidiendo «cambia su cara por la de esta foto»:
  ChatGPT lo bloquea por sus normas (visto en `1311` B, 2026-11-14); rehazla en un chat nuevo con las dos desde el
  principio. Los retoques de parecido que sí pasan: «his hair is fuller and wavier, his beard thicker», sin pedir un cambio de cara.
- 2026-11-17 — **La cara de la persona, lo más fiel posible: es la persona real, no un parecido.** La IA conserva la
  cara que VE y redibuja la que tiene que imaginar. Por eso:
  1. **La referencia de la cara ya tiene el ángulo, la mirada y el gesto que pide la miniatura**: con el molde único,
     de frente, mirando a la lente, ojos abiertos y boca cerrada (una foto de `recursos/creador/`, un fotograma así o
     una miniatura suya publicada así). Nunca ojos cerrados, cabeza gacha ni cara de lado como única referencia.
  2. **La cara grande y aparte**: `miniatura.py cara A` recorta la cara de la referencia a ≥ 1024 px
     (`youtube/A_cara.jpg`) y se adjunta SIEMPRE como segunda imagen: «image 2 is a close-up of his face: identity
     reference, copy his facial features exactly (eye shape, nose, jaw, beard line, hairline, skin texture). Same
     person, do not beautify, do not change his age». Si avisa de que la cara mide menos de 160 px o no encuentra ninguna, se busca otro
     fotograma o una foto. **Más fotos de la cara solo si son coherentes**: lo que mejor clava la cara es una referencia
     de cuerpo y su propio recorte (la misma foto: misma luz, mismo día, mismo ángulo). Una tercera foto de otro momento,
     con otra luz, otro peinado u otro ángulo, no suma: la IA las mezcla y saca una cara «media». Como mucho una más, del
     mismo día y en un ángulo parecido. (Pregunta de Lucas, 2026-11-17; es lo que se espera de cómo funcionan estas IA,
     sin medir aún: si una prueba dice otra cosa, se corrige aquí.)
  3. **En la miniatura, la cara no es diminuta** (como mínimo ~20–25 % del alto si sale): una cara pequeña la IA la
     inventa entera.
  4. **Se comprueba**: `miniatura.py final` deja `youtube/caras.jpg` con la cara de cada miniatura junto a la de su
     referencia. Misma nariz, ojos, mandíbula, barba y nacimiento del pelo; si no es él, **se rehace en un chat nuevo**
     con mejor referencia (pedir «cambia su cara» en el mismo chat lo bloquea ChatGPT, regla de arriba). Lo que no se
     pueda comprobar se le dice a quien edita al entregar.
  Por qué: Lucas, alimentacion, «en la miniatura B le ha cambiado la cara a la persona demasiado… hay que intentar
  mantener lo más fiel posible la cara de la persona» y «lo mismo en la E». **Causa:** la referencia de la cara de la
  B era un fotograma con él mirando abajo y los ojos casi cerrados (la IA inventó los ojos y la mirada), y la E pedía
  mirar a la lente sonriendo con una referencia de tres cuartos mirando a otro lado (tuvo que inventar la cara de
  frente). En la A, con la cara grande y en un ángulo parecido al pedido, salió fiel. Se comprobaba solo a 168 px, donde
  no se ve si la cara es la suya. (vídeo: alimentacion)
- **Orden fijo de bloques** (el del esqueleto de abajo):

| Bloque | Qué pide |
|---|---|
| 1. Encargo y formato | «YouTube thumbnail, 16:9 landscape». ChatGPT a veces devuelve 3:2: todo lo importante, en la franja central 16:9 (`miniatura.py final` recorta y deja 1920×1080 en JPG de menos de 2 MB) |
| 2. Adjuntos y qué se conserva | solo la cara («image 1 is the man; image 2 is a close-up of his face… same person, do not beautify, do not change his age»; «man» o «woman» según quien salga) y «ignore the background and clothes of the attached photos; dress him as described». Si va el animal u objeto real: «keep the exact same <thing>; ignore the man and the background in image 3» |
| 3. **Instante** (nuevo) | «the moment just before…» (desenlace incierto, riesgo a la vista) o «in the middle of…» (el daño, la acción). Nunca «after» ni «posing next to»; una obra o un objeto, «half-finished» |
| 4. Composición | **qué ve primero el ojo** («the first thing the eye sees is the <subject>; his face is the second»), dónde va cada cosa y cuánto ocupa (% del alto), plano y lente. Creador pequeño: «a tiny human figure / a car for scale». Animal junto a la cara: «about 50 % taller than his head». Muchas cosas: «many of the same <thing>, in rows, repeating to the horizon», nunca «a variety of». Máximo dos caras |
| 5. Expresión y mirada | **con su causa en el cuadro**: «wincing because the <animal> is biting his hand», no «shocked face». Por defecto (molde único), mirando a la lente, serio y en calma, con la boca cerrada; ante algo enorme, «calm, almost unimpressed». Mirada a algo: «looking at the <thing> in the frame», «looking up at…», o «looking off-frame to the left» si se vende «hay más»; nunca «looking sideways» sin objeto. Dos caras: «one is enjoying it, the other is suffering». Si la referencia ya tiene el gesto, «keep his expression» (cambiarlo arriesga el parecido: mejor otro fotograma o foto) |
| 6. **Manos** (nuevo) | «his hands grip / hold / offer the <object> toward the lens, diagonal, close to the camera»; inquietud, «hands on his own straps / on his face». Nunca «pointing» |
| 7. Fondo, luz y color | el sitio llevado a postal: luz de cine (hora dorada, atardecer, aurora, neón con lluvia, velas), un detalle que diga dónde, nítido de punta a punta y **limpio** («clean uncluttered background, no hoses, buckets, tools or clutter»); «one single saturated accent of the opposite temperature: the <subject>»; luz en la cara. En viajes, prueba antes la noche o el interior cálido con frío fuera que el cielo azul |
| 8. Texto | literal entre comillas, hasta 4 palabras, con tipografía, color, borde, tamaño y sitio. Mejor **dentro de la escena** si confirma o mide (cartel de aviso, reloj, termómetro, etiqueta a mano colgada del objeto) o, si es rótulo, **detrás de la cabeza del sujeto** o arriba sobre el cielo. Las dos cifras de un versus, cada una en su lado. O «No text anywhere in the image» |
| 9. Acabado | «like a top YouTube thumbnail: one huge hero subject that tells the story, right next to his face or pushed toward the lens; a spectacular, cinematic version of the place, like a travel postcard; bright saturated colors; everything razor sharp. Photorealistic, like a real photo, not an illustration, no plastic AI skin» (antes de G010 pedía «foto de móvil con luz natural»: salía la realidad un poco mejor) |
| 10. `DO NOT ADD` | marcas de agua, el logo del canal y cualquier logo, marca o bandera que no salga en el vídeo (una marca o bandera solo si está en el vídeo y es parte del gancho, y nunca la que delata el sitio que el título calla); texto de más; flechas o círculos que señalan lo ya visible (una línea fina que **une** dos cosas se pide expresamente); «?» sobre algo visible; pixelado; caras de más; gafas de sol o casco; imagen partida (salvo antes/después de la misma persona); objetos modernos si la historia lo pide; nada pequeño abajo a la derecha; personas o animales que no se describan; ningún suceso, animal, persona ni peligro que no esté en el vídeo (el decorado, la luz, la ropa, la escala y la abundancia se inventan y se exageran todo lo que haga falta) |

- **No pidas**: «shocked face» o «screaming» sin causa a la vista; «pointing at…»; «split screen» (pide «both worlds in
  one continuous scene, one person in each»); «stacks of cash» o un precio como único gancho; «posing proudly», «after».
- **Corto y concreto**: 120–200 palabras. Medidas y posiciones, no adjetivos («huge», «epic», «insane» no dicen nada).
- **Debajo de cada prompt, 2–3 retoques listos** para pedir en el mismo chat si no sale a la primera («make the
  tortoise 20 % larger», «remove all text», «keep the face exactly as in the photo»).

Esqueleto (uno solo, el del molde único; se rellena y se pega como un único párrafo, sin huecos). Prefijo y sufijo
fijos; entre los dos, la escena:

```
Create a YouTube thumbnail, 16:9 landscape, everything important in the central area. Image 1 is the man; image 2 is
a close-up of his face: identity reference, copy his facial features exactly (eye shape, nose, jaw, beard line,
hairline, skin texture). Same person, do not beautify, do not change his age. Ignore the background and clothes of
the attached photos; dress him as described.
[Image 3 is his <animal / object>: keep the exact same <animal / object> (species, size, coat, pattern / shape,
colors); ignore the man and the background in image 3.]
SCENE: <the place turned into a postcard + time of day + light>. <The hero subject that says the title, huge, right
beside his face or pushed toward the lens, in the moment just before / in the middle of what the title says>. He
<pose: kneels / crouches / stands chest-deep / selfie arm…> in <clothes of the scene, with traces: wet, mud, sweat>,
<what each hand holds: one object or two that tell the story together>.
FRAMING: close shot, chest up, his face about 30 % of the frame height, well lit, looking straight into the lens,
calm serious deadpan, eyes open, mouth closed. His body is cut by the frame edge or by something meaningful in front,
never by the ground. ANATOMY: both arms clearly attached to his shoulders, normal hands with five fingers, nothing
floating; animals with correct anatomy. No other people and no animals beyond those described.
STYLE: like a top YouTube thumbnail: one huge hero subject that tells the story, right next to his face or pushed
toward the lens; a spectacular, cinematic version of the place, like a travel postcard, with dramatic light; bright
saturated colors; clean uncluttered background (no hoses, buckets, tools or clutter); everything razor sharp.
Photorealistic, like a real photo, not an illustration, no plastic AI skin. No text, no numbers, no letters, no
logos, no watermarks, nothing in the bottom-right corner.
```

Si la miniatura lleva texto (preferencias del creador), cambia en el sufijo «No text, no numbers, no letters» por el
bloque 8 (literal entre comillas, letra, color, sitio y tamaño). Lo que pida el `DO NOT ADD` de la tabla y no esté en el
sufijo (una bandera, un monumento que delata el sitio, gafas de sol) se añade al final.

Cada imagen va en un **chat nuevo** y hay que borrar en el cuadro de texto lo que quede escrito antes de pegar: ChatGPT
arrastra el borrador de una pestaña a otra y dos peticiones salieron mezcladas. **Al revisar cada imagen**: brazos y
manos, especie, que no haya animales de más y que el suelo no corte el cuerpo.

Con Claude in Chrome se pueden llevar 2–3 chats a la vez en pestañas distintas; la imagen se guarda en local antes de
cerrar el chat (y luego se borran los chats, regla de arriba).

**Fotos del creador** (`personal/<creador>/recursos/creador/`). **La imprescindible: un retrato de frente, mirando a la
lente, serio y con la boca cerrada**, buena luz y nitidez: es la que usa el molde único en todas. Además, pídele una vez un juego de 10–12 retratos para
miniaturas (fondo liso, luz suave de frente, de pecho hacia arriba, con la ropa de sus vídeos o la de la prueba, sin
gafas de sol ni gorra que tape los ojos): serio en calma, asombro contenido con la boca cerrada, media sonrisa de quien
sabe algo, sonrisa abierta (para lujo), mirando hacia arriba (HC x1,99), de reojo a izquierda y a derecha (solo con un
objeto en el cuadro), palma abierta hacia arriba (HC x1,41), ofreciendo algo a cámara con las dos manos, agarrando algo
con fuerza, manos en las correas o en la cara con inquietud (FG), agotamiento, mueca de apuro (BZ 6 → x1,36). Ninguna
señalando (los gestos distintos, solo si el creador los pide en vez del de serie). Mientras no las haya, el fotograma
o la miniatura publicada más limpia de frente (§ 2, paso 6).

### Lo que el estudio no resuelve (decide el creador o un test)

Si una pareja depende de esto, dilo en el paquete y prueba las dos opciones en «Probar y comparar»:
- **¿Lo inventado atrae o decepciona?** El ratio no lo castiga, pero sus éxitos tienen pocos «me gusta» por visita; hace
  falta la retención de YouTube Studio del creador. Mientras tanto, manda la norma del § 1.8.
- **Tamaño de la cara**: medio gana en HC, RH, NV, MB, CC; grande en SM, BC, BW, BZ; pequeño en BM, BB. «La cara es el
  producto» lo explica solo en parte, y las medidas a ojo varían ±10 puntos entre lectores.
- **Antes o durante**: FG antes x1,49 / durante x0,83; BW al revés. La condición de la regla 8 se escribió a posteriori.
- **Barato o caro**: RH, NV, HC, barato; FG, MB, BC, PC, caro; CC (caro sube) y BM (barato baja) no casan con § 1.7.
- **Rótulo que repite el título**: funciona en SM, CC, FG, BC, PC; hunde en HC, MB, BW, BZ, NO, NV.
- **Texto de escena o encima**: casi todos a favor del de escena; HC al revés (x1,08 frente a x1,41).
- **Mayúsculas, «!», logos y banderas del tema**: suben en unos canales y bajan en otros (banderas: HC x1,78, RH x0,90);
  seguramente marca de casa. **Longitud, «Investigué», «[N] Días…»**: pocos casos o depende del molde.
- **Nada de esto es el CTR**: las impresiones, el CTR y las pruebas A/B del creador valen más que todo el estudio (§ 9).

## 7. La prueba antes de entregar (cada pareja)

*Encaje*
1. Di en una frase qué parece la imagen sola y en otra qué dice con el título. Si son la misma, no hay segunda lectura.
2. ¿La segunda lectura sube lo que está en juego en un solo paso, sin saber nada de fuera ni dejar al creador de verdugo?
3. Borra el rótulo: ¿el título pierde algo? Si no, es eco aunque no comparta palabras (salvo formato o cifras del versus).
4. ¿Algo de la imagen contesta la pregunta, enseña el después o delata lo que el título calla (monumento, bandera)?
5. ¿Algo desmiente la premisa (objeto moderno en un náufrago, sonrisa bajo un arrepentimiento, amenaza que no se ve)?

*Miniatura*
6. ¿En qué instante? Antes con el riesgo a la vista, o durante si el formato promete el daño. Nunca después ni posando.
7. ¿Qué mira primero el ojo? Lo prometido, no la cara ni una palabra. ¿Se siente algo en un segundo sin leer?
8. ¿La expresión tiene su causa en el cuadro? ¿La mirada va a algo que está en él (o fuera, si se vende «hay más»)?
9. ¿Las manos agarran, sufren u ofrecen? ¿Nadie señala? ¿El objeto va hacia la lente y se valora a la vista?
10. ¿Como mucho dos caras grandes, con gestos distintos? ¿Se reconoce al creador (sin gafas ni casco)?
11. Si algo está tapado: ¿se ve la forma y hay ancla? ¿Nunca la persona, nunca un «?» sobre lo que ya se ve?
12. Creador pequeño: ¿algo manda y hay escala? Grande: ¿la cara es el producto? Muchas cosas: ¿del mismo tipo y en orden?
13. Si hay cifra, ¿choca con algo? Si hay flecha, ¿une dos cosas? ¿Ni precio suelto ni premio del reto en la imagen?
14. ¿Una sola mancha de color contrario en el sujeto, luz en la cara, nada pequeño abajo a la derecha? ¿Y distinta de
    la miniatura anterior del canal?

*Título*
15. ¿El verbo promete un resultado, un coste o algo en el cuerpo (no Visité, Busqué, I Visited, Living)?
16. ¿El gancho cabe en ~50 caracteres y empieza por algo reconocible, no por un nombre desconocido ni por el episodio?
17. ¿Calla lo pequeño y nombra lo famoso? ¿Lo entiende alguien que nunca ha visto el canal?
18. ¿Paradoja o choque (en el título o con la imagen)? ¿Superlativo de algo que se ve? ¿La cifra mide lo que se juega?
19. ¿Es una secuela, un molde ya usado o la sorpresa de la tanda anterior? Cambia el sustantivo o el ángulo.
20. ¿Suena a alguien de ese idioma y sigue la forma de la casa (§ 4–5)? ¿Nombre exacto y bien escrito?
20b. **Si es de animales** (§ 1, «Animales: qué se vende»): ¿el título lleva un animal (o la colección, o el recinto)?
    En un vídeo de obra o de arreglos: ¿ese animal sale de verdad y está en juego? Si no, ¿has dejado el gancho propio
    del vídeo en lugar de añadir un animal de relleno? ¿Se reconoce en el título **de qué va el vídeo** (la obra, el
    arreglo, el tema principal), con el animal sumado y no en su lugar?
    ¿El protagonista es el animal o lo que el creador hace con él, no una hazaña con una condición inventada? ¿El animal
    grande va por su nombre y el pequeño no es el gancho? ¿Sale ese animal en la miniatura, grande y antes de la
    consecuencia? ¿Algún título de las cinco parejas usa un molde nativo del nicho (colección, nacimiento, pérdida, el
    animal que entra, obra con superlativo, rescate, cuidador, ventana documental, veredicto)?

*Producto*
21. ¿Todo lo que promete sale en el vídeo, en qué minuto y cuánto dura (apúntalo)? Si llega al final o dura menos de dos
    minutos, es de recambio. Lo que el vídeo no tenga (agua que no se grabó, un bocado que no se ve), al `DO NOT ADD`.
22. ¿Lo inventado es decorado o símbolo de algo que el vídeo cumple? ¿Nada de suceso, emoción, animal ni famoso inventados?
23. ¿El prompt describe una escena nueva (molde único) y no «transforma esta foto»? ¿La única referencia es la cara de
    frente mirando a la lente, con su recorte (`A.jpg`, `A_cara.jpg`), y el animal u objeto real solo si es el gancho?
    ¿El fondo es limpio y de postal, sin los trastos del rodaje? ¿Se entiende en un segundo a 168 px?
24. ¿Cada título dice qué ES el vídeo (su promesa central), y las cinco cambian solo el gancho? ¿Tiran de palancas distintas sin cambiar de tema? ¿Ninguna es relleno para llegar a cinco? (Mejor cuatro buenas.)

## 8. Entrega: el paquete de YouTube

Tras el render final y sus comprobaciones (paso 7 del flujo), desde `out/<slug>/`:

- `youtube/PAQUETE.md` — todo, en este orden:
  1. **De qué va y qué se vende**: 3–5 líneas con el bloque más fuerte y la lista de activos (hecho · minuto · palanca).
  2. **Las 5 parejas**, de más a menos recomendada, cada una con: letra, ángulo y palanca; **título** (con su nº de
     caracteres); **texto de la miniatura** o «sin texto»; la segunda lectura en dos frases; qué pregunta deja abierta;
     **qué adjuntar** (la cara: `youtube/A.jpg` + `A_cara.jpg`, iguales para las cinco; y, si la lleva, la imagen del
     animal u objeto real con su minuto y clip); **de qué momento del vídeo sale** lo que se enseña (minuto); **idea en
     español**; **prompt** en un bloque de código para copiar; retoques.
  3. **Qué probar primero**: las tres para «Probar y comparar» de YouTube (admite hasta 3 combinaciones de título y
     miniatura y elige por tiempo de visualización, no por clics; si el canal solo deja probar miniaturas, las tres con
     el título de la A) y por qué esas. Las otras dos quedan de recambio si el vídeo arranca flojo, con 2–3 títulos
     sueltos más. Si se cambia un título ya publicado, revisa la miniatura: su rótulo puede quedarse sin ancla (BM: el
     rótulo respondía al título viejo, x0,19).
  4. **Descripción**, capítulos y etiquetas (`base/descripciones.md`).
  5. **Comprobado y por confirmar**: lo que el creador debe revisar (nombres, cifras, caras de terceros) y lo que
     depende de algo que el estudio no resuelve (§ 6, último bloque).
- `youtube/A.jpg` y `youtube/A_cara.jpg` (la cara, para las cinco) y, solo si alguna lleva el animal u objeto real,
  su imagen (`C2.jpg`…). Las descartadas se borran: en la carpeta solo queda lo que se adjunta.
- `out/AAAA-MM-DD_<slug>.txt` — solo lo que se pega en YouTube: los 5 títulos, la descripción con capítulos y las
  etiquetas. Si el vídeo aún no está entregado en `out/` (se hace el paquete sobre una versión de prueba),
  `youtube/pegar.txt`, y se mueve al entregar.
- Ejemplo completo: `base/ejemplos/ramon/youtube/PAQUETE.md` (vídeo en inglés, canal de animales).

Al entregar, **enseña en el chat** los cinco títulos con el texto de su miniatura y la idea de cada imagen; el resto,
en el archivo. Cuando quien edita traiga las miniaturas generadas: `miniatura.py final A <imagen> …` → mira
`youtube/prueba.jpg` (a 168 px: ¿se entiende?, ¿se lee?, ¿es su cara?, ¿es la especie?) y dilo.

Lo que el creador elija, lo que cambie y lo que gane el test **se apunta** (`SKILL.md` § 3): en
`personal/<creador>/preferencias.md` → «Títulos y miniaturas» si es de su canal; aquí, si vale para todos.

## 9. Personalizar y ampliar

- **El canal del creador es la mejor referencia.** Con `PY herramientas/canal_youtube.py @sucanal` se bajan sus títulos,
  descripciones y miniaturas con el ratio de cada vídeo, las hojas pequeñas y las hojas `detalle/` (4 miniaturas
  grandes por hoja, de mayor a menor ratio). Un agente con `base/refs/_youtube/ENCARGO_CANAL.md` saca qué le funciona
  A ÉL; con `base/refs/_youtube/ENCARGO_DETALLE.md`, el estudio al detalle (recorrido del ojo, cara, manos, instante,
  texto, encaje y segunda lectura, vídeo a vídeo). Las conclusiones, a `personal/<creador>/preferencias.md` → «Títulos
  y miniaturas» (sus moldes, su tono, su tipografía y color de texto, lo que nunca hace). Mandan sobre estas bases.
- **Lee su ratio con cuidado** (`base/refs/_youtube/METODO.md`): separa tema, serie, invitado y época; corrige por
  antigüedad y por la caída normal de una serie (−2 a −3 % por episodio); descuenta estrenos pegados y vueltas tras un
  parón; mira los «me gusta» por visita (ratio alto con pocos «me gusta» = gente de fuera).
- **Copiar un molde de otro canal no copia su resultado** (CC copió letra a letra un título de PC: x0,88 frente a x2,68):
  copia el mecanismo, adaptado a su público y a su tamaño.
- **Marca de miniatura**: mismo tipo de letra, mismo color de acento (`marca.json`) y mismo tratamiento vídeo tras
  vídeo; el parecido entre miniaturas hace canal, sin repetir la paleta ni la escena de la semana anterior (§ 6, 22).
  Si tiene una serie que funciona, la serie es la marca: la misma imagen con una variable (BM, indicio). Se apunta la
  primera vez que el creador aprueba una.
- **Otro canal de referencia** (un nicho nuevo, otro idioma): mismo método, `base/refs/_youtube/METODO.md`.
