import streamlit as st
from streamlit_tree_select import tree_select
from visualsetup import load_visual_identity

st.set_page_config(
    page_title="Mapa Příležitostí",
    page_icon="favicon.ico",
    layout="wide"
)
load_visual_identity("header.jpg")
st.title("")
st.title("")

st.logo('logo_notext.svg', size='large', icon_image='logo_notext.svg')

# Main Title
st.markdown("# Metodologie")

# --- Úvod k datům ---
st.markdown("""
### Odkud jsme čerpali data ohledně velikosti vývozu v jednotlivých výrobkových kategoriích

Celá datová základna je založena na harmonizovaném datasetu světového obchodu **BACI**, který je každoročně publikován organizací **CEPII**. CEPII harmonizuje data z databáze **UN Comtrade** tak, aby každý export z jedné země odpovídal importu v zemi druhé a nedocházelo k dvojímu započítání obchodních toků.

Databáze **UN Comtrade** je oficiální globální databáze OSN, která obsahuje detailní statistiky o mezinárodním obchodu se zbožím mezi státy podle zemí, komodit a let.
""")

# --- Klasifikace výrobků ---
st.markdown("""
### Klasifikace výrobků

Pro účely Mapy příležitostí využíváme klasifikaci **Harmonized System (HS)** ve verzi **HS 2022**. Analýza je prováděna na úrovni šesticiferného členění výrobků (**HS6**), kde se nachází **5 605** jednotlivých typů výrobků. V této klasifikaci jsou k dispozici data za roky **2022 a 2023**.
""")

# --- Výběr zelených produktů ---
st.markdown("""
### Jak jsme vybírali tzv. „zelené výrobky“

Za „zelené“ nebo „clean-tech“ označujeme výrobky (finální i komponenty), které hrají klíčovou roli při přechodu na čistou, nízkouhlíkovou ekonomiku. Výběr probíhá na základě:

- rešerší akademických studií,
- materiálů mezinárodních organizací a vlád,
- konzultací s českými experty.

Zahrnujeme nejen produkty přispívající ke snižování emisí, ale i komponenty nutné pro transformaci, jejichž poptávka poroste.
""")

# --- Terminologie ---
st.markdown("""
### Využívání termínu „zelená“ vs. „clean-tech“

Rovnocenně používáme termíny **zelené výrobky**, **clean-tech** a **čisté technologie**. „Zelená transformace“ zahrnuje změny v energetice, průmyslu, dopravě, stavebnictví, cirkularitě i v zacházení se zdroji.
""")

# --- Taxonomie ---
st.markdown("""
### Třídění zelených výrobků

Zelené výrobky třídíme do:

- **6 Taxonomických grup**
- **17 Skupin**
- **40 Podskupin**
- **58 Kategorií**

Některé skupiny zatím nemají přiřazené HS2022 kódy (např. Biodiverzita, CCS), ale očekáváme jejich doplnění s vývojem technologií.
""")

# --- Klíčové ukazatele ---
st.markdown("""
### Na jaké ukazatele se zaměřujeme

- **Příbuznost**: Míra vazby na český export (viz kapitola „Datová metodologie“ níže).
- **Komplexita (Unikátnost)**: Vzácnost produktu, vypočítaná pomocí modulu `py-ecomplexity` (viz níže).
- **Velikost vývozu**: V USD dle BACI/Comtrade, převod na CZK podle ČNB.
- **Růst**: Meziroční růst v USD za 2022–23.
- **Podíl na světovém trhu**: % českého exportu z globálního obratu.
- **Pořadí na světovém trhu**: Umístění ČR v absolutních USD hodnotách vývozu daného výrobku.
""")

# --- BACI Info Link ---
st.link_button("Více o BACI datasetu", "https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37")

# --- Interaktivní strom zelených výrobků ---
st.markdown("""
K některým Skupinám či Podskupinám (Zadržování uhlíku, Zachytávání a ukládání uhlíku, Ochrana půdy, Biodiverzita či Nové zdroje vody) v tuto chvíli nevidíme jednoznačně přiřaditelné výrobky v HS 2022 klasifikaci a tyto pozice v našem stromu tak zůstávají neobsazené. S dalším vývojem technologií a obchodování s těmito technologiemi počítáme, že se i tyto kategorie obsadí jednoznačně definovatelnými kódy výrobků.
""")

st.markdown("### Interaktivní strom zelených výrobků")

tree_data = {
    "Snížení celkové emisní náročnosti": {
        "Snížení emisí výroby": {
            "ocel, cement, efektivita, elektrifikace průmyslu i zemědělství": {}
        },
        "Snížení emisí dopravy (rozvoj vlaků)": {
            "elektromobilita, vodík, infrastruktura": {}
        },
        "Snížení emisí budov": {
            "izolace, elektrifikace vytápění": {}
        },
        "Snížení emisí energie": {
            "nízkoemisní elektřina a paliva (vítr, FVE)": {}
        },
        "Ukládání energie": {},
        "Posílení sítí": {
            "elektrické a distribuční sítě, elektrifikace": {}
        },
        "Zadržování uhlíku v krajině": {
            "půda a lesnictví": {}
        },
        "Zachytávání a ukládání CO₂": {}
    },
    "Snížení materiálové náročnosti": {
        "redesign produktů a balení": {},
        "sběr, třídění, přepoužití, recyklace": {}
    },
    "Ochrana životního prostředí": {
        "distribuce vody, snížení znečištění, ochrana biodiverzity": {}
    },
    "Příprava na nepříznivé klima": {
        "živelné pohromy, sucho, nové zdroje bílkovin": {}
    },
    "Měřící a diagnostické přístroje": {
        "termostaty, senzory, spektrometry, chemická analýza": {}
    },
    "Materiály a komponenty": {
        "vzácné kovy, alternativy chemických látek": {},
        "alternativní pohony a stroje": {}
    }
}

selected = tree_select(
    tree_data,
    checked=[],
    expanded=["Snížení celkové emisní náročnosti", "Materiály a komponenty"])

if selected:
    st.markdown("### Vybrané kategorie:")
    st.write(", ".join(selected))
