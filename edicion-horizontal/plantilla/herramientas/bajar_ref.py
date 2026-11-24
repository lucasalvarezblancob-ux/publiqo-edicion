#!/usr/bin/env python3
"""Baja UN vídeo de referencia de YouTube para analizar su EDICIÓN.

Uso (desde la raíz de la carpeta de edición):
  PY herramientas/bajar_ref.py URL --estilo vlog [--creador alessio-pierucci] [--tipo dinamicos] [--calidad 1080]
                                   [--simular] [--min-libre-gb 15]

- 1080p (o la calidad pedida, la más cercana por debajo) con audio, en mp4 → refs/<tipo>/<creador>/AAAA-MM-DD_<slug>.mp4
  (fecha de PUBLICACIÓN; slug del título). El creador sale del canal si no se da.
- Añade o actualiza su fila en refs/<tipo>/VIDEOS.tsv: archivo, creador, url, titulo, duracion, publicado, estilo.
- No baja si queda menos de --min-libre-gb en el disco (el vídeo se borra al terminar su ficha: cola_refs.py).
- --simular: solo metadatos y formato elegido, no baja nada.
Imprime al final una línea JSON con {"archivo", "creador", "estilo", "duracion_s", "url"} para quien lo llame.
Necesita yt-dlp (winget install yt-dlp, brew install yt-dlp o pip install yt-dlp en la .venv) y ffmpeg."""
import argparse, csv, json, os, re, shutil, subprocess, sys, unicodedata

ap = argparse.ArgumentParser()
ap.add_argument("url"); ap.add_argument("--estilo", default="")
ap.add_argument("--creador", default=""); ap.add_argument("--tipo", default="dinamicos")
ap.add_argument("--calidad", type=int, default=1080); ap.add_argument("--simular", action="store_true")
ap.add_argument("--min-libre-gb", type=float, default=15.0)
a = ap.parse_args()


def slug(s, n=60):
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:n].rstrip("-") or "video"


url = a.url if a.url.startswith("http") else "https://" + a.url
m = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})", url)
if not m: raise SystemExit(f"No reconozco el id del vídeo en {a.url}")
VID = m.group(1); url = f"https://www.youtube.com/watch?v={VID}"            # sin &t=, &pp=… (no cambian el vídeo)
YTDLP = [shutil.which("yt-dlp")] if shutil.which("yt-dlp") else [sys.executable, "-m", "yt_dlp"]
FMT = (f"bv*[height<={a.calidad}][ext=mp4]+ba[ext=m4a]/bv*[height<={a.calidad}]+ba/b[height<={a.calidad}]/b")

r = subprocess.run([*YTDLP, "-J", "--no-warnings", "--no-playlist", "-f", FMT, url], capture_output=True, text=True,
                   encoding="utf-8", errors="replace")
if r.returncode != 0 or not r.stdout.strip():
    raise SystemExit(f"yt-dlp no ha podido leer {url} (¿privado, borrado, región?):\n{(r.stderr or '')[-600:]}")
info = json.loads(r.stdout)
pub = info.get("upload_date") or "00000000"; pub = f"{pub[:4]}-{pub[4:6]}-{pub[6:]}"
creador = a.creador or slug(info.get("channel") or info.get("uploader") or "creador", 40)
nombre = f"{pub}_{slug(info.get('title', VID), 50)}"
CARP = f"refs/{a.tipo}/{creador}"; MP4 = f"{CARP}/{nombre}.mp4"
dur = float(info.get("duration") or 0)
alto = info.get("height") or max((f.get("height") or 0) for f in info.get("requested_formats", [info]))
resumen = {"archivo": MP4, "creador": creador, "canal": info.get("channel"), "titulo": info.get("title"), "estilo": a.estilo,
           "duracion_s": round(dur, 1), "publicado": pub, "url": url, "alto": alto, "id": VID}

if a.simular:
    print(f"(simulación) {info.get('channel')} · «{info.get('title')}» · {pub} · {dur / 60:.1f} min · {alto}p → {MP4}")
    print(json.dumps(resumen, ensure_ascii=False)); sys.exit(0)

os.makedirs(CARP, exist_ok=True)
libre = shutil.disk_usage(CARP).free / 1e9
if libre < a.min_libre_gb:
    raise SystemExit(f"Solo quedan {libre:.1f} GB libres (mínimo {a.min_libre_gb}): borra vídeos ya analizados antes de bajar más.")
if not os.path.exists(MP4):
    print(f"Bajando {info.get('channel')} · «{info.get('title')}» ({dur / 60:.1f} min, {alto}p)…", flush=True)
    r = subprocess.run([*YTDLP, "--no-warnings", "--no-playlist", "-f", FMT, "--merge-output-format", "mp4",
                        "--retries", "10", "--fragment-retries", "10", "--continue", "-o", MP4, url])
    if r.returncode != 0 or not os.path.exists(MP4): raise SystemExit(f"Falló la descarga de {url}")

# VIDEOS.tsv (una fila por archivo; si ya está, se actualiza)
TSV = f"refs/{a.tipo}/VIDEOS.tsv"; CAMPOS = ["archivo", "creador", "url", "titulo", "duracion", "publicado", "estilo"]
filas = []
if os.path.exists(TSV):
    with open(TSV, encoding="utf-8", newline="") as f: filas = list(csv.DictReader(f, delimiter="\t"))
rel = f"{creador}/{nombre}.mp4"
filas = [x for x in filas if x.get("archivo") != rel and x.get("url") != url]
filas.append({"archivo": rel, "creador": info.get("channel") or creador, "url": url, "titulo": info.get("title", ""),
              "duracion": f"{int(dur // 60)}:{int(dur % 60):02d}", "publicado": pub, "estilo": a.estilo})
with open(TSV, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, CAMPOS, delimiter="\t", extrasaction="ignore", lineterminator="\n"); w.writeheader(); w.writerows(filas)
print(f"✓ {MP4} ({os.path.getsize(MP4) / 1e6:.0f} MB)")
print(json.dumps(resumen, ensure_ascii=False))
