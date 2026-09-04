# -*- coding: utf-8 -*-
"""Rozměry podpisu odvozené z jednoho měřítka.

Sdílí je `build.py` (staví HTML) i `assety.py` (renderuje obrázky), aby se nemohly
rozejít — obrázek v jiném rozlišení než počítá HTML by byl rozmazaný.
"""
import os

RADIUS_ZAKLAD = 6          # zaoblení tlačítek a pruhu při měřítku 1.0

# Velikost podpisu se řídí jediným číslem. 1.0 = 600 px na šířku (výchozí návrh z Canvy),
# 1.2 = 720 px. Mění se tím rozměry i velikost písma; po změně je nutné přegenerovat
# obrázky (`python assety.py`), protože se mění i jejich rozlišení.
MERITKO = float(os.environ.get('MERITKO', '1.15'))

def p(x):
    """Přepočte rozměr z výchozího návrhu na aktuální měřítko."""
    return int(round(x * MERITKO))

PAD_L, OBR, LOGO_H = p(12), p(144), p(81)          # okraj, šířka loga i QR, výška loga
DIV, PRAVY = p(4), p(418)                          # dělicí linka, pravý sloupec
PRAVY_PAD_L, PRAVY_PAD_R = p(8), p(2)
LEVY = 2 * PAD_L + OBR                             # ať sedí součet, ne zaokrouhlení
CELKEM = LEVY + DIV + PRAVY_PAD_L + PRAVY + PRAVY_PAD_R
PRUH_W = CELKEM - PAD_L - PRAVY_PAD_R
LEVY_TOP, DIV_TOP, MEZERA, LINKA_V_H = p(28), p(84), p(9), p(176)
JMENO_F, JMENO_LH, FIRMA_F, FIRMA_LH = p(21), p(29), p(17), p(24)
TEXT_F, TEXT_LH, IKONA, IKONA_PAD, RADEK_PAD = p(11), p(18), p(18), p(8), p(5)
BTN_W, BTN_F, BTN_LH, BTN_PAD_V, BTN_PAD_H = p(64), p(11), p(12), p(3), p(2)
PRUH_H, PRUH_F, PRUH_PAD, PRUH_TOP = p(18), p(10), p(8), p(4)
MEZ_TL, MEZ_LABEL, LINKA_H_V = p(3), p(6), p(4)
RADIUS = p(RADIUS_ZAKLAD)
