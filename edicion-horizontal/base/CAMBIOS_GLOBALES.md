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
