"""prueba_clip.py: render CORTO y LIGERO de un trozo del montaje, para el banco de pruebas (Lucas, 2026-11-24: «clips de
menos de 15 segundos o lo que tarde el recurso … en 1080 y un formato que pese poco»). Desde out/<slug>/, con el plan ya
hecho (paso3_plan.py) y, si quieres sonido, el audio (paso5_audio.py y paso6_musica.py).
  prueba_clip.py DESDE HASTA SALIDA.mp4        segundos del montaje (p. ej. 20.5 32 ~/Desktop/pruebas-skill/x/nuestro.mp4)
Renderiza SOLO los tramos y capas que tocan ese trozo (lo hecho se reutiliza), recorta, baja a 1920x1080 y codifica ligero
(x264 CRF 24 + AAC 160k). Si cambias el plan para otra prueba, borra trabajo/tramos y trabajo/capas de esos tramos (o
usa una copia del proyecto por prueba)."""
import json, os, subprocess, sys
from comun import FPS, TRABAJO

if len(sys.argv) != 4: raise SystemExit(__doc__)
a, b, sal = int(round(float(sys.argv[1]) * FPS)), int(round(float(sys.argv[2]) * FPS)), os.path.expanduser(sys.argv[3])
V = json.load(open(f"{TRABAJO}/video.json")); b = min(b, V["total"])
ids = [i for i, tr in enumerate(V["tramos"]) if tr[0]["o"] < b and tr[-1]["o"] + tr[-1]["n"] > a]
if not ids: raise SystemExit("ese trozo no cae en ningún tramo")
P4 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "paso4_render.py")
subprocess.run([sys.executable, P4, "capas"], env={**os.environ, "SOLO_TRAMOS": ",".join(map(str, ids))}, check=True)
subprocess.run([sys.executable, P4, "tramos", "auto", "2", *map(str, ids)], check=True)
T0 = V["tramos"][ids[0]][0]["o"]
lista = f"{TRABAJO}/prueba_lista.txt"; open(lista, "w").write("".join(f"file 'tramos/t{i:03d}.mp4'\n" for i in ids))
aud = next((f"{TRABAJO}/{x}" for x in ("audio_final_musica.wav", "audio_final.wav") if os.path.exists(f"{TRABAJO}/{x}")), None)
os.makedirs(os.path.dirname(os.path.abspath(sal)), exist_ok=True)
cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista]
if aud: cmd += ["-ss", f"{a / FPS:.3f}", "-t", f"{(b - a) / FPS:.3f}", "-i", aud]
cmd += ["-vf", f"trim=start_frame={a - T0}:end_frame={b - T0},setpts=PTS-STARTPTS,scale=1920:1080:flags=lanczos,format=yuv420p",
        "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]
cmd += (["-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "160k", "-shortest"] if aud else ["-an"]) + ["-movflags", "+faststart", sal]
subprocess.run(cmd, check=True); os.remove(lista)
print(f"{sal}  ({(b - a) / FPS:.1f} s, {os.path.getsize(sal) / 1e6:.1f} MB{'' if aud else ', SIN audio: lanza paso5_audio.py y paso6_musica.py'})")
