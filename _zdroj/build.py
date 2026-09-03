# -*- coding: utf-8 -*-
"""Sestaví HTML e-mailový podpis OFTALMED. Zdroj designu: Canva DAHUKO-ess4.
Po úpravě spustit `python build.py` — přepíše podpis.html i podpis-nahled.html."""
import io

WEB = "https://oftalmed.github.io/podpis/obrazky/"   # úložiště obrázků podpisu (GitHub Pages)

FONT = "Roboto,'Helvetica Neue',Arial,Helvetica,sans-serif"
MODRA, CERVENA, TEXT, PODKLAD = "#020873", "#880913", "#070808", "#fefefe"
RADIUS = 6          # zaoblení tlačítek a spodního pruhu (px)
PRUH_NAHRADA = "#450843"   # plná barva pod gradientem pruhu

URL_ORDINACE    = "https://my.medevio.cz/oftalmed"
URL_OPTIKY      = "https://my.medevio.cz/oftalmed-optika"
URL_WEB         = "https://oftalmed.cz"
URL_WEB_OPTIKA  = "https://oftalmed-optika.cz"
URL_CHATBOT     = "https://oftalmed-optika.cz/chatbot/"
URL_MAPA = ("https://www.google.com/maps/place/OFTALMED+OPTIKA+s.r.o./@49.2110276,16.6304261,17z/"
            "data=!3m1!4b1!4m6!3m5!1s0x471295dd34cd7b53:0xc57afb6776774aa5!8m2!3d49.2110276"
            "!4d16.633001!16s%2Fg%2F11n2v0hw4p?authuser=0&amp;entry=ttu")

TEXT_PRUH = ("Máte nějaké otázky? Zeptejte se nejdříve našeho virtuální AI asistenta, "
             "ví toho docela hodně a učí se...")

def img(base, soubor, w, h, alt, style=""):
    return (f'<img src="{base}{soubor}" width="{w}" height="{h}" alt="{alt}" '
            f'border="0" style="display:block;border:0;outline:none;text-decoration:none;'
            f'width:{w}px;height:{h}px;{style}">')

def radek(base, ikona, alt, obsah):
    """Jeden kontaktní řádek: ikonka + text."""
    return f'''
          <tr>
            <td width="18" valign="middle" style="width:18px;padding:0 8px 5px 0;">{img(base, ikona, 18, 18, alt)}</td>
            <td valign="middle" style="padding:0 0 5px 0;font-family:{FONT};font-size:11px;line-height:18px;color:{TEXT};">{obsah}</td>
          </tr>'''

def tlacitko(barva, popisek, url):
    return (f'<table role="presentation" width="64" cellpadding="0" cellspacing="0" border="0" '
            f'style="width:64px;border-collapse:separate;border-radius:{RADIUS}px;background-color:{barva};">'
            f'<tr><td align="center" bgcolor="{barva}" '
            f'style="border-radius:{RADIUS}px;padding:3px 2px;font-family:{FONT};font-size:11px;'
            f'font-weight:bold;line-height:12px;white-space:nowrap;">'
            f'<a href="{url}" style="color:#fefefe;text-decoration:none;display:block;">{popisek}</a>'
            f'</td></tr></table>')

def sestav(base):
    A = f'color:{TEXT};text-decoration:none;'          # odkaz splývající s textem
    return f'''<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;border-collapse:collapse;background-color:{PODKLAD};font-family:{FONT};color:{TEXT};">
  <tr>
    <!-- LEVÝ SLOUPEC: logo + QR -->
    <td width="168" valign="top" style="width:168px;padding:28px 12px 0 12px;">
      {img(base, 'podpis-logo.png', 144, 81, 'OFTALMED')}
      <div style="height:9px;line-height:9px;font-size:0;">&nbsp;</div>
      {img(base, 'podpis-qr.png', 144, 144, 'QR kontakt MUDr. Tomas Mnuk')}
    </td>
    <!-- SVISLÁ DĚLICÍ LINKA -->
    <td width="4" valign="top" style="width:4px;padding:84px 0 0 0;">{img(base, 'podpis-linka-v.png', 4, 176, '')}</td>
    <!-- PRAVÝ SLOUPEC -->
    <td valign="top" style="padding:84px 2px 0 8px;">
      <table role="presentation" width="418" cellpadding="0" cellspacing="0" border="0" style="width:418px;border-collapse:collapse;">
        <tr><td style="font-family:{FONT};font-size:21px;font-weight:bold;line-height:29px;color:{MODRA};">MUDr.&nbsp;Tomáš&nbsp;Mňuk</td></tr>
        <tr><td style="font-family:{FONT};font-size:17px;font-weight:bold;line-height:24px;color:{MODRA};padding-bottom:5px;">OFTALMED OPTIKA s.r.o. &amp; OFTALMED s.r.o.</td></tr>
        <tr><td style="font-size:0;line-height:0;padding-bottom:5px;">{img(base, 'podpis-linka-h.png', 418, 4, '')}</td></tr>
        <tr><td>
          <table role="presentation" width="418" cellpadding="0" cellspacing="0" border="0" style="width:418px;border-collapse:collapse;">{radek(base, 'podpis-ikona-telefon.png', 'Telefon',
              f'<a href="tel:+420736220797" style="{A}"><strong>lékař: +420 736 220 797</strong></a> (konzultace akutních potíží)')}{radek(base, 'podpis-ikona-telefon.png', 'Telefon',
              f'<a href="tel:+420530000195" style="{A}"><strong>ústředna: +420 530 000 195</strong></a> (poskytování informací, objednání do optiky)')}{radek(base, 'podpis-ikona-web.png', 'Web',
              f'<a href="{URL_WEB_OPTIKA}" style="{A}"><strong>www.OFTALMED-OPTIKA.cz</strong></a> &nbsp; &amp; &nbsp; <a href="{URL_WEB}" style="{A}"><strong>www.OFTALMED.cz</strong></a>')}{radek(base, 'podpis-ikona-adresa.png', 'Adresa',
              f'<a href="{URL_MAPA}" style="{A}"><strong>nám. Republiky 744/5, 614 00 Brno</strong></a>')}
          </table>
        </td></tr>
        <tr><td style="font-size:0;line-height:0;padding:0 0 5px 0;">{img(base, 'podpis-linka-h.png', 418, 4, '')}</td></tr>
        <tr><td>
          <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
            <tr>
              <td valign="middle" style="font-family:{FONT};font-size:11px;font-weight:bold;line-height:18px;color:{TEXT};padding-right:6px;white-space:nowrap;">Skrze systém MEDEVIO se můžete objednat do</td>
              <td valign="middle">{tlacitko(MODRA, 'ORDINACE', URL_ORDINACE)}</td>
              <td valign="middle" style="font-family:{FONT};font-size:11px;font-weight:bold;line-height:18px;color:{TEXT};padding:0 3px;white-space:nowrap;">nebo do</td>
              <td valign="middle">{tlacitko(CERVENA, 'OPTIKY', URL_OPTIKY)}</td>
            </tr>
          </table>
        </td></tr>
      </table>
    </td>
  </tr>
  <!-- SPODNÍ PRUH -->
  <tr>
    <td colspan="3" style="padding:4px 0 0 12px;">
      <table role="presentation" width="586" cellpadding="0" cellspacing="0" border="0" style="width:586px;border-collapse:collapse;">
        <tr>
          <td height="18" align="center" background="{base}podpis-pruh.png" bgcolor="{PRUH_NAHRADA}" style="height:18px;border-radius:{RADIUS}px;background-color:{PRUH_NAHRADA};background-image:url('{base}podpis-pruh.png');background-repeat:no-repeat;background-size:586px 18px;padding:0 8px;font-family:{FONT};font-size:10px;font-weight:bold;line-height:18px;color:#ffffff;white-space:nowrap;">
            <a href="{URL_CHATBOT}" style="color:#ffffff;text-decoration:none;">{TEXT_PRUH}</a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>'''

HLAVICKA = ('<!DOCTYPE html><html lang="cs"><head><meta charset="utf-8">'
            '<title>Podpis OFTALMED</title></head>'
            '<body style="margin:0;padding:24px;background:#ffffff;">')

# index.html = totéž co podpis.html; díky němu jde podpis zkopírovat rovnou
# z https://oftalmed.github.io/podpis/ bez otevírání lokálního souboru
for jmeno, base in (('podpis.html', WEB), ('index.html', WEB), ('podpis-nahled.html', 'assets/')):
    with io.open(jmeno, 'w', encoding='utf-8') as f:
        f.write(HLAVICKA + sestav(base) + '</body></html>')
    print('zapsano:', jmeno)
