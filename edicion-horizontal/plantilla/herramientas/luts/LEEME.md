# LUTs (G009)

- **Conversión de Log a Rec.709** (`<marca>_<cámara>_<perfil>.cube`, p. ej. `dji_osmo_action5pro_dlogm_vivid.cube`):
  los OFICIALES del fabricante. No van en el repo de la skill (licencias): se bajan aquí a mano o los baja Claude con
  permiso. `PY herramientas/color_log.py luts` dice cuáles hay, cuáles faltan y de dónde bajarlos. El nombre tiene que
  llevar el perfil (dlogm, dlog, applelog, slog3, vlog, clog3, flog, nlog, gplog, logc) y, si hay varios del mismo
  perfil, la cámara. Los de un creador concreto van en `personal/<creador>/recursos/luts/` y mandan sobre estos.
- **Looks de la casa** (`looks/natural.cube`, `calido.cube`, `cine.cube`): los genera `color_log.py` solo la primera
  vez que hacen falta. Son nuestros (sin licencias de terceros).
- Apunta aquí debajo, por cada LUT que bajes: archivo · cámara y perfil · URL oficial · fecha.

| Archivo | Cámara / perfil | Origen | Fecha |
|---|---|---|---|
