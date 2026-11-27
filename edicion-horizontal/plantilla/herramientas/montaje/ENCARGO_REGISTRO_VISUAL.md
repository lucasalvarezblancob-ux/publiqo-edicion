# Encargo: registro visual de un bruto

Plantilla del encargo que se le da a cada agente (uno por bruto; los brutos de más de ~9 min, partidos en rangos).
Rellena lo que va entre `<…>` y pégalo como prompt. **En Mac, lanza hasta 4–5 agentes a la vez**; en Windows con 16 GB de RAM, de dos en dos.

---

Objetivo: saber **qué se ve en cada momento** del bruto, para que el montador elija bien los planos de recurso (los que
se ponen encima de la voz) y los zooms. Sin este registro se acaban poniendo recursos donde solo se ve una pared o un
barrido de cámara. Todo en español de España.

## Material
- Bruto: `<ruta del bruto>` (`<resolución y fps>`). `<Una frase: de qué va el vídeo, quién sale y en qué idioma habla>`.
- `<Solo si hay varias cámaras: «Este bruto es la cámara <fija en trípode / la que le sigue / …>; a la vez graba <la
  otra>. Puede hablar a una o a otra»>`.
- Hojas densas: `<ANALISIS>/visual/hojas/<clip>_NN.jpg`: un fotograma por segundo, 6 columnas × 6 filas por hoja, con el
  segundo rotulado en cada miniatura (la hoja NN empieza en el segundo NN × 36).
- Transcripción con tiempos: `<ANALISIS>/transcripcion/<clip>.txt` (y `<clip>.w.json` con cada palabra: `p` palabra,
  `t` inicio, `fin`). Úsala para saber de qué se habla mientras se ve cada cosa.

## Qué hacer
1. Mira TODAS las hojas de tu clip (o del rango que te toque: `<t0>`–`<t1>` s), en orden. No te saltes ninguna.
2. Donde haga falta más detalle (cambios rápidos, dudas de qué es, inicio y final exactos de un plano bueno), saca
   fotogramas sueltos con ffmpeg a `<ANALISIS>/visual/tmp_<clip>/` (por ejemplo
   `ffmpeg -nostdin -v error -ss 131.5 -i <bruto> -frames:v 1 -vf scale=960:-1 salida.jpg`) y míralos.
3. Escribe `<ANALISIS>/visual/<clip>.json` (si te toca solo un rango, `<clip>_<t0>-<t1>.json`), JSON válido, así:

```json
{
  "clip": "C0247",
  "resumen": "dos o tres frases: dónde está, qué enseña, en qué orden",
  "donde": "sitio(s) en que transcurre el clip, y de dónde viene y a dónde va el creador si se deduce",
  "tramos": [
    {"t0": 0, "t1": 12, "tipo": "a_camara", "que": "de pie en el garaje hablando a cámara, plano medio",
     "sujeto": "el creador", "camara": "trípode", "recurso": 0, "dice": "presenta la tortuga rusa", "mirada": "camara", "nota": ""}
  ],
  "mejores_recursos": [
    {"t0": 541.0, "t1": 545.5, "que": "tortuga rusa quieta bajo la lámpara, plano cercano estable", "para": "cuando hable de la tortuga rusa o de recintos secos"}
  ],
  "evitar": [
    {"t0": 127, "t1": 135, "por_que": "barrido de cámara: pared, coche y jaulas vacías antes de llegar al acuario"}
  ],
  "momentos": [
    {"t0": 604.8, "t1": 609.5, "que": "se agacha y el micro se le cae al agua del estanque; lo saca chorreando", "tipo": "fail", "luego_dice": "se me ha caído el micro (621 s)"}
  ],
  "personas_fondo": [
    {"t0": 41.5, "t1": 54.1, "donde": "al fondo a la izquierda, entre las plantas; se agacha y cruza hacia el centro", "reconocible": "sí (camiseta blanca, cara visible a ratos)"}
  ]
}
```

- `tramos` cubre el clip (o el rango) entero sin huecos, un tramo por cada cosa distinta que se ve (normalmente 2–15 s;
  un tramo a cámara sin cambios puede durar más). Tiempos en segundos del bruto.
- `tipo`: `a_camara` (habla mirando a cámara), `sujeto` (se ve claramente el animal, objeto, plato, sitio… del que va el
  vídeo), `manos` (enseña algo en las manos), `lugar` (instalación, paisaje, sala, sin sujeto protagonista), `accion`
  (alguien hace algo: entrena, cocina, conduce), `barrido` (la cámara se mueve de un sitio a otro), `transicion`
  (camina, coloca la cámara, borroso, suelo, pared), `otro`.
- `que`: descripción concreta de lo que se VE (qué es, qué hace, encuadre). Nombres propios solo si salen en la transcripción.
- `camara`: `trípode`, `mano estable`, `mano movida`, `barrido`.
- `recurso`: 0 = no vale como plano de recurso; 1 = flojo; 2 = bueno; 3 = muy bueno (sujeto claro, estable y bien
  encuadrado durante al menos 2,5 s seguidos).
- `dice`: de qué habla en ese tramo (una frase, en español), o "" si no habla.
- `mirada` (solo si habla): `camara` (mira a ESTA cámara), `otra_camara` (habla «a cámara», con el tono de quien
  presenta, pero a otro objetivo del rodaje: se le ve de tres cuartos o de perfil y delante no hay nadie con quien
  hable), `fuera_lee` (mira fijo a un lado o un poco por encima del objetivo, como quien lee: teleprompter o notas) o
  `fuera_habla` (habla con alguien fuera de plano). Si dudas entre `otra_camara` y `fuera_habla`, pon `otra_camara` y
  dilo en `nota`. Un tramo leído no se queda en el montaje aunque la voz sea buena: el montador lo tapa con la otra
  cámara o con recursos de lo que nombra. Con varias cámaras, mientras habla, el montador pone en cada frase la cámara
  en la que mira (`camara`).
- `desplazamiento` (solo si alguien se mueve de un sitio a otro: anda, baja escaleras, entra, conduce): de dónde sale y
  a dónde llega, por lo que se ve ("de la piscina, por la portezuela, baja a la terraza de los recintos"). El montador lo
  usa para poner ese plano en el momento del vídeo en que ocurre ese trayecto, no en otro.
- `mejores_recursos`: los mejores tramos para usar como plano de recurso, con inicio y final EXACTOS en los que el sujeto
  ya está en imagen y la cámara estable (comprueba inicio y final con fotogramas sueltos), y para qué frase o tema sirven.
- `evitar`: tramos que por la transcripción parecen aprovechables pero no enseñan nada (paredes, barridos, desenfoques).
- `momentos`: **todo lo que PASA y hace gracia o importa, aunque se vea movido o feo** (nota de recurso 0 da igual):
  un fallo o accidente (se le cae algo, al agua, se rompe, resbala, se moja, se clava algo), un susto, el animal que
  hace algo (roba, salta, se escapa), algo que sale de golpe muy bien o muy mal. `tipo`: `fail`, `susto`, `animal`,
  `exito`, `otro`. Inicio un poco antes de que pase y final cuando ya se ha visto entero (fotogramas sueltos). Si el
  creador lo cuenta después («se me ha caído el micro»), pon en `luego_dice` qué y en qué segundo: **el momento en sí
  vale más que contarlo** y va en el vídeo junto a la frase. Búscalos sobre todo en los segundos de antes de un «se me
  ha caído», «me he mojado», «casi», «¡ay!», «mira lo que ha hecho»: casi siempre la acción no tiene palabras.
- `personas_fondo`: TODA persona que no sea el creador y se vea en el plano, aunque esté lejos, pequeña, de espaldas o
  solo asome por un borde. Mira los bordes y el fondo de cada hoja, no solo el primer plano. Inicio y final exactos con
  fotogramas sueltos. Se difuminan todo el rato que estén en plano (lección de vaciamos-estanque, 2026-11-19: un
  operario trabajando al fondo entre las plantas se escapó porque solo se anotaron las personas en primer plano).
- Apunta en `nota` cualquier cosa que el creador deba decidir: matrículas, caras de terceros, pantallas con datos
  personales, menores, marcas.

## Reglas
- Describe solo lo que ves; si dudas de qué es algo, dilo en `nota`. No inventes especies, marcas ni nombres.
- No modifiques nada fuera de tu JSON y tu carpeta `tmp_<clip>`. No descargues ni subas nada, no toques git.
- En bucles con ffmpeg usa `-nostdin`. Para scripts largos escribe un archivo, no un heredoc.
- Devuélveme al final: la ruta del JSON, el número de tramos, los 5 mejores recursos del clip en una línea cada uno, los
  momentos (fallos, sustos, animales), las personas del fondo, los tramos en que lee (`fuera_lee`) o habla a otra cámara (`otra_camara`) y los avisos (lo que
  NO hay en imagen aunque se hable de ello; lo que haya que tapar).
