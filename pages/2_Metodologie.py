import streamlit as st

st.logo('logo.svg')

"""
# Metodologie

Tato aplikace se opírá o harmonizovaný dataset [BACI](https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37), který je každý rok publikován organizací CEPII.
CEPII pomocí své publikované metodologie harmonizuje data z UN databáze Comtrade tak, aby se každý export rovnal importu a předešlo se dvojímu počítání obchodních toků.

Pro vypočítání komplexity produktu je použit [python modul](https://github.com/cid-harvard/py-ecomplexity) publikovaný Centre for International Developlent při Harvardské univerzitě.
Stejný modul je také použit pro výpočet matice příbuznosti v produktovém prostoru. Jako vstupní obchodní data je použita celá databáze BACI. Jako test přítomnosti aktivity v dané zemi je použita standartní podmínka RCA>1.
Tento postup blízce napodobuje přístup OEC, nicméně absolutní hodnoty komplexit se mohou lišit, co je důležité jsou relativní vztahy mezi produktu.
Potíže v jasném definování absolutních hodnot komplexit jsou hlavní kritikou používání těchto metod, nicméně v tomto nástroji se soustředíme na percentil a žebíček příbuznosti, tedy relativí komplexitu a příbuznost vůči zbytku produktů v BACI.

Pro výpočet příbuznosti produktů české ekonomice je použit stejný vzorec jako používá OEC a publikuje [na svých stránkách](https://oec.world/en/resources/methods).


"""
st.latex(r"""Příbuznost_{cp}=\frac{\sum_{p'}{M_{cp'}\phi_{pp'}}}{\sum_{p'} \phi_{pp'}}""")