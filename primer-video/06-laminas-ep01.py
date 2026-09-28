#!/usr/bin/env python3
"""
TIERRA ALTA - Laminas de concepto del Episodio 1, dibujadas por codigo.

NO son fotogramas generados por IA ni capturas de la serie. Son laminas de concepto:
composicion, luz y paleta de ocho momentos del Episodio 1, dibujadas proceduralmente en
estilo grafico de siluetas. Sirven para lo que sirve un concept board: fijar el encuadre y
el color antes de generar, y poder mostrarle a alguien de que se trata la serie.

Produce:
    salida/laminas/L1..L8.png      las ocho laminas, 2400x1005
    salida/TIERRA_ALTA_EP01_MUESTRA.mp4   muestra de 45 s con movimiento lento y textos

USO
    python3 06-laminas-ep01.py [carpeta_de_salida]

REQUISITOS
    ffmpeg, Pillow, numpy
"""

import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ----------------------------------------------------------------- base

PW, PH = 2400, 1005           # tamano de lamina (sobredimensionada para poder hacer zoom)
OW, OH = 1920, 1080           # entrega
CH = 804                      # ventana 2.39:1
Y0 = (OH - CH) // 2
FPS = 24
PLATE_SEC = 5.0
HEAD_SEC = 3.0
TAIL_SEC = 2.0

BONE = (233, 229, 221)
DIM = (139, 134, 124)
DIMMER = (93, 89, 79)
FAINT = (52, 50, 45)

FDIR = "/usr/share/fonts/truetype/dejavu"
F_SLUG = ImageFont.truetype(os.path.join(FDIR, "DejaVuSerif.ttf"), 40)
F_TITLE = ImageFont.truetype(os.path.join(FDIR, "DejaVuSerif-Bold.ttf"), 54)
F_SM = ImageFont.truetype(os.path.join(FDIR, "DejaVuSansMono.ttf"), 18)
F_XS = ImageFont.truetype(os.path.join(FDIR, "DejaVuSansMono.ttf"), 15)
F_MAP = ImageFont.truetype(os.path.join(FDIR, "DejaVuSansMono.ttf"), 22)
F_SIGN = ImageFont.truetype(os.path.join(FDIR, "DejaVuSans-Bold.ttf"), 26)

RNG = np.random.default_rng(11)


def hexc(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def vgrad(stops, w=PW, h=PH):
    """Degrade vertical. stops = [(pos 0..1, '#rrggbb'), ...]"""
    ys = np.linspace(0, 1, h, dtype=np.float32)
    pos = np.array([p for p, _ in stops], dtype=np.float32)
    cols = np.array([hexc(c) for _, c in stops], dtype=np.float32)
    out = np.empty((h, 3), dtype=np.float32)
    for k in range(3):
        out[:, k] = np.interp(ys, pos, cols[:, k])
    return np.repeat(out[:, None, :], w, axis=1)


def glow(arr, cx, cy, r, color, strength=1.0, power=2.2):
    """Halo radial aditivo."""
    h, w = arr.shape[:2]
    yy, xx = np.ogrid[0:h, 0:w]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    f = np.clip(1.0 - d, 0, 1) ** power * strength
    arr += f[:, :, None] * np.array(hexc(color), dtype=np.float32)
    return arr


def grain(arr, amt=6.0):
    return arr + RNG.standard_normal(arr.shape).astype(np.float32) * amt


def vignette(arr, strength=0.34):
    h, w = arr.shape[:2]
    yy, xx = np.ogrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    f = 1.0 - np.clip((d - 0.55) / 0.9, 0, 1) * strength
    return arr * f[:, :, None]


def to_img(arr):
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def to_arr(img):
    return np.asarray(img, dtype=np.float32).copy()


def finish(img, vig=0.34, gr=6.0):
    a = to_arr(img)
    a = vignette(a, vig)
    a = grain(a, gr)
    return to_img(a)


def overlay(img):
    """Capa RGBA para dibujar con transparencia."""
    return Image.new("RGBA", img.size, (0, 0, 0, 0))


def merge(img, ov):
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")


# ----------------------------------------------------------------- laminas

def L1_trigo():
    """Campo de trigo al amanecer. Los pajaros se van."""
    hz = int(PH * 0.50)
    a = vgrad([(0.0, "#1b3450"), (0.30, "#4a6a86"), (0.44, "#9db1b8"),
               (0.499, "#f2c887"), (0.50, "#c9a45e"), (1.0, "#5a4526")])
    a = glow(a, PW * 0.27, hz - 26, 520, "#3a2a0e", 1.0, 2.6)
    a = glow(a, PW * 0.27, hz - 26, 150, "#6b5320", 1.0, 2.0)
    img = to_img(a)
    d = ImageDraw.Draw(img)

    # sol
    d.ellipse([PW * 0.27 - 44, hz - 70, PW * 0.27 + 44, hz + 18], fill=hexc("#ffe2a6"))

    # linea de eucaliptos muy lejos
    for i in range(40):
        x = 120 + i * 13 + RNG.integers(-4, 4)
        hh = 16 + RNG.integers(0, 14)
        d.rectangle([x, hz - hh, x + 11, hz + 2], fill=hexc("#8d7b55"))

    # trigo: miles de trazos cortos, mas oscuros y largos cerca de camara
    for _ in range(70000):
        u = RNG.random() ** 1.7
        y = hz + u * (PH - hz)
        x = RNG.random() * PW
        depth = (y - hz) / (PH - hz)
        ln = 7 + depth * 34
        lean = RNG.normal(0, 0.30) * (0.4 + depth)
        base = np.array([214, 168, 86]) * (1.0 - depth * 0.62)
        base = base * (0.80 + RNG.random() * 0.42)
        d.line([x, y, x + lean * ln, y - ln], fill=tuple(np.clip(base, 0, 255).astype(int)),
               width=1 if depth < 0.55 else 2)

    # pajaros yendose hacia el oeste
    for i in range(16):
        bx = PW * 0.56 + RNG.random() * PW * 0.34
        by = PH * 0.10 + RNG.random() * PH * 0.20
        s = 7 + RNG.random() * 8
        d.line([bx - s, by, bx, by - s * 0.45], fill=hexc("#1c2a38"), width=2)
        d.line([bx, by - s * 0.45, bx + s, by], fill=hexc("#1c2a38"), width=2)

    return finish(img, 0.30, 5.0)


def L2_calle():
    """La calle vacia al amanecer. Pampa mira hacia el este."""
    hz = int(PH * 0.47)
    vpx = PW * 0.52
    a = vgrad([(0.0, "#39434e"), (0.34, "#6e7b85"), (0.46, "#a8b2b6"),
               (0.47, "#6a6257"), (1.0, "#2b2723")])
    img = to_img(a)
    d = ImageDraw.Draw(img)

    # calzada
    d.polygon([(vpx - 22, hz), (vpx + 22, hz), (PW * 1.22, PH), (-PW * 0.22, PH)],
              fill=hexc("#43403b"))
    # veredas
    d.polygon([(vpx - 30, hz), (vpx - 20, hz), (-PW * 0.16, PH), (-PW * 0.30, PH)],
              fill=hexc("#514c44"))
    d.polygon([(vpx + 20, hz), (vpx + 30, hz), (PW * 1.30, PH), (PW * 1.16, PH)],
              fill=hexc("#514c44"))

    # casas bajas a los costados, en silueta
    for side in (-1, 1):
        z = 0.055
        while z < 1.0:
            sc = z ** 1.5
            x0 = vpx + side * (34 + 1500 * sc)
            x1 = vpx + side * (34 + 1500 * (sc + 0.09 * (0.3 + sc)))
            hh = (36 + 300 * sc) * (0.75 + RNG.random() * 0.6)
            top = hz - hh
            v = int(26 + 30 * (1 - sc))
            d.polygon([(x0, top), (x1, top - hh * 0.10), (x1, PH), (x0, PH)],
                      fill=(v, v - 2, v - 5))
            z += 0.085

    # postes de luz
    z = 0.09
    while z < 1.0:
        sc = z ** 1.5
        x = vpx - (30 + 1400 * sc)
        hh = 60 + 520 * sc
        d.line([x, hz - hh, x, hz + 12 * sc], fill=hexc("#1b1a18"), width=max(1, int(2 + 7 * sc)))
        d.line([x, hz - hh, x + 40 * sc + 6, hz - hh + 6], fill=hexc("#1b1a18"),
               width=max(1, int(1 + 5 * sc)))
        z += 0.17

    # la perra, de espaldas, en primer plano
    cx, cy, s = PW * 0.30, PH * 0.93, 1.0
    body = [(cx - 62 * s, cy), (cx - 46 * s, cy - 150 * s), (cx - 30 * s, cy - 215 * s),
            (cx + 30 * s, cy - 215 * s), (cx + 46 * s, cy - 150 * s), (cx + 62 * s, cy)]
    d.polygon(body, fill=(14, 13, 12))
    d.ellipse([cx - 44 * s, cy - 300 * s, cx + 44 * s, cy - 196 * s], fill=(14, 13, 12))
    d.polygon([(cx - 42 * s, cy - 268 * s), (cx - 20 * s, cy - 336 * s),
               (cx - 8 * s, cy - 262 * s)], fill=(14, 13, 12))   # oreja parada
    d.polygon([(cx + 10 * s, cy - 262 * s), (cx + 30 * s, cy - 320 * s),
               (cx + 44 * s, cy - 258 * s)], fill=(14, 13, 12))  # oreja doblada
    d.polygon([(cx + 52 * s, cy - 20 * s), (cx + 120 * s, cy - 54 * s),
               (cx + 126 * s, cy - 34 * s), (cx + 58 * s, cy + 4 * s)], fill=(14, 13, 12))

    return finish(img, 0.40, 5.5)


def L3_tele():
    """El mapa en la television. Dos puntos rojos."""
    a = np.zeros((PH, PW, 3), dtype=np.float32)
    a[:] = np.array([9, 9, 10], dtype=np.float32)
    img = to_img(a)
    d = ImageDraw.Draw(img)

    sx0, sy0, sx1, sy1 = PW * 0.14, PH * 0.10, PW * 0.86, PH * 0.90
    d.rounded_rectangle([sx0, sy0, sx1, sy1], radius=90, fill=hexc("#0d1712"))

    # resplandor de fosforo
    ov = overlay(img)
    od = ImageDraw.Draw(ov)
    od.rounded_rectangle([sx0 + 14, sy0 + 14, sx1 - 14, sy1 - 14], radius=78,
                         fill=(24, 46, 34, 255))
    ov = ov.filter(ImageFilter.GaussianBlur(40))
    img = merge(img, ov)
    d = ImageDraw.Draw(img)

    # cono sur, simplificado
    cx, cy, sc = PW * 0.50, PH * 0.50, PH * 0.0034
    pts = [(-52, -130), (-20, -128), (10, -112), (28, -86), (34, -58), (30, -30),
           (22, 4), (12, 44), (2, 82), (-6, 112), (-16, 128), (-30, 126),
           (-34, 104), (-30, 70), (-36, 34), (-44, -2), (-52, -40), (-58, -78),
           (-60, -108)]
    poly = [(cx + x * sc * 3.2, cy + y * sc * 3.2) for x, y in pts]
    d.polygon(poly, fill=hexc("#2a4a3a"), outline=hexc("#5f8f72"))

    # trayectorias punteadas
    for (ex, ey) in ((cx - 235, cy - 60), (cx + 215, cy - 30)):
        x0, y0 = cx + (ex - cx) * 0.25, sy0 + 40
        for i in range(30):
            t = i / 29.0
            px = x0 + (ex - x0) * t
            py = y0 + (ey - y0) * t - np.sin(t * np.pi) * 70
            if i % 2 == 0:
                d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=hexc("#cfe4d6"))

    # los dos puntos rojos
    ov = overlay(img)
    od = ImageDraw.Draw(ov)
    for (ex, ey) in ((cx - 235, cy - 60), (cx + 215, cy - 30)):
        od.ellipse([ex - 46, ey - 46, ex + 46, ey + 46], fill=(220, 40, 30, 120))
    ov = ov.filter(ImageFilter.GaussianBlur(26))
    img = merge(img, ov)
    d = ImageDraw.Draw(img)
    for (ex, ey) in ((cx - 235, cy - 60), (cx + 215, cy - 30)):
        d.ellipse([ex - 13, ey - 13, ex + 13, ey + 13], fill=hexc("#ff4a36"))

    # franja roja de placa, sin texto legible
    d.rectangle([sx0 + 60, sy1 - 150, sx1 - 60, sy1 - 78], fill=hexc("#8e1a12"))
    for i in range(7):
        x = sx0 + 92 + i * 168
        d.rectangle([x, sy1 - 126, x + 118, sy1 - 104], fill=hexc("#d8b9b4"))

    # scanlines
    a = to_arr(img)
    a[::3, :, :] *= 0.86
    img = to_img(a)

    return finish(img, 0.46, 7.0)


def L4_cocina():
    """La cocina. Camila entiende, a contraluz de la ventana."""
    a = vgrad([(0.0, "#14120f"), (1.0, "#0a0908")])
    img = to_img(a)

    # ventana
    ov = overlay(img)
    od = ImageDraw.Draw(ov)
    wx0, wy0, wx1, wy1 = PW * 0.42, PH * 0.07, PW * 0.86, PH * 0.66
    od.rectangle([wx0, wy0, wx1, wy1], fill=(255, 238, 205, 255))
    ov2 = ov.filter(ImageFilter.GaussianBlur(70))
    img = merge(img, ov2)
    img = merge(img, ov)
    d = ImageDraw.Draw(img)

    # cruz de la ventana
    d.rectangle([(wx0 + wx1) / 2 - 9, wy0, (wx0 + wx1) / 2 + 9, wy1], fill=hexc("#6a5c44"))
    d.rectangle([wx0, PH * 0.34, wx1, PH * 0.34 + 9], fill=hexc("#6a5c44"))

    # mesa
    d.rectangle([0, PH * 0.735, PW, PH * 0.79], fill=hexc("#241f19"))
    d.rectangle([0, PH * 0.79, PW, PH], fill=hexc("#0c0b09"))

    # silueta sentada
    hx, hy = PW * 0.60, PH * 0.44
    d.ellipse([hx - 76, hy - 96, hx + 76, hy + 62], fill=(7, 7, 7))
    d.polygon([(hx - 250, PH * 0.78), (hx - 150, hy + 78), (hx - 60, hy + 40),
               (hx + 60, hy + 40), (hx + 150, hy + 78), (hx + 250, PH * 0.78)],
              fill=(7, 7, 7))
    # brazo sobre la mesa y llaves colgando
    d.polygon([(hx + 70, hy + 96), (hx + 210, PH * 0.70), (hx + 226, PH * 0.735),
               (hx + 78, hy + 132)], fill=(7, 7, 7))
    d.line([hx + 222, PH * 0.735, hx + 226, PH * 0.775], fill=(7, 7, 7), width=3)
    d.ellipse([hx + 218, PH * 0.775, hx + 236, PH * 0.793], fill=(7, 7, 7))

    # mate sobre la mesa
    d.ellipse([PW * 0.27, PH * 0.700, PW * 0.27 + 58, PH * 0.700 + 58], fill=(9, 8, 8))
    d.line([PW * 0.27 + 44, PH * 0.700 + 6, PW * 0.27 + 58, PH * 0.640],
           fill=(9, 8, 8), width=7)

    return finish(img, 0.48, 6.0)


def L5_mapa():
    """El mapa de papel. La linea al oeste, y las cotas."""
    a = np.full((PH, PW, 3), 0.0, dtype=np.float32)
    a[:] = np.array([206, 190, 158], dtype=np.float32)
    a = a + RNG.standard_normal((PH, PW, 1)).astype(np.float32) * 9
    a = glow(a, PW * 0.5, PH * 0.42, PW * 0.62, "#2a2416", -0.55, 1.6)
    img = to_img(a)
    d = ImageDraw.Draw(img)

    # dobleces del mapa
    for x in (PW * 0.25, PW * 0.5, PW * 0.75):
        d.line([x, 0, x, PH], fill=hexc("#b6a488"), width=3)
    d.line([0, PH * 0.5, PW, PH * 0.5], fill=hexc("#b6a488"), width=3)

    cities = [
        ("TRES ARROYOS", 115, 0.845, 0.40),
        ("BAHÍA BLANCA", 12, 0.735, 0.47),
        ("RÍO COLORADO", 79, 0.620, 0.50),
        ("CHOELE CHOEL", 86, 0.530, 0.52),
        ("NEUQUÉN", 265, 0.360, 0.55),
        ("PIEDRA DEL ÁGUILA", 600, 0.235, 0.63),
        ("BARILOCHE", 770, 0.130, 0.68),
    ]

    # la ruta
    pts = [(PW * fx, PH * fy) for _, _, fx, fy in cities]
    d.line(pts, fill=hexc("#8e2f1c"), width=9, joint="curve")

    for (nm, cota, fx, fy) in cities:
        x, y = PW * fx, PH * fy
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=hexc("#2b2418"))
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=hexc("#cebe9e"))
        label = "%s  %d m" % (nm, cota)
        tw = F_MAP.getlength(label)
        up = cota >= 265
        d.text((x - tw / 2, y - 52 if up else y + 26), label, font=F_MAP, fill=hexc("#2b2418"))

    # anotacion a mano
    d.line([PW * 0.845, PH * 0.40, PW * 0.130, PH * 0.68], fill=hexc("#1d4f7a"), width=3)
    d.text((PW * 0.40, PH * 0.80), "1.320 km", font=F_TITLE, fill=hexc("#1d4f7a"))
    d.text((PW * 0.40, PH * 0.875), "115 m  →  770 m", font=F_MAP, fill=hexc("#1d4f7a"))

    return finish(img, 0.42, 7.0)


def L6_ruta():
    """Ruta 3 de noche. La cola de cuatro kilometros."""
    hz = int(PH * 0.42)
    vpx = PW * 0.47
    a = vgrad([(0.0, "#05070c"), (0.36, "#0a1018"), (0.42, "#161c22"), (1.0, "#08090a")])
    img = to_img(a)
    d = ImageDraw.Draw(img)

    # estrellas
    for _ in range(320):
        x, y = RNG.random() * PW, RNG.random() * hz * 0.9
        v = int(70 + RNG.random() * 150)
        d.point((x, y), fill=(v, v, v))

    d.polygon([(vpx - 14, hz), (vpx + 14, hz), (PW * 1.25, PH), (-PW * 0.25, PH)],
              fill=hexc("#14161a"))

    # luces rojas: la fila que no se mueve
    ov = overlay(img)
    od = ImageDraw.Draw(ov)
    z = 0.006
    while z < 1.0:
        sc = z ** 2.0
        y = hz + (PH - hz) * sc
        off = 30 + 900 * sc
        r = max(1.4, 2 + 17 * sc)
        for sgn, col in ((1, (255, 46, 30)), (-1, (255, 74, 40))):
            for dx in (-r * 2.6, r * 2.6):
                x = vpx + sgn * off + dx
                od.ellipse([x - r * 2.4, y - r * 2.4, x + r * 2.4, y + r * 2.4],
                           fill=col + (70,))
        z += 0.020
    ov = ov.filter(ImageFilter.GaussianBlur(9))
    img = merge(img, ov)
    d = ImageDraw.Draw(img)

    z = 0.006
    while z < 1.0:
        sc = z ** 2.0
        y = hz + (PH - hz) * sc
        off = 30 + 900 * sc
        r = max(1.0, 1.4 + 9 * sc)
        for dx in (-r * 2.6, r * 2.6):
            d.ellipse([vpx + off + dx - r, y - r, vpx + off + dx + r, y + r],
                      fill=hexc("#ff5a3c"))
        # del otro lado, unos pocos faros blancos que vuelven
        if int(z * 1000) % 7 == 0:
            d.ellipse([vpx - off - r, y - r, vpx - off + r, y + r], fill=hexc("#e9e2cf"))
        z += 0.020

    return finish(img, 0.44, 6.0)


def L7_salida():
    """La salida del pueblo. El camion y el cartel."""
    hz = int(PH * 0.46)
    a = vgrad([(0.0, "#05070d"), (0.38, "#0b1119"), (0.46, "#1a1a1c"), (1.0, "#0a0a0b")])
    img = to_img(a)
    a = to_arr(img)
    a = glow(a, PW * 0.20, hz + 30, 700, "#personal".replace("#personal", "#7a3410"), 1.0, 2.4)
    img = to_img(a)
    d = ImageDraw.Draw(img)

    for _ in range(220):
        x, y = RNG.random() * PW, RNG.random() * hz * 0.75
        v = int(60 + RNG.random() * 130)
        d.point((x, y), fill=(v, v, v))

    d.polygon([(PW * 0.50, hz), (PW * 0.56, hz), (PW * 1.3, PH), (-PW * 0.2, PH)],
              fill=hexc("#141416"))

    # el camion, de atras, alejandose
    bx, by, bw, bh = PW * 0.50, PH * 0.78, 300, 250
    d.rectangle([bx - bw / 2, by - bh, bx + bw / 2, by], fill=(10, 10, 11))
    d.rectangle([bx - bw / 2 - 16, by - bh - 14, bx + bw / 2 + 16, by - bh],
                fill=(10, 10, 11))
    for i in range(5):
        x = bx - 96 + i * 48
        d.rectangle([x, by - bh - 11, x + 16, by - bh - 3], fill=hexc("#c8721f"))
    ov = overlay(img)
    od = ImageDraw.Draw(ov)
    for sgn in (-1, 1):
        od.ellipse([bx + sgn * 104 - 44, by - 74 - 44, bx + sgn * 104 + 44, by - 74 + 44],
                   fill=(255, 40, 26, 110))
    ov = ov.filter(ImageFilter.GaussianBlur(20))
    img = merge(img, ov)
    d = ImageDraw.Draw(img)
    for sgn in (-1, 1):
        d.rectangle([bx + sgn * 104 - 20, by - 88, bx + sgn * 104 + 20, by - 60],
                    fill=hexc("#ff3b26"))

    # el cartel
    cx0, cy0, cx1, cy1 = PW * 0.70, PH * 0.42, PW * 0.945, PH * 0.63
    d.rectangle([cx0 - 8, cy0 - 8, cx1 + 8, cy1 + 8], fill=hexc("#2a2620"))
    d.rectangle([cx0, cy0, cx1, cy1], fill=hexc("#5d5748"))
    d.rectangle([(cx0 + cx1) / 2 - 9, cy1, (cx0 + cx1) / 2 + 9, PH * 0.88],
                fill=hexc("#241f19"))
    t1 = "TRES ARROYOS"
    t2 = "GRACIAS POR SU VISITA"
    d.text(((cx0 + cx1) / 2 - F_SIGN.getlength(t1) / 2, cy0 + 40), t1,
           font=F_SIGN, fill=hexc("#cdc6b2"))
    d.text(((cx0 + cx1) / 2 - F_XS.getlength(t2) * 1.55 / 2, cy0 + 106), t2,
           font=F_MAP, fill=hexc("#a49d8b"))

    return finish(img, 0.46, 6.0)


def L8_espejo():
    """El espejo retrovisor. El punto de luz que no es la luna."""
    a = np.full((PH, PW, 3), 7.0, dtype=np.float32)
    img = to_img(a)
    d = ImageDraw.Draw(img)

    mx0, my0, mx1, my1 = PW * 0.17, PH * 0.14, PW * 0.83, PH * 0.86
    d.rounded_rectangle([mx0 - 26, my0 - 26, mx1 + 26, my1 + 26], radius=40,
                        fill=hexc("#131315"))

    # reflejo
    inner = Image.new("RGB", (int(mx1 - mx0), int(my1 - my0)))
    iw, ih = inner.size
    hz = int(ih * 0.45)
    ia = vgrad([(0.0, "#070a10"), (0.36, "#0d141c"), (0.45, "#241a12"), (1.0, "#0c0b0a")],
               w=iw, h=ih)
    ia = glow(ia, iw * 0.52, hz + 8, iw * 0.42, "#function".replace("#function", "#803312"),
              1.0, 2.6)
    inner = to_img(ia)
    idr = ImageDraw.Draw(inner)
    for _ in range(140):
        x, y = RNG.random() * iw, RNG.random() * hz * 0.8
        v = int(50 + RNG.random() * 110)
        idr.point((x, y), fill=(v, v, v))
    idr.polygon([(iw * 0.48, hz), (iw * 0.54, hz), (iw * 1.25, ih), (-iw * 0.25, ih)],
                fill=hexc("#17171a"))

    # el punto de luz: chico, quieto, con un halo minimo
    lx, ly = iw * 0.70, hz - ih * 0.26
    iov = Image.new("RGBA", inner.size, (0, 0, 0, 0))
    iod = ImageDraw.Draw(iov)
    iod.ellipse([lx - 26, ly - 26, lx + 26, ly + 26], fill=(235, 240, 255, 90))
    iov = iov.filter(ImageFilter.GaussianBlur(13))
    inner = Image.alpha_composite(inner.convert("RGBA"), iov).convert("RGB")
    idr = ImageDraw.Draw(inner)
    idr.ellipse([lx - 5, ly - 4, lx + 5, ly + 4], fill=hexc("#f2f5ff"))

    img.paste(inner, (int(mx0), int(my0)))
    d = ImageDraw.Draw(img)

    # polvo sobre el vidrio
    for _ in range(240):
        x = mx0 + RNG.random() * (mx1 - mx0)
        y = my0 + RNG.random() * (my1 - my0)
        v = int(30 + RNG.random() * 60)
        d.point((x, y), fill=(v, v, v))
    d.rounded_rectangle([mx0, my0, mx1, my1], radius=18, outline=hexc("#2a2a2d"), width=5)

    return finish(img, 0.52, 6.5)


PLATES = [
    (L1_trigo, "1.01", "Un mar de trigo maduro moviéndose despacio.",
     "TRES ARROYOS, BUENOS AIRES   ·   H − 31:40", (1.00, 0.90), (0.5, 0.52)),
    (L2_calle, "1.03", "Pampa mira hacia el este. No hay nada que ver.",
     "H − 31:40   ·   COTA 115 m", (0.93, 1.00), (0.42, 0.55)),
    (L3_tele, "1.06", "Dos líneas punteadas. Dos puntos rojos.",
     "CADENA NACIONAL   ·   H − 31:12", (1.00, 0.88), (0.5, 0.5)),
    (L4_cocina, "1.07", "Una mujer se sienta sin mirar la silla.",
     "H − 31:10", (0.95, 0.86), (0.58, 0.46)),
    (L5_mapa, "1.33", "Mil trescientos veinte kilómetros. Y ochocientos metros para arriba.",
     "TALLER DE DON ALDO   ·   H − 28:10", (0.88, 1.00), (0.5, 0.5)),
    (L6_ruta, "3.01", "Esto ya no es una ruta. Es una cola.",
     "RN 3 OESTE   ·   H − 21:00   ·   COTA 98 m", (1.00, 0.90), (0.47, 0.5)),
    (L7_salida, "2.09", "Y después, la última casa del pueblo.",
     "H − 22:00   ·   COTA 112 m   ·   8 km RECORRIDOS", (0.92, 1.00), (0.5, 0.55)),
    (L8_espejo, "1.49", "Y en el cielo del este, un punto de luz que no es la luna.",
     "H − 27:00", (1.00, 0.85), (0.62, 0.42)),
]


# ----------------------------------------------------------------- video

def spaced(draw, xy, text, fnt, fill, sp):
    x, y = xy
    for ch in text:
        if draw:
            draw.text((x, y), ch, font=fnt, fill=fill)
        x += fnt.getlength(ch) + sp
    return x - xy[0] - sp


def spaced_w(text, fnt, sp):
    return sum(fnt.getlength(c) + sp for c in text) - sp


def chrome(img, slug, rot, alpha):
    """Bandas negras con los textos."""
    d = ImageDraw.Draw(img)
    x = 110
    x += spaced(d, (x, 52), "TIERRA ALTA", F_SM, BONE, 3.2) + 16
    spaced(d, (x, 52), "·  EPISODIO 1  ·  MUESTRA VISUAL", F_SM, DIMMER, 1.6)
    lbl = "LÁMINAS DE CONCEPTO  ·  DIBUJADAS, NO GENERADAS"
    spaced(d, (OW - 110 - spaced_w(lbl, F_XS, 1.8), 56), lbl, F_XS, FAINT, 1.8)

    if alpha > 0.01:
        c = tuple(int(v * alpha) for v in BONE)
        d.text((110, 968), slug, font=F_SLUG, fill=c)
        c2 = tuple(int(v * alpha) for v in DIMMER)
        spaced(d, (110, 1026), rot, F_XS, c2, 2.2)
    return img


def build_audio(path, total):
    sr = 48000
    n = int(total * sr)
    rng = np.random.default_rng(3)
    out = rng.standard_normal(n).astype(np.float32) * 0.0030

    dur = int(0.020 * sr)
    env = np.exp(-np.linspace(0, 9, dur, dtype=np.float32))
    for k in range(len(PLATES)):
        i = int((HEAD_SEC + k * PLATE_SEC) * sr)
        seg = np.sin(2 * np.pi * 1900 * np.arange(dur, dtype=np.float32) / sr) * env * 0.20
        out[i:i + dur] += seg[: max(0, min(dur, n - i))]

    i = int((HEAD_SEC + 7 * PLATE_SEC) * sr)
    k = n - i
    tt = np.arange(k, dtype=np.float32) / sr
    out[i:] += np.sin(2 * np.pi * 25.0 * tt) * np.linspace(0.02, 0.26, k, dtype=np.float32)

    pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
    st = np.repeat(pcm[:, None], 2, axis=1).reshape(-1)
    with wave.open(path, "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes(st.tobytes())


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "salida"
    ldir = os.path.join(outdir, "laminas")
    os.makedirs(ldir, exist_ok=True)

    imgs = []
    for i, (fn, sc, slug, rot, zoom, center) in enumerate(PLATES, 1):
        print("==> lámina %d/8  %s" % (i, fn.__name__))
        im = fn()
        im.save(os.path.join(ldir, "L%d.png" % i))
        imgs.append(im)

    total = HEAD_SEC + len(PLATES) * PLATE_SEC + TAIL_SEC
    wav = os.path.join(outdir, "_muestra_audio.wav")
    build_audio(wav, total)

    mp4 = os.path.join(outdir, "TIERRA_ALTA_EP01_MUESTRA.mp4")
    cmd = ["ffmpeg", "-y", "-v", "error", "-stats",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (OW, OH), "-r", str(FPS),
           "-i", "-", "-i", wav,
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", mp4]
    nframes = int(total * FPS)
    print("==> %d cuadros" % nframes)
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    for f in range(nframes):
        t = f / FPS
        frame = Image.new("RGB", (OW, OH), (0, 0, 0))

        if t < HEAD_SEC:
            d = ImageDraw.Draw(frame)
            k = min(1.0, t / 0.8) * min(1.0, (HEAD_SEC - t) / 0.6)
            c = tuple(int(v * k) for v in BONE)
            t1 = "TIERRA ALTA"
            spaced(d, ((OW - spaced_w(t1, F_TITLE, 22)) / 2, OH / 2 - 90), t1, F_TITLE, c, 22)
            t2 = "EPISODIO 1  ·  «HORA CERO»  ·  MUESTRA VISUAL"
            c2 = tuple(int(v * k) for v in DIM)
            spaced(d, ((OW - spaced_w(t2, F_SM, 6)) / 2, OH / 2 + 20), t2, F_SM, c2, 6)
        elif t >= HEAD_SEC + len(PLATES) * PLATE_SEC:
            d = ImageDraw.Draw(frame)
            k = min(1.0, (t - HEAD_SEC - len(PLATES) * PLATE_SEC) / 0.6)
            k *= min(1.0, (total - t) / 0.8)
            c = tuple(int(v * k) for v in DIM)
            t3 = "OCHO LÁMINAS  ·  EPISODIO 1  ·  TIERRA ALTA"
            spaced(d, ((OW - spaced_w(t3, F_SM, 7)) / 2, OH / 2 - 12), t3, F_SM, c, 7)
        else:
            idx = int((t - HEAD_SEC) // PLATE_SEC)
            local = (t - HEAD_SEC) - idx * PLATE_SEC
            p = local / PLATE_SEC
            _, sc, slug, rot, (z0, z1), (cxf, cyf) = PLATES[idx]
            z = z0 + (z1 - z0) * p
            cw, chh = PW * z, PH * z
            cx = cxf * PW
            cy = cyf * PH
            x0 = min(max(cx - cw / 2, 0), PW - cw)
            y0 = min(max(cy - chh / 2, 0), PH - chh)
            crop = imgs[idx].crop((int(x0), int(y0), int(x0 + cw), int(y0 + chh)))
            crop = crop.resize((OW, CH), Image.LANCZOS)
            frame.paste(crop, (0, Y0))
            # entrada y salida del plano
            fade = min(1.0, local / 0.5) * min(1.0, (PLATE_SEC - local) / 0.4)
            if fade < 0.999:
                frame = Image.blend(Image.new("RGB", (OW, OH), (0, 0, 0)), frame, fade)
            chrome(frame, slug, "%s   ·   PLANO %s" % (rot, sc),
                   min(1.0, max(0.0, (local - 0.6) / 0.6)) * fade)

        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    rc = proc.wait()
    os.remove(wav)
    if rc != 0:
        return rc
    print("\n==> listo: %s  (%.1f MB)" % (mp4, os.path.getsize(mp4) / 1e6))
    print("==> láminas en %s" % ldir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
