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
Jasné určení absolutních hodnot komplexity je problematické a často kritizované. Tato aplikace se však zaměřuje na relativní komplexitu produktů, tedy percentil a pořadí příbuznosti vůči ostatním produktům v datasetu BACI.
"""

# Výpočet příbuznosti produktů
"""
## Výpočet příbuznosti produktů
Příbuznost produktů vůči české ekonomice je vypočítána stejným způsobem jako v OEC, který zveřejňuje podrobný popis této metodiky [na svých stránkách](https://oec.world/en/resources/methods).
"""

# LaTeX vzorec
st.latex(r"""Příbuznost_{cp}=\frac{\sum_{p'}{M_{cp'}\phi_{pp'}}}{\sum_{p'} \phi_{pp'}}""")

# Popis vzorce
r"""
Příbuznost pro produkt \\( p \\) v zemi \\( c \\) je počítána jako kontrakce v produktovém prostoru, kde:
- \\( M_{cp'} \\) je matice s hodnotou 1, pokud \\( \text{RCA} > 1 \\), jinak 0,
- \\( \phi_{pp'} \\) vyjadřuje příbuznost mezi produkty \\( p \\) a \\( p' \\).

Celý výpočet je normalizován sumou příbuzností produktu \\( p \\) k ostatním produktům \\( p' \\).
"""
