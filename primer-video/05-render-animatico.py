#!/usr/bin/env python3
"""
TIERRA ALTA - Renderiza el animatico del primer video como un .mp4 real.

No contiene imagen generada: es una pieza de previsualizacion (previz). Lo que renderiza
son los TIEMPOS del montaje, cuadro por cuadro, con timecode quemado, las placas de titulo
y de cierre, los rotulos en sus posiciones reales, y una pista de audio con un tick en cada
corte y los tres silencios del guion, para que el ritmo se pueda escuchar y aprobar antes
de gastar una sola generacion de video.

Es el espejo exacto de primer-video/02-montaje.md. Si cambia el montaje, se cambia la tabla
SHOTS de aca y se vuelve a correr.

USO
    python3 05-render-animatico.py [carpeta_de_salida]

REQUISITOS
    ffmpeg, Pillow, numpy
        apt-get install -y ffmpeg
        pip3 install Pillow numpy
"""

import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ----------------------------------------------------------------- configuracion

W, H = 1920, 1080
FPS = 24
CH = 804                      # alto de la imagen en 2.39:1
Y0 = (H - CH) // 2            # 138: arriba de la ventana de imagen
Y1 = Y0 + CH                  # 942: abajo de la ventana de imagen
PAD = 110                     # margen lateral
TOTAL = 99.0

INK = (10, 10, 11)            # ventana de imagen
BLACK = (0, 0, 0)             # bandas negras
BONE = (233, 229, 221)
DIM = (139, 134, 124)
DIMMER = (93, 89, 79)
FAINT = (52, 50, 45)
WHEAT = (201, 162, 75)
COLD = (125, 149, 171)
SODIO = (208, 111, 57)
ROT = (178, 175, 168)         # rotulo: blanco al 70 % sobre negro

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


F_SLUG = font("DejaVuSerif.ttf", 44)
F_TITLE = font("DejaVuSerif-Bold.ttf", 58)
F_END = font("DejaVuSerif-Bold.ttf", 46)
F_ACT = font("DejaVuSans.ttf", 23)
F_TAG = font("DejaVuSansMono.ttf", 19)
F_TC = font("DejaVuSansMono.ttf", 27)
F_SM = font("DejaVuSansMono.ttf", 18)
F_XS = font("DejaVuSansMono.ttf", 15)
F_ROT = font("DejaVuSansMono.ttf", 24)

BLOCKCOL = {"A": WHEAT, "B": COLD, "C": SODIO, "T": BONE}
BLOCKNM = {
    "A": "BLOQUE A · EL MUNDO NORMAL",
    "B": "BLOQUE B · LA CUENTA",
    "C": "BLOQUE C · LA SALIDA",
    "T": "PLACA",
}

# t = inicio en segundos, d = duracion. Espejo de 02-montaje.md
SHOTS = [
    ("T01", 0, 8, "A", "Campo de trigo al amanecer",
     "Un mar de trigo maduro moviéndose despacio.",
     "Plano fijo. El sol sale por la izquierda. Es hermoso y es completamente común. "
     "No pasa nada, y eso es lo que tiene que pasar.",
     "40 mm · trípode · sin movimiento"),
    ("T02", 8, 6, "A", "Los pájaros se van",
     "Cuarenta pájaros levantan vuelo al mismo tiempo.",
     "Nadie los asusta. Se van todos juntos y el alambre queda vibrando y vacío. "
     "Después el sonido se corta.",
     "28 mm · contrapicado · trípode"),
    ("T03", 14, 8, "A", "La perra mira hacia el este",
     "Pampa, sentada en la vereda, mirando algo que no está.",
     "Las orejas tiesas. Gruñe bajo sin moverse. La calle vacía se va hasta un horizonte "
     "plano. No hay nada que ver.",
     "50 mm · altura de perro · f/2.8"),
    ("T04", 22, 6, "A", "El mapa en la televisión",
     "Dos líneas punteadas. Dos puntos rojos.",
     "Un gráfico de noticiero berreta en un tubo de rayos catódicos. Uno de los puntos cae "
     "en el Pacífico. El otro, frente a Buenos Aires.",
     "85 mm · macro de pantalla · scanlines"),
    ("T05", 28, 8, "A", "Camila entiende",
     "Una mujer se sienta sin mirar la silla.",
     "Tiene las llaves del auto todavía en la mano, a mitad de camino. No llora, no se tapa "
     "la boca. No parpadea en ocho segundos.",
     "85 mm · f/2.0 · sólo los ojos en foco"),
    ("T06", 36, 8, "A", "La bandeja de agua",
     "El agua salta el borde y voltea los bloques de madera.",
     "Levanta una punta quince centímetros y la suelta. Es toda la ciencia de la serie "
     "explicada sin una palabra.",
     "50 mm · lateral a la altura de la mesada"),
    ("TIT", 44, 4, "T", "Placa de título", "", "", ""),
    ("T07", 48, 7, "B", "El mapa de papel",
     "Un dedo cruza la Argentina de este a oeste.",
     "Mapa de rutas YPF del 2003, remendado con cinta, sobre el capó de un Torino. El dedo "
     "se detiene en la cordillera y golpea dos veces.",
     "35 mm · picado total · lámpara colgante"),
    ("T08", 55, 5, "B", "El cajero sin billetes",
     "SIN EXISTENCIA DE BILLETES.",
     "Una mano aprieta el teclado dos veces, fuerte. El mensaje no cambia. Detrás, en el "
     "reflejo, catorce personas que no hablan.",
     "85 mm · macro de pantalla · reflejos"),
    ("T09", 60, 5, "B", "La góndola vacía",
     "Estanterías de metal pelado y harina en el piso.",
     "La cámara pasa de largo, despacio. Un carrito torcido en el pasillo. Los carteles de "
     "precio escritos a mano siguen colgados de las repisas vacías.",
     "40 mm · travelling lateral · tubo parpadeando"),
    ("T10", 65, 5, "B", "La radio se queda muda",
     "La aguja salta dos veces y cae a cero.",
     "Una voz chilena pide auxilio a través de la estática y se corta a mitad de palabra. "
     "Después, ruido blanco. Y nadie en ninguna frecuencia.",
     "85 mm macro · sólo el brillo verde del panel"),
    ("T11", 70, 5, "B", "Humo detrás de la iglesia",
     "Humo negro subiendo, iluminado de naranja desde abajo.",
     "Una luz azul y roja barre la torre. No se ve el fuego, no se ve gente, no se ven "
     "bomberos. Sólo el humo y la luz que gira.",
     "40 mm · contrapicado leve · trípode"),
    ("T12", 75, 6, "C", "Las manos en la chapa",
     "Manos de todas las edades contra la puerta blanca.",
     "El camión avanza a quince por hora y la gente golpea la chapa. Una mano se agarra del "
     "espejo y desaparece de cuadro.",
     "50 mm · en mano · acompañando al camión"),
    ("T13", 81, 6, "C", "El cartel de salida del pueblo",
     "TRES ARROYOS — GRACIAS POR SU VISITA.",
     "La Porfiada pasa el cartel y las luces de posición se hacen chiquitas hasta la nada. "
     "El ruido de la multitud desaparece de un fotograma al otro.",
     "28 mm · trípode al borde de la ruta"),
    ("T14", 87, 7, "C", "El espejo retrovisor",
     "Y en el cielo del este, un punto de luz que no es la luna.",
     "Adentro del reflejo: la ruta, el resplandor naranja del pueblo muy lejos, y arriba una "
     "luz blanca fría, quieta, demasiado brillante. Dura tres segundos más de lo cómodo.",
     "85 mm macro · f/2.0 · vibración del motor"),
    ("FIN", 94, 5, "T", "Placa final", "", "", ""),
]

ROTULOS = [
    (2.0, 7.0, ["TRES ARROYOS, BUENOS AIRES", "H − 31:40"]),
    (88.0, 93.0, ["H − 22:00  ·  COTA 112 m"]),
]
SILENCIOS = [(12.0, 14.0), (68.0, 70.0), (81.0, 82.5)]
CORTES = [s[1] for s in SHOTS]

# ----------------------------------------------------------------- dibujo

def spaced(draw, xy, text, fnt, fill, sp):
    """Dibuja texto con espaciado entre letras y devuelve el ancho total."""
    x, y = xy
    for ch in text:
        if draw:
            draw.text((x, y), ch, font=fnt, fill=fill)
        x += fnt.getlength(ch) + sp
    return x - xy[0] - sp


def spaced_w(text, fnt, sp):
    return sum(fnt.getlength(c) + sp for c in text) - sp


def wrap(text, fnt, maxw):
    out, line = [], ""
    for word in text.split():
        probe = (line + " " + word).strip()
        if fnt.getlength(probe) <= maxw or not line:
            line = probe
        else:
            out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def fmt(t):
    m = int(t // 60)
    return "%d:%04.1f" % (m, t - m * 60)


def base_frame(shot, rot_lines, silent):
    """Cuadro base de un plano, sin timecode ni barra de progreso."""
    sid, st, sd, blk, _nm, slug, act, lens = shot
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    d.rectangle([0, Y0, W, Y1], fill=BLACK if (silent or blk == "T") else INK)

    # banda superior
    x = PAD
    x += spaced(d, (x, 52), "TIERRA ALTA", F_SM, BONE, 3.2) + 16
    spaced(d, (x, 52), "·  ANIMÁTICO  ·  VIDEO Nº 1  ·  APERTURA", F_SM, DIMMER, 1.6)
    lbl = "SIN IMAGEN GENERADA  ·  PREVIZ  ·  2.39:1  ·  24 fps"
    spaced(d, (W - PAD - spaced_w(lbl, F_XS, 1.8), 56), lbl, F_XS, FAINT, 1.8)

    if silent:
        txt = "S I L E N C I O"
        spaced(d, ((W - spaced_w(txt, F_SM, 6)) / 2, Y0 + CH / 2 - 12), txt, F_SM, DIMMER, 6)

    elif sid == "TIT":
        txt = "TIERRA ALTA"
        spaced(d, ((W - spaced_w(txt, F_TITLE, 24)) / 2, Y0 + CH / 2 - 40),
               txt, F_TITLE, BONE, 24)

    elif sid == "FIN":
        t1 = "TIERRA ALTA"
        spaced(d, ((W - spaced_w(t1, F_END, 18)) / 2, Y0 + CH / 2 - 150), t1, F_END, BONE, 18)
        t2 = "EPISODIO 1  ·  «HORA CERO»"
        spaced(d, ((W - spaced_w(t2, F_TC, 7)) / 2, Y0 + CH / 2 - 20), t2, F_TC, DIM, 7)
        t3 = "PRÓXIMAMENTE"
        spaced(d, ((W - spaced_w(t3, F_SM, 9)) / 2, Y0 + CH / 2 + 80), t3, F_SM, DIMMER, 9)

    else:
        col = BLOCKCOL[blk]
        x = PAD
        x += spaced(d, (x, Y0 + 66), sid, F_TAG, col, 4) + 22
        spaced(d, (x, Y0 + 66), "·   " + BLOCKNM[blk], F_TAG, col, 2.4)

        y = Y0 + 152
        for ln in wrap(slug, F_SLUG, W - 2 * PAD - 120):
            d.text((PAD, y), ln, font=F_SLUG, fill=BONE)
            y += 58
        y += 26
        for ln in wrap(act, F_ACT, 1180):
            d.text((PAD, y), ln, font=F_ACT, fill=DIM)
            y += 34

        lw = spaced_w(lens, F_XS, 1.8)
        spaced(d, (W - PAD - lw, Y1 - 62), lens, F_XS, DIMMER, 1.8)

    if rot_lines:
        y = Y1 - 56 - 34 * (len(rot_lines) - 1)
        for ln in rot_lines:
            d.text((PAD, y), ln, font=F_ROT, fill=ROT)
            y += 34

    return img


def draw_hud(img, t, idx):
    """Timecode y barra de progreso, en la banda negra de abajo."""
    d = ImageDraw.Draw(img)
    sid, st, sd = SHOTS[idx][0], SHOTS[idx][1], SHOTS[idx][2]

    d.text((PAD, 972), fmt(t), font=F_TC, fill=BONE)
    off = F_TC.getlength(fmt(t))
    d.text((PAD + off + 14, 976), "/  1:39.0", font=F_SM, fill=DIMMER)

    right = "%s  ·  %d s  ·  plano %d de %d" % (sid, sd, idx + 1, len(SHOTS))
    spaced(d, (W - PAD - spaced_w(right, F_SM, 1.8), 976), right, F_SM, DIM, 1.8)

    # barra segmentada
    bx, by, bw, bh = PAD, 1040, W - 2 * PAD, 7
    for j, sh in enumerate(SHOTS):
        x = bx + bw * sh[1] / TOTAL
        w = bw * sh[2] / TOTAL
        c = BLOCKCOL[sh[3]]
        played = t >= sh[1] + sh[2]
        cur = j == idx
        if played or cur:
            fill = c
        else:
            fill = tuple(int(v * 0.3) for v in c)
        d.rectangle([x, by, x + w - 2, by + bh], fill=fill)
        if cur:
            # parte ya transcurrida del plano actual, un poco mas alta
            p = (t - sh[1]) / sh[2]
            d.rectangle([x, by - 3, x + (w - 2) * p, by + bh], fill=c)
    px = bx + bw * t / TOTAL
    d.line([px, by - 9, px, by + bh + 6], fill=BONE, width=1)
    return img


# ----------------------------------------------------------------- audio

def build_audio(path):
    """Pista guia: cama de ruido muy baja, tick en cada corte, infrasonido al final,
    y los tres silencios del guion como caidas reales a cero."""
    sr = 48000
    n = int(TOTAL * sr)
    rng = np.random.default_rng(7)

    # cama de ruido a -50 dBFS: existe para que los silencios se noten por contraste
    bed = rng.standard_normal(n).astype(np.float32) * 0.0032

    # los tres silencios, con rampas de 30 ms para que no chasqueen
    ramp = int(0.03 * sr)
    for a, b in SILENCIOS:
        i, j = int(a * sr), int(b * sr)
        bed[i:j] = 0.0
        bed[max(0, i - ramp):i] *= np.linspace(1, 0, min(ramp, i), dtype=np.float32)
        bed[j:j + ramp] *= np.linspace(0, 1, ramp, dtype=np.float32)

    out = bed

    # tick en cada corte: 2000 Hz en los planos, 1200 Hz en las placas
    dur = int(0.022 * sr)
    env = np.exp(-np.linspace(0, 9, dur, dtype=np.float32))
    for sh in SHOTS:
        t = sh[1]
        freq = 1200.0 if sh[3] == "T" else 2000.0
        amp = 0.22 if sh[3] != "T" else 0.16
        i = int(t * sr)
        seg = np.sin(2 * np.pi * freq * np.arange(dur, dtype=np.float32) / sr) * env * amp
        out[i:i + dur] += seg[: max(0, min(dur, n - i))]

    # infrasonido de 25 Hz desde 1:27 hasta el final, creciendo
    i = int(87 * sr)
    k = n - i
    tt = np.arange(k, dtype=np.float32) / sr
    out[i:] += np.sin(2 * np.pi * 25.0 * tt) * np.linspace(0.02, 0.30, k, dtype=np.float32)

    out = np.clip(out, -1.0, 1.0)
    pcm = (out * 32767).astype(np.int16)
    stereo = np.repeat(pcm[:, None], 2, axis=1).reshape(-1)

    with wave.open(path, "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes(stereo.tobytes())


# ----------------------------------------------------------------- render

def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "salida"
    os.makedirs(outdir, exist_ok=True)
    wav = os.path.join(outdir, "_animatico_audio.wav")
    mp4 = os.path.join(outdir, "TIERRA_ALTA_ANIMATICO.mp4")

    print("==> audio")
    build_audio(wav)

    nframes = int(TOTAL * FPS)
    cache = {}

    cmd = [
        "ffmpeg", "-y", "-v", "error", "-stats",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H), "-r", str(FPS),
        "-i", "-",
        "-i", wav,
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart", mp4,
    ]
    print("==> %d cuadros a %d fps" % (nframes, FPS))
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    idx = 0
    for f in range(nframes):
        t = f / FPS
        while idx + 1 < len(SHOTS) and t >= SHOTS[idx + 1][1]:
            idx += 1

        rot = None
        for a, b, lines in ROTULOS:
            if a <= t < b:
                rot = tuple(lines)
                break
        silent = any(a <= t < b for a, b in SILENCIOS)

        key = (idx, rot, silent)
        if key not in cache:
            cache[key] = base_frame(SHOTS[idx], list(rot) if rot else None, silent)
        img = cache[key].copy()
        draw_hud(img, t, idx)
        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    rc = proc.wait()
    os.remove(wav)
    if rc != 0:
        print("ERROR: ffmpeg devolvio %d" % rc)
        return rc

    size = os.path.getsize(mp4) / 1e6
    print("\n==> listo: %s  (%.1f MB)" % (mp4, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
