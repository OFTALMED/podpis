# Podpisy OFTALMED

E-mailové podpisy pro tým OFTALMED s.r.o. & OFTALMED OPTIKA s.r.o. a obrázky, ze kterých
se skládají. Repozitář zároveň slouží jako **hosting těch obrázků** přes GitHub Pages —
podpisy se na ně odkazují přes `https://`, takže přežijí i odpověď z Outlooku.

## Podpisy

Otevřít, `Ctrl+A`, `Ctrl+C` a vložit v Gmailu do *Nastavení → Obecné → Podpis*.

| Kdo | Adresa |
|---|---|
| Rozcestník | https://oftalmed.github.io/podpis/ |
| MUDr. Tomáš Mňuk | https://oftalmed.github.io/podpis/mnuk/ |
| Bc. Nina Šutáková | https://oftalmed.github.io/podpis/sutakova/ |
| Viktor Wildner, DiS. | https://oftalmed.github.io/podpis/wildner/ |
| Viktor Wildner, DiS. (druhé číslo) | https://oftalmed.github.io/podpis/wildner-2/ |
| Virtuální asistent | https://oftalmed.github.io/podpis/asistent/ |

## Proč to takhle je

Předchozí podpis nesl obrázky jako vložené přílohy (`cid:`). Při prvním odeslání to
funguje, ale jakmile příjemce odpověděl z Outlooku, Outlook všechny přílohy zahodil
a nahradil je jedním zástupným souborem — z podpisu zbyla sada prázdných rámečků.
Obrázky na veřejné `https://` adrese tenhle problém nemají: každý klient si je stáhne
znovu, kolikrát se na e-mail odpoví.

## Co je kde

| Cesta | Co to je |
|---|---|
| `<slug>/index.html` | jeden hotový podpis (generovaný) |
| `index.html` | rozcestník se všemi podpisy (generovaný) |
| `nahled.png` | jak mají všechny vypadat |
| `obrazky/` | obrázky podpisů, publikované přes GitHub Pages |
| `_zdroj/build.py` | generátor podpisů — **zdroj pravdy, edituje se tohle** |
| `_zdroj/gradienty.py` | generátor linek a spodního pruhu |
| `_zdroj/navrh-canva-6x.png` | výchozí grafický návrh (Canva `DAF3o89v8Jo`) |

Obrázky jsou uložené ve dvojnásobném rozlišení kvůli retina displejům; podpisy je
zmenšují atributy `width`/`height`.

## QR kódy

Každý podpis má **vlastní soubor** `obrazky/podpis-qr-<slug>.png`. Předlohy jsou vektorové
SVG v `_zdroj/qr/` — z nich se PNG renderuje, needituje se rastr.

| Podpis | Osobní číslo | Předloha |
|---|---|---|
| `mnuk` | 736 220 797 | `_zdroj/qr/mnuk.svg` |
| `sutakova` | 731 875 187 | `_zdroj/qr/sutakova.svg` |
| `wildner` | 734 608 608 | `_zdroj/qr/wildner.svg` (vizitka optika) |
| `wildner-2` | 737 916 707 | `_zdroj/qr/wildner-2.svg` (vizitka osobní) |
| `asistent` | — | `_zdroj/qr/asistent.svg` |

Protože má každý podpis vlastní název souboru, **výměna QR znamená přepsat jeden obrázek** —
HTML se nemění a nikdo nemusí podpis znovu vkládat do Gmailu.

### Převod SVG → PNG

Podpisy potřebují PNG; SVG e-mailoví klienti nevykreslí (Gmail ho odstraní, Outlook neumí).
Renderuje se přes headless Chrome na 288 × 288 px (dvojnásobek zobrazených 144) s podkladem
`#fefefe`:

```bash
printf '%s' '<!doctype html><meta charset="utf-8"><body style="margin:0;background:#fefefe">
<img src="mnuk.svg" width="288" height="288"></body>' > mnuk.html
chrome --headless=new --disable-gpu --force-device-scale-factor=1 --window-size=288,288        --screenshot=podpis-qr-mnuk.png mnuk.html
```

`obrazky/podpis-qr.png` je starý název Mňukova QR, držený kvůli podpisu vloženému do Gmailu
před zavedením per-osobních názvů. Obsahuje totéž co `podpis-qr-mnuk.png`. Až budou všechny
podpisy nasazené z aktuálních adres, může se smazat.

### Hustota kódů — ověřeno

QR nesou celou vizitku (vCard, ~300 znaků) při chybové korekci H, což dělá ~76–86 modulů
na stranu (Šutáková ~52). Na 144 px v podpisu to vychází jen ~1,8 px na modul, což vypadá
málo — **v praxi se ale všech pět kódů mobilem z monitoru načte** (ověřeno 4. 9. 2026).

Měřeno dekodérem jsQR na renderech: tvar modulů (tečky × plné čtverečky × obdélníky)
ani počet modulů **neměl na čitelnost měřitelný vliv** — všechny varianty snesly stejné
rozmazání. Takže tečkovaný styl není potřeba měnit.

Kdyby se čitelnost někdy zhoršila (menší zobrazení, tisk, horší monitor), pořadí zásahů
podle očekávaného účinku je: krátká URL místo celé vCard → korekce M místo H → plné
čtverečky místo teček. Zvyšovat rozlišení exportu nemá smysl, limit je hustota modulů.

Otestovat kódy jde kdykoli na **https://oftalmed.github.io/podpis/test/** — jsou tam
v přesné velikosti, jakou mají v podpisu.

## Úprava podpisů

```bash
python _zdroj/assety.py    # vyrenderuje obrázky v rozlišení podle měřítka
python _zdroj/build.py     # přepíše všechny podpisy, rozcestník i testovací stránku
```

Skripty se spouštějí z kořene repozitáře.

- **Lidé, čísla a role** — seznam `LIDE` na začátku `build.py`.
- **Texty spodního pruhu** — `TEXT_PRUH` a `TEXT_PRUH_ASISTENT` tamtéž.
- **Adresa úložiště obrázků** — konstanta `WEB` (lze přebít proměnnou prostředí).

### Velikost podpisu

Řídí ji **jediné číslo** — `MERITKO` v `rozmery.py`, které sdílí `build.py` i `assety.py`,
aby se rozměry HTML a rozlišení obrázků nemohly rozejít. `1.0` = 600 px podle původního
návrhu z Canvy, **nasazeno je `1.15`** = 689 px, text 13 px, QR 166 px.

Po změně měřítka je nutné spustit **obě** dávky — jinak by obrázky měly rozlišení
neodpovídající HTML a byly by rozmazané:

```bash
MERITKO=1.25 python _zdroj/assety.py && MERITKO=1.25 python _zdroj/build.py
```

Nad ~700 px pozor: v užším čtecím podokně (rozdělené okno Outlooku) si klient podpis
zmenší nebo přidá vodorovné posouvání. Řádek „Skrze systém MEDEVIO…" a text spodního
pruhu se **nezalamují**, takže při zvětšování je hlídej — při 1.15 zabírají 482 z 481 px,
resp. 597 z 675 px.

## Kontrola po nasazení

V odeslané zprávě **nesmí být ikona sponky** (sponka = obrázky se zase posílají jako
přílohy) a po odpovědi z Outlooku musí obrázky pořád držet.

## Pravidla, která se tu nesmí porušit

0. **Telefonní čísla nejsou odkazy.** `tel:` na počítači vyvolá dialog „Otevřít aplikaci?",
   a přes počítač skoro nikdo nevolá. Mobilní klienti si čísla rozpoznají a udělají
   ťukatelná sami, takže se tím nic neztrácí.
1. Obrázky jen přes `https://`, nikdy `cid:` ani `data:`.
2. Adresa vždy končí `.png` — nikdy varianta `.png.webp` (Outlook WebP neumí).
3. Text zůstává textem, nikdy se nevykresluje do obrázku.
4. Barevná tlačítka jsou buňky tabulky, ne obrázky — přežijí vypnuté načítání obrázků.
5. Layout výhradně tabulkami, šířka 600 px. Flexbox ani grid v e-mailu neexistují.
6. Každý `<img>` má `width` a `height` jako HTML atribut a `border="0"`.
