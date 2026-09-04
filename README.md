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

Každý podpis má **vlastní soubor** `obrazky/podpis-qr-<slug>.png`, i když je obrázek
zatím shodný s jiným. Výměna QR proto znamená přepsat jeden obrázek — HTML se nemění
a nikdo nemusí podpis znovu vkládat do Gmailu.

> **Nedodělek:** `podpis-qr-wildner-2.png` a `podpis-qr-asistent.png` nesou zatím
> **převzatý QR z návrhu** (Wildnerův, resp. Mňukův). Tomáš je opravuje v Canvě.
> Až budou hotové, stačí přepsat ty dva soubory.

`obrazky/podpis-qr.png` je starý název Mňukova QR. Zůstává jen kvůli podpisu, který
mohl být vložený do Gmailu dřív, než vznikly per-osobní názvy. Až budou všechny podpisy
nasazené z aktuálních adres, může se smazat.

## Úprava podpisů

```bash
python _zdroj/build.py     # přepíše všechny podpisy i rozcestník
python _zdroj/gradienty.py # jen když se mění barvy linek nebo pruhu
```

Lidé, čísla a role jsou v seznamu `LIDE` na začátku `build.py`; adresa úložiště obrázků
v konstantě `WEB`. Skripty se spouštějí z kořene repozitáře.

## Kontrola po nasazení

V odeslané zprávě **nesmí být ikona sponky** (sponka = obrázky se zase posílají jako
přílohy) a po odpovědi z Outlooku musí obrázky pořád držet.

## Pravidla, která se tu nesmí porušit

1. Obrázky jen přes `https://`, nikdy `cid:` ani `data:`.
2. Adresa vždy končí `.png` — nikdy varianta `.png.webp` (Outlook WebP neumí).
3. Text zůstává textem, nikdy se nevykresluje do obrázku.
4. Barevná tlačítka jsou buňky tabulky, ne obrázky — přežijí vypnuté načítání obrázků.
5. Layout výhradně tabulkami, šířka 600 px. Flexbox ani grid v e-mailu neexistují.
6. Každý `<img>` má `width` a `height` jako HTML atribut a `border="0"`.
