#!/usr/bin/env python3
"""¿Qué fuente lleva este rótulo? Compara un recorte con fuentes de Google Fonts y da las 3 más parecidas.

Uso (desde la raíz de la carpeta de edición):
  PY herramientas/fuente_rotulo.py RECORTE.png [--texto "LAS PLANTAS"] [--mayus] [--json salida.json]
  PY herramientas/fuente_rotulo.py VIDEO.mp4 --t 72.6 --caja x,y,ancho,alto [--texto ...]   (saca el fotograma él)

- El recorte: SOLO el texto (una línea o un bloque), lo más ajustado posible, a resolución completa (1080p).
- Texto: lo lee con tesseract si está instalado (brew install tesseract / winget install UB-Mannheim.TesseractOCR);
  si no, o si lo lee mal, pásalo con --texto (exacto, con sus mayúsculas).
- Método: separa las letras del fondo, escribe el mismo texto con cada candidata (pesos 400–900), lo encaja en la
  misma caja y compara las formas (solapamiento de máscaras y de contornos). Aproximado: distingue familias (condensada
  vs ancha, redonda vs geométrica, con o sin remate), no siempre el peso exacto. Es una pista para la ficha, no prueba.
- Las fuentes se bajan una vez de github.com/google/fonts a herramientas/modelos/fuentes/ (OFL, libres)."""
import argparse, json, os, re, shutil, subprocess, sys, tempfile, urllib.request
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(AQUI, "modelos", "fuentes")
G = "https://raw.githubusercontent.com/google/fonts/main/"
# nombre -> (ruta en google/fonts, pesos a probar; None = fuente estática de un peso)
CANDIDATAS = {
    "Anton": ("ofl/anton/Anton-Regular.ttf", None),
    "Bebas Neue": ("ofl/bebasneue/BebasNeue-Regular.ttf", None),
    "League Gothic": ("ofl/leaguegothic/LeagueGothic%5Bwdth%5D.ttf", None),
    "Oswald": ("ofl/oswald/Oswald%5Bwght%5D.ttf", [500, 700]),
    "Barlow Condensed": ("ofl/barlowcondensed/BarlowCondensed-Black.ttf", None),
    "Roboto Condensed": ("ofl/robotocondensed/RobotoCondensed%5Bwght%5D.ttf", [700, 900]),
    "Montserrat": ("ofl/montserrat/Montserrat%5Bwght%5D.ttf", [600, 800, 900]),
    "Poppins": ("ofl/poppins/Poppins-ExtraBold.ttf", None),
    "Poppins Black": ("ofl/poppins/Poppins-Black.ttf", None),
    "Inter": ("ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf", [600, 800, 900]),
    "DM Sans": ("ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf", [700, 900]),
    "Space Grotesk": ("ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf", [700]),
    "Archivo Black": ("ofl/archivoblack/ArchivoBlack-Regular.ttf", None),
    "Unbounded": ("ofl/unbounded/Unbounded%5Bwght%5D.ttf", [700, 900]),
    "Lexend": ("ofl/lexend/Lexend%5Bwght%5D.ttf", [600, 800]),
    "Rubik": ("ofl/rubik/Rubik%5Bwght%5D.ttf", [700, 900]),
    "Kanit": ("ofl/kanit/Kanit-Black.ttf", None),
    "Outfit": ("ofl/outfit/Outfit%5Bwght%5D.ttf", [700, 900]),
    "Bricolage Grotesque": ("ofl/bricolagegrotesque/BricolageGrotesque%5Bopsz%2Cwdth%2Cwght%5D.ttf", [700, 800]),
    "Luckiest Guy": ("ofl/luckiestguy/LuckiestGuy-Regular.ttf", None),
    "Bangers": ("ofl/bangers/Bangers-Regular.ttf", None),
    "Titan One": ("ofl/titanone/TitanOne-Regular.ttf", None),
    "Lilita One": ("ofl/lilitaone/LilitaOne-Regular.ttf", None),
    "Permanent Marker": ("apache/permanentmarker/PermanentMarker-Regular.ttf", None),
    "Playfair Display": ("ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf", [700, 900]),
    "DM Serif Display": ("ofl/dmserifdisplay/DMSerifDisplay-Regular.ttf", None),
}

ap = argparse.ArgumentParser()
ap.add_argument("entrada"); ap.add_argument("--t", type=float); ap.add_argument("--caja")
ap.add_argument("--texto"); ap.add_argument("--mayus", action="store_true"); ap.add_argument("--json")
a = ap.parse_args()


def bajar(ruta):
    os.makedirs(CACHE, exist_ok=True)
    loc = os.path.join(CACHE, re.sub(r"%[0-9A-F]{2}", "_", os.path.basename(ruta)))
    if not os.path.exists(loc):
        try: urllib.request.urlretrieve(G + ruta, loc)
        except Exception as e: print(f"  (no he podido bajar {ruta}: {e})"); return None
    return loc


# ---------- recorte ----------
if a.t is not None:
    if not a.caja: raise SystemExit("Con --t hace falta --caja x,y,ancho,alto (en píxeles del vídeo)")
    with tempfile.TemporaryDirectory() as tmp:
        f = os.path.join(tmp, "f.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a.t), "-i", a.entrada, "-frames:v", "1", f], check=True)
        img = cv2.imread(f)
    x, y, w, h = map(int, a.caja.split(",")); img = img[y:y + h, x:x + w]
else:
    img = cv2.imread(a.entrada)
if img is None or img.size == 0: raise SystemExit("No he podido leer el recorte")

# máscara de las letras: el color de las letras es el más saturado o más claro/oscuro respecto al borde del recorte
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
borde = np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]); fondo = np.median(borde, axis=0)
dist = np.linalg.norm(lab - fondo, axis=2)
_, m = cv2.threshold(cv2.normalize(dist, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
ys, xs = np.where(m > 0)
if len(xs) < 30: raise SystemExit("No distingo letras en el recorte (¿muy pequeño o sin contraste?)")
m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
H0, W0 = m.shape

# ---------- texto ----------
texto = a.texto
if not texto:
    tes = shutil.which("tesseract") or (r"C:\Program Files\Tesseract-OCR\tesseract.exe" if os.path.exists(r"C:\Program Files\Tesseract-OCR\tesseract.exe") else None)
    if not tes: raise SystemExit("No hay tesseract: pasa el texto con --texto \"...\"")
    with tempfile.TemporaryDirectory() as tmp:
        f = os.path.join(tmp, "m.png"); cv2.imwrite(f, cv2.copyMakeBorder(255 - m, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255))
        texto = subprocess.run([tes, f, "-", "--psm", "6", "-l", "spa+eng"], capture_output=True, text=True).stdout.strip()
        if not texto:
            texto = subprocess.run([tes, f, "-", "--psm", "6"], capture_output=True, text=True).stdout.strip()
    if not texto: raise SystemExit("tesseract no ha leído nada: pasa el texto con --texto")
if a.mayus: texto = texto.upper()
lineas = [l for l in texto.splitlines() if l.strip()] or [texto]


def render(ruta, peso):
    tam = 160
    try:
        fnt = ImageFont.truetype(ruta, tam)
        if peso:
            try: fnt.set_variation_by_axes([peso] if len(fnt.get_variation_axes()) == 1 else
                                           [peso if ax.get("name", b"") in (b"Weight", "Weight") else ax["default"] for ax in fnt.get_variation_axes()])
            except Exception:
                try: fnt.set_variation_by_name({600: "SemiBold", 700: "Bold", 800: "ExtraBold", 900: "Black"}.get(peso, "Bold"))
                except Exception: pass
    except Exception: return None
    W = int(tam * 0.9 * max(len(l) for l in lineas)) + 200; Hh = int(tam * 1.4 * len(lineas)) + 100
    im = Image.new("L", (W, Hh), 0); d = ImageDraw.Draw(im)
    d.multiline_text((50, 30), "\n".join(lineas), font=fnt, fill=255, spacing=int(tam * 0.15))
    r = np.array(im); ys, xs = np.where(r > 127)
    if len(xs) == 0: return None
    return r[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def parecido(r):
    # proporción ancho/alto: una condensada y una ancha se separan sobre todo por aquí
    asp = abs(np.log((r.shape[1] / r.shape[0]) / (W0 / H0)))
    rr = cv2.resize(r, (W0, H0), interpolation=cv2.INTER_AREA) > 127; mm = m > 127
    iou = (rr & mm).sum() / max(1, (rr | mm).sum())
    tinta = abs(rr.mean() - mm.mean()) / max(1e-3, mm.mean())                  # grosor del trazo
    er = cv2.Canny(rr.astype(np.uint8) * 255, 50, 150) > 0; em = cv2.Canny(mm.astype(np.uint8) * 255, 50, 150) > 0
    dt = cv2.distanceTransform((~em).astype(np.uint8), cv2.DIST_L2, 3); chamfer = float(dt[er].mean()) if er.any() else 99
    return iou - 0.6 * asp - 0.35 * tinta - 0.02 * chamfer, {"iou": round(float(iou), 3), "proporcion": round(float(asp), 3),
                                                            "grosor": round(float(tinta), 3), "contorno_px": round(chamfer, 2)}


res = []
for nombre, (ruta, pesos) in CANDIDATAS.items():
    loc = bajar(ruta)
    if not loc: continue
    for p in (pesos or [None]):
        r = render(loc, p)
        if r is None: continue
        s, det = parecido(r)
        res.append({"fuente": nombre, "peso": p, "puntuacion": round(float(s), 3), **det})
res.sort(key=lambda x: -x["puntuacion"])
mejores = []
for x in res:                                         # una entrada por familia en el top
    if x["fuente"] not in [y["fuente"] for y in mejores]: mejores.append(x)
    if len(mejores) == 3: break
print(f"Texto: {' / '.join(lineas)}   (recorte {W0}x{H0} px de letras)")
for k, x in enumerate(mejores, 1):
    print(f"  {k}. {x['fuente']}{' ' + str(x['peso']) if x['peso'] else ''}  ({x['puntuacion']:+.3f}; solape {x['iou']}, proporción {x['proporcion']}, grosor {x['grosor']})")
if a.json:
    json.dump({"texto": lineas, "top3": mejores, "todas": res[:15]}, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
