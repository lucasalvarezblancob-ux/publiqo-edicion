import React from "react";
import { AbsoluteFill, Easing, interpolate, useVideoConfig } from "remotion";
import { ACENTO } from "./marca";
import { F_ANCHA, F_TXT } from "./fuentes";
import { borde, Item } from "./Graficos";

// PIEZAS DE JUEGO Y DESTELLO (estudio de estilos 2026-11-24: estilos/reto.md «Progreso y estado», vlog.md § En viajes).
// Solo salen si el plan.py los pide (DESTELLOS, MARCADORES, BARRAS, LISTAS, VIDAS, ELIMINADOS): sin pedirlos, nada cambia.
// Reglas medidas: una plantilla por función, siempre igual (mismo sitio, misma letra); el marcador entra MUDO y por corte
// (1 f, sin animación de entrada) y lo que suena es el cambio (casilla, vida, X), con "snd" en el plan.
// Medidas en fracción del alto (H). Esquinas: "si" sup-izq, "sd" sup-der, "ii" inf-izq, "id" inf-der.

const MARGEN = 0.045;   // de la esquina, en fracción del alto
const esquina = (e: string | undefined, W: number, H: number): React.CSSProperties => {
  const m = H * MARGEN, s: React.CSSProperties = { position: "absolute" };
  const k = e ?? "si";
  if (k[0] === "s") s.top = m; else s.bottom = m;
  if (k[1] === "i") s.left = m * 1.3; else s.right = m * 1.3;
  return s;
};
const caja: React.CSSProperties = { background: "rgba(0,0,0,.55)", borderRadius: 10 };

// DESTELLO (reto: blanco 4–8 f que marca «paso siguiente»; vlog: 2 f; Rubén: verde de misión 4 f de subida y 15–18 de
// bajada). Sube en `sube` f hasta `nivel` y baja hasta 0 al final. No es una transición: no cuenta para el tope de 5.
export const Destello: React.FC<{ f: number; dur: number; it: Item }> = ({ f, dur, it }) => {
  const su = Math.max(0, it.sube ?? 0);
  const o = f < su ? interpolate(f, [0, su], [0, 1]) : interpolate(f, [su, dur], [1, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.quad) });
  return <AbsoluteFill style={{ backgroundColor: it.color ?? "white", opacity: (it.nivel ?? 1) * o }} />;
};

// MARCADOR fijo en una esquina («N PLAYERS LEFT», «TOTAL REPS», «DÍA 3/7»): etiqueta pequeña + cifra grande. Si trae
// `desde`, la cifra va de `desde` a `hasta` en `dur_f` f (salto seco si dur_f = 0, como el contador de THE FEZZ).
export const Marcador: React.FC<{ f: number; it: Item }> = ({ f, it }) => {
  const { height: H, width: W } = useVideoConfig();
  const hasta = Number(it.hasta ?? 0), desde = it.desde ?? hasta, d = it.dur_f ?? 12;
  const v = d > 0 ? interpolate(f, [0, d], [desde, hasta], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }) : (f >= 0 ? hasta : desde);
  const num = Math.round(v).toLocaleString(it.idioma === "en" ? "en-US" : "es-ES");
  const fs = H * (it.alto ?? 0.085);
  return (
    <AbsoluteFill>
      <div style={{ ...esquina(it.esquina, W, H), textAlign: (it.esquina ?? "si")[1] === "i" ? "left" : "right", textShadow: borde(H * 0.004) }}>
        {it.etiqueta ? <div style={{ fontFamily: F_TXT, fontWeight: 800, fontSize: fs * 0.3, color: "white", letterSpacing: fs * 0.01, textTransform: "uppercase" }}>{it.etiqueta}</div> : null}
        <div style={{ fontFamily: F_ANCHA, fontWeight: 900, fontSize: fs, lineHeight: 1, color: it.color ?? "white" }}>{it.prefijo ?? ""}{num}{it.sufijo ?? ""}</div>
      </div>
    </AbsoluteFill>
  );
};

// BARRA de progreso (Rubén Titanic: se presenta, vuelve cuando el dato duele y se llena al llegar, 5 → 90 % en 2,6 s;
// MrBeast: 3 barras con %). `desde`/`hasta` en %, llenado con frenada en `dur_f` f.
export const Barra: React.FC<{ f: number; it: Item }> = ({ f, it }) => {
  const { height: H, width: W } = useVideoConfig();
  const p = interpolate(f, [0, it.dur_f ?? 65], [it.desde ?? 0, it.hasta ?? 100], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const ancho = W * (it.ancho ?? 0.34), alto = H * 0.026;
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: (W - ancho) / 2, top: H * (it.y ?? 0.1), width: ancho }}>
        <div style={{ display: "flex", justifyContent: "space-between", fontFamily: F_TXT, fontWeight: 800, fontSize: H * 0.026, color: "white", textShadow: borde(H * 0.003), marginBottom: H * 0.008 }}>
          <span>{it.izq ?? ""}</span><span>{it.pct === false ? (it.der ?? "") : `${Math.round(p)} %`}</span>
        </div>
        <div style={{ ...caja, height: alto, borderRadius: alto / 2, overflow: "hidden", border: `${H * 0.003}px solid white` }}>
          <div style={{ width: `${p}%`, height: "100%", background: it.color ?? ACENTO }} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

// LISTA con casillas (Jesse James West: abajo a la izquierda, 19,7 % × 36,5 %, entra muda por corte; la casilla se
// rellena en 1 f en su frase, con un «ding» en "snd"; Rubén: misiones que se tachan). `items`: textos; `hechas`: índices
// ya marcados al entrar; `marca`: {índice: fotograma (desde el inicio de la pieza) en que se marca}.
export const Lista: React.FC<{ f: number; it: Item }> = ({ f, it }) => {
  const { height: H, width: W } = useVideoConfig();
  const fs = H * (it.alto ?? 0.03), lado = fs * 1.05;
  const hechas = new Set<number>(it.hechas ?? []);
  Object.entries(it.marca ?? {}).forEach(([i, fr]) => { if (f >= Number(fr)) hechas.add(Number(i)); });
  return (
    <AbsoluteFill>
      <div style={{ ...esquina(it.esquina ?? "ii", W, H), ...caja, padding: `${fs * 0.6}px ${fs * 0.8}px` }}>
        {it.titulo ? <div style={{ fontFamily: F_ANCHA, fontWeight: 900, fontSize: fs * 0.9, color: it.color ?? ACENTO, marginBottom: fs * 0.4 }}>{it.titulo}</div> : null}
        {(it.items ?? []).map((t: string, i: number) => (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: fs * 0.5, marginTop: i ? fs * 0.35 : 0 }}>
            <div style={{ width: lado, height: lado, border: `${H * 0.0035}px solid white`, borderRadius: 4, background: hechas.has(i) ? (it.color ?? ACENTO) : "transparent",
              display: "flex", alignItems: "center", justifyContent: "center", color: "black", fontWeight: 900, fontSize: fs * 0.8, fontFamily: F_TXT }}>{hechas.has(i) ? "✓" : ""}</div>
            <div style={{ fontFamily: F_TXT, fontWeight: 600, fontSize: fs, color: "white", textDecoration: hechas.has(i) && it.tachar ? "line-through" : "none", opacity: hechas.has(i) && it.tachar ? 0.7 : 1 }}>{t}</div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// VIDAS (Jesse James West «RULES BROKEN»: 3 corazones, pierde uno cada vez, con un tono de videojuego en "snd").
// `total`, `quedan` (antes) y `pierde_en` (fotograma de la pieza en que se pierde una; sin él, solo enseña).
export const Vidas: React.FC<{ f: number; it: Item }> = ({ f, it }) => {
  const { height: H, width: W } = useVideoConfig();
  const total = it.total ?? 3, antes = it.quedan ?? total, pe = it.pierde_en;
  const quedan = pe != null && f >= pe ? antes - 1 : antes;
  const fs = H * (it.alto ?? 0.06);
  const golpe = pe != null ? interpolate(f, [pe, pe + 3, pe + 9], [1, 1.35, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 1;
  return (
    <AbsoluteFill>
      <div style={{ ...esquina(it.esquina ?? "sd", W, H), display: "flex", flexDirection: "column", alignItems: (it.esquina ?? "sd")[1] === "i" ? "flex-start" : "flex-end" }}>
        {it.etiqueta ? <div style={{ fontFamily: F_TXT, fontWeight: 800, fontSize: fs * 0.38, color: "white", textShadow: borde(H * 0.003), textTransform: "uppercase" }}>{it.etiqueta}</div> : null}
        <div style={{ display: "flex", gap: fs * 0.15 }}>
          {Array.from({ length: total }, (_, i) => (
            <span key={i} style={{ fontSize: fs, lineHeight: 1, filter: i < quedan ? "none" : "grayscale(1) brightness(.45)", transform: i === quedan && pe != null && f >= pe ? `scale(${golpe})` : "none", display: "inline-block" }}>❤️</span>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// X DE ELIMINADO (MrBeast Trap: siempre igual, roja). Aparece en 3 f sobre (x, y) con tamaño `tam` (fracción del alto).
export const Eliminado: React.FC<{ f: number; it: Item }> = ({ f, it }) => {
  const { height: H, width: W } = useVideoConfig();
  const s = interpolate(f, [0, 3], [1.6, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const t = H * (it.tam ?? 0.42), g = t * 0.13;
  const raya = (r: number): React.CSSProperties => ({ position: "absolute", left: 0, top: (t - g) / 2, width: t, height: g, background: it.color ?? "#E3262B", borderRadius: g / 2, transform: `rotate(${r}deg)`, boxShadow: `0 0 ${H * 0.01}px rgba(0,0,0,.6)` });
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: W * (it.x ?? 0.5) - t / 2, top: H * (it.y ?? 0.5) - t / 2, width: t, height: t, transform: `scale(${s})`, opacity: interpolate(f, [0, 2], [0, 1], { extrapolateRight: "clamp" }) }}>
        <div style={raya(45)} /><div style={raya(-45)} />
      </div>
    </AbsoluteFill>
  );
};

export const TIPOS_JUEGO = new Set(["destello", "marcador", "barra", "lista", "vidas", "eliminado"]);

export const PiezaJuego: React.FC<{ f: number; dur: number; it: Item }> = ({ f, dur, it }) => {
  if (it.t === "destello") return <Destello f={f} dur={dur} it={it} />;
  if (it.t === "marcador") return <Marcador f={f} it={it} />;
  if (it.t === "barra") return <Barra f={f} it={it} />;
  if (it.t === "lista") return <Lista f={f} it={it} />;
  if (it.t === "vidas") return <Vidas f={f} it={it} />;
  if (it.t === "eliminado") return <Eliminado f={f} it={it} />;
  return null;
};
