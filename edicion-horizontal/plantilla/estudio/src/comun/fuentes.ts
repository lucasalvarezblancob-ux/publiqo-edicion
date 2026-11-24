// FUENTES DEL CREADOR (o de un vídeo): cambian F_ANCHA / F_TXT si capas.json["marca"] trae "fuentes".
// paso3_plan.py copia ahí personal/<creador>/marca.json, con MARCA de proyecto.py encima (comun.marca()):
//   "fuentes": {"titulos": "Anton", "textos": "Montserrat"}   (nombre exacto de la familia en Google Fonts)
//   o con pesos: {"titulos": {"familia": "Anton", "pesos": ["400"]}}
// Sin "fuentes", o con una familia que no existe en Google Fonts: las de marca.ts (LOCAL), exactamente como antes.
// Los gráficos de serie importan F_ANCHA, F_TXT y F_RELLENO de aquí; los propios de un creador, si quieren seguirlas,
// también ("../../comun/fuentes"). Lo pide la ventana de arranque (Cambiar estilo → color y fuente). Lucas, 2026-11-24.
import { continueRender, delayRender } from "remotion";
import { getAvailableFonts } from "@remotion/google-fonts";
import * as M from "./marca";

type Fuente = string | { familia: string; pesos?: string[] };
export type Fuentes = { titulos?: Fuente; textos?: Fuente };

export let F_ANCHA: string = M.F_ANCHA;
export let F_TXT: string = M.F_TXT;
export let F_RELLENO: string = M.F_RELLENO;

const PESOS = ["400", "500", "600", "700", "800", "900"];
const cargadas: Record<string, string> = {};   // familia pedida -> fontFamily para CSS ("" mientras carga o si no existe)

const cargar = (f?: Fuente): string | null => {
  if (!f) return null;
  const familia = typeof f === "string" ? f : f.familia;
  if (!familia) return null;
  if (familia in cargadas) return cargadas[familia] || null;
  const info = getAvailableFonts().find((x) => x.fontFamily.toLowerCase() === familia.toLowerCase());
  if (!info) { cargadas[familia] = ""; console.warn(`fuentes.ts: «${familia}» no está en Google Fonts; se usa la de marca.ts`); return null; }
  cargadas[familia] = info.fontFamily;
  const h = delayRender(`fuente ${info.fontFamily}`);
  info.load().then((mod) => {
    const fi = mod.getInfo();
    const hay = Object.keys(fi.fonts.normal || {});
    const pide = typeof f === "string" || !f.pesos ? PESOS : f.pesos;
    const pesos = pide.filter((p) => hay.includes(p));
    const subs = ["latin", "latin-ext"].filter((s) => fi.subsets.includes(s));
    const r = mod.loadFont("normal", { weights: (pesos.length ? pesos : hay) as never, subsets: (subs.length ? subs : fi.subsets) as never });
    return r.waitUntilDone();
  }).then(() => continueRender(h), (e) => { console.warn("fuentes.ts:", e); cargadas[familia] = ""; continueRender(h); });
  return info.fontFamily;
};

// Se llama al pintar, junto a usarMarca(): con la marca de ESTE vídeo.
export const usarFuentes = (m?: object) => {
  const fz: Fuentes = (m && (m as { fuentes?: Fuentes }).fuentes) || {};
  F_ANCHA = cargar(fz.titulos) || M.F_ANCHA;
  const txt = cargar(fz.textos);
  F_TXT = txt || M.F_TXT;
  F_RELLENO = txt || M.F_RELLENO;
};
