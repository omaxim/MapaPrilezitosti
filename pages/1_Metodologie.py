import streamlit as st
from visualsetup import load_visual_identity
import streamlit.components.v1 as components
import json
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



# 1. Define your tree data in jsTree's JSON format
# Each node needs an 'id', 'parent' ('#' for root nodes), and 'text'
tree_data = [
    # Snížení celkové emisní náročnosti Branch
    {"id": "root_snizeni_emisi", "parent": "#", "text": "Snížení celkové emisní náročnosti"},
    {"id": "emise_vyroba", "parent": "root_snizeni_emisi", "text": "Snížení emisí výroby"},
    {"id": "emise_vyroba_detail", "parent": "emise_vyroba", "text": "(ocel, cement, efektivita, elektrifikace průmyslu i zemědělství)"},
    {"id": "emise_doprava", "parent": "root_snizeni_emisi", "text": "Snížení emisí dopravy"},
    {"id": "emise_doprava_detail", "parent": "emise_doprava", "text": "(rozvoj vlaků; elektromobilita, vodík, infrastruktura)"},
    {"id": "emise_budov", "parent": "root_snizeni_emisi", "text": "Snížení emisí budov"},
    {"id": "emise_budov_detail", "parent": "emise_budov", "text": "(izolace; elektrifikace vytápění)"},
    {"id": "emise_energie", "parent": "root_snizeni_emisi", "text": "Snížení emisí energie"},
    {"id": "emise_energie_detail", "parent": "emise_energie", "text": "(nízkoemisní elektřina a paliva – vítr, FVE, …)"},
    {"id": "ukladani_energie", "parent": "root_snizeni_emisi", "text": "Ukládání energie"},
    {"id": "posileni_siti", "parent": "root_snizeni_emisi", "text": "Posílení sítí"},
    {"id": "posileni_siti_detail", "parent": "posileni_siti", "text": "(elektrické a distribuční sítě, elektrifikace)"},
    {"id": "zadrzovani_uhliku", "parent": "root_snizeni_emisi", "text": "Zadržování uhlíku v krajině"},
    {"id": "zadrzovani_uhliku_detail", "parent": "zadrzovani_uhliku", "text": "(půda a lesnictví)"},
    {"id": "zachytavani_co2", "parent": "root_snizeni_emisi", "text": "Zachytávání a ukládání CO₂"},

    # Snížení materiálové náročnosti Branch
    {"id": "root_snizeni_materialu", "parent": "#", "text": "Snížení materiálové náročnosti"},
    {"id": "snizeni_materialu_detail", "parent": "root_snizeni_materialu", "text": "(redesign produktů a balení, sběr, třídění, přepoužití, recyklace)"},

    # Ochrana životního prostředí Branch
    {"id": "root_ochrana_zp", "parent": "#", "text": "Ochrana životního prostředí"},
    {"id": "ochrana_zp_detail", "parent": "root_ochrana_zp", "text": "(distribuce vody, snížení znečištění, ochrana biodiverzity)"},

    # Příprava na nepříznivé klima Branch
    {"id": "root_priprava_klima", "parent": "#", "text": "Příprava na nepříznivé klima"},
    {"id": "priprava_klima_detail", "parent": "root_priprava_klima", "text": "(živelné pohromy, sucho, nové zdroje bílkovin)"},

    # Měřící a diagnostické přístroje Branch
    {"id": "root_merici_pristroje", "parent": "#", "text": "Měřící a diagnostické přístroje"},
    {"id": "merici_pristroje_detail", "parent": "root_merici_pristroje", "text": "(termostaty, senzory, spektrometry, chemická analýza)"},

    # Materiály a komponenty Branch
    {"id": "root_materialy_komponenty", "parent": "#", "text": "Materiály a komponenty"},
    {"id": "materialy_komponenty_detail", "parent": "root_materialy_komponenty", "text": "(vzácné kovy, alternativy chemických látek, alternativní pohony a stroje)"},
]

# Convert the Python list of dictionaries to a JSON string
# This is important to safely inject it into the JavaScript part of the HTML
tree_data_json = json.dumps(tree_data)

# 2. Create the HTML string
#    - Includes CDN links for jQuery and jsTree
#    - Contains a div with id="jstree_div" where the tree will be rendered
#    - Includes the JavaScript to initialize jsTree
html_string = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>jsTree Example</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.12/themes/default/style.min.css" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.12/jstree.min.js"></script>
<style>
  /* Optional: Add some basic styling */
  body {{ font-family: sans-serif; }}
  #jstree_div {{ padding: 10px; border: 1px solid #eee; border-radius: 5px; }}
</style>
</head>
<body>

<div id="jstree_div"></div>

<script>
$(function () {{
  // Get the JSON data string passed from Python
  var treeData = {tree_data_json};

  // Initialize jsTree
  $('#jstree_div').jstree({{
    'core' : {{
      'data' : treeData, // Use the data defined above
      'themes': {{
          'name': 'default', // Use the default theme
          'responsive': true, // Make the tree responsive
          'stripes': true // Add stripes for better readability (optional)
      }}
    }},
    "plugins" : ["wholerow"] // Use the wholerow plugin for better selection highlighting (optional)
  }});

  // Optional: Expand all nodes initially
  $('#jstree_div').on('ready.jstree', function () {{
    $(this).jstree('open_all');
  }});

}});
</script>

</body>
</html>
"""

# 3. Embed the HTML in Streamlit
# Use st.components.v1.html to render the interactive tree
# Adjust height as needed
# Assuming this runs within your col2 context:
# col2.components.v1.html(html_string, height=600, scrolling=True)
# If not in a column, use st directly:
st.components.v1.html(html_string, height=600, scrolling=True)
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
