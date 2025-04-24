import streamlit as st
from mapatools.visualsetup import load_visual_identity
import os
# Page config
st.set_page_config(
    page_title="Mapa Příležitostí",
    page_icon="resources/favicon.ico",
    layout="wide"
)
# Load custom branding
load_visual_identity("resources/header.jpg")
st.logo('resources/logo_notext.svg', size='large', icon_image='resources/logo_notext.svg')

col1,col2,col3 = st.columns([1,5,1])
col2.subheader("")
col2.subheader("")

# Main Section Title
# --- Introduction and Data Sources ---
col2.markdown("""
## Odkud jsme čerpali data ohledně velikosti vývozu v jednotlivých výrobkových kategoriích
Celá datová základna je založena na harmonizovaném datasetu světového obchodu **BACI**, který je každoročně publikován organizací **CEPII**. CEPII harmonizuje data z databáze **UN Comtrade** tak, aby každý export z jedné země odpovídal importu v zemi druhé a nedocházelo k dvojímu započítání obchodních toků.  
Databáze **UN Comtrade** je oficiální globální databáze OSN, která obsahuje detailní statistiky o mezinárodním obchodu se zbožím mezi státy.
""")

col2.link_button("Více o BACI datasetu", "https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37")

col2.divider()
# --- Product Classification ---
col2.markdown("""
## Klasifikace výrobků
Pro účely Mapy příležitostí využíváme klasifikaci **Harmonized System (HS)** ve verzi **HS 2022**.  
Analýza je prováděna na úrovni **šesticiferného členění výrobků (HS6)**, kde je celkem 5 606 typů výrobků.  
Data jsou k dispozici za rok **2022 a 2023**.
""")

# --- Green Products ---
col2.markdown("""
### Jak jsme vybírali tzv. „zelené výrobky“
Za „zelené“ či „clean-tech“ označujeme produkty klíčové pro přechod na čistou, nízkouhlíkovou ekonomiku.  
Výběr vychází z:
- rešerší globálních akademických studií,
- materiálů veřejného sektoru,
- konzultací s experty z ČR.

Zahrnujeme i komponenty důležité pro zelenou transformaci.
""")

col2.markdown("""
### Využívání termínu „zelená“ vs. „clean-tech“
Termíny **zelené výrobky**, **clean-tech** a **čisté technologie** používáme rovnocenně.  
Zahrnujeme široké spektrum změn – od energetiky přes průmyslové technologie až po hospodaření s vodou, půdou a surovinami.
""")
col2.divider()

# --- Cleantech Taxonomy Tree Placeholder ---
col2.markdown("## Třídění zelených výrobků")
col2.markdown("""
Zelené výrobky třídíme do **6 Taxonomických grup**, **17 Skupin**, **40 Podskupin** a **58 Kategorií**.  
Některé kategorie zatím nejsou obsazené, ale počítáme s jejich doplněním.
""")

col2.graphviz_chart("""
digraph G {
    rankdir=LR;
    bgcolor=transparent;
    splines=ortho;

    node [
        shape=box,
        style=filled,
        fillcolor=white,
        fontname="Montserrat, sans-serif",
        fontcolor="#666666",
        color="#666666",
        style=bold,
        fontsize=14,
        fontstyle=bold,
        fixedsize=true,
        width=4,
        height=0.5,
        margin=0.2,
        labelloc=c,
        justify=center
    ];

    edge [arrowhead=none];

    // Top-level categories (not connected)
    "Snížení celkové emisní náročnosti";
    "Snížení materiálové náročnosti\\n(redesign produktů a balení, sběr, třídění, přepoužití, recyklace)";
    "Ochrana životního prostředí\\n(distribuce vody, snížení znečištění, ochrana biodiverzity)";
    "Příprava na nepříznivé klima\\n(živelné pohromy, sucho, nové zdroje bílkovin)";
    "Měřící a diagnostické přístroje\\n(termostaty, senzory, spektrometry, chemická analýza)";
    "Materiály a komponenty\\n(vzácné kovy, alternativy chemických látek, alternativní pohony a stroje)";

    // Children for emissions strategy
    "Snížení celkové emisní náročnosti" -> "Snížení emisí výroby\\n(ocel, cement, efektivita, elektrifikace průmyslu i zemědělství)";
    "Snížení celkové emisní náročnosti" -> "Snížení emisí dopravy\\n(rozvoj vlaků; elektromobilita, vodík, infrastruktura)";
    "Snížení celkové emisní náročnosti" -> "Snížení emisí budov\\n(izolace; elektrifikace vytápění)";
    "Snížení celkové emisní náročnosti" -> "Snížení emisí energie\\n(nízkoemisní elektřina a paliva – vítr, FVE, …)";
    "Snížení celkové emisní náročnosti" -> "Ukládání energie";
    "Snížení celkové emisní náročnosti" -> "Posílení sítí\\n(elektrické a distribuční sítě, elektrifikace)";
    "Snížení celkové emisní náročnosti" -> "Zadržování uhlíku v krajině\\n(půda a lesnictví)";
    "Snížení celkové emisní náročnosti" -> "Zachytávání a ukládání CO₂";
}
""")
col2.divider()

# --- Key Indicators ---
col2.markdown("## Na jaké ukazatele se zaměřujeme")
col2.markdown("""
**Příbuznost**  
Produkty „příbuzné“ těm, které ČR už exportuje. Metrika je založená na metodologii OEC.

**Komplexita**  
Vyjadřuje unikátnost výrobku – čím vyšší, tím méně zemí jej umí vyvézt. Počítáno pomocí modulu **py-ecomplexity** (Harvard CID).
""")
kurzcol1, kurzcol2,kurzcol3 = col2.columns(3)
kurzcol1.markdown("""
**Exportní objem**  
Měříme v USD. Pro CZK převod:  """)

kurzcol2.metric("Kurz v roce 2022",23.36)
kurzcol3.metric("Kurz v roce 2023",22.21)
col2.markdown(
"""
**Růst**  
Výpočet růstu vývozu za 2022–23 v USD (neočištěno o inflaci).

**Podíl a pořadí na světovém trhu**  
V procentech a absolutní hodnotě vývozu ČR ve srovnání se světem.
""")
col2.divider()
# --- Detailed Data Methodology Section ---
col2.markdown("## Datová metodologie")

col2.markdown("""
### Výpočet komplexity produktu
Používáme Python modul **py-ecomplexity** od **Centre for International Development (Harvard)**.
""")
col2.link_button("Více o modulu py-ecomplexity", "https://github.com/cid-harvard/py-ecomplexity")

# --- RCA Condition ---
col2.markdown("""
### Podmínka aktivity v dané zemi
Používáme kritérium **RCA > 1** jako důkaz komparativní výhody, podobně jako v **OEC**.
""")
col2.link_button("Přečíst kritický článek", "https://pmc.ncbi.nlm.nih.gov/articles/PMC7335174/")

# --- Relatedness Formula ---
col2.markdown("### Výpočet příbuznosti produktů")

latexcol1,latexcol2 = col2.columns(2)

latexcol1.latex(r"""
\text{příbuznost}_{cp} = \frac{\sum_{p'} M_{cp'} \, \phi_{pp'}}{\sum_{p'} \phi_{pp'}}
""")

latexcol2.markdown("""
- **$$M_{cp'}$$**: 1 pokud má produkt $$p'$$ v zemi $$c$$ RCA > 1, jinak 0.  
- **$$\phi_{pp'}$$**: Míra příbuznosti mezi produkty.  

""", unsafe_allow_html=True)
col2.markdown("""
Výpočet je **normalizovaný** a ukazuje příbuznost produktu $$p$$ k aktivním produktům v zemi $$c$$.

""", unsafe_allow_html=True)

col2.link_button("Metodika OEC", "https://oec.world/en/resources/methods")
