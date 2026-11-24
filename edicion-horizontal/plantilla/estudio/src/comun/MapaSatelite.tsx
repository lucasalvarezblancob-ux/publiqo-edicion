import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useVideoConfig } from "remotion";
import { ACENTO } from "./marca";
import { F_ANCHA } from "./fuentes";
import { borde, entra, Item, sale } from "./Graficos";

// Mapa de satélite animado (recurso estándar: a Lucas le gustó en `ramon`, 2026-11-11).
// Receta (refs/dinamicos/_mapas): base de SATÉLITE, la cámara VUELA hacia la zona (~1,2 s con aceleración y frenada),
// el BORDE se dibuja progresivamente (~1,2 s), el RELLENO llega después (~0,5 s) y al final SALTA la etiqueta.
// Las regiones ya presentadas quedan encendidas más tenues. Nada de mapa plano vectorial con fundidos.
//
// Base: una imagen equirectangular (grados por píxel constantes) bajada con `herramientas/mapa_satelite.py`
// (NASA Blue Marble vía GIBS, dominio público) y copiada a `estudio/public/<slug>/`. El .json que escribe ese script
// trae lon0, lat0, grados_por_px, ancho y alto: son los campos de `base`.
// Técnica «static map» de la skill remotion-maps: <Img> + SVG animado encima. MapLibre no cargó en render
// (timeout de delayRender), así que para este estilo no hace falta ni clave ni teselas en vivo.
export type Region = {
  n: number; // orden de presentación (para el contador n/total)
  nombre: string; // etiqueta grande
  nota?: string; // píldora pequeña bajo el nombre
  color: string;
  cam: [number, number, number]; // lon, lat del centro del encuadre y escala (1 = 1 px de imagen por px de un lienzo de 2160 de alto)
  pol?: [number, number][]; // contorno aproximado [lon, lat], cerrado; se suaviza solo
  ruta?: [number, number][]; // alternativa a pol: línea abierta [lon, lat] (recorrido), se dibuja igual
};
export type MapaCfg = {
  imagen: string; // ruta dentro de public/, p. ej. "ramon/sudamerica.jpg"
  base: { lon0: number; lat0: number; grados_por_px: number; ancho: number; alto: number };
  regiones: Record<string, Region>;
  general: [number, number, number]; // encuadre de partida (lon, lat, escala)
  cabecera?: string; // texto arriba a la izquierda
  pie?: string; // crédito abajo a la derecha (por defecto, el de la NASA)
};

const suave = (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

// item: { reg: [claves ya encendidas, incluida la nueva], nueva: clave que se presenta }
export const MapaSatelite: React.FC<{ f: number; dur: number; it: Item; cfg: MapaCfg }> = ({ f, dur, it, cfg }) => {
  const { width: W, height: H } = useVideoConfig();
  const { lon0, lat0, grados_por_px: gpp, ancho, alto } = cfg.base;
  const px = (p: number[]): [number, number] => [(p[0] - lon0) / gpp, (lat0 - p[1]) / gpp];
  // contorno suavizado (Catmull-Rom -> Bézier cúbicas); cerrado para polígonos, abierto para rutas
  const curva = (pts: [number, number][], cerrado: boolean) => {
    const P = pts.map(px), n = P.length;
    const g = (i: number) => (cerrado ? P[(i + n) % n] : P[Math.min(Math.max(i, 0), n - 1)]);
    let d = "M" + P[0][0].toFixed(1) + "," + P[0][1].toFixed(1);
    for (let i = 0; i < (cerrado ? n : n - 1); i++) {
      const p0 = g(i - 1), p1 = g(i), p2 = g(i + 1), p3 = g(i + 2);
      const c = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]];
      d += "C" + c.map((v) => v.toFixed(1)).join(",");
    }
    return d + (cerrado ? "Z" : "");
  };
  const camino = (r: Region) => (r.pol ? curva(r.pol, true) : curva(r.ruta ?? [], false));

  const R = cfg.regiones[it.nueva as string];
  const previas = (it.reg as string[]).filter((r) => r !== it.nueva);
  const desde = previas.length ? cfg.regiones[previas[previas.length - 1]].cam : cfg.general;
  const total = Object.keys(cfg.regiones).length;
  // vuelo: abre en el encuadre anterior, del frame 4 al 34 vuela a la zona, luego deriva lenta hacia dentro
  const k = suave(interpolate(f, [4, 34], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const esc = H / 2160;
  const lon = desde[0] + (R.cam[0] - desde[0]) * k, lat = desde[1] + (R.cam[1] - desde[1]) * k;
  const z = (desde[2] + (R.cam[2] - desde[2]) * k) * (1 + 0.0012 * Math.max(0, f - 34)) * esc;
  const [cx, cy] = px([lon, lat]);
  const trazo = interpolate(f, [22, 52], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const relleno = interpolate(f, [46, 60], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const etq = interpolate(f, [54, 58, 62], [0, 1.08, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const [ex, ey] = px(R.cam);
  const o = entra(f, 5) * sale(f, dur, 6);
  const grosor = (H * 0.006) / z;
  return (
    <AbsoluteFill style={{ opacity: o, backgroundColor: "#03060c", overflow: "hidden" }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: ancho, height: alto, transformOrigin: "0 0", transform: "translate(" + (W / 2 - cx * z) + "px, " + (H / 2 - cy * z) + "px) scale(" + z + ")" }}>
        <Img src={staticFile(cfg.imagen)} style={{ position: "absolute", width: ancho, height: alto }} />
        <svg width={ancho} height={alto} style={{ position: "absolute", overflow: "visible" }}>
          {previas.map((r) => {
            const P = cfg.regiones[r];
            return <path key={r} d={camino(P)} fill={P.pol ? P.color : "none"} fillOpacity={0.28} stroke={P.color} strokeOpacity={0.8} strokeWidth={grosor * 0.6} />;
          })}
          {R.pol ? <path d={camino(R)} fill={R.color} fillOpacity={0.42 * relleno} stroke="none" /> : null}
          <path d={camino(R)} fill="none" stroke={R.color} strokeWidth={grosor} strokeLinejoin="round" strokeLinecap="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - trazo} style={{ filter: "drop-shadow(0 0 " + grosor * 2 + "px " + R.color + ")" }} />
        </svg>
      </div>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%)" }} />
      <div style={{ position: "absolute", left: W / 2 + (ex - cx) * z, top: H / 2 + (ey - cy) * z, transform: "translate(-50%, -50%) scale(" + etq + ")", opacity: Math.min(etq, 1), textAlign: "center", whiteSpace: "nowrap" }}>
        <div style={{ fontFamily: F_ANCHA, fontSize: H * 0.085, fontWeight: 900, color: "white", lineHeight: 1, textShadow: borde(H * 0.005) }}>{R.nombre}</div>
        {R.nota ? <div style={{ display: "inline-block", marginTop: H * 0.012, background: R.color, color: "#0b1016", fontWeight: 800, fontSize: H * 0.03, padding: H * 0.005 + "px " + H * 0.016 + "px", borderRadius: H * 0.008 }}>{R.nota}</div> : null}
      </div>
      <div style={{ position: "absolute", left: H * 0.07, top: H * 0.07, display: "flex", alignItems: "center", gap: H * 0.018 }}>
        {total > 1 ? <div style={{ background: ACENTO, color: "#14160a", fontWeight: 800, fontSize: H * 0.04, padding: H * 0.004 + "px " + H * 0.018 + "px", borderRadius: H * 0.008 }}>{R.n}/{total}</div> : null}
        {cfg.cabecera ? <div style={{ fontFamily: F_ANCHA, color: "white", fontWeight: 700, fontSize: H * 0.03, textShadow: borde(H * 0.0025) }}>{cfg.cabecera}</div> : null}
      </div>
      <div style={{ position: "absolute", right: H * 0.03, bottom: H * 0.02, color: "rgba(255,255,255,.5)", fontSize: H * 0.016, fontWeight: 600 }}>{cfg.pie ?? "Imagery: NASA Blue Marble"}</div>
    </AbsoluteFill>
  );
};
