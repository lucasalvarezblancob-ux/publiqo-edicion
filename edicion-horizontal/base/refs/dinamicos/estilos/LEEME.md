# Estilos de vídeo dinámico

Un **estilo** es una capa opcional encima de `../CONTEXTO.md`. **No sustituye nada**: si nadie pide un estilo, se edita
exactamente como hasta ahora (`../CONTEXTO.md` + la personalización del creador). Así siguen, por ejemplo, los vídeos
de Reino Selva.

## Cuándo se aplica

- **Solo si se pide de forma explícita** para ESE vídeo («edítalo como vlog», «es un vídeo de retos», «estilo viaje»),
  o si el `perfil.md` del creador tiene una línea `Estilo por defecto: <estilo>`.
- Sin estilo pedido ni estilo por defecto → **nada cambia**: `../CONTEXTO.md` tal cual. No se deduce el estilo del
  contenido del bruto: si parece un vlog pero no lo han pedido, se edita como siempre (como mucho, se pregunta en una línea).
- Se apunta en `out/<slug>/proyecto.py`: `ESTILO = "<estilo>"` (o nada, si va sin estilo).

## Orden (lo de abajo manda)

`../CONTEXTO.md` → `estilos/<estilo>.md` → `refs/dinamicos/estilos/<estilo>.md` de la carpeta (local, si existe)
→ `personal/<creador>/` (preferencias, ajustes.py) → lo que pidan para el vídeo.

La personalización del creador sigue mandando sobre el estilo: el estilo cambia ritmo, estructura y recursos de
edición, nunca su marca, sus recursos ni sus reglas.

## Estilos

| Estilo | Estado | Referencias candidatas (ya en `../`) |
|---|---|---|
| [vlog](vlog.md) | sin analizar | Paul Cuffaro ×4 |
| [viaje](viaje.md) | sin analizar | Rubén Holgado (Yakutia, Titanic del Amazonas), YoSoyPlex ×4, TheGrefg (Tailandia) |
| [reto](reto.md) | sin analizar | Rubén Holgado (Avispas, Sumo, Mejor trabajo), ElXokas (Café de Colombia) |
| [visita](visita.md) | sin analizar | Lucas Valero (zoo Fuerteventura), ElXokas (Santuario de Frank) |
| [entreno](entreno.md) | sin analizar | ninguna: hacen falta referencias |

Un estilo **sin analizar** todavía no cambia nada: si lo piden, se avisa en una línea («el estilo X aún no tiene
reglas propias; lo edito con la base y, si quieres, analizo referencias») y se edita con `../CONTEXTO.md`.

## Números del motor

Un estilo puede llevar `<estilo>.py` con los mismos nombres que `personal/<creador>/ajustes.py` (ESCALAS, CAMBIO_CADA,
Z_FUERTE, SFX, MUSICA_NIVELES…). Lo carga `herramientas/montaje/comun.py` solo si `proyecto.py` lleva `ESTILO`:

`estándar de la skill < <skill>/…/estilos/<estilo>.py < refs/dinamicos/estilos/<estilo>.py (local) < personal/<creador>/ajustes.py < plan.py`

Los diccionarios (SFX, MUSICA_NIVELES) se suman: el creador solo pisa las claves que pone. Un ESTILO que no existe
para el montaje con un aviso. Sin `<estilo>.py`, el estilo no cambia ningún número.

## Cómo se llena un estilo

Con 3–5 referencias del estilo, analizadas con `../_analisis/METODO.md`. En `<estilo>.md` solo va **lo que difiere de
`../CONTEXTO.md`** (con números), nunca una copia de lo común, y la sección «Qué NO se hereda» repasada
contra `../CONTEXTO.md`. Los números que lee el motor, en `<estilo>.py`. Un estilo nuevo = un archivo aquí y una fila en la tabla.
