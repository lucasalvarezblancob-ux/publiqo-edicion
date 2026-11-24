import React from "react";
import { AbsoluteFill, Easing, interpolate, useVideoConfig } from "remotion";
import { ACENTO } from "./marca";
import { F_ANCHA, F_TXT, fuente } from "./fuentes";
import { Item, contorno } from "./Graficos";

// KIT DE INTROS (base/intros.md → «Dos tipos de intro»; números de base/refs/dinamicos/estilos/INTROS_corta_vs_explicativa.md).
// Solo salen si el plan.py del vídeo los pide (PARTIDAS, MAQUINA, CONTADORES, CARTELAS_DIA, OSCURECER): un vídeo que no
// los pide sale exactamente igual que antes. Medidas en fracción del alto (H).

// Etiqueta PARTIDA «izquierda | derecha» (Alessio Pierucci): dos palabras a media altura que flanquean al sujeto
// centrado; la de la izquierda aparece de golpe (1 f, sin animación) y la de la derecha `desfase` fotogramas después
// (11–15). Blancas, sin caja ni borde, 4,2 % del alto. Sirve para el nombre del creador, el título, «lugar | hora».
export const Partida: React.FC<{ f: number; it: Item }> = ({ f, it }) => {
  const { height: H, width: W } = useVideoConfig();
  const fs = H * (it.alto ?? 0.042) * 1.38;            // alto de mayúscula ≈ 0,72 del cuerpo
  const y = H * (it.y ?? 0.495);
  const color = it.color ?? "white";
  const est: React.CSSProperties = { position: "absolute", top: y - fs / 2, fontFamily: it.fuente === "ancha" ? F_ANCHA : F_TXT, fontWeight: it.peso ?? 600,
    fontSize: fs, lineHeight: 1, color, letterSpacing: -fs * 0.01, whiteSpace: "nowrap", textShadow: it.sombra === false ? "none" : `0 0 ${fs * 0.12}px rgba(0,0,0,.55), 0 ${fs * 0.03}px ${fs * 0.06}px rgba(0,0,0,.35)` };      // se lee sobre cielo claro (banco)
  return (
    <AbsoluteFill>
      <div style={{ ...est, left: W * (it.margen_izq ?? 0.077) }}>{it.izq}</div>
      {f >= (it.desfase ?? 11) ? <div style={{ ...est, right: W * (it.margen_der ?? 0.095) }}>{it.der}</div> : null}
    </AbsoluteFill>
  );
};

// LEMA A MÁQUINA (Alessio): una letra por fotograma (`cps` letras por fotograma), sin cursor, anclado a la izquierda
// dentro de una caja centrada (la frase no «baila» mientras se escribe), y quieto `fijo` fotogramas al acabar.
// Sobre negro de serie (fondo: "negro" | "ninguno").
export const Maquina: React.FC<{ f: number; it: Item }> = ({ f, it }) => {
  const { height: H, width: W } = useVideoConfig();
  const txt = String(it.txt ?? "");
  const fs = Math.min(H * (it.alto ?? 0.034) * 1.38, (W * 0.84) / (Math.max(txt.length, 8) * 0.55));
  const n = Math.min(txt.length, Math.floor((f + 1) * (it.cps ?? 1)));
  return (
    <AbsoluteFill style={{ backgroundColor: it.fondo === "ninguno" ? "transparent" : "black", justifyContent: "center", alignItems: "center" }}>
      {/* Letra de la referencia (Alessio: grotesca tipo Helvetica/Inter, peso ~800, interletra cerrada −0,04 em, caja normal;
          Lucas, banco 2026-11-24: «no es la misma fuente, en la referencia es más bold»). `fuente`: "ancha", "textos" o el
          nombre de una Google Font. El texto va como se escribe en el plan: nada de mayúsculas forzadas. */}
      <div style={{ position: "relative", fontFamily: it.fuente === "ancha" ? F_ANCHA : it.fuente === "textos" ? F_TXT : fuente(it.fuente ?? "Inter", F_TXT),
        fontWeight: it.peso ?? 800, letterSpacing: it.espaciado ?? "-0.04em", fontSize: fs, color: it.color ?? "white", whiteSpace: "pre" }}>
        <span style={{ visibility: "hidden" }}>{txt}</span>
        <span style={{ position: "absolute", left: 0, top: 0 }}>{txt.slice(0, n)}</span>
      </div>
    </AbsoluteFill>
  );
};

// CONTADOR animado (Nil OGT, «172.5 M»): de `desde` a `hasta` con frenada (ease-out) en `dur_f` fotogramas (~28), en el
// color de acento, con sufijo y una flecha opcional que apunta a lo que se cuenta.
export const Contador: React.FC<{ f: number; it: Item }> = ({ f, it }) => {
  const { height: H, width: W } = useVideoConfig();
  const v = interpolate(f, [0, it.dur_f ?? 28], [it.desde ?? 0, it.hasta ?? 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const dec = it.dec ?? (Number.isInteger(it.hasta) ? 0 : 1);
  const num = v.toLocaleString(it.idioma === "en" ? "en-US" : "es-ES", { minimumFractionDigits: dec, maximumFractionDigits: dec });
  const txt = `${it.prefijo ?? ""}${num}${it.sufijo ?? ""}`;
  // ancho real medido en el banco (letra ancha con +0,03 em): ~0,74 del cuerpo por carácter + 0,9 la flecha. El MISMO
  // cálculo está en comun.caja_texto: si no coinciden, la comprobación de «se sale» y la colocación fallan (banco 2026-11-24).
  const fs = Math.min(H * (it.alto ?? 0.14), (W * 0.42) / (Math.max(txt.length, 2) * 0.74 + (it.flecha ? 0.9 : 0)));
  const ent = interpolate(f, [0, 4], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      {/* letterSpacing +0,03 em: en la letra ancha la coma se pegaba al «2» y al «5» (revisión del banco, 2026-11-24).
          La flecha es un SVG del alto de las mayúsculas y alineado con ellas (el carácter «↑» salía más bajo y pequeño). */}
      <div style={{ position: "absolute", left: W * (it.x ?? 0.5), top: H * (it.y ?? 0.4), transform: `translate(-50%,-50%) rotate(${it.giro ?? 0}deg)`, opacity: ent,
        fontFamily: F_ANCHA, fontWeight: 900, fontSize: fs, lineHeight: 1, color: it.color ?? ACENTO, ...contorno(H * 0.005), whiteSpace: "nowrap", letterSpacing: "0.03em", display: "flex", alignItems: "baseline" }}>
        <span>{txt}</span>
        {it.flecha ? <Flecha alto={fs * 0.72} dir={it.flecha} color={it.color ?? ACENTO} grueso={H * 0.005} /> : null}
      </div>
    </AbsoluteFill>
  );
};

const Flecha: React.FC<{ alto: number; dir: string; color: string; grueso: number }> = ({ alto, dir, color, grueso }) => {
  const rot = { arriba: 0, der: 90, abajo: 180, izq: 270 }[dir] ?? 0;
  return (
    <svg viewBox="0 0 100 100" width={alto} height={alto} style={{ marginLeft: alto * 0.15, flexShrink: 0, overflow: "visible", transform: `rotate(${rot}deg)`, filter: `drop-shadow(0 ${grueso * 1.6}px ${grueso * 2.5}px rgba(0,0,0,.6))` }}>
      {/* una sola forma: contorno negro (trazo) por debajo y relleno encima, sin cruces visibles */}
      <path d="M50 4 L94 50 L66 50 L66 96 L34 96 L34 50 L6 50 Z" fill={color} stroke="#000" strokeWidth={grueso * 100 / alto * 2} strokeLinejoin="round" paintOrder="stroke" />
    </svg>
  );
};

// CARTELA DE CAMBIO DE DÍA (Alessio): destello blanco `flash_in` f → negro con el texto `negro` f → destello `flash_out` f.
// Tapa la imagen entera (va encima de todo). El obturador o el whoosh que muere en el destello van en su sonido.
export const CartelaDia: React.FC<{ f: number; dur: number; it: Item }> = ({ f, dur, it }) => {
  const { height: H } = useVideoConfig();
  const fi = it.flash_in ?? 6, fo = it.flash_out ?? 5;
  const blanco = f < fi ? interpolate(f, [0, fi], [1, 0]) : f >= dur - fo ? interpolate(f, [dur - fo, dur], [0, 1]) : 0;
  return (
    <AbsoluteFill style={{ backgroundColor: "black", justifyContent: "center", alignItems: "center" }}>
      <div style={{ fontFamily: F_TXT, fontWeight: 600, fontSize: H * (it.alto ?? 0.022) * 1.38, color: "white", opacity: f >= fi && f < dur - fo ? 1 : 0 }}>{it.txt}</div>
      <AbsoluteFill style={{ backgroundColor: "white", opacity: blanco }} />
    </AbsoluteFill>
  );
};

// OSCURECER el fondo (Nil: icono o rótulo con el fondo al 45–50 %; Plex: rótulo de sección sobre el plano al 50 %).
// Entra y sale en `fundido` fotogramas. Lo que deba quedar por encima (el texto, la persona recortada) va en otra capa.
export const Oscurecer: React.FC<{ f: number; dur: number; it: Item }> = ({ f, dur, it }) => {
  const d = it.fundido ?? 4;
  const o = Math.min(interpolate(f, [0, d], [0, 1], { extrapolateRight: "clamp" }), interpolate(f, [dur - d, dur], [1, 0], { extrapolateLeft: "clamp" }));
  return <AbsoluteFill style={{ backgroundColor: "black", opacity: (it.nivel ?? 0.5) * o }} />;
};

export const TIPOS_INTRO = new Set(["partida", "maquina", "contador", "cartela_dia", "oscurecer"]);

export const PiezaIntro: React.FC<{ f: number; dur: number; it: Item }> = ({ f, dur, it }) => {
  if (it.t === "partida") return <Partida f={f} it={it} />;
  if (it.t === "maquina") return <Maquina f={f} it={it} />;
  if (it.t === "contador") return <Contador f={f} it={it} />;
  if (it.t === "cartela_dia") return <CartelaDia f={f} dur={dur} it={it} />;
  if (it.t === "oscurecer") return <Oscurecer f={f} dur={dur} it={it} />;
  return null;
};
