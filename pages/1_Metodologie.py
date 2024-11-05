import streamlit as st
from visualsetup import load_visual_identity
#Loading loads of custom css in markdown
st.set_page_config(
    page_title="Mapa Příležitostí",
    page_icon="favicon.png"
)
#load_visual_identity("header.jpg")

st.logo('logo_web.svg',size='large',icon_image='logo_notext.svg')

# Main Title
st.markdown("# 📊 Metodologie")

# Introduction
st.markdown("""
Tato aplikace je založena na harmonizovaném datasetu **BACI**, který je každoročně publikován organizací **CEPII**. CEPII harmonizuje data z databáze **UN Comtrade** tak, aby každý export odpovídal importu a nedocházelo k dvojímu započítání obchodních toků. 
""")

# Link to BACI dataset
st.link_button("ℹ️ Více o BACI datasetu", "https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37")

# Product Complexity Calculation
st.markdown("### 📈 Výpočet komplexity produktu")
st.markdown("""
Pro výpočet komplexity produktu používáme **Python modul py-ecomplexity** od Centre for International Development při **Harvardské univerzitě**. Tento modul také umožňuje výpočet **matice příbuznosti** v produktovém prostoru. Data pro výpočet zahrnují celou databázi **BACI**.
""")
st.link_button("📜 Více o modulu py-ecomplexity", "https://github.com/cid-harvard/py-ecomplexity")

# Condition for Country Activity
st.markdown("""
### 🌍 Podmínka aktivity v dané zemi
Pro detekci ekonomické aktivity konkrétního produktu v zemi se používá kritérium **RCA > 1**. Tento postup je obdobný metodice používané v **OEC**, kde jsou důležité relativní vztahy mezi produkty, i když absolutní hodnoty komplexity se mohou mírně lišit.
""")

st.markdown("""
Jednoznačné určení absolutních hodnot komplexity je často zpochybňované. Tato aplikace se však zaměřuje na **relativní komplexitu produktů** (percentil a pořadí v rámci datasetu BACI).
""")
st.link_button("📑 Přečíst kritický článek", "https://pmc.ncbi.nlm.nih.gov/articles/PMC7335174/")

# Product Relatedness Calculation
st.markdown("### 🔍 Výpočet příbuznosti produktů")
st.markdown("""
Příbuznost produktů vůči ekonomice ČR je vypočítána podobně jako v OEC. Podrobný popis této metodiky je k dispozici na stránkách **OEC**.

              
Příbuznost produktu $$p$$ v zemi $$c$$ se vypočítá podle následujícího vzorce:

              """)


# LaTeX Formula with Explanation
st.latex(r"""
\text{příbuznost}_{cp} = \frac{\sum_{p'} M_{cp'} \, \phi_{pp'}}{\sum_{p'} \phi_{pp'}}
""")

# Explanation with inline LaTeX
st.markdown("""

- **$$M_{cp'}$$**: Hodnota v matici $$M$$, která je rovna **1**, pokud produkt $$p'$$ v zemi $$c$$ vykazuje **RCA > 1** (tj. komparativní výhodu); jinak je rovna **0**.
- **$$\phi_{pp'}$$**: Míra příbuznosti mezi produkty $$p$$ a $$p'$$, vyjadřující jejich blízkost v produktovém prostoru.

Celkový vzorec tedy počítá příbuznost produktu $$p$$ s produkty $$p'$$, které jsou v zemi $$c$$ aktivní (splňují podmínku **RCA > 1**). Výpočet je **normalizován**, což zajistí, že výsledek zohledňuje vztahy produktu $$p$$ vůči celé produktové struktuře.
""", unsafe_allow_html=True)
st.link_button("📘 Metodika OEC", "https://oec.world/en/resources/methods")
