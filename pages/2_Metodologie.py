import streamlit as st

# Logo
st.image('logo.svg')

# Hlavní nadpis
"""
# Metodologie aplikace
"""

# Úvodní popis
"""
Tato aplikace vychází z harmonizovaného datasetu [BACI](https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37), který je každoročně publikován organizací CEPII. CEPII harmonizuje data z UN databáze Comtrade pomocí své metodologie, aby každý export odpovídal importu a předešlo se dvojímu započítání obchodních toků.
"""

# Výpočet komplexity produktu
"""
## Výpočet komplexity produktu
Pro výpočet komplexity produktu je použit [Python modul py-ecomplexity](https://github.com/cid-harvard/py-ecomplexity), který publikuje Centre for International Development při Harvardské univerzitě. Tento modul také slouží k výpočtu matice příbuznosti v produktovém prostoru. Vstupní data pro tento výpočet zahrnují celou databázi BACI.
"""

# Podmínka pro aktivitu v dané zemi
"""
Pro test přítomnosti aktivity v konkrétní zemi je použita standardní podmínka RCA > 1.
Tento postup napodobuje přístup používaný v OEC, kde absolutní hodnoty komplexity nemusí být přesně stejné jako zde, ale důležité jsou relativní vztahy mezi jednotlivými produkty.
"""

# Kritika absolutních hodnot
"""
### Kritika absolutních hodnot
Jasné určení absolutních hodnot komplexity je problematické a často kritizované. Tato aplikace se však zaměřuje na relativní komplexitu produktů, tedy percentil a pořadí příbuznosti vůči ostatním produktům v datasetu BACI. Kritika ekonomických metod komplexity je dobře vzstižená v tomto [akademickém článku.](https://pmc.ncbi.nlm.nih.gov/articles/PMC7335174/)
"""

# Výpočet příbuznosti produktů
"""
## Výpočet příbuznosti produktů
Příbuznost produktů vůči české ekonomice je vypočítána stejným způsobem jako v OEC, který zveřejňuje podrobný popis této metodiky [na svých stránkách](https://oec.world/en/resources/methods).
"""

# LaTeX vzorec s vysvětlením
st.latex(r"""
\text{Příbuznost}_{cp} = \frac{\sum_{p'} M_{cp'} \, \phi_{pp'}}{\sum_{p'} \phi_{pp'}}
""")

# Rozšířený popis vzorce s použitím LaTeXu pro jednotlivé výrazy
"""
Příbuznost produktu \\( p \\) v zemi \\( c \\) se vypočítá na základě následujícího vzorce:

- \\( M_{cp'} \\): Hodnota v matici \\( M \\), která je rovna 1, pokud daný produkt \\( p' \\) má v zemi \\( c \\) zjištěný **Revealed Comparative Advantage (RCA)** větší než 1. Pokud \\( \text{RCA} \leq 1 \\), hodnota je 0.
  
- \\( \phi_{pp'} \\): Míra příbuznosti mezi produkty \\( p \\) a \\( p' \\). Tato hodnota vyjadřuje, jak jsou produkty \\( p \\) a \\( p' \\) vzájemně blízké v produktovém prostoru.

Celkový vzorec tedy počítá **průměrnou příbuznost** produktu \\( p \\) s ostatními produkty \\( p' \\), které jsou v zemi \\( c \\) aktivní (tj. splňují podmínku \\( \text{RCA} > 1 \\)).

Výpočet je normalizován sumou příbuzností \\( \phi_{pp'} \\) pro všechny produkty \\( p' \\), což zajistí, že výsledná hodnota zohledňuje příbuznost produktu \\( p \\) vůči celé produktové struktuře.
"""