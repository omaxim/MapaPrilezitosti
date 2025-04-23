import streamlit as st
from visualsetup import load_visual_identity
from streamlit_flow import streamlit_flow
from streamlit_flow.interfaces import StreamlitFlowNode, StreamlitFlowEdge

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



# Define nodes
nodes = [
    StreamlitFlowNode(id="root", data={"label": "Snížení celkové emisní náročnosti"}, pos=(0, 0)),
    StreamlitFlowNode(id="vyroba", data={"label": "Snížení emisí výroby\n(ocel, cement, efektivita, elektrifikace průmyslu i zemědělství)"}, pos=(200, -200)),
    StreamlitFlowNode(id="doprava", data={"label": "Snížení emisí dopravy\n(rozvoj vlaků; elektromobilita, vodík, infrastruktura)"}, pos=(200, -100)),
    StreamlitFlowNode(id="budovy", data={"label": "Snížení emisí budov\n(izolace; elektrifikace vytápění)"}, pos=(200, 0)),
    StreamlitFlowNode(id="energie", data={"label": "Snížení emisí energie\n(nízkoemisní elektřina a paliva – vítr, FVE, …)"}, pos=(200, 100)),
    StreamlitFlowNode(id="ukladani", data={"label": "Ukládání energie"}, pos=(200, 200)),
    StreamlitFlowNode(id="site", data={"label": "Posílení sítí\n(elektrické a distribuční sítě, elektrifikace)"}, pos=(200, 300)),
    StreamlitFlowNode(id="krajina", data={"label": "Zadržování uhlíku v krajině\n(půda a lesnictví)"}, pos=(200, 400)),
    StreamlitFlowNode(id="co2", data={"label": "Zachytávání a ukládání CO₂"}, pos=(200, 500)),
    StreamlitFlowNode(id="material", data={"label": "Snížení materiálové náročnosti\n(redesign produktů a balení, sběr, třídění, přepoužití, recyklace)"}, pos=(0, 600)),
    StreamlitFlowNode(id="zivotni", data={"label": "Ochrana životního prostředí\n(distribuce vody, snížení znečištění, ochrana biodiverzity)"}, pos=(0, 700)),
    StreamlitFlowNode(id="klima", data={"label": "Příprava na nepříznivé klima\n(živelné pohromy, sucho, nové zdroje bílkovin)"}, pos=(0, 800)),
    StreamlitFlowNode(id="pristroje", data={"label": "Měřící a diagnostické přístroje\n(termostaty, senzory, spektrometry, chemická analýza)"}, pos=(0, 900)),
    StreamlitFlowNode(id="materialy", data={"label": "Materiály a komponenty\n(vzácné kovy, alternativy chemických látek, alternativní pohony a stroje)"}, pos=(0, 1000)),
]

# Define edges
edges = [
    StreamlitFlowEdge(source="root", target="vyroba"),
    StreamlitFlowEdge(source="root", target="doprava"),
    StreamlitFlowEdge(source="root", target="budovy"),
    StreamlitFlowEdge(source="root", target="energie"),
    StreamlitFlowEdge(source="root", target="ukladani"),
    StreamlitFlowEdge(source="root", target="site"),
    StreamlitFlowEdge(source="root", target="krajina"),
    StreamlitFlowEdge(source="root", target="co2"),
    StreamlitFlowEdge(source="root", target="material"),
    StreamlitFlowEdge(source="root", target="zivotni"),
    StreamlitFlowEdge(source="root", target="klima"),
    StreamlitFlowEdge(source="root", target="pristroje"),
    StreamlitFlowEdge(source="root", target="materialy"),
]

# Render the flow diagram
with col2:
    streamlit_flow(nodes=nodes, edges=edges, layout="tree")
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
