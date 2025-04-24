# 📊 Mapa Příležitostí – Metodologie

Tato stránka popisuje datové zdroje, klasifikaci a metodologii použité v aplikaci **Mapa příležitostí**, která vizualizuje exportní potenciál České republiky, se zaměřením na tzv. *zelené výrobky*.

---

## 📦 Datové zdroje

Základem analýzy je dataset světového obchodu **BACI**, který publikuje organizace **CEPII**. Tento dataset harmonizuje data z **UN Comtrade** tak, aby nedocházelo k dvojímu započítání obchodních toků.

- **UN Comtrade** je globální databáze OSN obsahující detailní statistiky o mezinárodním obchodu.
- BACI zajišťuje jednotnost mezi exporty a importy na úrovni států.

🔗 [Více o BACI datasetu](https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37)

---

## 🧾 Klasifikace výrobků

Pro kategorizaci využíváme standard **Harmonized System (HS)** ve verzi **HS 2022**, konkrétně na úrovni **HS6** (šesticiferné členění).

- Datový rozsah: **roky 2022 a 2023**
- Počet typů výrobků: **5 605**

---

## 🌱 Co považujeme za „zelené“ výrobky?

Zelené produkty (také označované jako *clean-tech* nebo *čisté technologie*) jsou klíčové pro přechod na nízkouhlíkovou ekonomiku. Zahrnujeme:

- technologie šetřící energii a emise,
- udržitelné materiály a suroviny,
- komponenty pro obnovitelné zdroje energie.

**Zdroj klasifikace:**
- akademické studie,
- veřejné dokumenty,
- konzultace s odborníky v ČR.

---

## 🧠 Taxonomie zelených výrobků

Struktura třídění zahrnuje:

- **6 hlavních grup**
- **17 skupin**
- **40 podskupin**
- **58 kategorií** (některé budou doplněny)

```
Snížení celkové emisní náročnosti
├── Výroba
├── Doprava
├── Budovy
├── Energie
├── Ukládání energie
├── Posílení sítí
├── Uhlík v krajině
└── Zachytávání CO₂
...
```

> Kompletní grafická vizualizace taxonomie je k dispozici v aplikaci.

---

## 📈 Klíčové ukazatele

### 🧬 Příbuznost
Produkty, které jsou „blízké“ těm, které ČR již vyváží. Měříme pomocí metodiky OEC.

### 🧠 Komplexita
Ukazuje unikátnost produktu – čím vyšší, tím méně zemí jej vyváží. Vypočítáno pomocí [py-ecomplexity](https://github.com/cid-harvard/py-ecomplexity).

### 💵 Exportní objem
Udává se v USD.

| Rok  | Směnný kurz (CZK/USD) |
|------|------------------------|
| 2022 | 23.36                 |
| 2023 | 22.21                 |

### 📊 Růst
Meziroční růst exportu (2022–2023) v USD (není očištěn o inflaci).

### 🌍 Podíl na světovém trhu
Porovnání exportu ČR s globálním exportem.

---

## 🧮 Datová metodologie

### Komplexita produktu

Využíváme open-source modul:

🔗 [py-ecomplexity od Harvard CID](https://github.com/cid-harvard/py-ecomplexity)

### Podmínka aktivity: RCA > 1

Země má **komparativní výhodu** v produktu, pokud platí `RCA > 1`, obdobně jako ve [vizualizacích OEC](https://oec.world/en/resources/methods).

🔗 [Kritický článek o RCA](https://pmc.ncbi.nlm.nih.gov/articles/PMC7335174/)

### Výpočet příbuznosti

Používáme následující vzorec:

\[
\text{příbuznost}_{cp} = \frac{\sum_{p'} M_{cp'} \cdot \phi_{pp'}}{\sum_{p'} \phi_{pp'}}
\]

- \( M_{cp'} = 1 \), pokud má produkt \( p' \) v zemi \( c \) `RCA > 1`, jinak 0.
- \( \phi_{pp'} \) = míra příbuznosti mezi produkty.

---

## 📍 O projektu

Tato metodologie je součástí aplikace **Mapa příležitostí**, jejímž cílem je zviditelnit příležitosti českého exportu v kontextu zelené transformace.

---
