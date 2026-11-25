// Texto plano estilo "texto nativo de Instagram/TikTok" (letra Classic, blanca, sombra suave, sin pastilla ni animación
// llamativa). Pedido de Lucas (2026-11-25, Black Friday 70 %): "un gancho de texto al principio… igual de simple, texto
// plano" (ref: reel de fernandovalx "Hasta un 70% en gymshark 🤯") y "20% EXTRA code FERNANDO10" pero con su código.
// Letra: Inter 600 = la aproximación de la casa a la "Classic" de Instagram (como en bicep-fah). Emojis: Apple Color Emoji.
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";

export const F_PLANO = loadInter("normal", { weights: ["600", "700"], subsets: ["latin", "latin-ext"] }).fontFamily;
export const SOMBRA_PLANO = "0 2px 6px rgba(0,0,0,0.55), 0 0 18px rgba(0,0,0,0.25)";
// Sombra más marcada para fondos claros (techo blanco/beige detrás del código arriba).
export const SOMBRA_PLANO_FUERTE = "0 2px 8px rgba(0,0,0,0.75), 0 0 26px rgba(0,0,0,0.5), 0 0 60px rgba(0,0,0,0.25)";

// top: y (px en 1080×1920) del borde superior de la línea. dur: frames que dura (para el fundido de salida; opcional).
export const TextoPlano: React.FC<{ texto: string; top: number; size?: number; dur?: number; peso?: 600 | 700; sombra?: string }> = ({
  texto,
  top,
  size = 52,
  dur,
  peso = 600,
  sombra = SOMBRA_PLANO,
}) => {
  const frame = useCurrentFrame();
  const entra = interpolate(frame, [0, 3], [0, 1], { extrapolateRight: "clamp" });
  const sale = dur ? interpolate(frame, [dur - 4, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 1;
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: top, pointerEvents: "none" }}>
      <div
        style={{
          fontFamily: `${F_PLANO}, "Apple Color Emoji"`,
          fontWeight: peso,
          fontSize: size,
          color: "white",
          letterSpacing: -0.5,
          lineHeight: 1.15,
          textAlign: "center",
          whiteSpace: "pre-line",
          maxWidth: 960,
          textShadow: sombra,
          opacity: Math.min(entra, sale),
        }}
      >
        {texto}
      </div>
    </AbsoluteFill>
  );
};

// Línea del código ("20% EXTRA código ALVAREZ10") que se queda desde `en` hasta el final. Va FUERA de cualquier Sequence
// (usa el frame absoluto). Mientras está en pantalla la suma "50% + 20% EXTRA" (intervalos `suma`, [desde, hasta) en
// frames), la línea se queda solo en "código ALVAREZ10" para no repetir el "20% EXTRA" (Lucas, 2026-11-25: "esto es
// redundante, sale 2 veces en pantalla 20% extra"); se lee como un bloque: "50% + 20% EXTRA / código ALVAREZ10".
// Posición: ARRIBA, encima de la cabeza (top ≈ 290): Lucas señala hacia arriba al decir el código ("cuando señalo
// arriba y digo alvarez10 la idea es que salga mi código de creador arriba", 2026-11-25) → size 56 + sombra fuerte (techo claro).
export const CodigoPlano: React.FC<{ en: number; top: number; codigo: string; suma?: [number, number][]; extra?: string; size?: number; sombra?: string }> = ({
  en,
  top,
  codigo,
  suma = [],
  extra = "20% EXTRA",
  size = 56,
  sombra = SOMBRA_PLANO_FUERTE,
}) => {
  const frame = useCurrentFrame();
  if (frame < en) return null;
  // cambia 2 f antes de que acabe la suma (la suma se funde en sus 4 últimos frames)
  const conSuma = suma.some(([a, b]) => frame >= a && frame < b - 2);
  const entra = interpolate(frame, [en, en + 3], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity: entra }}>
      <TextoPlano texto={conSuma ? `código ${codigo}` : `${extra} código ${codigo}`} top={top} size={size} sombra={sombra} />
    </AbsoluteFill>
  );
};
