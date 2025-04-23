import streamlit as st
from visualsetup import load_visual_identity

# Page config
st.set_page_config(
    page_title="Mapa Příležitostí",
    page_icon="favicon.ico",
    layout="wide"
)

# Load custom branding
load_visual_identity("header.jpg")
st.logo('logo_notext.svg', size='large', icon_image='logo_notext.svg')
logocol1, logocol2 = st.columns([2, 3])
logocol1.image('logo_text.svg', use_container_width=True)
logocol2.text("")
logocol2.text("")
p1, p2, p3, p4, p5, p6, p7 = logocol2.columns(7)
p1.image('partners/01.png', use_container_width=True)
p2.image('partners/07.png', use_container_width=True)
p3.image('partners/03.png', use_container_width=True)
p4.image('partners/04.png', use_container_width=True)
p5.image('partners/05.png', use_container_width=True)
p6.image('partners/06.png', use_container_width=True)
p7.image('partners/02.png', use_container_width=True)
st.logo('logo_notext.svg', size='large', icon_image='logo_notext.svg')

col1,col2,col3 = st.columns([1,5,1])
col2.subheader("")
# Main Section Title
# --- Introduction and Data Sources ---
col2.markdown("""
### Odkud jsme čerpali data ohledně velikosti vývozu v jednotlivých výrobkových kategoriích
Celá datová základna je založena na harmonizovaném datasetu světového obchodu **BACI**, který je každoročně publikován organizací **CEPII**. CEPII harmonizuje data z databáze **UN Comtrade** tak, aby každý export z jedné země odpovídal importu v zemi druhé a nedocházelo k dvojímu započítání obchodních toků.  
Databáze **UN Comtrade** je oficiální globální databáze OSN, která obsahuje detailní statistiky o mezinárodním obchodu se zbožím mezi státy.
""")

col2.link_button("Více o BACI datasetu", "https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37")

# --- Product Classification ---
col2.markdown("""
### Klasifikace výrobků
Pro účely Mapy příležitostí využíváme klasifikaci **Harmonized System (HS)** ve verzi **HS 2022**.  
Analýza je prováděna na úrovni **šesticiferného členění výrobků (HS6)**, kde je celkem 5 605 typů výrobků.  
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

# --- Cleantech Taxonomy Tree Placeholder ---
col2.markdown("### Třídění zelených výrobků")
col2.markdown("""
Zelené výrobky třídíme do **6 Taxonomických grup**, **17 Skupin**, **40 Podskupin** a **58 Kategorií**.  
Některé kategorie zatím nejsou obsazené, ale počítáme s jejich doplněním.
""")
col2.code("""
├─ Snížení celkové emisní náročnosti  
│   ├─ Snížení emisí výroby  
│   │     (ocel, cement, efektivita, elektrifikace průmyslu i zemědělství)  
│   ├─ Snížení emisí dopravy  
│   │     (rozvoj vlaků; elektromobilita, vodík, infrastruktura)  
│   ├─ Snížení emisí budov  
│   │     (izolace; elektrifikace vytápění)  
│   ├─ Snížení emisí energie  
│   │     (nízkoemisní elektřina a paliva – vítr, FVE, …)  
│   ├─ Ukládání energie  
│   ├─ Posílení sítí  
│   │     (elektrické a distribuční sítě, elektrifikace)  
│   ├─ Zadržování uhlíku v krajině  
│   │     (půda a lesnictví)  
│   ├─ Zachytávání a ukládání CO₂  
├─ Snížení materiálové náročnosti  
│     (redesign produktů a balení, sběr, třídění, přepoužití, recyklace)  
├─ Ochrana životního prostředí  
│     (distribuce vody, snížení znečištění, ochrana biodiverzity)  
├─ Příprava na nepříznivé klima  
│     (živelné pohromy, sucho, nové zdroje bílkovin)  
├─ Měřící a diagnostické přístroje  
│     (termostaty, senzory, spektrometry, chemická analýza)  
├─ Materiály a komponenty  
      (vzácné kovy, alternativy chemických látek, alternativní pohony a stroje)  
""")

# Define the HTML structure (using nested lists)
html_tree = """
<style>
/* Basic CSS for tree structure */
.tree-view ul {
    padding-left: 20px; /* Indentation for sub-levels */
    list-style-type: none; /* Remove default bullets */
    position: relative; /* Needed for positioning lines */
}

.tree-view li {
    position: relative; /* Needed for positioning lines */
    padding-left: 25px; /* Space for lines and text */
    line-height: 1.5; /* Adjust spacing */
    margin-left: -15px; /* Align text nicely after lines */
}

/* Tree lines using pseudo-elements */
.tree-view li::before, .tree-view li::after {
    content: '';
    position: absolute;
    left: 0;
}

/* Vertical line segment for all items */
.tree-view li::before {
    border-left: 1px solid #aaa; /* Line color and style */
    height: 100%;
    top: 0;
    width: 1px;
}

/* Horizontal line segment for all items */
.tree-view li::after {
    border-top: 1px solid #aaa; /* Line color and style */
    height: 1px;
    top: 0.75em; /* Position horizontal line vertically (half of line-height) */
    width: 20px; /* Length of the horizontal line */
}

/* Remove vertical line from the top part of the first item in any list */
.tree-view ul > li:first-child::before {
    top: 0.75em; /* Start vertical line at the horizontal line */
    height: calc(100% - 0.75em);
}

/* Remove lines for the very last item in the entire tree */
.tree-view > ul > li:last-child::before {
    height: 0.75em; /* Only draw vertical line up to the horizontal line */
}

/* Remove horizontal line for items without children (or style differently if needed) */
/* This basic CSS adds lines to all; more complex CSS needed to hide for leaves */
/* A simpler approach is to manually add a class to leaf nodes if needed */

/* Adjust root level indentation if necessary */
.tree-view > ul {
    padding-left: 0;
}
.tree-view > ul > li {
     margin-left: 0;
}


</style>

<div class="tree-view">
<ul>
  <li>Snížení celkové emisní náročnosti
    <ul>
      <li>Snížení emisí výroby
          <ul><li>(ocel, cement, efektivita, elektrifikace průmyslu i zemědělství)</li></ul>
      </li>
      <li>Snížení emisí dopravy
          <ul><li>(rozvoj vlaků; elektromobilita, vodík, infrastruktura)</li></ul>
      </li>
      <li>Snížení emisí budov
          <ul><li>(izolace; elektrifikace vytápění)</li></ul>
      </li>
      <li>Snížení emisí energie
          <ul><li>(nízkoemisní elektřina a paliva – vítr, FVE, …)</li></ul>
      </li>
      <li>Ukládání energie</li>
      <li>Posílení sítí
          <ul><li>(elektrické a distribuční sítě, elektrifikace)</li></ul>
      </li>
      <li>Zadržování uhlíku v krajině
          <ul><li>(půda a lesnictví)</li></ul>
      </li>
      <li>Zachytávání a ukládání CO₂</li>
    </ul>
  </li>
  <li>Snížení materiálové náročnosti
      <ul><li>(redesign produktů a balení, sběr, třídění, přepoužití, recyklace)</li></ul>
  </li>
  <li>Ochrana životního prostředí
      <ul><li>(distribuce vody, snížení znečištění, ochrana biodiverzity)</li></ul>
  </li>
  <li>Příprava na nepříznivé klima
      <ul><li>(živelné pohromy, sucho, nové zdroje bílkovin)</li></ul>
  </li>
  <li>Měřící a diagnostické přístroje
      <ul><li>(termostaty, senzory, spektrometry, chemická analýza)</li></ul>
  </li>
  <li>Materiály a komponenty
      <ul><li>(vzácné kovy, alternativy chemických látek, alternativní pohony a stroje)</li></ul>
  </li>
</ul>
</div>
"""

# Use st.markdown to render the HTML with CSS
st.markdown(html_tree, unsafe_allow_html=True)
# --- Key Indicators ---
col2.markdown("### Na jaké ukazatele se zaměřujeme")
col2.markdown("""
**Příbuznost**  
Produkty „příbuzné“ těm, které ČR už exportuje. Metrika je založená na metodologii OEC.

**Komplexita**  
Vyjadřuje unikátnost výrobku – čím vyšší, tím méně zemí jej umí vyvézt. Počítáno pomocí modulu **py-ecomplexity** (Harvard CID).

**Exportní objem**  
Měříme v USD. Pro CZK převod:  
- 2022: kurz 23,36  
- 2023: kurz 22,21

**Růst**  
Výpočet růstu vývozu za 2022–23 v USD (neočištěno o inflaci).

**Podíl a pořadí na světovém trhu**  
V procentech a absolutní hodnotě vývozu ČR ve srovnání se světem.
""")

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

col2.latex(r"""
\text{příbuznost}_{cp} = \frac{\sum_{p'} M_{cp'} \, \phi_{pp'}}{\sum_{p'} \phi_{pp'}}
""")

col2.markdown("""
- **$$M_{cp'}$$**: 1 pokud má produkt $$p'$$ v zemi $$c$$ RCA > 1, jinak 0.  
- **$$\phi_{pp'}$$**: Míra příbuznosti mezi produkty.  

Výpočet je **normalizovaný** a ukazuje příbuznost produktu $$p$$ k aktivním produktům v zemi $$c$$.
""", unsafe_allow_html=True)

col2.link_button("Metodika OEC", "https://oec.world/en/resources/methods")
