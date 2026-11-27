# Edición de vídeo horizontal (YouTube)

Esta carpeta es **solo para editar vídeo horizontal 16:9** (vlogs, viajes, retos, días de entreno, visitas). Para
cualquier petición de edición, intro o recap, rótulos, mapas, música, títulos, miniaturas y descripción de YouTube, referencias o
"que aprendas" de una corrección: **carga primero la skill `edicion-horizontal`**
(`.claude/skills/edicion-horizontal/SKILL.md`).

| Carpeta | Qué hay |
|---|---|
| `personal/<creador>/` | **La PERSONALIZACIÓN de cada creador** (local, fuera de git; una carpeta por creador, se crea con `herramientas/montaje/nuevo_creador.py <nombre>`): `perfil.md`, `preferencias.md` (sus reglas; mandan sobre las bases de la skill), `recursos.md` (sus recursos fijos y cuándo van), `marca.json` (color, canal, @), `ajustes.py` (los números de la base a su gusto), `recursos/` (**todo su material, ordenado por carpetas** y con ficha en `INDICE.md`: `marca/` con su intro, outro, logos y mascota; una carpeta por tema para sus clips de archivo y b-roll; `creador/`, `fotos/`, `mapas/`, `sonidos/` y `musica/` con su `CATALOGO.md`) y `refs/` (cómo edita él). Ver `personal/LEEME.md`. |
| `bruto/` | Bandeja de entrada: brutos pendientes de editar. `bruto/<slug>-analisis/`: transcripciones, hojas y registro visual de cada vídeo. |
| `bruto terminado/` | Brutos ya editados (para repasos). |
| `refs/dinamicos/`, `refs/estudio/` | Tus referencias locales (las estándar vienen con la skill). |
| `out/` | Vídeos terminados (`AAAA-MM-DD_<slug>.mp4`) + `REGISTRO.md`. `out/<slug>/`: el montaje de cada vídeo (`proyecto.py`, `edl.py`, `plan.py`, `trabajo/`) y `youtube/` (el paquete: títulos, prompts de miniatura desde cero con la cara del creador y descripción). |
| `estudio/` | Proyecto Remotion, solo para las capas gráficas. Fuentes en `src/comun/marca.ts`; gráficos propios de cada creador en `src/personal/<creador>/` y sus recursos listos para superponer en `public/personal/<creador>/`; botones de YouTube de serie en `public/botones/`. |
| `herramientas/` | Scripts (análisis, transcripción, proxies, `canal_youtube.py` para estudiar un canal) + `montaje/` (los pasos del montaje, `miniatura.py`) + `.venv`. |

La skill es de solo lectura: lo que cambies o aprendas se queda en esta carpeta. No crees carpetas nuevas en la raíz
sin preguntar (tampoco `recursos/`: los recursos van dentro de cada creador). No se sube nada a ningún sitio (ni vídeos, ni repos) si no lo pide quien edita.
