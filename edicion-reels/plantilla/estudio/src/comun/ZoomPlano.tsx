// Cámara virtual para versiones de un plano fijo a cámara (Lucas, 2026-11-25, Black Friday 70 %: "12 versiones más, unas
// con un poco de zooms y otras más dinámicas con algo más de zooms" → 3 versiones por vídeo: original / suave / dinámico).
// Envuelve SOLO la capa de vídeo: los textos y subtítulos van fuera, fijos a pantalla.
//   suave:    cada tramo arranca alternando ×1,00 / ×1,06 (acercar/alejar seco en los cortes: tapa el jump cut) y se acerca
//             lento (+1,5 %/s). Nada más.
//   dinamico: zoom de entrada ×1,18→×1,04 en 18 f (con whoosh, lo pone el vídeo), cada tramo alterna ×1,04 / ×1,16, empuje
//             +3 %/s y golpe a cada palabra clave (+12 % en 5 f que vuelve en ~20 f).
// Tope ×1,32 (proxy 4K: no pierde nitidez). Centro = la cara (px de 1080×1920).
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";

export type EstiloZoom = "ninguno" | "suave" | "dinamico";

export const escalaZoom = (frame: number, estilo: EstiloZoom, cortes: number[], golpes: number[], fps = 30): number => {
  if (estilo === "ninguno") return 1;
  const cs = [...cortes].sort((a, b) => a - b);
  let i = 0;
  for (let k = 0; k < cs.length; k++) if (cs[k] <= frame) i = k;
  const ini = cs.length ? cs[i] : 0;
  const t = (frame - ini) / fps;
  let s: number;
  if (estilo === "suave") {
    s = (i % 2 === 0 ? 1.0 : 1.06) + 0.015 * t;
  } else {
    s = (i % 2 === 0 ? 1.04 : 1.16) + 0.03 * t;
    // zoom de entrada
    s += interpolate(frame, [0, 18], [0.14, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
    for (const g of golpes) {
      const d = frame - g;
      if (d >= 0 && d < 26) {
        s += d < 5
          ? interpolate(d, [0, 5], [0, 0.12], { easing: Easing.out(Easing.cubic) })
          : interpolate(d, [5, 26], [0.12, 0], { easing: Easing.inOut(Easing.cubic) });
      }
    }
  }
  return Math.min(s, 1.32);
};

export const ZoomPlano: React.FC<{
  estilo: EstiloZoom;
  cortes: number[]; // frames de salida donde empieza cada tramo (incluye 0)
  golpes?: number[]; // frames de salida de palabras clave (solo "dinamico")
  centro?: { x: number; y: number }; // cara, px de 1080×1920
  children: React.ReactNode;
}> = ({ estilo, cortes, golpes = [], centro = { x: 540, y: 700 }, children }) => {
  const frame = useCurrentFrame();
  const s = escalaZoom(frame, estilo, cortes, golpes);
  return (
    <AbsoluteFill style={{ transform: `scale(${s})`, transformOrigin: `${centro.x}px ${centro.y}px` }}>{children}</AbsoluteFill>
  );
};
