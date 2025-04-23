import streamlit as st
from visualsetup import load_visual_identity
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import TreeLayout

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



# Define the main root node
nodes = [
    StreamlitFlowNode(id='root', pos=(0, 0), data={'content': 'Snížení celkové emisní náročnosti'}, node_type='input', source_position='right'),
    
    # Sub-nodes
    StreamlitFlowNode(id='vyroba', pos=(0, 0), data={'content': 'Snížení emisí výroby\n(ocel, cement, efektivita, elektrifikace průmyslu i zemědělství)'}),
    StreamlitFlowNode(id='doprava', pos=(0, 0), data={'content': 'Snížení emisí dopravy\n(rozvoj vlaků; elektromobilita, vodík, infrastruktura)'}),
    StreamlitFlowNode(id='budovy', pos=(0, 0), data={'content': 'Snížení emisí budov\n(izolace; elektrifikace vytápění)'}),
    StreamlitFlowNode(id='energie', pos=(0, 0), data={'content': 'Snížení emisí energie\n(nízkoemisní elektřina a paliva – vítr, FVE, …)'}),
    StreamlitFlowNode(id='ukladani', pos=(0, 0), data={'content': 'Ukládání energie'}),
    StreamlitFlowNode(id='site', pos=(0, 0), data={'content': 'Posílení sítí\n(elektrické a distribuční sítě, elektrifikace)'}),
    StreamlitFlowNode(id='uhlík', pos=(0, 0), data={'content': 'Zadržování uhlíku v krajině\n(půda a lesnictví)'}),
    StreamlitFlowNode(id='zachytavani', pos=(0, 0), data={'content': 'Zachytávání a ukládání CO₂'}),

    # Parallel branches
    StreamlitFlowNode(id='materialy', pos=(0, 0), data={'content': 'Snížení materiálové náročnosti\n(redesign produktů a balení, sběr, třídění, přepoužití, recyklace)'}),
    StreamlitFlowNode(id='zivotni', pos=(0, 0), data={'content': 'Ochrana životního prostředí\n(distribuce vody, snížení znečištění, ochrana biodiverzity)'}),
    StreamlitFlowNode(id='klima', pos=(0, 0), data={'content': 'Příprava na nepříznivé klima\n(živelné pohromy, sucho, nové zdroje bílkovin)'}),
    StreamlitFlowNode(id='merici', pos=(0, 0), data={'content': 'Měřící a diagnostické přístroje\n(termostaty, senzory, spektrometry, chemická analýza)'}),
    StreamlitFlowNode(id='komponenty', pos=(0, 0), data={'content': 'Materiály a komponenty\n(vzácné kovy, alternativy chemických látek, alternativní pohony a stroje)'}),
]

# Create edges from the root to sub-nodes
edges = [
    StreamlitFlowEdge(id='root-vyroba', source='root', target='vyroba'),
    StreamlitFlowEdge(id='root-doprava', source='root', target='doprava'),
    StreamlitFlowEdge(id='root-budovy', source='root', target='budovy'),
    StreamlitFlowEdge(id='root-energie', source='root', target='energie'),
    StreamlitFlowEdge(id='root-ukladani', source='root', target='ukladani'),
    StreamlitFlowEdge(id='root-site', source='root', target='site'),
    StreamlitFlowEdge(id='root-uhlik', source='root', target='uhlík'),
    StreamlitFlowEdge(id='root-zachytavani', source='root', target='zachytavani'),

    # Additional major branches
    StreamlitFlowEdge(id='root-materialy', source='root', target='materialy'),
    StreamlitFlowEdge(id='root-zivotni', source='root', target='zivotni'),
    StreamlitFlowEdge(id='root-klima', source='root', target='klima'),
    StreamlitFlowEdge(id='root-merici', source='root', target='merici'),
    StreamlitFlowEdge(id='root-komponenty', source='root', target='komponenty'),
]

# Initialize state
if 'flow_state' not in st.session_state:
    st.session_state.flow_state = StreamlitFlowState(nodes, edges)

# Display in your column
with col2:
    streamlit_flow('tree_layout', st.session_state.flow_state, layout=TreeLayout(direction='right'), fit_view=True)
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
