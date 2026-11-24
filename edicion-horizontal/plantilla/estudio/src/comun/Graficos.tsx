import React from "react";
import { AbsoluteFill, Easing, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { ACENTO, Marca, usarMarca } from "./marca";
import { F_ANCHA, F_RELLENO, F_TXT, usarFuentes } from "./fuentes";
import { PiezaIntro, TIPOS_INTRO } from "./Intro";
import { PiezaJuego, TIPOS_JUEGO } from "./Juego";

// Capas gráficas del vídeo horizontal: SOLO lo que va encima de la imagen (fondo transparente, salvo el mapa).
// El montaje (cortes, zooms, planos de recurso) lo hace ffmpeg desde los brutos (herramientas/montaje/paso4_render.py);
// Remotion renderiza estas capas en ProRes 4444 con alfa, únicamente en los rangos de frames que llevan gráfico.
// Los items salen de capas.json, que escribe herramientas/montaje/paso3_plan.py. Todas las medidas van en fracción del
// alto (H), así el mismo código vale para 3840x2160, 2560x1440 y 1920x1080.
//
// Estilo (refs/dinamicos/CONTEXTO.md → Textos y títulos): una familia ancha y negra para lo grande, otra limpia para lo
// pequeño. Color por función: acento de marca = dato/énfasis; blanco = información; blanco en minúsculas entre
// asteriscos = comentario del editor. Contorno negro + sombra corta, sin cajas. Entran de golpe (pop) y salen por corte.
export type Item = Record<string, any>;

export const entra = (f: number, d = 7) => interpolate(f, [0, d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
export const sale = (f: number, dur: number, d = 7) => interpolate(f, [dur - d, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
// Entrada de un texto: de x0,86 a x1 en 5 fotogramas, frenando, SIN PASARSE (Lucas, 2026-11-14: «aparecen, se encogen un
// poco y luego se zoomean»: el antiguo 0,8 -> 1,06 -> 1 multiplicado por el crecimiento continuo encogía el texto un 5 %
// entre los fotogramas 3 y 6). Como nunca baja, pop(f) * crecimiento solo crece: entra rápido y sigue creciendo despacio.
export const pop = (f: number) => interpolate(f, [0, 5], [0.86, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
// contorno negro hecho con sombras (doce direcciones) + sombra corta
export const borde = (r: number) => {
  const s: string[] = [];
  for (let i = 0; i < 12; i++) s.push((Math.cos((i * Math.PI) / 6) * r).toFixed(1) + "px " + (Math.sin((i * Math.PI) / 6) * r).toFixed(1) + "px 0 #000");
  s.push("0 " + (r * 1.6).toFixed(1) + "px " + (r * 2.5).toFixed(1) + "px rgba(0,0,0,.6)");
  return s.join(", ");
};
// tamaño de letra para que un texto de una línea quepa en `max` px (la familia ancha ocupa ~0,82 de su cuerpo por letra)
export const ajusta = (txt: string, max: number, tope: number, ancho = 0.82) => Math.min(tope, max / (Math.max(txt.length, 2) * ancho));
// NINGÚN texto se sale del cuadro (Lucas, 2026-11-17: «los textos no se pueden salir de pantalla nunca, es un error muy
// grande»): margen al borde y centro que se encoge para que la caja entera quepa. Mismo cálculo en comun.caja_texto.
export const MARGEN = 0.04;          // del ancho
export const dentro = (centro: number, mitad: number, W: number) => Math.min(Math.max(centro, W * MARGEN + mitad), W * (1 - MARGEN) - mitad);

// Título del vídeo: línea pequeña, palabra enorme en acento, línea pequeña. Sobre el plano de fondo oscurecido.
export const Titulo: React.FC<{ f: number; dur: number; it: Item }> = ({ f, dur, it }) => {
  const { height: H, width: W } = useVideoConfig();
  const fuera = f >= dur - 2 ? 0 : 1;
  const fs = ajusta(String(it.grande ?? ""), W * 0.9, H * 0.2);
  return (
    <AbsoluteFill style={{ backgroundColor: "rgba(0,0,0,.45)", justifyContent: "center", alignItems: "center", opacity: fuera }}>
      {it.arriba ? <div style={{ fontFamily: F_TXT, fontSize: H * 0.036, letterSpacing: H * 0.006, color: "white", fontWeight: 800, textShadow: borde(H * 0.003), opacity: f >= 8 ? 1 : 0 }}>{it.arriba}</div> : null}
      <div style={{ fontFamily: F_ANCHA, fontSize: fs, lineHeight: 1.05, fontWeight: 900, color: ACENTO, textShadow: borde(H * 0.006), transform: "scale(" + pop(f) + ")", whiteSpace: "nowrap" }}>{it.grande}</div>
      {it.abajo ? <div style={{ fontFamily: F_TXT, fontSize: H * 0.036, color: "white", fontWeight: 600, textShadow: borde(H * 0.003), marginTop: H * 0.012, opacity: f >= 16 ? 1 : 0 }}>{it.abajo}</div> : null}
    </AbsoluteFill>
  );
};

// Capítulo: número enorme en acento + título blanco, de golpe; debajo, las casillas del contador (marcador de progreso).
// De serie SIN contador (Lucas, 2026-11-24: fuera el «1/7» y las casillas): solo título y subtítulo. CONTADOR_CAPITULOS = True en ajustes.py lo vuelve a poner.
export const Seccion: React.FC<{ f: number; dur: number; it: Item }> = ({ f, it }) => {
  const { height: H, width: W } = useVideoConfig();
  // it.contador === false: sin número «n/total» ni casillas, solo título y subtítulo (Reino Selva, 2026-11-19: «saca el contador»)
  const sinContador = it.contador === false;
  const de = sinContador ? 0 : Number(it.de ?? 0);
  const fs = ajusta(String(it.titulo ?? ""), W * 0.62, H * 0.075);
  return (
    <AbsoluteFill style={{ background: "linear-gradient(15deg, rgba(0,0,0,.7) 0%, rgba(0,0,0,0) 50%)" }}>
      <div style={{ position: "absolute", left: H * 0.07, bottom: H * 0.07, display: "flex", alignItems: "flex-end", gap: H * 0.03, transform: "scale(" + pop(f) + ")", transformOrigin: "0 100%" }}>
        {sinContador ? null : (
          <div style={{ fontFamily: F_ANCHA, fontWeight: 900, fontSize: H * 0.23, lineHeight: 0.86, color: ACENTO, textShadow: borde(H * 0.006) }}>
            {it.n}
            {de ? <span style={{ fontSize: H * 0.085, color: "white" }}>/{de}</span> : null}
          </div>
        )}
        <div style={{ paddingBottom: H * 0.004 }}>
          <div style={{ fontFamily: F_ANCHA, fontWeight: 900, fontSize: fs, color: "white", textShadow: borde(H * 0.004), lineHeight: 1.1, whiteSpace: "nowrap", opacity: f >= 4 ? 1 : 0 }}>{it.titulo}</div>
          <div style={{ fontFamily: F_TXT, fontSize: H * 0.034, fontWeight: 600, color: "white", textShadow: borde(H * 0.0025), marginTop: H * 0.006, opacity: f >= 10 ? 1 : 0 }}>{it.sub}</div>
          <div style={{ display: "flex", gap: H * 0.006, marginTop: H * 0.018 }}>
            {Array.from({ length: de }, (_, i) => (
              <div key={i} style={{ width: H * 0.05, height: H * 0.009, background: i < it.n ? ACENTO : "rgba(255,255,255,.4)", opacity: f >= 10 + i ? 1 : 0 }} />
            ))}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Cifra junto a la cara: el plano ya viene reencuadrado con la cara a un tercio (paso3_plan.py) y la cifra va al otro lado.
export const Dato: React.FC<{ f: number; it: Item }> = ({ f, it }) => {
  const { height: H, width: W } = useVideoConfig();
  const fs = ajusta(String(it.grande), W * it.mw, H * 0.22);
  const mitad = (Math.max(String(it.grande).length * fs * 0.9, String(it.peq ?? "").length * H * 0.04 * 0.6) * 1.15) / 2;
  return (
    <div style={{ position: "absolute", left: dentro(W * it.x, mitad, W), top: H * it.y, transform: "translate(-50%, -50%) scale(" + pop(f) + ") rotate(-3deg)", textAlign: "center", whiteSpace: "nowrap" }}>
      <div style={{ fontFamily: F_ANCHA, fontWeight: 900, fontSize: fs, lineHeight: 1, color: ACENTO, textShadow: borde(H * 0.007) }}>{it.grande}</div>
      <div style={{ fontFamily: F_TXT, fontWeight: 800, fontSize: H * 0.04, color: "white", textShadow: borde(H * 0.003), marginTop: H * 0.012, opacity: f >= 7 ? 1 : 0 }}>{it.peq}</div>
    </div>
  );
};

// Palabra-golpe: entra con pop y sigue creciendo de forma CONTINUA y suave (x1 -> x1,22, con frenada); la escala nunca baja.
// Regla (2026-11-11): nunca a escalones («se zumea a trozos, no es suave»). «|» parte el texto en líneas.
// it.y: altura de la base (0,1 = abajo, de serie); más arriba cuando abajo está lo que se enseña (la rosa, los platos).
export const Golpe: React.FC<{ f: number; dur: number; it: Item }> = ({ f, dur, it }) => {
  const { height: H, width: W } = useVideoConfig();
  const lineas = String(it.txt).split("|");
  const largo = Math.max(...lineas.map((l) => l.length));
  const fs = Math.min(H * 0.105, (W * 0.66) / (largo * 0.82));
  const esc = pop(f) * interpolate(f, [0, dur], [1, 1.22], { extrapolateRight: "clamp", easing: Easing.out(Easing.quad) });
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: H * (it.y ?? 0.1) }}>
      <div style={{ fontFamily: F_ANCHA, fontWeight: 900, fontSize: fs, lineHeight: 1.12, color: ACENTO, textShadow: borde(H * 0.006), textAlign: "center", whiteSpace: "nowrap", transform: "scale(" + esc + ")", transformOrigin: "50% 100%" }}>
        {lineas.map((l, i) => (
          <div key={i}>{l}</div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// Comentario del editor: minúsculas, blanco, entre asteriscos, de golpe.
export const Nota: React.FC<{ it: Item }> = ({ it }) => {
  const { height: H } = useVideoConfig();
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: H * 0.075 }}>
      <div style={{ fontFamily: F_TXT, fontWeight: 600, fontSize: H * 0.046, color: "white", textShadow: borde(H * 0.003) }}>{it.txt}</div>
    </AbsoluteFill>
  );
};

// Subtítulo: SOLO donde no se entiende (ruido, voz lejana, otro idioma). Una línea, abajo, de golpe.
export const Sub: React.FC<{ it: Item }> = ({ it }) => {
  const { height: H } = useVideoConfig();
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: H * 0.1 }}>
      <div style={{ fontFamily: F_TXT, fontSize: H * 0.05, fontWeight: 800, color: it.color ?? "white", textShadow: borde(H * 0.0035) }}>{it.txt}</div>
    </AbsoluteFill>
  );
};

// Botón de suscripción: aparece cuando se dice. El texto va en el idioma del vídeo (it.txt).
export const Suscribe: React.FC<{ f: number; it: Item }> = ({ f, it }) => {
  const { height: H } = useVideoConfig();
  return (
    <div style={{ position: "absolute", left: H * 0.07, bottom: H * 0.08, transform: "scale(" + pop(f) + ")", transformOrigin: "0 100%", background: ACENTO, color: "#14160a", fontFamily: F_ANCHA, fontWeight: 900, fontSize: H * 0.046, padding: H * 0.014 + "px " + H * 0.03 + "px", borderRadius: H * 0.012, boxShadow: "0 0.4vh 2vh rgba(0,0,0,.5)" }}>{it.txt ?? "SUSCRÍBETE"}</div>
  );
};

// Clip con transparencia (un .webm hecho con herramientas/quitar_fondo.py) colocado en el cuadro. Empieza con el item.
// x, y, w en píxeles del lienzo (esquina superior izquierda y ancho); desde = segundo del clip en que empieza.
export const Clip: React.FC<{ it: Item; src: string; caja: { w: number; h: number }; x: number; y: number; w: number; desde?: number; vel?: number; espejo?: boolean; estilo?: React.CSSProperties }> = ({ it, src, caja, x, y, w, desde = 0, vel = 1, espejo, estilo }) => {
  const { fps } = useVideoConfig();
  return (
    <Sequence from={it.f0} durationInFrames={it.f1 - it.f0} layout="none">
      <OffthreadVideo transparent muted src={staticFile(src)} startFrom={Math.round(desde * fps)} playbackRate={vel}
        style={{ position: "absolute", left: x, top: y, width: w, height: (w * caja.h) / caja.w, transform: espejo ? "scaleX(-1)" : undefined, ...estilo }} />
    </Sequence>
  );
};

// Botón animado de YouTube (suscríbete, me gusta, campana): recurso de la skill, estudio/public/botones/bNN.webm.
// Cuál usar y cuándo: base/recursos.md → «Botones de YouTube». El clip conserva su sitio dentro del original de
// 1920x1080: ese lienzo se pinta a `esc` del ancho (0,5 = la mitad) con su centro en (x, y); de serie, abajo al centro,
// que es donde va SIEMPRE una petición de suscripción. `arch` = el archivo (bNN o su versión en otro idioma); `vel` = velocidad.
export const Boton: React.FC<{ it: Item }> = ({ it }) => {
  const { height: H, width: W } = useVideoConfig();
  const k = (W * (it.esc ?? 0.34)) / it.caja.ancho_original;      // 0,34 de serie (un tercio del ancho); era 0,5 y quedaba enorme (Lucas, 2026-11-17: «la animación de suscribirse es muy grande, hazla algo más pequeña»)
  return <Clip it={it} src={"botones/" + (it.arch ?? "b" + String(it.n).padStart(2, "0")) + ".webm"} caja={it.caja} w={it.caja.w * k} vel={it.vel ?? 1}
    x={W * (it.x ?? 0.5) + (it.caja.x - it.caja.ancho_original / 2) * k} y={H * (it.y ?? 0.8) + (it.caja.y - it.caja.alto_original / 2) * k} />;
};

// Rótulo anclado al sujeto (animal, persona, objeto): la posición viene del seguimiento de puntos de paso3_plan.py,
// una por frame, en píxeles del lienzo. Flecha en acento hacia el sujeto y nombre al lado contrario.
export const Seguido: React.FC<{ f: number; dur: number; it: Item }> = ({ f, dur, it }) => {
  const { height: H, width: Wd } = useVideoConfig();
  const [x, y] = it.pos[Math.min(f, it.pos.length - 1)];
  const o = entra(f, 4) * sale(f, dur, 5);
  const s = pop(f);
  // el nombre va al lado pedido; si por ese lado no cabe entero, al otro (ningún texto se sale del cuadro)
  const ancho = Math.max(String(it.grande).length * H * 0.06 * 0.9, String(it.peq ?? "").length * H * 0.034 * 0.6) * 1.12;
  let izq = it.lado === "izq";
  const sitio = (iz: boolean) => { const t = Math.min(Math.max(x + (iz ? -1 : 1) * H * 0.13, H * 0.3), Wd - H * 0.3); return iz ? t - ancho >= Wd * 0.02 : t + ancho <= Wd * 0.98; };
  if (!sitio(izq) && sitio(!izq)) izq = !izq;
  const dx = (izq ? -1 : 1) * H * 0.13, dy = -H * 0.13;
  const tx0 = Math.min(Math.max(x + dx, H * 0.3), Wd - H * 0.3);
  const tx = izq ? Math.max(tx0, Wd * 0.02 + ancho) : Math.min(tx0, Wd * 0.98 - ancho), ty = Math.max(y + dy, H * 0.12);
  const ang = (Math.atan2(y - ty, x - tx) * 180) / Math.PI;
  const largo = Math.hypot(x - tx, y - ty) - H * 0.075;
  return (
    <AbsoluteFill style={{ opacity: o }}>
      <div style={{ position: "absolute", left: tx, top: ty, width: Math.max(largo, 0), height: H * 0.008, background: ACENTO, transformOrigin: "0 50%", transform: `rotate(${ang}deg) translateX(${H * 0.02}px)`, borderRadius: H * 0.004, boxShadow: "0 0 1vh rgba(0,0,0,.6)" }}>
        <div style={{ position: "absolute", right: -H * 0.012, top: -H * 0.011, width: 0, height: 0, borderTop: `${H * 0.015}px solid transparent`, borderBottom: `${H * 0.015}px solid transparent`, borderLeft: `${H * 0.026}px solid ${ACENTO}` }} />
      </div>
      <div style={{ position: "absolute", left: tx, top: ty, transform: `translate(${izq ? "-100%" : "0"}, -100%) scale(${s})`, transformOrigin: izq ? "100% 100%" : "0 100%", textAlign: izq ? "right" : "left", whiteSpace: "nowrap" }}>
        <div style={{ fontFamily: F_ANCHA, fontSize: H * 0.06, fontWeight: 900, color: ACENTO, textShadow: borde(H * 0.004), lineHeight: 1.1 }}>{it.grande}</div>
        <div style={{ fontFamily: F_TXT, fontSize: H * 0.034, fontWeight: 800, color: "white", textShadow: borde(H * 0.0025) }}>{it.peq}</div>
      </div>
    </AbsoluteFill>
  );
};

// Composición de capas: pinta los items vivos en cada frame. `extra` pinta los tipos propios del vídeo (p. ej. "mapa").
export const CapasBase: React.FC<{ datos: { items: Item[]; marca?: Marca }; extra?: (it: Item, f: number, dur: number, k: string) => React.ReactNode }> = ({ datos, extra }) => {
  const frame = useCurrentFrame();
  usarMarca(datos.marca);      // color y cuentas del creador de ESTE vídeo (personal/<creador>/marca.json)
  usarFuentes(datos.marca);    // sus fuentes, si marca.json o MARCA de proyecto.py traen "fuentes" (si no, las de marca.ts)
  const vivos = datos.items.filter((it) => frame >= it.f0 && frame < it.f1);
  return (
    <AbsoluteFill style={{ fontFamily: F_RELLENO }}>
      {vivos.map((it) => {
        const f = frame - it.f0, dur = it.f1 - it.f0, k = `${it.t}${it.f0}`;
        if (it.t === "titulo") return <Titulo key={k} f={f} dur={dur} it={it} />;
        if (it.t === "seccion") return <Seccion key={k} f={f} dur={dur} it={it} />;
        if (it.t === "trk") return <Seguido key={k} f={f} dur={dur} it={it} />;
        if (it.t === "sub") return <Sub key={k} it={it} />;
        if (it.t === "dato") return <Dato key={k} f={f} it={it} />;
        if (it.t === "golpe") return <Golpe key={k} f={f} dur={dur} it={it} />;
        if (it.t === "nota") return <Nota key={k} it={it} />;
        if (it.t === "suscribe") return <Suscribe key={k} f={f} it={it} />;
        if (it.t === "boton") return <Boton key={k} it={it} />;
        if (TIPOS_INTRO.has(it.t)) return <PiezaIntro key={k} f={f} dur={dur} it={it} />;
        if (TIPOS_JUEGO.has(it.t)) return <PiezaJuego key={k} f={f} dur={dur} it={it} />;   // juego y destello (Juego.tsx)   // kit de intros (Intro.tsx)
        return extra ? <React.Fragment key={k}>{extra(it, f, dur, k)}</React.Fragment> : null;
      })}
    </AbsoluteFill>
  );
};
