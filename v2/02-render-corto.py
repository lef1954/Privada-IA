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
TOTAL = 130.0

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

EMBER = (196, 104, 52)
DEEP = (150, 122, 96)
BLOCKCOL = {"A": WHEAT, "B": COLD, "C": SODIO, "D": EMBER, "E": DEEP, "T": BONE}
BLOCKNM = {
    "A": "BLOQUE 1 · LA MAÑANA",
    "B": "BLOQUE 2 · LA DECISIÓN",
    "C": "BLOQUE 3 · EL ROBO",
    "D": "BLOQUE 4 · EL CIELO",
    "E": "BLOQUE 5 · EL AGUA",
    "T": "PLACA",
}

# t = inicio en segundos, d = duracion. Espejo de 02-montaje.md
SHOTS = [
    ("C01", 0, 7, "A", "Cosechadora en el trigo",
     "Diciembre. Treinta y ocho grados. La cosecha.",
     "Una cosechadora roja cruza el cuadro tirando una nube de polvo dorado. El horizonte es "
     "absolutamente plano. Es el día más común del año.", "40 mm · trípode · fijo"),
    ("C02", 7, 6, "A", "La cola de camiones",
     "Marcos trabaja. El camión que va a robar ya está ahí.",
     "Diez camiones cargados esperando la balanza de la cooperativa. Él pasa arrastrando una "
     "lona y golpea dos veces un acoplado al pasar.", "35 mm · en mano"),
    ("C03", 13, 7, "A", "La cocina y el televisor",
     "Andrea se queda quieta con un plato en la mano.",
     "Tiene el ambo del hospital puesto. En la tele, placa roja: se confirma el ingreso de tres "
     "cuerpos en la atmósfera.", "35 mm · en mano · luz de persiana"),
    ("C04", 20, 6, "A", "Lucía mira el cielo",
     "Hay una estela pálida a pleno mediodía.",
     "La nena de espaldas, sin cara. Arriba, una raya blanca corta y quieta que no debería "
     "estar. Y las chicharras se callan.", "40 mm · contrapicado · sin cara"),
    ("C05", 26, 6, "A", "La radio de la cabina",
     "Menos de nueve horas para el primero.",
     "Marcos con la mano en el dial. No se mueve por cinco segundos. Después mira para el lado "
     "del pueblo.", "85 mm · f/2.0"),
    ("C06", 32, 7, "B", "El patio",
     "«Agarrá lo que puedas cargar, nada más.»",
     "Los dos se mueven rápido por el patio hablando encima del otro. Ella llena bolsas de "
     "supermercado, él descuelga un bidón y no la mira.", "35 mm · en mano · sol duro"),
    ("C07", 39, 6, "B", "El botiquín",
     "No clasifica nada. Sabe exactamente qué hace falta.",
     "Barre el armario entero adentro del bolso. Al final vuelve, elige una caja de ampollas y "
     "la apoya arriba de todo, sola.", "50 mm · picado total · macro"),
    ("C08", 45, 5, "B", "Las llaves puestas",
     "Diez cabinas abiertas. Diez llaves colgando.",
     "La cámara pasa de largo por la fila. No hay nadie. Un guante de trabajo tirado en la "
     "tierra.", "50 mm · travelling lateral"),
    ("C09", 50, 6, "B", "La mano en la llave",
     "Tres segundos quieta. Después gira.",
     "El plano que decide si el robo se siente o no. Arranca el diésel y todo el cuadro empieza "
     "a vibrar.", "85 mm macro · fijo"),
    ("C10", 56, 6, "C", "Rompe la barrera",
     "Sale sin frenar.",
     "El Scania blanco revienta la barrera de madera y sale de la cooperativa. Atrás, dos "
     "hombres corren y se paran. En la puerta dice COOPERATIVA AGRÍCOLA — TRES ARROYOS.",
     "28 mm · trípode · al ras"),
    ("C11", 62, 6, "C", "Suben Andrea y los chicos",
     "Seis segundos para subir una familia entera.",
     "Bolsas de supermercado, el nene alzado de un brazo, la nena trepando sola. Quedan bolsas "
     "en la vereda que nadie levanta.", "35 mm · en mano · sin caras"),
    ("C12", 68, 6, "C", "El pueblo desbordado",
     "Un colchón atado al techo de un Renault 12.",
     "Cuarenta personas en la puerta de un almacén, una moto zigzagueando, humo negro atrás de "
     "los techos. Nadie mira a cámara.", "21 mm · en mano · avanzando"),
    ("C13", 74, 5, "C", "Suben los vecinos",
     "«¡Dale la mano! ¡La mano!»",
     "Manos de todas las edades agarrándose de las tablas del acoplado en movimiento. Un "
     "antebrazo con guardapolvo blanco. Una caja de herramientas que sube primero.",
     "50 mm · acompañando al camión"),
    ("C14", 79, 5, "C", "El cartel de salida",
     "TRES ARROYOS.",
     "El camión se aleja con el acoplado lleno de gente parada. Atrás, el pueblo chato y una "
     "sola columna de humo negro.", "28 mm · trípode"),
    ("C15", 84, 7, "D", "Las esquirlas",
     "Doce rayas de fuego bajando en paralelo.",
     "Chiquitas, lejos, y muchas. Dejan estelas rectas que quedan colgadas en el cielo. El "
     "silbido llega después, desfasado.", "35 mm · trípode · al cielo"),
    ("C16", 91, 6, "D", "Impacto en el campo",
     "A trescientos metros de la ruta.",
     "Flash blanco, columna de tierra negra y trigo ardiendo, y un anillo de polvo rodando por "
     "el sembrado hacia cámara. Dos segundos de silencio antes del golpe.",
     "40 mm · al ras · temblor"),
    ("C17", 97, 5, "D", "Bauti en la ventanilla",
     "«No mires.»",
     "El nene apenas como silueta contra el vidrio. En foco, sobre el marco de la ventanilla, "
     "el dinosaurio de plástico, con la luz naranja titilando encima.",
     "85 mm · f/2.0 · sin cara"),
    ("C18", 102, 6, "D", "El terremoto",
     "El asfalto se ondula como una alfombra.",
     "La ruta de frente. Se abre una grieta en los dos carriles. El camión viene de frente, "
     "cruza los dos carriles y vuelve, con el acoplado coleando.", "28 mm · fijo · temblor duro"),
    ("C19", 108, 6, "E", "El espejo retrovisor",
     "Una línea pálida en el horizonte. Podría ser niebla.",
     "Adentro del reflejo: la ruta recta, el horizonte plano, el cielo naranja. Y esa línea, "
     "apenas un poco más gruesa al final del plano que al principio.", "85 mm macro · fijo"),
    ("C20", 114, 8, "E", "La pared de agua",
     "Los silos desaparecen adentro, uno por uno, de derecha a izquierda.",
     "Teleobjetivo. Adelante, silos y dos molinos de campo para dar escala. Atrás, ocupando "
     "todo el horizonte, el agua marrón. No parece rápida: es enorme. Y entra muda.",
     "135 mm · trípode · sin movimiento"),
    ("C21", 122, 3, "E", "Marcos acelera",
     "Mira el espejo un segundo. Vuelve al frente. Aprieta.",
     "Corte a negro en el fotograma exacto.", "85 mm · f/2.0"),
    ("FIN", 125, 5, "T", "Placa final", "", "", ""),
]

ROTULOS = [
    (2.0, 7.5, ["TRES ARROYOS, BUENOS AIRES", "21 DE DICIEMBRE DE 2012"]),
    (109.0, 114.0, ["H + 32"]),
]
SILENCIOS = [(24.0, 26.0), (89.0, 91.0), (114.0, 118.0)]
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
    x += spaced(d, (x, 52), "21 DE DICIEMBRE", F_SM, BONE, 3.2) + 16
    spaced(d, (x, 52), "·  ANIMÁTICO  ·  CORTO  ·  21 PLANOS", F_SM, DIMMER, 1.6)
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
        t1 = "21 DE DICIEMBRE"
        spaced(d, ((W - spaced_w(t1, F_END, 10)) / 2, Y0 + CH / 2 - 150), t1, F_END, BONE, 10)
        t2 = "CORTO DE PRESENTACIÓN"
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
    d.text((PAD + off + 14, 976), "/  2:10.0", font=F_SM, fill=DIMMER)

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
    mp4 = os.path.join(outdir, "21_DE_DICIEMBRE_CORTO.mp4")

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
