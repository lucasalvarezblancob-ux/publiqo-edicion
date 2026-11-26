# Recursos: cómo clasificarlos, analizarlos y elegirlos — ESTÁNDAR

> Estándar de `edicion-horizontal` (solo lo cambia Lucas). Vale para cualquier nicho. Las reglas de cómo usarlos en un
> vídeo están en `base/preferencias.md` → Planos de recurso. Lo que es de un creador concreto (su cabecera, sus
> cortinillas, su música de siempre y cuándo van) se apunta en `personal/<creador>/recursos.md`, no aquí.
>
> **Todo recurso es de un creador** (Lucas, 2026-11-13): no hay `recursos/` en la raíz de la carpeta de edición. Sus
> fijos, sus clips de archivo y b-roll, sus fotos, mapas, sonidos y música van en **`personal/<creador>/recursos/`**.
> En este documento, `recursos/` es siempre esa carpeta. Por qué: «los recursos tienen que ir ligados a la
> personalización; recursos estará dentro del perfil de creador» y «también los vídeos de recursos, clips, b-roll».
> Una carpeta antigua con `recursos/` en la raíz se pasa con `herramientas/montaje/mover_recursos.py <creador>`.

En un vídeo horizontal hay **tres fuentes** de planos de recurso (los que van encima de la voz):

1. **Los propios brutos del vídeo** (lo normal: se graba mucho más de lo que se usa). Se localizan con el **registro
   visual** (§ 1). No se catalogan en `recursos/`.
2. **Material reutilizable del creador** en `recursos/` (planos de otros días, drones, fotos, mapas), con ficha en
   `recursos/INDICE.md` (§ 2–4).
3. **Material de banco** (foto o clip con licencia) cuando se nombra algo que no hay grabado. Lo decide y lo descarga el
   creador; Claude dice qué falta, no lo baja por su cuenta.

## 1. Registro visual de los brutos (obligatorio antes de montar)

1. `paso0_preparar.py` saca las **hojas densas**: un fotograma por segundo, 36 por hoja, con el segundo rotulado.
2. **Un agente por bruto** (los de más de ~9 min, partidos en rangos) con el encargo de
   `herramientas/montaje/ENCARGO_REGISTRO_VISUAL.md`, **hasta 4–5 a la vez en Mac**; de dos en dos en Windows con 16 GB.
   Cada uno mira todas las
   hojas y escribe `bruto/<slug>-analisis/visual/<clip>.json`: `tramos` (qué se ve en cada momento, tipo, cámara, nota
   0–3 como recurso, de qué se habla), `mejores_recursos` (con inicio y final exactos) y `evitar` (paredes, barridos).
3. Con eso se sabe **qué hay y qué no hay en imagen**. Lo que se nombra y no se ve se apunta para decírselo al creador.

Al elegir cada recurso: tómalo de `mejores_recursos`, **míralo** con `tira.py CLIP t0 t1 0.5` (el primer fotograma ya
tiene que enseñar el sujeto) y, con el plan montado, revísalos todos con `hoja_recursos.py`. Un tramo con nota 0–1 no se usa.

## 2. Carpetas de `recursos/`: todo ordenado por carpetas, por lo que vas a buscar

Como en `edicion-reels` (Lucas, 2026-11-13: «se tienen que ordenar por carpetas como hacíamos en los recursos de la
skill de reels»): **nada suelto**. En la raíz de `recursos/` solo está `INDICE.md`; cada archivo va en la carpeta de su
tema y tiene su ficha. Sin ficha, el clip no existe: al montar se busca en el índice, no mirando carpetas.

- Clasifica por **el tema que ilustra**, que es lo que se busca al montar (la voz dice «la várzea», «cuando lo
  construimos» o «las crías» y hay que encontrar un plano que lo enseñe). No por fecha ni por cámara.
- **Primer nivel = los grandes temas del contenido del creador (5–8). Segundo nivel solo cuando una carpeta pasa de
  ~15 clips o tiene subtemas claros** (`recintos/<recinto>/`, `<país>/<ciudad>/`). Al partir una carpeta, actualiza las
  rutas del índice.
- Las carpetas de tema **se crean al dar de alta al creador**, según su nicho (`perfil.md`), y se apuntan en la tabla
  de arriba de su `INDICE.md`. Ideas:

  | Nicho | Primer nivel | Segundo nivel cuando crezca |
  |---|---|---|
  | Animales / naturaleza | `recintos/` (o `instalaciones/`), `especies/`, `plantas/`, `obras/`, `comida/`, `campo/`, `drones/` | `recintos/<recinto>/`, `especies/<grupo>/` |
  | Viajes | `<país o ciudad>/`, `transporte/`, `alojamiento/`, `comida/`, `paisajes/`, `drones/` | `<país>/<ciudad>/` |
  | Fitness | `gym/`, `running/`, `competicion/`, `aire-libre/`, `lifestyle/`, `recuperacion/` | `gym/<zona muscular>/` |
  | Cocina | `recetas/`, `ingredientes/`, `mercado/`, `emplatado/`, `comiendo/` | `recetas/<tipo de plato>/` |
  | Tech / negocio | `setup/`, `pantalla/`, `producto/`, `oficina/`, `eventos/` | `producto/<marca>/` |

- **Siempre existen** (las crea `nuevo_creador.py`): `marca/` (sus archivos fijos ORIGINALES: intro, outro,
  cortinillas, logos, mascota; § 8), `creador/` (él **sin acción concreta**: a cámara, andando, posados; sirven para
  ganchos y cierres), `fotos/` (fotos y recortes PNG), `mapas/` (bases de satélite con su `.json`), `musica/` (con
  `CATALOGO.md`) y `sonidos/` (efectos propios; los de serie están en `estudio/public/sonidos/`).
- Si un clip encaja en dos carpetas, va a la del **tema principal** y el otro tema se apunta en **Temas**.
- Un clip de `recursos/` se pide en `edl.py` y en `plan.py` como un bruto, por su nombre de archivo sin extensión, esté
  en la carpeta que esté (`BROLL = [(ancla, "2026-05-02_construccion-estanque", 12.0, 2.6)]`,
  `V("intro", 0, 4.8, vol=0)`): **no repitas nombres entre carpetas**.
- Los brutos ya editados que no sirven como recurso genérico van a `bruto terminado/`.

## 3. Nombre y análisis de un clip

- Nombre: `AAAA-MM-DD_<que-se-ve>[_<detalle>].ext`, minúsculas con guiones; la fecha es la de grabación
  (`ffprobe -v error -show_entries format_tags=creation_time`). El nombre original (`C0247`) va en la ficha.
  Clips de una misma sesión: `AAAA-MM-DD_<sesion>_NN-<que-se-ve>.ext` (`NN` = orden en que se grabaron).
- Técnica con `ffprobe`: duración, resolución, fps, giro y **HDR o SDR** (`color_transfer` = `arib-std-b67` o
  `smpte2084` → HDR: `sdr.py` convierte solo los trozos que se usen; preferencias → COLOR) y **si está en Log**
  (`herramientas/color_log.py <clip>`: se revela con el LUT de su perfil; G009).
- Vista general con `herramientas/hoja_contactos.sh CLIP hoja.jpg 1` (una celda por segundo) y, donde haya algo bueno,
  más fino (`… 0.25 <inicio> <duración>`) para dar inicio y final exactos.
- Si hablan: `herramientas/transcribir.sh` (el idioma se detecta) → qué se dice y si el audio sirve.
- **Un lote de clips (o una biblioteca entera de un disco): `herramientas/inventario_recursos.py`**, siempre:
  1. `PY herramientas/inventario_recursos.py pendientes`: qué clips no tienen ficha, qué fichas son POBRES (y por qué),
     duplicados, nombres repetidos entre carpetas y fichas de archivos que ya no están. Encuentra sola la carpeta
     (`personal/<creador>/recursos`, aunque esté enlazada a un disco; con varios creadores, `--creador <nombre>`).
  2. `… preparar [--transcribir]`: técnica, hoja de contactos con la leyenda de segundos, audio y lo que se dice de cada
     clip, y los lotes (`herramientas/alta_recursos/lote_NN.md`, la misma sesión junta). Se retoma si se corta.
  3. Un agente por lote con `herramientas/ENCARGO_RECURSOS.md` (formato, criterios y ejemplos), en paralelo: hasta
     4–5 en Mac, de dos en dos en Windows con 16 GB.
  4. `… juntar [--mover]`: mete las fichas en `INDICE.md` (sustituye la vieja del mismo archivo; con `--mover`, mueve y
     renombra cada clip a su carpeta y nombre, con `deshacer_movimientos.sh`) y `… comprobar`: sale con error si queda
     un clip sin ficha o una ficha pobre. **Una ficha pobre no se da por buena**: se repite su lote.
  Por qué (Lucas, 2026-11-17): «tiene que haber un buen contexto generado de cada vídeo de recursos. No puede ser un
  contexto pobre, porque así los timings son buenos a la hora de meter la edición». **Causa:** el método estaba escrito,
  pero «agentes en paralelo y se juntan las fichas» sin encargo fijo daba fichas desiguales (unas con la línea de tiempo
  segundo a segundo, otras de una frase sin Vibe ni Temas), y nada medía si una ficha bastaba para editar.

## 4. La ficha en `recursos/INDICE.md`: contexto RICO (lo único que se lee al editar)

Al editar nadie vuelve a mirar el clip: se elige y se corta con la ficha. Por eso lleva **cada segundo del clip con lo
que pasa** (Momentos), lo mejor (Útil), y para qué frases de voz sirve (Temas). Formato y ejemplos buenos y malos:
`herramientas/ENCARGO_RECURSOS.md`.

```
- `carpeta/AAAA-MM-DD_que-se-ve.MP4` (C0123, 42 s, 3840×2160 25 fps SDR, trípode)
  **Qué se ve**: sujeto y acción, quién sale, dónde, encuadre.
  **Momentos**: 0–1,8 coloca la cámara (no sirve) · 1,8–6,2 **la sulcata muerde la lechuga, primer plano** · 6,2–9,5 … · 41+ se va.
  **Útil**: **1,8–6,2** (el mejor) · 12–15,5 (pequeña: zoom ×1,3 a la derecha).
  **Vibe**: sitio, luz, época, energía. **Temas**: «…» · «…» · «…» (3–5 frases de voz).
  **Outfit**: si sale una persona. **Audio**: sirve / quitar (por qué). **Ojo**: matrículas, caras, marcas, la casa.
  Usado en: <slug> (tramos)
```

Mínimo para que valga (lo mide `inventario_recursos.py comprobar`): la línea de tiempo cubre el 70 % del clip (50 % en
clips de más de 3 min) con un tramo cada 10–15 s como mucho; Útil, Vibe, Temas (≥ 2) y Audio; ≥ 35 palabras.

- Cada ficha, en la **sección de su carpeta** (`## recintos/varzea/`). Clips de la misma sesión: una cabecera
  de sesión con lo común (fecha, sitio, luz, outfit, técnica) y debajo una línea por clip con lo que cambia.
- Tiempos en segundos del archivo original. Si sale una persona, apunta **outfit** (para que case con el vídeo).
- Si hay marcas, matrículas o caras de terceros, apúntalo.

Un tramo es **útil** si el sujeto se entiende en menos de 1 s y ya está en imagen en el primer fotograma, la cámara está
estable, está enfocado y bien expuesto, y dura al menos 2,5 s. En 16:9 el sujeto debe ocupar una parte clara del cuadro:
si queda pequeño, apunta dónde está para cerrarle zoom (hasta ×1,4 sin que se note en 4K).

## 5. Elegir recursos para un vídeo

1. **Tema**: lo que ilustra **la frase que suena en ese momento**. Manda sobre todo lo demás. Se busca en
   `personal/<creador>/recursos/INDICE.md` por **Temas** y «Qué se ve» (y en el registro visual de los brutos del día).
   **El tramo sale de la ficha**: de **Momentos** y **Útil**, con su segundo exacto de entrada (`BROLL`), empezando en
   el gesto y no en el arranque; la duración, la que cubre la frase.
2. **Del mismo día y sitio antes que de archivo**: primero los brutos del vídeo; luego `recursos/` que casen en sitio,
   luz, época y outfit.
3. **Técnica**: la mejor resolución que haya; HDR y SDR se pueden mezclar: `sdr.py` pasa a SDR los trozos HDR que se usan.
4. **Variedad**: no repitas un tramo en el mismo vídeo; mira «Usado en» para no repetir el mismo clip en vídeos seguidos.
5. **Si nada encaja**: primero el banco de stock del ordenador (§ 5 bis: Shutterstock con Claude in Chrome, si
   `personal/bancos.md` dice que hay); si tampoco, se queda el plano a cámara (con zoom o texto) y se le dice al creador
   qué falta. No se inventa nada.
6. **Menciones sin imagen → archivo** (Lucas, 2026-11-12). Al estudiar los brutos se hace la lista de **todo lo que se
   nombra y no se ve en ellos**: el pasado («cuando construimos esto»), especies, sitios, plantas, obras, otra época.
   Para cada mención se busca en `recursos/INDICE.md` (por tema, especie, sitio y época) y, si hay clip, va sobre su
   voz cuando lo nombra: una mención, un plano; no una ristra. Las que se quedan sin imagen se entregan al creador
   como **lista de material que falta** (qué, en qué minuto lo dice, cuántos segundos haría falta) y se apuntan en
   `personal/<creador>/recursos.md` para ir llenando el archivo: cuando llegue el clip, ese vídeo y los siguientes
   lo usan. Archivo de otra época: se nota que es de archivo y no pasa nada si cuenta el pasado; si cuenta el
   presente, que case en sitio y luz (punto 2).

Al acabar el vídeo, añade «Usado en: <slug> (tramos)» en la ficha de cada recurso de `recursos/` usado.

## 5 bis. Música nueva y vídeo de stock: Shutterstock con Claude in Chrome, primero

**Orden para lo que no está en los brutos ni en `recursos/` del creador** (pistas nuevas, el animal o el sitio que se
nombra y no hay, un plano de recurso): 1) **Shutterstock, buscado y descargado por Claude con Claude in Chrome** en el
navegador de ese ordenador, si `personal/bancos.md` dice que tiene sesión; 2) el banco que el creador use (su
`perfil.md`); 3) solo si no hay nada de eso, bancos gratis (Mixkit, Pexels) o el plano a cámara. Por qué: Lucas,
2026-11-17, «para sacar músicas nuevas y vídeos de stock, prioritariamente la skill debería usar Claude in Chrome con
Shutterstock… la primera vez se haga un test de si tiene Shutterstock… y así para músicas nuevas, etcétera, siempre
puedes usar Claude in Chrome en ese ordenador». (En alimentacion la música salió de Mixkit porque era una prueba sin
banco: con Shutterstock en el ordenador, no vuelve a pasar.)

**`personal/bancos.md`: lo que hay en ESTE ordenador** (local, no va en git; uno por carpeta de edición, sirve para
todos los creadores de esa carpeta). Si no existe, **la primera vez que haga falta música o stock se hace la prueba**:
1. ¿Hay Claude in Chrome? (`tabs_context_mcp` responde). Si hay varios navegadores conectados, se elige con
   `switch_browser` y lo confirma quien edita; se apunta cuál es.
2. Pestaña nueva en `https://www.shutterstock.com/`: ¿hay sesión iniciada (menú de la cuenta, «Descargas» o
   «Licencias») o pide «Iniciar sesión»? En el menú de la cuenta, qué cubre el plan (música, vídeo, imágenes) y los
   créditos que quedan, si se ven. **Claude nunca inicia sesión ni escribe contraseñas**: si no hay sesión, se le
   pide a quien edita que la inicie él en ese navegador y se repite la prueba.
3. Si no hay Claude in Chrome o no se puede comprobar, se pregunta en una línea: «¿tienes Shutterstock (música y/o
   vídeo)? ¿lo abro con Claude in Chrome en este ordenador?».
4. Se escribe `personal/bancos.md`:
   ```
   # Bancos de este ordenador (prueba: AAAA-MM-DD)
   - Shutterstock: SÍ | NO | SIN SESIÓN — por Claude in Chrome, navegador «<nombre que da switch_browser>»
     - cubre: música sí/no · vídeo sí/no · imágenes sí/no · créditos: <n o «no se ve»>
   - Otros bancos: …
   - Notas: (lo que falle al descargar, cambios de la web)
   ```
   Si una descarga falla porque se cerró la sesión o cambió el plan, se repite la prueba y se actualiza el archivo.

**Cómo se usa** (con `bancos.md` en SÍ):
- **Buscar y escuchar/ver previas, libre**: se busca por mood, género y BPM (música) o por lo que dice la frase
  (vídeo: la especie exacta, el sitio, el gesto; en un canal de animales, la especie correcta o nada). Para cada hueco,
  2–3 candidatos.
- **Descargar, con UNA confirmación por tanda**: antes de descargar se enseña la lista (pista o clip, id, duración,
  para qué ventana o frase, y créditos que gasta si el plan los cuenta) y quien edita dice «sí» una vez para esa tanda;
  no hace falta pedir pista a pista. **Nunca** extras de pago (stems, licencias ampliadas, comprar créditos o cambiar
  de plan) ni aceptar condiciones nuevas: si la web los pide, se para y se pregunta.
  Excepción: si en la ventana de arranque (SKILL.md § 2, paso 0) se eligió «Librería y stock», ese sí vale para todas las tandas del vídeo: no se vuelve a preguntar, pero solo
  para lo que no hay en los brutos ni en su librería, y al entregar se lista cada descarga (id, para qué, créditos).
  Los extras de pago y las condiciones nuevas se siguen preguntando siempre (Lucas, 2026-11-24).
- Lo descargado va a la carpeta del creador: música a `recursos/musica/` + `CATALOGO.md` (con banco e id); vídeo a
  la carpeta de su tema + ficha en `recursos/INDICE.md` (banco, id, «stock»). Así el siguiente vídeo ya lo tiene.
- Las previas con marca de agua no se usan nunca en un vídeo.
- Los pasos de la web (botones, formatos) se apuntan en «Shutterstock, lo aprendido» (§ 6 para música, abajo para
  vídeo) y en `bancos.md` → Notas.
- **El stock también sirve para tapar partes leídas**: si el creador lee de un teleprompter o de notas y no hay otra
  cámara en la que mire al objetivo, se tapa con planos de lo que nombra, uno por frase (preferencias → Planos de recurso).

**Shutterstock vídeo, lo aprendido** (2026-11-19, vaciamos-estanque-2: 14 clips, 33 planos):
- **Resolución**: la más alta viene preseleccionada. Hay clips que **solo** se ofrecen en HD aunque el buscador diga 4K;
  se aceptan si el plano es bueno.
- **Extra de pago**: en cada página aparece «Protecciones legales mejoradas». Se deja **sin marcar** (no hace falta y se
  cobra aparte).
- **Archivos**: bajan como `shutterstock_<id>.mov`/`.mp4`. Pueden ser verticales o DCI 4096×2160: `ffprobe` antes de
  montar. El render recorta al centro a 16:9 lo que no lo es (`hoja_recursos.py` avisa con `AVISO PROPORCIÓN`); un
  vertical, mejor como copia `_h` recortada a mano a la altura del sujeto (preferencias → Lecciones técnicas).
- **Tamaño**: pueden pesar hasta 2,2 GB cada uno (ProRes). Se bajan por tandas y se mueven al disco de recursos del
  creador en cuanto acaban, para no llenar el ordenador.
- **Especie**: en un canal de animales, compruébala en el título de cada clip. Garza real es *Ardea cinerea*, no la garza
  azulada (*A. herodias*) ni garcetas. Cormorán grande es *Phalacrocorax carbo*. Martín pescador común es *Alcedo atthis*.
- **Encuadre**: el sujeto suele salir pequeño. `(zoom, cx, cy)` en el `BROLL` y se mira en `hoja_recursos.py`.
- **Uno por frase**: cada plano empieza en la frase que nombra al animal o lo que hace («se lanzan directamente sobre
  sus presas» → el martín pescador lanzándose; «puede entrar caminando» → garza andando).
- **Ficha**: cada clip con ficha en el `INDICE.md` del creador, en la carpeta de su especie o tema: «**Stock de
  Shutterstock**», id, fecha, resolución y tramos útiles con lo que pasa en cada segundo, para poder reutilizarlo.
- **Cuenta**: `personal/bancos.md` dice si hay cuenta y qué plan.

## 6. Música

- **La skill no trae música.** Cada creador usa su banco con licencia. La música nueva sale primero de **Shutterstock
  con Claude in Chrome** si el ordenador lo tiene (§ 5 bis, `personal/bancos.md`): Claude busca, propone y descarga con
  una confirmación por tanda; nunca se sube nada.
- Van a `recursos/musica/` como `<titulo>_<autor>_<bpm>bpm.wav` (WAV 48 kHz si el banco lo da) y se apuntan en
  `recursos/musica/CATALOGO.md`: título, autor, banco e id, BPM, duración, sonoridad original, mood, energía 1–5 y en
  qué vídeos se ha usado.
- **Claude no puede escuchar.** Mood y energía salen de la ficha del banco (título, etiquetas, BPM) y de medidas
  (sonoridad, dónde sube la energía); se marcan con ✔ cuando el creador las confirma de oído. Al entregar un vídeo, di
  qué pista suena en cada ventana para que la valide.
- Cómo elegir: 2–4 pistas por vídeo largo, una por tono (alegre para gancho y secciones, tranquila para explicación,
  emotiva para el momento serio, épica o con final claro para el cierre). BPM 90–125 para vlog hablado. Instrumentales.
- Dónde suena y a qué nivel: `base/preferencias.md` → Audio (`PISTAS` y `VENTANAS` en `plan.py`).
- **Shutterstock Music, lo aprendido** (2026-11-11): se busca en la caja de búsqueda de música (por mood o género); en la
  ficha de la pista, «Descargar» → «Descargar» otra vez en el panel → formato «Original». **No marcar extras de pago**
  (stems, licencias ampliadas) ni aceptar nada que cambie el plan. Si la web pide iniciar sesión, lo hace el creador.
  El paso a paso de cada banco se apunta en «Notas del banco» del catálogo.

## 7. Mapas

`herramientas/mapa_satelite.py` descarga una base de satélite (NASA Blue Marble por GIBS, dominio público) de la zona
que le pidas a `personal/<creador>/recursos/mapas/<nombre>.jpg` con su `.json` (los límites geográficos, para convertir coordenadas a
píxeles). Se reutilizan entre vídeos: apúntalas en el índice. Las regiones (polígonos) y rutas se definen en el
`Capas.tsx` de cada vídeo (`MapaSatelite`); ejemplo en `base/ejemplos/ramon/Capas.tsx`.

## 8. Recursos fijos de un creador

Su intro, su outro, sus logos, su mascota: los originales van en **`personal/<creador>/recursos/marca/`** (nunca en
la skill) y, ya preparados para superponer, a `estudio/public/personal/<creador>/`. La regla de uso de cada uno,
en `personal/<creador>/recursos.md`. Cómo se monta todo eso: `SKILL.md` § 4.

## 9. Botones de YouTube (recurso de la skill)

16 animaciones de «suscríbete / me gusta / campana», ya sin fondo, en `estudio/public/botones/bNN.webm` (+ `.json` con
sus medidas y `.mp3` con su sonido: clic y campanilla). Se piden en `plan.py`:

```python
BOTONES = [((A, "suscríbete al canal", -1), 2)]                       # abajo al centro, a un tercio del ancho (así va siempre)
BOTONES = [(((A, "suscríbete al canal", -1), -4.1), 2, {"vel": 1.25})]  # empieza 4,1 s antes de la frase y va un 25 % más rápido
```
**Regla (Lucas, 2026-11-12): cada vez que el creador pide suscribirse, dar a me gusta o activar la campana, va uno de
estos botones animados, y va ABAJO EN EL CENTRO.** No a un lado, y no un texto o un botón dibujado en su lugar (el
`SUSCRIBE` dibujado de `plan.py` es antiguo: no se usa para esto). Por qué: «no seguiste la norma de suscribir, al final
pone subscribe en texto en vez de usar lo que te dije» y «cuando se ponga suscribir, lo ponemos abajo en medio con las
animaciones estas, no en un lado» (vídeo: ramon, v5).

Dura lo que dura la animación y suena su propio sonido (0,35). Opciones: `vel` (velocidad; el sonido se acelera igual,
sin cambiar de tono), `esc` (tamaño: ancho del lienzo original; 0,34 de serie desde 2026-11-17: con 0,5 Lucas lo veía «muy grande»), `y` (altura del centro, 0,8 de serie; solo
se cambia si abajo tapa algo que se está enseñando). **Encájalo con la voz**: que el clic en «SUSCRÍBETE» caiga en la
palabra (en el 2, el clic es a los 5,2 s de animación: empieza 5,2 s antes, o 4,1 s con `vel` 1,25) y que la barra se
haya recogido antes del corte siguiente o del outro. Si no cabe: `vel` hasta 1,5 o un botón corto (6, 10).

| Nº | Dura | Qué es | Cuándo |
|---|---|---|---|
| 1 | 8,7 s | Barra blanca redondeada: logo de YouTube, pulgar, «SUSCRITO» y campana; un cursor los pulsa | petición completa (suscríbete + like + campana), sobria |
| 2 | 9,8 s | Barra con el logo rojo de YouTube, pulgar, «SUSCRÍBETE» en rojo que pasa a «SUSCRITO», campana | la petición completa clásica; la más reconocible |
| 3 | 12,0 s | Botón rosa «DALE ME GUSTA» con pulgar que pasa a «COMPARTE» con flecha | cuando pide like y compartir, no suscripción |
| 4 | 10,5 s | Tira gris como la interfaz de YouTube: me gusta / no me gusta, «Suscrito», campana; cursor de flecha | discreta, estilo interfaz |
| 5 | 9,7 s | Pulgar azul, «Suscrito» en rojo sobre blanco y campana roja | suscripción + campana, colorida |
| 6 | 2,6 s | Botón rojo de reproducir + «SUSCRÍBETE PARA MÁS» | **corto**: recordatorio rápido a mitad de vídeo |
| 7 | 6,7 s | Tira **muy pequeña**: «DALE LIKE CRACK» · «SUSCRÍBETE» · «ACTIVA LA CAMPANA» | tono coloquial; el texto es diminuto: súbele `esc` |
| 8 | 7,1 s | Botón grande «Suscrito» + campana amarilla | solo suscripción, grande |
| 9 | 6,0 s | Barra oscura «Suscrito» + campana naranja, cursor de mano | sobre planos claros |
| 10 | 4,5 s | Reproducir en blanco + «SUSCRÍBETE» rojo con campana | **corto** y limpio |
| 11 | 8,4 s | Pulgar azul, «Suscrito» y campana roja con cursor | como el 5, con el cursor pulsando |
| 12 | 8,3 s | Barra gris clara ancha, «SUSCRITO» pequeño y campana | discreta |
| 13 | 8,0 s | Lista de tres renglones: «DALE LIKE», «SUSCRÍBETE», «ACTIVA LA CAMPANA» | cuando pide las tres cosas seguidas; más alta que las barras: mira que no tape |
| 14 | 9,9 s | Botón rojo grande «SUSCRÍBETE» que una mano pulsa y se vuelve campana | la más llamativa: cierre del vídeo |
| 15 | 8,6 s | Tira gris: me gusta / no me gusta, «SUSCRÍBETE» rojo que pasa a gris, campana | estilo interfaz, con el cambio de color |
| 16 | 8,5 s | Barra gris ancha «Suscrito» + campana | discreta |

- **Todos llevan texto en ESPAÑOL, y el texto va en el idioma del vídeo.** En un vídeo en otro idioma se usa la
  **versión traducida** del botón, que `paso3_plan.py` coge sola si existe (`bNN_<idioma>.webm`, según `IDIOMA` de
  `proyecto.py`; si no existe, avisa). Hecha: **el 2 en inglés** (`b02_en`: «SUBSCRIBE» → «SUBSCRIBED»). Para otro
  idioma del 2: `PY herramientas/boton_idioma.py fr "S'ABONNER" "ABONNÉ" --prueba hoja.jpg` y **mira la hoja** (que
  quepa entre el pulgar y la campana, sin restos del texto viejo, con la mano del cursor entera por delante). La
  herramienta solo sabe el 2 (borra el texto fotograma a fotograma, escribe el nuevo con su misma animación y repinta
  el cursor); para traducir otro botón hay que medirlo igual. Nunca un botón en español sobre un vídeo en otro idioma.
- Uno o dos por vídeo como base (al pedirlo y en el cierre); no el mismo dos veces seguidas. Si el creador usa siempre
  uno, se apunta en `personal/<creador>/recursos.md`.
- No pisan otro gráfico ni tapan lo que se enseña: `ver.py` en el frame.
- Son animaciones de banco sobre verde, recortadas con `quitar_fondo.py`. Para añadir otra: mismo método, y a
  `estudio/public/botones/` solo en modo autor (si es de un creador, a `estudio/public/personal/<creador>/`).

## 10. Quitar el fondo a una animación o a un logo

- **Animación sobre verde** (botón, mascota, logo animado): `PY herramientas/quitar_fondo.py ENTRADA SALIDA.webm
  [--t0 S --t1 S] [--modo croma|mate] [--caja x0,y0,x1,y1] [--audio SALIDA.mp3] [--prueba HOJA.jpg]`. `croma` para verde
  puro de banco; `mate` para verde apagado con dibujo de contorno oscuro (mascotas generadas). Deja un `.webm` VP9 con
  transparencia recortado a lo que se mueve y un `.json` con sus medidas. En Remotion: componente `Clip` de `Graficos.tsx`.
- **Logo o dibujo sobre fondo liso** (blanco, crema, negro): `PY herramientas/quitar_fondo_imagen.py ENTRADA SALIDA.png
  [--prueba HOJA.jpg]`. Quita el fondo de fuera y los huecos cerrados de ese mismo color (el interior de una O) y
  respeta lo que es de otro color aunque se parezca (el blanco de un ojo). Un `.png` con canal alfa **no** garantiza
  que el fondo sea transparente: míralo.
- **Mira siempre la hoja de prueba** (sobre oscuro, sobre claro, sobre verde) y, en las animaciones, una hoja con todos
  los fotogramas del tramo que vas a usar. Reglas: `base/preferencias.md` → Clips y gráficos superpuestos.
- Si un logo oscuro va sobre imagen oscura (letras verdes sobre selva), dale un resplandor claro detrás.

- **Logo sobre negro con resplandor** (el brillo claro que se funde con el fondo): `PY herramientas/quitar_fondo_resplandor.py
  ENTRADA SALIDA.png PRUEBA.jpg [FOTOGRAMA.jpg]`. Con `quitar_fondo_imagen.py` el resplandor queda como un cerco oscuro
  sobre fondos claros; esta lo deja en su color con transparencia. Mira la hoja sobre el fotograma real donde irá.

## 11. Mantenimiento

- Al cerrar un edit, los brutos con planos que sirvan para otros vídeos van a su carpeta de tema de `recursos/` con ficha; el
  resto, a `bruto terminado/`.
- Antes de pedirle material nuevo al creador, busca en el registro visual y en el índice.
- **Nunca se borran recursos** (ni a mano ni con la limpieza automática).
