"""Paso 5: audio final SIN música = voz montada + efectos de sonido puntuales, filtrado suave y -14 LUFS.
Efectos: SOLO pegados a gráficos (título, capítulo, rótulo, mapa, cifra…), nunca en cada corte («a veces»).
El mapa tipo -> (sonido, ganancia) se puede cambiar o vaciar en plan.py con SFX = {...}; los sonidos están en
estudio/public/sonidos/. Salida: trabajo/mezcla.wav (sin normalizar, para el paso 6) y trabajo/audio_final.wav."""
import json, os, subprocess
import numpy as np, soundfile as sf
from comun import CAPAS_JSON, ESTUDIO, FPS, TRABAJO, ajuste
import plan      # después de comun: es quien mete la carpeta del vídeo en el path

SR = 48000; SND = f"{ESTUDIO}/public/sonidos"
# G003 (2026-11-24, estudio de 22 referencias): suena la CONSECUENCIA, no la entrada. Etiquetas (trk), cifras (dato) y
# golpes de zoom entran mudos; el sonido va con "snd" en el instante del cambio (casilla, logro, plaza). Excepción: el
# DINERO suena siempre (7 de 7 refs que rotulan precios): cualquier texto con €, $, «euros», «dólares»… lleva "dinero".
# Rollback por creador: deshacer_cambio.py <creador> G003.
SFX = {"titulo": ("impact-bass-1", 0.30), "seccion": ("whoosh-short", 0.22), "trk": None, "mapa": ("click-soft", 0.30),
       "suscribe": ("pop", 0.25), "dato": None, "golpe": None, "dinero": ("ping", 0.22)}
SFX = {**SFX, **ajuste("SFX", {})}                 # personal/<creador>/ajustes.py: cambia o quita (None) el de un tipo
SFX = {k: v for k, v in getattr(plan, "SFX", SFX).items() if v}   # plan.py del vídeo: sustituye el mapa entero
LUFS = ajuste("LUFS", -14)
import re
DINERO = re.compile(r"[€$£¥]|\b(euros?|d[oó]lares?|dollars?|pesos?|d[ií]rhams?|libras?)\b", re.I)


def normalizar(entrada, salida):
    """-14 LUFS integrados (o el LUFS de personal/<creador>/ajustes.py), pico real -1,5 dB, en dos pasadas (medir y aplicar lineal)."""
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", entrada, "-af", f"loudnorm=I={LUFS}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", entrada, "-af",
                    f"loudnorm=I={LUFS}:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
                    "-ar", str(SR), salida], check=True)
    return m


if __name__ == "__main__":
    C = json.load(open(CAPAS_JSON, encoding="utf-8"))
    y, _ = sf.read(f"{TRABAJO}/voz.wav", dtype="float32")
    # ---- voz disfrazada: lo que dice alguien que no quiere que se le reconozca (quien graba, un tercero) ----
    # plan.py: VOZ_DISFRAZ = [(clip, "frase literal", n), …] -> de la primera a la última palabra de esa frase, tono arriba
    # sin cambiar la duración (voz de pitufo). Cuánto: VOZ_DISFRAZ_TONO en personal/<creador>/ajustes.py (1,45 ≈ +6 semitonos).
    # Lucas, 2026-11-14 (prueba-3): «cuando habla el cámara (señor misterio) […] distorsiona un poco la voz para que no se le
    # reconozca, puede ser como una voz de pitufo».
    disfraz = getattr(plan, "VOZ_DISFRAZ", [])
    if disfraz:
        # La frase se busca en lo que SUENA (voz.json, voces.buscar_oido): así vale también lo que dice quien graba entre
        # las palabras de una pieza aunque no esté en el texto del EDL, y los bordes son los del audio (en prueba-3 la
        # línea alineada ponía «¿Qué ha pasado?» 2,6 s antes de donde sonaba). Si ahí no está, se usa la línea del EDL.
        from comun import Linea, buscar
        from voces import buscar_oido, candidatas
        Lv, tono = Linea(), float(ajuste("VOZ_DISFRAZ_TONO", 1.45)); xf = int(0.02 * SR); hechas = []
        for a in disfraz:
            try: i, j = buscar(Lv.palabras, *a); lin = (Lv.palabras[i]["o0"] / FPS, Lv.palabras[j]["o1"] / FPS)
            except (Exception, SystemExit): lin = None          # no está en el texto del EDL (lo dice quien graba entre palabras)
            r = buscar_oido(a[1], a[2], lin[0] if lin else None)
            if not r and not lin: raise SystemExit(f"VOZ_DISFRAZ: «{a[1]}» no se oye en voz.json ni está en el EDL")
            s0, s1 = r or lin
            if r and lin and min(r[1], lin[1] + 0.3) > max(r[0], lin[0] - 0.3):    # las dos: lo que suena, sin pasarse de la línea
                s0, s1 = max(r[0], lin[0] - 0.3), min(r[1], lin[1] + 0.3)
            hechas.append((s0, s1))
            a0 = max(0, int(s0 * SR) - int(0.08 * SR)); a1 = min(len(y), int(s1 * SR) + int(0.12 * SR))
            seg = np.ascontiguousarray(y[a0:a1], dtype=np.float32).reshape(a1 - a0, -1)
            raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", str(seg.shape[1]), "-i", "-", "-af",
                                  f"asetrate={int(SR * tono)},aresample={SR},atempo={1 / tono:.5f}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout
            pr = np.frombuffer(raw, np.float32).reshape(-1, seg.shape[1])[:len(seg)]
            pr = np.vstack([pr, np.zeros((len(seg) - len(pr), seg.shape[1]), np.float32)])
            w = np.ones(len(seg), np.float32); w[:xf] = np.linspace(0, 1, xf); w[-xf:] = np.linspace(1, 0, xf)
            y[a0:a1] = (seg * (1 - w[:, None]) + pr * w[:, None]).reshape(y[a0:a1].shape)
            # lo que suena ahí según voz.json: así se ve al momento si se ha disfrazado la aparición equivocada (en
            # vaciamos-estanque, ("IMG_2053", "un mes", 0) era el «un mes» del creador; el de fondo era n=1)
            oido = " ".join(f["texto"].strip() for f in json.load(open(f"{TRABAJO}/voz.json", encoding="utf-8"))["frases"]
                            if f["hasta"] > a0 / SR and f["desde"] < a1 / SR) if os.path.exists(f"{TRABAJO}/voz.json") else "?"
            print(f"voz disfrazada {a0 / SR:.2f}-{a1 / SR:.2f} s: «{a[1]}»  — lo que suena ahí: «{oido}» (¿es de la otra persona?)")
        # ¿queda alguna frase con pinta de ser de la otra persona sin disfrazar? (voces.py; Lucas, prueba-3 v2: «se te han
        # escapado bastantes partes en las que habla el cámara»)
        for t0, t1, txt, p, db in candidatas()[0]:
            if not any(min(t1, b) - max(t0, a) > 0.3 * (t1 - t0) for a, b in hechas):
                print(f"AVISO VOZ: {int(t0 // 60)}:{t0 % 60:05.2f} «{txt}» suena a la otra persona ({p:.0f} Hz, {db:.0f} dB) y no está en VOZ_DISFRAZ")
    # ---- fails (FALLOS en plan.py; paso3 deja los tramos en trabajo/fallos.json): la voz algo saturada, como una radio
    # rota, mientras la imagen va en blanco y negro. Lucas, 2026-11-17: «poner en blanco y negro y saturar un poco la voz
    # porque es un fail». Entra y sale con un fundido corto, para que no haya clic.
    fallos = json.load(open(f"{TRABAJO}/fallos.json")) if os.path.exists(f"{TRABAJO}/fallos.json") else []
    for f0, f1 in fallos:
        a0, a1 = f0 * SR // FPS, min(len(y), f1 * SR // FPS); seg = np.ascontiguousarray(y[a0:a1], dtype=np.float32).reshape(a1 - a0, -1)
        raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", str(seg.shape[1]), "-i", "-", "-af",
                              "highpass=f=350,lowpass=f=3800,volume=14dB,asoftclip=type=tanh,volume=-9dB", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout
        pr = np.frombuffer(raw, np.float32).reshape(-1, seg.shape[1])[:len(seg)]; pr = np.vstack([pr, np.zeros((len(seg) - len(pr), seg.shape[1]), np.float32)])
        xf = min(int(0.03 * SR), len(seg) // 4); w = np.ones(len(seg), np.float32); w[:xf] = np.linspace(0, 1, xf); w[-xf:] = np.linspace(1, 0, xf)
        y[a0:a1] = (seg * (1 - w[:, None]) + pr * w[:, None]).reshape(y[a0:a1].shape); print(f"fail: voz saturada {f0 / FPS:.1f}-{f1 / FPS:.1f} s")
    # ---- pitidos (PITIDOS en plan.py): cada palabrota tapada con un pitido de 1 kHz, del principio al final de la palabra
    # según la alineación forzada (linea.json), con 15 ms de fundido para que no haya clic. Formato: (clip, "palabra o frase
    # literal", n) como cualquier ancla de frase (n = 0 la primera vez que suena en el montaje, -1 la última, 1 la segunda…).
    # Va DESPUÉS de VOZ_DISFRAZ y de los fails: si una palabra está en los dos, manda el pitido. Lista de las que suenan:
    # palabrotas.py. Reino Selva, 2026-11-19 (vaciamos-estanque): «pita también los hostia y cojones y demás palabrotas».
    pitidos = getattr(plan, "PITIDOS", [])
    if pitidos:
        from comun import Linea, buscar
        from voces import buscar_oido
        Lp = Linea()
        for a in pitidos:
            try:
                i, j = buscar(Lp.palabras, *a); s0, s1 = Lp.palabras[i]["o0"] / FPS - 0.03, Lp.palabras[j]["o1"] / FPS + 0.04
            except (Exception, SystemExit):          # no está en el texto del EDL: la dice quien graba entre palabras (en voz.json)
                r = buscar_oido(a[1], a[2])
                if not r: raise SystemExit(f"PITIDOS: «{a[1]}» no está en el EDL ni se oye en voz.json")
                s0, s1 = r[0] - 0.03, r[1] + 0.04
            a0, a1 = max(0, int(s0 * SR)), min(len(y), int(s1 * SR)); n_ = a1 - a0; xf = min(int(0.015 * SR), n_ // 3)
            seg = y[a0:a1].reshape(n_, -1); rms = float(np.sqrt(np.mean(seg ** 2))) or 0.05
            tono = (np.sin(2 * np.pi * 1000 * np.arange(n_) / SR) * min(0.35, rms * 1.6)).astype(np.float32)
            w = np.ones(n_, np.float32); w[:xf] = np.linspace(0, 1, xf); w[n_ - xf:] = np.linspace(1, 0, xf)
            y[a0:a1] = (seg * (1 - w[:, None]) + tono[:, None] * w[:, None]).reshape(y[a0:a1].shape)
            print(f"pitido {s0:.2f}-{s1:.2f} s: «{a[1]}»")
    cache = {}
    def snd(n, vel=1.0):      # vel: el clip al que acompaña va a esa velocidad (un botón acelerado para que quepa); el tono no cambia
        if (n, vel) not in cache:
            ruta = f"{ESTUDIO}/public/{n}" if "/" in n else f"{SND}/{n}.mp3"      # con barra: archivo propio dentro de estudio/public/
            raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", ruta, *(["-af", f"atempo={vel:.4f}"] if abs(vel - 1) > 0.001 else []), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
            cache[(n, vel)] = np.frombuffer(raw, np.float32).reshape(-1, 2)
        return cache[(n, vel)]
    fx = np.zeros_like(y); n = 0
    for it in C["items"]:
        if not it.get("snd") and it["t"] not in SFX and "dinero" in SFX and DINERO.search(str(it.get("txt", "")) + " " + str(it.get("sub", ""))):
            it = {**it, "snd": SFX["dinero"]}
        if it.get("snd") or it["t"] in SFX:      # "snd": [archivo, ganancia, velocidad?] en el item (botones, gráficos propios) manda sobre el mapa por tipo
            nombre, g, *v = it.get("snd") or SFX[it["t"]]; s = snd(nombre, float(v[0]) if v else 1.0) * g; o = it["f0"] * SR // FPS; s = s[:len(fx) - o]; fx[o:o + len(s)] += s; n += 1
    sf.write(f"{TRABAJO}/voz_fx_pre.wav", y, SR); sf.write(f"{TRABAJO}/fx.wav", fx, SR)
    # voz: paso alto 80 Hz + compresión suave; luego mezcla con efectos
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{TRABAJO}/voz_fx_pre.wav", "-i", f"{TRABAJO}/fx.wav", "-filter_complex",
                    "[0:a]highpass=f=80,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=160:makeup=2[v];[v][1:a]amix=inputs=2:normalize=0[m]", "-map", "[m]", f"{TRABAJO}/mezcla.wav"], check=True)
    m = normalizar(f"{TRABAJO}/mezcla.wav", f"{TRABAJO}/audio_final.wav")
    print(f"{n} efectos; entrada {m['input_i']} LUFS, LRA {m['input_lra']}")
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", f"{TRABAJO}/audio_final.wav", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    print(r[r.rindex("Summary"):][:400])
