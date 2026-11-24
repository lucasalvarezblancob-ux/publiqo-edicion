import React from "react";
import { AbsoluteFill, Easing, interpolate, useVideoConfig } from "remotion";
import { ACENTO } from "./marca";
import { F_ANCHA, F_TXT } from "./fuentes";
import { borde, Item } from "./Graficos";

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
    fontSize: fs, lineHeight: 1, color, letterSpacing: -fs * 0.01, whiteSpace: "nowrap", textShadow: it.sombra === false ? "none" : `0 0 ${H * 0.006}px rgba(0,0,0,.35)` };
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
      <div style={{ position: "relative", fontFamily: it.fuente === "ancha" ? F_ANCHA : F_TXT, fontWeight: it.peso ?? 600, fontSize: fs, color: it.color ?? "white", whiteSpace: "pre" }}>
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
  const fs = Math.min(H * (it.alto ?? 0.14), (W * 0.42) / (Math.max(txt.length, 2) * 0.62));
  const ent = interpolate(f, [0, 4], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: W * (it.x ?? 0.5), top: H * (it.y ?? 0.4), transform: `translate(-50%,-50%) rotate(${it.giro ?? 0}deg)`, opacity: ent,
        fontFamily: F_ANCHA, fontWeight: 900, fontSize: fs, color: it.color ?? ACENTO, textShadow: borde(H * 0.005), whiteSpace: "nowrap" }}>
        {txt}
        {it.flecha ? <span style={{ fontSize: fs * 0.7, marginLeft: fs * 0.15 }}>{it.flecha === "arriba" ? "↑" : it.flecha === "abajo" ? "↓" : it.flecha === "izq" ? "←" : "→"}</span> : null}
      </div>
    </AbsoluteFill>
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
