#!/usr/bin/env python3
"""Busca los EFECTOS DE SONIDO de un vídeo y prepara su revisión (para las fichas de referencias o un montaje propio).

Uso: escuchar_sfx.py VIDEO SALIDA.json [--stems DIR] [--cortes cortes.json] [--umbral 6] [--por-min 10] [--sin-clap]

Claude no oye: este script es su oído aproximado. Qué hace:
1) Quita la voz: DIR/no_vocals.wav de analizar_audio.py (demucs; si no está, lo lanza él).
2) Candidatos: subidas bruscas de energía en lo que no es voz (>= --umbral dB sobre los 0,4 s anteriores) y subidas
   largas de 0,4–3 s (risers, whooshes largos).
3) Cada candidato se pasa por un modelo de audio (CLAP, laion/clap-htsat-unfused, zero-shot) que da una PISTA del tipo
   (whoosh, pop, impacto, ding, obturador, glitch, riser…) y cuánto tiene de nuevo respecto a lo que sonaba antes.
4) Se queda con los --por-min mejores por minuto y saca sfx_hoja_NN.jpg: espectrograma + fotograma de cada uno.
   Quien analiza CONFIRMA mirando la hoja (firmas al final del script) y el vídeo; solo lo confirmado va a la ficha.
Fiabilidad medida en el JSON («fiabilidad»). La primera vez baja el modelo (~600 MB). Con GPU (CUDA/MPS) va rápido;
--sin-clap: solo candidatos y hoja, sin modelo (poca RAM)."""
import argparse, json, os, subprocess, sys, tempfile
from pathlib import Path
import numpy as np, librosa, soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("salida")
ap.add_argument("--stems"); ap.add_argument("--cortes"); ap.add_argument("--umbral", type=float, default=6.0)
ap.add_argument("--sin-clap", action="store_true"); ap.add_argument("--por-min", type=float, default=10.0); ap.add_argument("--max", type=int, default=1500)
a = ap.parse_args()
sal = Path(a.salida); stems = Path(a.stems) if a.stems else sal.parent / "stems"
SR = 22050; HOP = 256

# ---------- 1. pistas ----------
if not (stems / "no_vocals.wav").exists():
    aqui = Path(__file__).resolve().parent
    print("No hay stems: separo voz y resto con analizar_audio.py (demucs)…", flush=True)
    subprocess.run([sys.executable, str(aqui / "analizar_audio.py"), a.video, str(sal.parent / "audio_demucs.json"),
                    "--stems", str(stems)], check=True)
resto, _ = librosa.load(stems / "no_vocals.wav", sr=SR)
voz, _ = librosa.load(stems / "vocals.wav", sr=SR) if (stems / "vocals.wav").exists() else (np.zeros_like(resto), SR)
ritmo = librosa.load(stems / "ritmo.wav", sr=SR)[0] if (stems / "ritmo.wav").exists() else None
n = min(len(resto), len(voz)); resto, voz = resto[:n], voz[:n]
if ritmo is not None: ritmo = ritmo[:n]

def rms_db(x):
    r = librosa.feature.rms(y=x, frame_length=1024, hop_length=HOP)[0]
    return 20 * np.log10(r + 1e-6)

E = rms_db(resto); EV = rms_db(voz); ER = rms_db(ritmo) if ritmo is not None else np.full_like(E, -90)
fps = SR / HOP; T = lambda i: i / fps; I = lambda t: int(round(t * fps))

# ---------- 2. candidatos ----------
cand = []
prev = I(0.4); gap = I(0.25); last = -10 ** 9
for i in range(prev, len(E) - 2):
    base = np.percentile(E[i - prev:i], 50)
    pico = E[i:i + 3].max()
    if pico - base >= a.umbral and pico > -50 and i - last >= gap and E[i] > E[i - 1]:
        cand.append(("golpe", i)); last = i
# subidas largas (riser/whoosh largo): energía que crece casi sin parar 0,4–3 s y acaba alta
sm = np.convolve(E, np.ones(9) / 9, mode="same"); d = np.diff(sm); i = 0
while i < len(d):
    if d[i] > 0.15:
        j = i
        while j < len(d) and d[j] > -0.05: j += 1
        if I(0.4) <= j - i <= I(3.0) and sm[j] - sm[i] >= 10 and sm[j] > -40: cand.append(("subida", i))
        i = j + 1
    else: i += 1
cand.sort(key=lambda c: c[1])
cand = cand[:a.max]
print(f"{len(cand)} candidatos", flush=True)

# ---------- 3. escuchar ----------
ETIQ = {
    "whoosh": "a fast whoosh sound effect of air swooshing past",
    "swoosh_largo": "a long cinematic swoosh transition sound effect",
    "riser": "a rising riser sound effect building tension",
    "pop": "a short cartoon pop sound effect, like a bubble popping",
    "click": "a short soft click sound of a mouse or button",
    "impacto": "a deep cinematic boom impact hit sound effect",
    "ding": "a bright ding chime bell notification sound",
    "obturador": "a camera shutter click sound",
    "scratch": "a vinyl record scratch sound effect",
    "caja_registradora": "a cash register cha-ching money sound",
    "glitch": "a digital glitch distortion sound effect",
    "risas": "an audience laughing out loud, sitcom laugh track",
    "tecleo": "typing on a keyboard sound",
    "explosion": "an explosion sound effect",
    "boing": "a cartoon boing spring sound effect",
    "notificacion": "a phone notification sound",
    "sparkle": "a magical sparkle shimmer sound effect",
    "error": "a wrong answer buzzer error sound",
    "redoble": "a drum roll",
    "silbido": "a whistle sound effect",
    "_musica": "a drum beat or note in background music, part of a song",
    "_ambiente": "ambient background noise of a room or the outdoors",
    "_ruido_directo": "real-world sound recorded by the camera, like footsteps, a door or objects",
    "_animal": "an animal sound, a bird or a dog",
}
claves = list(ETIQ)
ef = []
if a.sin_clap:
    for k, i in cand: ef.append({"t": round(T(i), 2), "pista_tipo": "sin_clasificar", "conf": None, "novedad": 0.0, "via": k, "_i": i})
else:
    import torch
    from transformers import ClapModel, ClapProcessor
    dev = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
    MOD = "laion/clap-htsat-unfused"
    vec = lambda o: o if torch.is_tensor(o) else (getattr(o, "text_embeds", None) or getattr(o, "audio_embeds", None) or o.pooler_output)   # transformers 4 da el tensor; la 5, un objeto
    proc = ClapProcessor.from_pretrained(MOD); mod = ClapModel.from_pretrained(MOD).to(dev).eval()
    with torch.no_grad():
        ti = proc(text=[ETIQ[k] for k in claves], return_tensors="pt", padding=True).to(dev)
        te = vec(mod.get_text_features(**ti)); te = te / te.norm(dim=-1, keepdim=True)
    # la mezcla (lo que se oye) a 48 kHz para el modelo: el efecto se juzga como suena, con la voz quitada
    resto48 = librosa.resample(resto, orig_sr=SR, target_sr=48000)
    # Se escucha el instante (desde 0,1 s antes) y lo que sonaba justo antes (1,2 s). «novedad» = cuánto se parece MÁS a
    # un efecto el instante que lo de antes (la música de fondo sale en los dos). Sirve para ORDENAR, no para decidir:
    # medido con efectos reales a -4 dB bajo la mezcla, CLAP no separa bien un efecto de un golpe de la música.
    SFXC = [k for k in claves if not k.startswith("_")]; isfx = [claves.index(k) for k in SFXC]
    def emb(lst):
        with torch.no_grad():
            ai = proc(audio=lst, sampling_rate=48000, return_tensors="pt", padding=True).to(dev)
            ae = vec(mod.get_audio_features(**ai)); return (ae / ae.norm(dim=-1, keepdim=True) @ te.T).cpu().numpy()
    lote = 32
    for b in range(0, len(cand), lote):
        trozo = cand[b:b + lote]; aud, pre = [], []
        for k, i in trozo:
            t0 = max(0.0, T(i) - 0.1); t1 = t0 + (2.5 if k == "subida" else 0.9)
            aud.append(resto48[int(t0 * 48000):int(t1 * 48000)])
            p0 = max(0.0, t0 - 1.2); pre.append(resto48[int(p0 * 48000):int(t0 * 48000)] if t0 - p0 > 0.3 else np.zeros(int(0.6 * 48000), np.float32))
        sw, sp = emb(aud), emb(pre)
        for (k, i), s, q in zip(trozo, sw, sp):
            ds = s[isfx]; pr = np.exp(100 * ds) / np.exp(100 * ds).sum(); o = np.argsort(-pr)
            ef.append({"t": round(T(i), 2), "pista_tipo": SFXC[o[0]], "conf": round(float(pr[o[0]]), 2),
                       "otras": [[SFXC[j], round(float(pr[j]), 2)] for j in o[1:3]],
                       "novedad": round(float((s[isfx] - q[isfx]).max()), 3), "via": k, "_i": i})
        print(f"  escuchados {min(b + lote, len(cand))}/{len(cand)}", flush=True)

# ---------- 4. medidas y contexto ----------
cortes = []
if a.cortes and os.path.exists(a.cortes):
    cj = json.load(open(a.cortes, encoding="utf-8"))
    cortes = sorted(float(c["t"] if isinstance(c, dict) else c) for c in (cj.get("cortes", cj) if isinstance(cj, dict) else cj))
for e in ef:
    i = e.pop("_i"); w = I(0.6)
    seg = E[i:i + w]; e["db_pico"] = round(float(seg.max()), 1)
    fin = next((j for j in range(i + 1, min(len(E), i + I(3))) if E[j] < seg.max() - 12), min(len(E) - 1, i + I(3)))
    e["dur"] = round(T(fin - i), 2)
    e["sobre_musica_db"] = round(float(seg.max() - np.median(ER[max(0, i - I(1)):i] if ritmo is not None else E[max(0, i - I(1)):i])), 1)
    vz = EV[max(0, i - I(1.5)):i + I(1.5)]; hab = vz[vz > -45]
    e["respecto_voz_db"] = round(float(seg.max() - np.median(hab)), 1) if len(hab) else None
    if cortes:
        k = int(np.searchsorted(cortes, e["t"])); dd = [abs(e["t"] - cortes[j]) for j in (k - 1, k) if 0 <= j < len(cortes)]
        e["a_corte_s"] = round(min(dd), 2) if dd else None

dur = n / SR
# Orden: primero lo más «nuevo» respecto a lo de antes y que más destaca sobre la música. Se quedan los mejores
# --por-min por minuto (los efectos de un vídeo de YouTube rara vez pasan de 8–10 por minuto).
for e in ef: e["puntuacion"] = round(e["novedad"] * 100 + 0.5 * max(0.0, e["sobre_musica_db"]), 2)
ef.sort(key=lambda e: -e["puntuacion"]); cupo = max(20, int(a.por_min * dur / 60)); ef = sorted(ef[:cupo], key=lambda e: e["t"])
for k, e in enumerate(ef, 1): e["n"] = k

# Hoja de revisión: por candidato, el espectrograma de lo que no es voz (-0,5 s a +1,0 s; la línea cian = el instante)
# y el fotograma del vídeo en ese momento. Firmas: whoosh = mancha de ruido ancha que sube o baja; pop/click = raya
# vertical finísima; impacto = mancha fuerte abajo (graves) que se apaga; ding/ping = rayas horizontales que se apagan;
# riser = mancha que sube de tono/volumen hasta el instante; un golpe de la música se repite a compás en las celdas vecinas.
hojas = []
try:
    from PIL import Image, ImageDraw
    tiene_video = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_type",
                                  "-of", "csv=p=0", a.video], capture_output=True, text=True).stdout.strip() == "video"
    TW, TH, COLS, FIL = 320, 150, 4, 6
    for h0 in range(0, len(ef), COLS * FIL):
        lote = ef[h0:h0 + COLS * FIL]; alto_c = TH + (180 if tiene_video else 0) + 18
        hoja = Image.new("RGB", (COLS * TW, ((len(lote) + COLS - 1) // COLS) * alto_c), (10, 10, 10))
        for k, e in enumerate(lote):
            x, y = (k % COLS) * TW, (k // COLS) * alto_c
            seg = resto[max(0, int((e["t"] - 0.5) * SR)):int((e["t"] + 1.0) * SR)]
            D = librosa.amplitude_to_db(np.abs(librosa.stft(seg, n_fft=1024, hop_length=128)) + 1e-9, ref=np.max)
            im = Image.fromarray((np.clip((D + 70) / 70, 0, 1)[::-1] * 255).astype(np.uint8)).resize((TW - 4, TH)).convert("RGB")
            dd = ImageDraw.Draw(im); xm = int((TW - 4) / 3); dd.line([(xm, 0), (xm, TH)], fill=(0, 220, 255))
            hoja.paste(im, (x + 2, y + 18))
            if tiene_video:
                with tempfile.TemporaryDirectory() as tmp:
                    fj = os.path.join(tmp, "f.jpg")
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(e["t"]), "-i", a.video, "-frames:v", "1",
                                    "-vf", f"scale={TW - 4}:-2", fj], check=False)
                    if os.path.exists(fj): hoja.paste(Image.open(fj).crop((0, 0, TW - 4, 178)), (x + 2, y + 18 + TH + 2))
            ImageDraw.Draw(hoja).text((x + 4, y + 3), f"#{e['n']} {int(e['t'] // 60):02d}:{e['t'] % 60:05.2f}  ¿{e['pista_tipo']}? {e['conf']}",
                                      fill=(255, 230, 80))
        ruta = sal.parent / f"sfx_hoja_{h0 // (COLS * FIL):02d}.jpg"; hoja.save(ruta, quality=85); hojas.append(ruta.name)
except Exception as ex:
    print(f"(sin hoja de revisión: {ex})")

por = {}
for e in ef: por.setdefault(e["pista_tipo"], []).append(e)
res = {"duracion_s": round(dur, 1), "candidatos": len(ef), "detectados_antes_de_cupo": len(cand),
       "pista_por_tipo": {k: len(v) for k, v in sorted(por.items(), key=lambda kv: -len(kv[1]))},
       "candidatos_en_corte_pct": (round(100 * np.mean([1.0 if (e.get("a_corte_s") is not None and e["a_corte_s"] <= 0.15) else 0.0 for e in ef]), 1)
                                   if cortes and ef else None)}
json.dump({"video": os.path.basename(a.video),
           "metodo": "candidatos por subida de energía en la pista sin voz (demucs) + pista de tipo con CLAP zero-shot",
           "fiabilidad": ("Medido (2026-11-24) con 24 efectos conocidos a -4 dB bajo la mezcla: los momentos se encuentran casi todos "
                          "(22/24) pero mezclados con golpes de la música; el tipo solo es fiable cuando el efecto suena limpio. "
                          "NO son efectos confirmados: se confirman mirando sfx_hoja_*.jpg y los fotogramas antes de citarlos. "
                          "Lo que vaya en la ficha: solo los confirmados, con su tipo y su momento en pantalla."),
           "hojas": hojas, "resumen": res, "candidatos": ef}, open(sal, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✓ {sal}: {len(ef)} candidatos para revisar (de {len(cand)} subidas); hojas: {', '.join(hojas) or 'ninguna'}")
