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
        {/* MrBeast «N PLAYERS LEFT»: la etiqueta DEBAJO de la cifra, ~4 % del alto, en una o dos líneas («|» parte); arriba con etiqueta_pos:"arriba" */}
        {it.etiqueta && it.etiqueta_pos === "arriba" ? <Etiq it={it} fs={fs} /> : null}
        <div style={{ fontFamily: F_ANCHA, fontWeight: 900, fontSize: fs, lineHeight: 1, color: it.color ?? "white" }}>{it.prefijo ?? ""}{num}{it.sufijo ?? ""}</div>
        {it.etiqueta && it.etiqueta_pos !== "arriba" ? <Etiq it={it} fs={fs} /> : null}
      </div>
    </AbsoluteFill>
  );
};

const Etiq: React.FC<{ it: Item; fs: number }> = ({ it, fs }) => (
  <div style={{ fontFamily: F_TXT, fontWeight: 800, fontSize: fs * 0.45, lineHeight: 1.05, color: "white", textTransform: "uppercase", margin: `${fs * 0.08}px 0` }}>
    {String(it.etiqueta).split("|").map((l: string, i: number) => <div key={i}>{l}</div>)}
  </div>
);

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
              display: "flex", alignItems: "center", justifyContent: "center" }}>
              {/* ✓ dibujada (SVG) y centrada en su casilla: el carácter «✓» salía descentrado (revisión del banco) */}
              {hechas.has(i) ? <svg viewBox="0 0 100 100" width={lado * 0.72} height={lado * 0.72}><path d="M16 54 L40 76 L86 24" fill="none" stroke="#000" strokeWidth={16} strokeLinecap="round" strokeLinejoin="round" /></svg> : null}
            </div>
            <div style={{ fontFamily: F_TXT, fontWeight: 600, fontSize: fs, color: "white", textDecoration: hechas.has(i) && it.tachar ? "line-through" : "none", opacity: hechas.has(i) && it.tachar ? 0.7 : 1 }}>{t}</div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// VIDAS (Jesse James West «RULES BROKEN»; Lucas, banco 2026-11-24: «mejor vidas de Minecraft»): corazones de PÍXELES
// dibujados aquí (estilo videojuego, sin imágenes de terceros), con medio corazón. Al perder: el corazón que se va
// parpadea en blanco 3 veces (8 f), la fila tiembla 8 f y queda vacío (contenedor oscuro). Sonido del golpe con "snd".
// `total` (3), `quedan` (antes; admite .5), `pierde` (1 o 0.5), `pierde_en` (fotograma de la pieza). estilo:"emoji" = ❤️.
const CORAZON = [         // 9×9, calcado de la referencia de Lucas (banco 2026-11-24): 0 nada · 1 borde · 2 rojo · 3 brillo · 4 sombra
  "001101100",
  "012212210",
  "123222221",
  "122222221",
  "142222241",
  "014222410",
  "001424100",
  "000141000",
  "000010000"];
// Colores exactos de la referencia (GIF de Minecraft que pasó Lucas): rojo, brillo, sombra; vacío #1F1F1F liso; borde negro.
const COL: Record<string, string> = { "1": "#000000", "2": "#F20000", "3": "#E6BFBF", "4": "#B00303" };
// Todos los corazones en UN svg con celdas de un número PAR de píxeles y origen en píxel par: al bajar de 4K a 1080 cada
// celda queda un bloque limpio (con celdas fraccionarias salían «deformes»: Lucas, banco 2026-11-24).
const Corazones: React.FC<{ px: number; total: number; quedan: number; golpe: number; blanco: boolean }> = ({ px, total, quedan, golpe, blanco }) => {
  const r: React.ReactNode[] = [];
  for (let h = 0; h < total; h++) {
    const lleno = Math.max(0, Math.min(1, quedan - h)), ox = h * 10 * px;      // 9 celdas + 1 de hueco (como la referencia)
    CORAZON.forEach((fila, y) => fila.split("").forEach((c, x) => {
      if (c === "0") return;
      const vivo = c !== "1" && (lleno >= 1 || (lleno >= 0.5 && x <= 4));      // medio corazón: rojo hasta la columna central
      const fill = c === "1" ? (blanco && h === golpe ? "#ffffff" : COL["1"]) : vivo ? COL[c] : "#1F1F1F";
      r.push(<rect key={`${h}-${x}-${y}`} x={ox + x * px} y={y * px} width={px} height={px} fill={fill} />);
    }));
  }
  return <svg width={(total * 10 - 1) * px} height={9 * px} shapeRendering="crispEdges" style={{ display: "block" }}>{r}</svg>;
};
export const Vidas: React.FC<{ f: number; it: Item }> = ({ f, it }) => {
  const { height: H, width: W } = useVideoConfig();
  const total = it.total ?? 3, antes = it.quedan ?? total, pe = it.pierde_en, menos = it.pierde ?? 1;
  const perdida = pe != null && f >= pe + 8, enGolpe = pe != null && f >= pe && f < pe + 8;
  const quedan = perdida ? antes - menos : antes;
  const e = it.esquina ?? "ii";      // JJW Diamond: abajo a la izquierda
  const px = Math.max(2, 2 * Math.round((H * (it.alto ?? 0.085)) / 9 / 2));      // celda: nº par de píxeles
  const ancho = (total * 10 - 1) * px, alto = 9 * px, m = 2 * Math.round((H * MARGEN) / 2), mx = 2 * Math.round((H * MARGEN * 1.3) / 2);
  const x = e[1] === "i" ? mx : W - mx - ancho, y = e[0] === "s" ? m + (it.etiqueta ? Math.round(px * 4.2) : 0) : H - m - alto;
  const tiembla = enGolpe ? ((f - pe) % 2 === 0 ? 1 : -1) * px * 0.5 : 0;
  const parpadea = enGolpe && Math.floor((f - pe) / 1.4) % 2 === 0;
  if (it.estilo === "emoji") {
    return (
      <AbsoluteFill><div style={{ ...esquina(e, W, H), display: "flex", flexDirection: "column", alignItems: "center" }}>
        {it.etiqueta ? <div style={{ fontFamily: F_TXT, fontWeight: 800, fontSize: px * 3.4, color: "white", textShadow: borde(H * 0.003), textTransform: "uppercase" }}>{it.etiqueta}</div> : null}
        <div style={{ display: "flex", gap: px }}>{Array.from({ length: total }, (_, i) => <span key={i} style={{ fontSize: px * 9, lineHeight: 1, filter: i < quedan ? "none" : "grayscale(1) brightness(.45)" }}>❤️</span>)}</div>
      </div></AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill>
      {/* los corazones anclados a la esquina en píxel par; la etiqueta centrada ENCIMA de ellos (no al revés) */}
      <div style={{ position: "absolute", left: x + tiembla, top: y, width: ancho, height: alto, filter: `drop-shadow(0 0 ${px * 0.6}px rgba(0,0,0,.55))` }}>
        {it.etiqueta ? <div style={{ position: "absolute", left: "50%", bottom: alto + px * 1.2, transform: "translateX(-50%)", whiteSpace: "nowrap", fontFamily: F_TXT, fontWeight: 800,
          fontSize: px * 3.4, lineHeight: 1, color: "white", textShadow: borde(H * 0.003), textTransform: "uppercase" }}>{it.etiqueta}</div> : null}
        <Corazones px={px} total={total} quedan={quedan} golpe={Math.ceil(antes) - 1} blanco={parpadea} />
      </div>
    </AbsoluteFill>
  );
};

// X DE ELIMINADO (MrBeast Trap: siempre igual, roja). Aparece en 3 f sobre (x, y) con tamaño `tam` (fracción del alto).
// UNA sola forma (un trazo SVG con las dos diagonales) y UNA sola sombra para todo (Lucas, banco 2026-11-24: con dos barras
// y una sombra cada una «se ve donde se juntan»). Regla para cualquier pieza hecha de partes que se cruzan: sombra al grupo.
export const Eliminado: React.FC<{ f: number; it: Item }> = ({ f, it }) => {
  const { height: H, width: W } = useVideoConfig();
  // MrBeast: entra en blanco, pasa por rosa y se asienta en rojo en ~12 f, con borde negro (medido en el Windows, banco)
  const s = interpolate(f, [0, 3], [1.6, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const k = interpolate(f, [0, 12], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.quad) });
  const rojo = it.color ?? "#E3262B";
  const mezcla = (a: number[], b: number[], u: number) => `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * u)).join(",")})`;
  const hex = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const col = k < 0.5 ? mezcla([255, 255, 255], [255, 150, 170], k * 2) : mezcla([255, 150, 170], hex(rojo), (k - 0.5) * 2);
  const t = H * (it.tam ?? 0.42), g = 13, m = g / 2 + 4;
  const d = `M ${m} ${m} L ${100 - m} ${100 - m} M ${100 - m} ${m} L ${m} ${100 - m}`;
  return (
    <AbsoluteFill>
      <svg viewBox="0 0 100 100" width={t} height={t} style={{ position: "absolute", left: W * (it.x ?? 0.5) - t / 2, top: H * (it.y ?? 0.5) - t / 2, overflow: "visible",
        transform: `scale(${s})`, filter: `drop-shadow(0 0 ${H * 0.008}px rgba(0,0,0,.55))` }}>
        {/* entra de golpe, opaca: con fundido, el primer fotograma era una X gris fantasma (banco 2026-11-24) */}
        {/* UNA forma: el borde negro es el mismo trazo más grueso por debajo; nada se cruza a la vista */}
        <path d={d} stroke="#000" strokeWidth={g + 5} strokeLinecap="round" fill="none" />
        <path d={d} stroke={col} strokeWidth={g} strokeLinecap="round" fill="none" />
      </svg>
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
