# -*- coding: utf-8 -*-
"""Generátor e-mailových podpisů OFTALMED.

Zdroj designu: Canva `DAF3o89v8Jo` (5 stran = 5 lidí), odkazy z novější kopie `DAHUKO-ess4`.
Spuštění `python build.py` přepíše všechny podpisy, náhledy i rozcestník.
"""
import io, os

WEB = os.environ.get('WEB', "https://oftalmed.github.io/podpis/obrazky/")  # úložiště obrázků

from rozmery import *   # MERITKO a všechny odvozené rozměry


FONT = "Roboto,'Helvetica Neue',Arial,Helvetica,sans-serif"
MODRA, CERVENA, TEXT, PODKLAD = "#020873", "#880913", "#070808", "#fefefe"
PRUH_NAHRADA = "#450843"   # plná barva pod gradientem pruhu

URL_ORDINACE   = "https://my.medevio.cz/oftalmed"
URL_OPTIKY     = "https://my.medevio.cz/oftalmed-optika"
URL_WEB        = "https://oftalmed.cz"
URL_WEB_OPTIKA = "https://oftalmed-optika.cz"
URL_CHATBOT    = "https://oftalmed-optika.cz/chatbot/"
URL_MAPA = ("https://www.google.com/maps/place/OFTALMED+OPTIKA+s.r.o./@49.2110276,16.6304261,17z/"
            "data=!3m1!4b1!4m6!3m5!1s0x471295dd34cd7b53:0xc57afb6776774aa5!8m2!3d49.2110276"
            "!4d16.633001!16s%2Fg%2F11n2v0hw4p?authuser=0&amp;entry=ttu")

TEXT_PRUH = ("Máte nějaké otázky? Zeptejte se nejdříve našeho virtuálního AI asistenta, "
             "ví toho docela hodně a pořád se učí...")

# Očko mluví ve vlastním podpisu v první osobě
TEXT_PRUH_ASISTENT = ("Máte nějaké otázky? Zeptejte se nejdříve mě, virtuálního AI asistenta, "
                      "vím toho docela hodně a pořád se učím...")

# slug, jméno, (popisek osobního čísla, číslo, poznámka v závorce) nebo None
#
# QR kód se odvozuje ze slugu: obrazky/podpis-qr-<slug>.png. Každý podpis má vlastní
# soubor i tam, kde je obrázek zatím shodný s jiným — výměna QR pak znamená přepsat
# jeden obrázek, HTML se nemění a podpis se nemusí znovu vkládat do Gmailu.
#
# Předlohy QR jsou vektorové SVG v _zdroj/qr/, PNG se z nich renderuje (postup v README).
# Wildner má dva podpisy: `wildner` = vizitka optika (734 608 608),
# `wildner-2` = vizitka osobní (737 916 707).
LIDE = [
    ("mnuk",      "MUDr. Tomáš Mňuk",     ("lékař",        "+420 736 220 797", "(konzultace akutních potíží)")),
    ("sutakova",  "Bc. Nina Šutáková",    ("optometrista", "+420 731 875 187", "(konzultace, objednávání)")),
    ("wildner",   "Viktor Wildner, DiS.", ("optik",        "+420 734 608 608", "(vyřizování zakázek, objednávání)")),
    ("wildner-2", "Viktor Wildner, DiS.", ("optik",        "+420 737 916 707", "")),
    ("asistent",  "Očko – virtuální asistent", None),
]

ODKAZ_V_TEXTU = "color:" + TEXT + ";text-decoration:none;"


def img(base, soubor, w, h, alt):
    return ('<img src="' + base + soubor + '" width="' + str(w) + '" height="' + str(h) +
            '" alt="' + alt + '" border="0" style="display:block;border:0;outline:none;'
            'text-decoration:none;width:' + str(w) + 'px;height:' + str(h) + 'px;">')


def radek(base, ikona, alt, obsah):
    return ('\n          <tr>'
            '\n            <td width="' + str(IKONA) + '" valign="middle" style="width:' + str(IKONA) + 'px;padding:0 ' + str(IKONA_PAD) + 'px ' + str(RADEK_PAD) + 'px 0;">'
            + img(base, ikona, IKONA, IKONA, alt) + '</td>'
            '\n            <td valign="middle" style="padding:0 0 ' + str(RADEK_PAD) + 'px 0;font-family:' + FONT +
            ';font-size:' + str(TEXT_F) + 'px;line-height:' + str(TEXT_LH) + 'px;color:' + TEXT + ';">' + obsah + '</td>'
            '\n          </tr>')


def prazdny_radek():
    """Virtuální asistent nemá osobní číslo. Slot zůstává prázdný, aby zbylé řádky
    i dělicí linky seděly na stejných místech jako u ostatních podpisů."""
    return ('\n          <tr><td colspan="2" height="' + str(IKONA + RADEK_PAD) + '" '
            'style="height:' + str(IKONA + RADEK_PAD) + 'px;font-size:0;line-height:0;">&nbsp;</td></tr>')


def tlacitko(barva, popisek, url):
    return ('<table role="presentation" width="' + str(BTN_W) + '" cellpadding="0" cellspacing="0" '
            'border="0" style="width:' + str(BTN_W) + 'px;border-collapse:separate;border-radius:'
            + str(RADIUS) + 'px;background-color:' + barva + ';">'
            '<tr><td align="center" bgcolor="' + barva + '" style="border-radius:' + str(RADIUS) +
            'px;padding:' + str(BTN_PAD_V) + 'px ' + str(BTN_PAD_H) + 'px;font-family:' + FONT +
            ';font-size:' + str(BTN_F) + 'px;font-weight:bold;'
            'line-height:' + str(BTN_LH) + 'px;white-space:nowrap;">'
            '<a href="' + url + '" style="color:#fefefe;text-decoration:none;display:block;">'
            + popisek + '</a></td></tr></table>')


SABLONA = """<table role="presentation" width="{CELKEM}" cellpadding="0" cellspacing="0" border="0" style="width:{CELKEM}px;max-width:{CELKEM}px;border-collapse:collapse;background-color:{PODKLAD};font-family:{FONT};color:{TEXT};">
  <tr>
    <!-- LEVY SLOUPEC: logo + QR -->
    <td width="{LEVY}" valign="top" style="width:{LEVY}px;padding:{LEVY_TOP}px {PAD_L}px 0 {PAD_L}px;">
      {LOGO}
      <div style="height:{MEZERA}px;line-height:{MEZERA}px;font-size:0;">&nbsp;</div>
      {QR}
    </td>
    <!-- SVISLA DELICI LINKA -->
    <td width="{DIV}" valign="top" style="width:{DIV}px;padding:{DIV_TOP}px 0 0 0;">{LINKA_V}</td>
    <!-- PRAVY SLOUPEC -->
    <td valign="top" style="padding:{DIV_TOP}px {PRAVY_PAD_R}px 0 {PRAVY_PAD_L}px;">
      <table role="presentation" width="{PRAVY}" cellpadding="0" cellspacing="0" border="0" style="width:{PRAVY}px;border-collapse:collapse;">
        <tr><td style="font-family:{FONT};font-size:{JMENO_F}px;font-weight:bold;line-height:{JMENO_LH}px;color:{MODRA};white-space:nowrap;">{JMENO}</td></tr>
        <tr><td style="font-family:{FONT};font-size:{FIRMA_F}px;font-weight:bold;line-height:{FIRMA_LH}px;color:{MODRA};padding-bottom:{RADEK_PAD}px;">OFTALMED OPTIKA s.r.o. &amp; OFTALMED s.r.o.</td></tr>
        <tr><td style="font-size:0;line-height:0;padding-bottom:{RADEK_PAD}px;">{LINKA_H}</td></tr>
        <tr><td>
          <table role="presentation" width="{PRAVY}" cellpadding="0" cellspacing="0" border="0" style="width:{PRAVY}px;border-collapse:collapse;">{RADKY}
          </table>
        </td></tr>
        <tr><td style="font-size:0;line-height:0;padding:0 0 {RADEK_PAD}px 0;">{LINKA_H}</td></tr>
        <tr><td>
          <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
            <tr>
              <td valign="middle" style="font-family:{FONT};font-size:{TEXT_F}px;font-weight:bold;line-height:{TEXT_LH}px;color:{TEXT};padding-right:{MEZ_LABEL}px;white-space:nowrap;">Skrze systém MEDEVIO se můžete objednat do</td>
              <td valign="middle">{BTN_ORD}</td>
              <td valign="middle" style="font-family:{FONT};font-size:{TEXT_F}px;font-weight:bold;line-height:{TEXT_LH}px;color:{TEXT};padding:0 {MEZ_TL}px;white-space:nowrap;">nebo do</td>
              <td valign="middle">{BTN_OPT}</td>
            </tr>
          </table>
        </td></tr>
      </table>
    </td>
  </tr>
  <!-- SPODNI PRUH -->
  <tr>
    <td colspan="3" style="padding:{PRUH_TOP}px 0 0 {PAD_L}px;">
      <table role="presentation" width="{PRUH_W}" cellpadding="0" cellspacing="0" border="0" style="width:{PRUH_W}px;border-collapse:collapse;">
        <tr>
          <td height="{PRUH_H}" align="center" background="{PRUH_URL}" bgcolor="{PRUH_NAHRADA}" style="height:{PRUH_H}px;border-radius:{RADIUS}px;background-color:{PRUH_NAHRADA};background-image:url({PRUH_CSS});background-repeat:no-repeat;background-size:{PRUH_W}px {PRUH_H}px;padding:0 {PRUH_PAD}px;font-family:{FONT};font-size:{PRUH_F}px;font-weight:bold;line-height:{PRUH_H}px;color:#ffffff;white-space:nowrap;">
            <a href="{URL_CHATBOT}" style="color:#ffffff;text-decoration:none;">{TEXT_PRUH}</a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>"""


def sestav(base, jmeno, osobni, qr, pruh=TEXT_PRUH):
    A = ODKAZ_V_TEXTU
    if osobni:
        popis, cislo, pozn = osobni
        # Bez odkazu tel: - na počítači vyvolává dialog "Otevřít aplikaci?".
        # Mobilní klienti si čísla stejně rozpoznají a udělají ťukatelná sami.
        obsah = '<strong>' + popis + ': ' + cislo + '</strong>'
        if pozn:
            obsah += ' ' + pozn
        prvni = radek(base, 'podpis-ikona-telefon.png', 'Telefon', obsah)
    else:
        prvni = prazdny_radek()

    radky = (prvni
        + radek(base, 'podpis-ikona-telefon.png', 'Telefon',
                '<strong>ústředna: +420 530 000 195</strong>'
                ' (poskytování informací, objednání do optiky)')
        + radek(base, 'podpis-ikona-web.png', 'Web',
                '<a href="' + URL_WEB_OPTIKA + '" style="' + A + '"><strong>www.OFTALMED-OPTIKA.cz'
                '</strong></a> &nbsp; &amp; &nbsp; <a href="' + URL_WEB + '" style="' + A + '">'
                '<strong>www.OFTALMED.cz</strong></a>')
        + radek(base, 'podpis-ikona-adresa.png', 'Adresa',
                '<a href="' + URL_MAPA + '" style="' + A + '">'
                '<strong>nám. Republiky 744/5, 614 00 Brno</strong></a>'))

    return SABLONA.format(
        PODKLAD=PODKLAD, FONT=FONT, TEXT=TEXT, MODRA=MODRA, RADIUS=RADIUS,
        PRUH_NAHRADA=PRUH_NAHRADA, URL_CHATBOT=URL_CHATBOT, TEXT_PRUH=pruh,
        JMENO=jmeno, RADKY=radky,
        CELKEM=CELKEM, LEVY=LEVY, PAD_L=PAD_L, LEVY_TOP=LEVY_TOP, MEZERA=MEZERA,
        DIV=DIV, DIV_TOP=DIV_TOP, PRAVY=PRAVY, PRAVY_PAD_L=PRAVY_PAD_L, PRAVY_PAD_R=PRAVY_PAD_R,
        JMENO_F=JMENO_F, JMENO_LH=JMENO_LH, FIRMA_F=FIRMA_F, FIRMA_LH=FIRMA_LH,
        TEXT_F=TEXT_F, TEXT_LH=TEXT_LH, RADEK_PAD=RADEK_PAD,
        MEZ_TL=MEZ_TL, MEZ_LABEL=MEZ_LABEL,
        PRUH_W=PRUH_W, PRUH_H=PRUH_H, PRUH_F=PRUH_F, PRUH_PAD=PRUH_PAD, PRUH_TOP=PRUH_TOP,
        LOGO=img(base, 'podpis-logo.png', OBR, LOGO_H, 'OFTALMED'),
        QR=img(base, qr, OBR, OBR, 'QR kontakt ' + jmeno),
        LINKA_V=img(base, 'podpis-linka-v.png', DIV, LINKA_V_H, ''),
        LINKA_H=img(base, 'podpis-linka-h.png', PRAVY, LINKA_H_V, ''),
        BTN_ORD=tlacitko(MODRA, 'ORDINACE', URL_ORDINACE),
        BTN_OPT=tlacitko(CERVENA, 'OPTIKY', URL_OPTIKY),
        PRUH_URL=base + 'podpis-pruh.png',
        PRUH_CSS="'" + base + "podpis-pruh.png'")


def stranka(telo, titulek):
    return ('<!DOCTYPE html><html lang="cs"><head><meta charset="utf-8">'
            '<title>' + titulek + '</title></head>'
            '<body style="margin:0;padding:24px;background:#ffffff;">' + telo + '</body></html>')


def zapis(cesta, obsah):
    adresar = os.path.dirname(cesta)
    if adresar:
        os.makedirs(adresar, exist_ok=True)
    with io.open(cesta, 'w', encoding='utf-8') as f:
        f.write(obsah)


for slug, jmeno, osobni in LIDE:
    # každý podpis má vlastní adresu https://oftalmed.github.io/podpis/<slug>/
    # Obrázky se tahají z WEB, takže soubor vypadá stejně otevřený lokálně i z Pages —
    # samostatná náhledová verze s relativními cestami už neexistuje, jen mátla.
    qr = 'podpis-qr-' + slug + '.png'
    pruh = TEXT_PRUH_ASISTENT if slug == 'asistent' else TEXT_PRUH
    zapis(slug + '/index.html',
          stranka(sestav(WEB, jmeno, osobni, qr, pruh), 'Podpis - ' + jmeno))
    print('{:11s} {}'.format(slug, jmeno))

polozky = '\n'.join(
    '        <li style="margin:0 0 10px 0;"><a href="' + slug + '/" '
    'style="color:' + MODRA + ';font-weight:bold;text-decoration:none;">' + jmeno + '</a></li>'
    for slug, jmeno, _ in LIDE)

# testovaci stranka: vsechny QR presne v te velikosti, jakou maji v podpisu (144 px),
# aby sly vyzkouset mobilem z monitoru na jeden zatah
dlazdice = '\n'.join(
    '  <div style="display:inline-block;margin:0 18px 18px 0;text-align:center;vertical-align:top;">'
    + img(WEB, 'podpis-qr-' + slug + '.png', OBR, OBR, 'QR ' + jmeno).replace('display:block', 'display:inline-block')
    + '<div style="font-family:' + FONT + ';font-size:12px;color:' + TEXT + ';margin-top:6px;">'
    + jmeno + '</div>'
    # cislo odlisi dva podpisy stejneho jmena
    + '<div style="font-family:' + FONT + ';font-size:11px;color:#666;">'
    + (osobni[1] if osobni else 'bez osobního čísla') + '</div></div>'
    for slug, jmeno, osobni in LIDE)

zapis('test/index.html', stranka(
    '<div style="font-family:' + FONT + ';color:' + TEXT + ';max-width:840px;">'
    '<h1 style="font-size:21px;color:' + MODRA + ';margin:0 0 4px 0;">Test QR kódů</h1>'
    '<p style="font-size:13px;line-height:20px;margin:0 0 6px 0;">Každý kód je tu <strong>přesně '
    'tak velký jako v podpisu</strong> (' + str(OBR) + ' px). Zkus je načíst mobilem z monitoru.</p>'
    '<p style="font-size:13px;line-height:20px;margin:0 0 20px 0;color:#666;">Aby test platil, '
    'musí mít prohlížeč zoom na 100 % (<strong>Ctrl+0</strong>). Windows si navíc obraz zvětšuje '
    'vlastním škálováním displeje — na jiném monitoru vyjde kód fyzicky jinak velký.</p>'
    + dlazdice + '</div>', 'Test QR kódů'))
print('test/index.html (QR ve skutecne velikosti) hotov')

zapis('index.html', stranka(
    '<div style="font-family:' + FONT + ';max-width:600px;color:' + TEXT + ';">'
    '<h1 style="font-size:21px;color:' + MODRA + ';margin:0 0 4px 0;">E-mailové podpisy OFTALMED</h1>'
    '<p style="font-size:13px;line-height:20px;margin:0 0 16px 0;">Otevři svůj podpis, '
    '<strong>Ctrl+A</strong>, <strong>Ctrl+C</strong> a vlož ho v Gmailu do '
    '<em>Nastavení &rarr; Obecné &rarr; Podpis</em>.</p>'
    '<ul style="font-size:15px;line-height:22px;padding-left:20px;margin:0;">\n'
    + polozky +
    '\n      </ul></div>', 'E-mailové podpisy OFTALMED'))
print('\nindex.html (rozcestnik) hotov')
