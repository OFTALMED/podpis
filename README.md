# Podpis OFTALMED

E-mailový podpis MUDr. Tomáše Mňuka (OFTALMED s.r.o. & OFTALMED OPTIKA s.r.o.)
a obrázky, ze kterých se skládá. Repozitář zároveň slouží jako **hosting těch obrázků**
přes GitHub Pages — podpis se na ně odkazuje přes `https://`, takže přežije i odpověď
z Outlooku.

## Proč to takhle je

Předchozí podpis nesl obrázky jako vložené přílohy (`cid:`). Při prvním odeslání to
funguje, ale jakmile příjemce odpověděl z Outlooku, Outlook všechny přílohy zahodil
a nahradil je jedním zástupným souborem — z podpisu zbyla sada prázdných rámečků.
Obrázky na veřejné `https://` adrese tenhle problém nemají: každý klient si je stáhne
znovu, kolikrát se na e-mail odpoví.

## Co je kde

| Cesta | Co to je |
|---|---|
| `podpis.html` | hotový podpis k vložení do Gmailu |
| `nahled.png` | jak má výsledek vypadat |
| `obrazky/` | 8 obrázků podpisu, publikovaných přes GitHub Pages |
| `_zdroj/build.py` | generátor `podpis.html` — **zdroj pravdy, edituje se tohle** |
| `_zdroj/gradienty.py` | generátor linek a spodního pruhu |
| `_zdroj/navrh-canva-6x.png` | výchozí grafický návrh (Canva `DAHUKO-ess4`) |

Obrázky jsou uložené ve dvojnásobném rozlišení kvůli retina displejům; podpis je
zmenšuje atributy `width`/`height`.

## Úprava podpisu

```bash
python _zdroj/build.py     # přepíše podpis.html i podpis-nahled.html
python _zdroj/gradienty.py # jen když se mění barvy linek nebo pruhu
```

Adresa úložiště obrázků je konstanta `WEB` na začátku `build.py`.

## Vložení do Gmailu

Gmail neumí vložit HTML kód přímo. `podpis.html` otevřít v Chrome → `Ctrl+A`, `Ctrl+C`
→ Gmail *Nastavení → Obecné → Podpis* → `Ctrl+V` → *Uložit změny*.
Nastavuje se ke každé odesílací adrese zvlášť.

**Po nasazení ověřit:** v odeslané zprávě nesmí být ikona sponky (sponka = obrázky se
zase posílají jako přílohy) a po odpovědi z Outlooku musí obrázky pořád držet.

## Pravidla, která se tu nesmí porušit

1. Obrázky jen přes `https://`, nikdy `cid:` ani `data:`.
2. Adresa vždy končí `.png` — nikdy varianta `.png.webp` (Outlook WebP neumí).
3. Text zůstává textem, nikdy se nevykresluje do obrázku.
4. Barevná tlačítka jsou buňky tabulky, ne obrázky — přežijí vypnuté načítání obrázků.
5. Layout výhradně tabulkami, šířka 600 px. Flexbox ani grid v e-mailu neexistují.
6. Každý `<img>` má `width` a `height` jako HTML atribut a `border="0"`.
