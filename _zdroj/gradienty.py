# -*- coding: utf-8 -*-
"""Vygeneruje gradientní prvky podpisu ze stopů odečtených z Canva návrhu DAHUKO-ess4."""
from PIL import Image, ImageDraw

PODKLAD = (254, 254, 254)
LINKA = [(0.0,(2,8,115)), (1/3,(198,222,241)), (2/3,(246,201,182)), (1.0,(136,9,19))]
PRUH  = [(0.0,(2,8,115)), (1.0,(136,9,19))]

def lerp(a, b, t): return tuple(round(a[i] + (b[i]-a[i])*t) for i in range(3))

def prubeh(stops, n):
    out = []
    for i in range(n):
        p = i/(n-1) if n > 1 else 0
        for j in range(len(stops)-1):
            p0, c0 = stops[j]; p1, c1 = stops[j+1]
            if p0 <= p <= p1:
                out.append(lerp(c0, c1, (p-p0)/(p1-p0) if p1 > p0 else 0)); break
        else:
            out.append(stops[-1][1])
    return out

def gradient(stops, w, h, svisly=False):
    px = prubeh(stops, h if svisly else w)
    img = Image.new('RGB', (w, h))
    d = ImageDraw.Draw(img)
    for i, c in enumerate(px):
        d.line([(0, i), (w-1, i)] if svisly else [(i, 0), (i, h-1)], fill=c)
    return img

def zaoblit(img, r, pozadi):
    """Zapeče zaoblené rohy do obrázku — drží i tam, kde se CSS border-radius ignoruje."""
    maska = Image.new('L', img.size, 0)
    ImageDraw.Draw(maska).rounded_rectangle([0, 0, img.size[0]-1, img.size[1]-1], radius=r, fill=255)
    out = Image.new('RGB', img.size, pozadi)
    out.paste(img, (0, 0), maska)
    return out

gradient(LINKA, 836, 8).save('assets/podpis-linka-h.png', optimize=True)
gradient(LINKA, 8, 352, svisly=True).save('assets/podpis-linka-v.png', optimize=True)
zaoblit(gradient(PRUH, 1172, 36), 12, PODKLAD).save('assets/podpis-pruh.png', optimize=True)
print('linka-h  418x4   (soubor 836x8)')
print('linka-v  4x176   (soubor 8x352)')
print('pruh     586x18  (soubor 1172x36, rohy zaobleny r=6)')
