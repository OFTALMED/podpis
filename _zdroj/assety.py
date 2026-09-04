# -*- coding: utf-8 -*-
"""Vyrenderuje všechny obrázky podpisu v rozlišení odpovídajícím aktuálnímu měřítku.

Všechno se ukládá ve **dvojnásobku** zobrazené velikosti kvůli retina displejům.
Zdroje: `_zdroj/navrh-canva-6x.png` (logo a ikonky) a `qr-svg/*.svg` (QR kódy).

Spouštět z kořene projektu:  python assety.py
Měřítko se bere z rozmery.py (proměnná prostředí MERITKO).
"""
import io, os, subprocess, tempfile
from PIL import Image, ImageDraw

from rozmery import (MERITKO, OBR, LOGO_H, IKONA, PRAVY, LINKA_H_V,
                     DIV, LINKA_V_H, PRUH_W, PRUH_H, RADIUS)

CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
NAVRH = '_zdroj/navrh-canva-6x.png'      # export Canvy v 6× rozlišení
CIL = 'obrazky'
PODKLAD = (254, 254, 254)                 # #fefefe, stejný jako podklad podpisu

# výřezy v souřadnicích návrhu (plátno 400 × 200 px), násobí se 6× kvůli exportu
VYREZY = {
    'podpis-logo.png':          (7.815535, 18.494744, 95.638324, 53.796557),
    'podpis-ikona-telefon.png': (119.595556, 98.070372, 12.266812, 12.266812),
    'podpis-ikona-web.png':     (119.545532, 128.603996, 12.366860, 12.366860),
    'podpis-ikona-adresa.png':  (119.595556, 143.970856, 12.408509, 12.408509),
}

LIDE = ('mnuk', 'sutakova', 'wildner', 'wildner-2', 'asistent')

# stopy gradientů odečtené z návrhu
LINKA = [(0.0, (2, 8, 115)), (1/3, (198, 222, 241)), (2/3, (246, 201, 182)), (1.0, (136, 9, 19))]
PRUH = [(0.0, (2, 8, 115)), (1.0, (136, 9, 19))]


def vyrez(zdroj, souradnice, sirka, vyska, nazev):
    l, t, w, h = souradnice
    box = (round(l * 6), round(t * 6), round((l + w) * 6), round((t + h) * 6))
    im = zdroj.crop(box).resize((sirka * 2, vyska * 2), Image.LANCZOS)
    im.save(os.path.join(CIL, nazev), optimize=True)
    return sirka, vyska


def qr_z_vektoru(svg, sirka, nazev):
    """QR se renderuje z vektoru, ne přeškálováním rastru — hrany modulů zůstanou ostré."""
    px = sirka * 2
    with tempfile.TemporaryDirectory() as tmp:
        html = os.path.join(tmp, 'q.html')
        io.open(html, 'w', encoding='utf-8').write(
            '<!doctype html><meta charset="utf-8"><body style="margin:0;background:#fefefe">'
            '<img src="' + os.path.abspath(svg).replace('\\', '/') + '" '
            'width="' + str(px) + '" height="' + str(px) + '"></body>')
        out = os.path.join(tmp, 'q.png')
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--allow-file-access-from-files',
                        '--force-device-scale-factor=1', '--window-size=%d,%d' % (px, px),
                        '--virtual-time-budget=6000', '--screenshot=' + out,
                        'file:///' + html.replace('\\', '/')],
                       capture_output=True)
        Image.open(out).convert('RGB').quantize(colors=96, dither=Image.Dither.NONE) \
            .save(os.path.join(CIL, nazev), optimize=True)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def prubeh(stopy, n):
    out = []
    for i in range(n):
        q = i / (n - 1) if n > 1 else 0
        for j in range(len(stopy) - 1):
            p0, c0 = stopy[j]
            p1, c1 = stopy[j + 1]
            if p0 <= q <= p1:
                out.append(lerp(c0, c1, (q - p0) / (p1 - p0) if p1 > p0 else 0))
                break
        else:
            out.append(stopy[-1][1])
    return out


def gradient(stopy, w, h, svisly=False):
    px = prubeh(stopy, h if svisly else w)
    img = Image.new('RGB', (w, h))
    d = ImageDraw.Draw(img)
    for i, c in enumerate(px):
        d.line([(0, i), (w - 1, i)] if svisly else [(i, 0), (i, h - 1)], fill=c)
    return img


def zaoblit(img, r):
    """Zaoblení se zapéká do obrázku — Outlook CSS border-radius ignoruje."""
    maska = Image.new('L', img.size, 0)
    ImageDraw.Draw(maska).rounded_rectangle([0, 0, img.size[0] - 1, img.size[1] - 1],
                                            radius=r, fill=255)
    out = Image.new('RGB', img.size, PODKLAD)
    out.paste(img, (0, 0), maska)
    return out


if __name__ == '__main__':
    os.makedirs(CIL, exist_ok=True)
    navrh = Image.open(NAVRH).convert('RGB')
    print('meritko %.2f -> podpis %d px, QR a logo %d px, ikony %d px'
          % (MERITKO, PRUH_W + 14, OBR, IKONA))

    vyrez(navrh, VYREZY['podpis-logo.png'], OBR, LOGO_H, 'podpis-logo.png')
    for n in ('podpis-ikona-telefon.png', 'podpis-ikona-web.png', 'podpis-ikona-adresa.png'):
        vyrez(navrh, VYREZY[n], IKONA, IKONA, n)

    for slug in LIDE:
        qr_z_vektoru('qr-svg/%s.svg' % slug, OBR, 'podpis-qr-%s.png' % slug)
    # starý název drží Mňukův kód kvůli podpisu vloženému do Gmailu dřív
    Image.open(os.path.join(CIL, 'podpis-qr-mnuk.png')).save(
        os.path.join(CIL, 'podpis-qr.png'), optimize=True)

    gradient(LINKA, PRAVY * 2, LINKA_H_V * 2).save(
        os.path.join(CIL, 'podpis-linka-h.png'), optimize=True)
    gradient(LINKA, DIV * 2, LINKA_V_H * 2, svisly=True).save(
        os.path.join(CIL, 'podpis-linka-v.png'), optimize=True)
    zaoblit(gradient(PRUH, PRUH_W * 2, PRUH_H * 2), RADIUS * 2).save(
        os.path.join(CIL, 'podpis-pruh.png'), optimize=True)

    celkem = sum(os.path.getsize(os.path.join(CIL, f)) for f in os.listdir(CIL))
    print('hotovo: %d souboru, %.0f kB' % (len(os.listdir(CIL)), celkem / 1024))
