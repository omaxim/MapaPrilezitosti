import streamlit as st
import pandas as pd

from mapatools.chartjsbubble import chartjs_plot
from mapatools.highchartpolararea import chart_highcharts_variable_pie
from mapatools.variable_names import get_plot_and_hover_display_names, get_hover_data
import streamlit.components.v1 as components
from mapatools.visualsetup import load_visual_identity

st.set_page_config(
    page_title="Mapa Příležitostí",
    page_icon="resources/logo_notext.svg",
    layout="wide"
)
# Loading custom CSS and identity assets
load_visual_identity("resources/header.jpg")
col1, col2 = st.columns([11, 4])
col1.subheader("")
col2.subheader("")
col2.subheader("Nastavení grafu")

# Sidebar: Year selection
year = col2.radio("Rok", ["2022", "2023", "2024"], index=2,horizontal=True)
# growth_pair = col2.radio("Růst", ["2023/2024", "2022/2023", "2022/2024"], index=0, horizontal=True)
# growth_from, growth_to = growth_pair.split("/")
growth_from, growth_to = "2022", "2024"  # fixed to 2-year comparison
topsubcol2 = col2.container()
def USDtoCZKdefault(year):
    if year == "2022":
        return 23.360
    elif year == "2023":
        return 22.21
    elif year == "2024":
        return 23.208

@st.cache_resource
def load_data(datayear):
    USD_to_czk = USDtoCZKdefault(datayear)
    taxonomy = pd.read_csv("BACI_analysis/outputs/PlnaDatabaze3.0.csv")
    CZE = pd.read_csv('BACI_analysis/outputs/CZE_' + datayear + '.csv')
    GreenProducts = taxonomy.merge(CZE, how='left', left_on='HS_ID', right_on='prod')
       
    df = GreenProducts.rename(columns={
        'ExportValue': 'Český export ' + datayear + ' CZK',
        'export_Rank': 'Pořadí Česka na světovém trhu ' + datayear,
        'pci': 'Komplexita výrobku (unikátnost) ' + datayear,
        'relatedness': 'Příbuznost CZ ' + datayear,
        'PCI_Rank': 'Žebříček komplexity ' + datayear,
        'PCI_Percentile': 'Percentil komplexity ' + datayear,
        'relatedness_Rank': 'Žebříček příbuznosti' + datayear,
        'relatedness_Percentile': 'Percentil příbuznosti ' + datayear,
        'WorldExport': 'Velikost světového trhu ' + datayear + ' CZK',
        'EUWorldMarketShare': 'EU Světový Podíl ' + datayear + ' %',
        'euhhi': 'Koncentrace evropského exportu ' + datayear,
        'hhi': 'Koncentrace světového trhu ' + datayear,
        'CZE_WorldMarketShare': 'Podíl Česka na světovém trhu ' + datayear + ' %',
        'CZE_EUMarketShare': 'CZ-EU Podíl ' + datayear + ' %',
        'rca': 'RCA ' + datayear,
        'EUTopExporter': 'EU Největší Exportér ' + datayear,
        'CZ_Nazev': 'Název',
    })
    df = df[df.Included == "IN"]
    df['CZ-EU Podíl ' + datayear + ' %'] = 100 * df['CZ-EU Podíl ' + datayear + ' %']
    df['EU Světový Podíl ' + datayear + ' %'] = 100 * df['EU Světový Podíl ' + datayear + ' %']
    df['Podíl Česka na světovém trhu ' + datayear + ' %'] = 100 * df['Podíl Česka na světovém trhu ' + datayear + ' %']
    df['Český export ' + datayear + ' USD'] = df['Český export ' + datayear + ' CZK']
    df['Český export ' + datayear + ' CZK'] = USD_to_czk * df['Český export ' + datayear + ' CZK']
    df['Velikost světového trhu ' + datayear + ' USD'] = df['Velikost světového trhu ' + datayear + ' CZK']
    df['Velikost světového trhu ' + datayear + ' CZK'] = USD_to_czk * df['Velikost světového trhu ' + datayear + ' CZK']
    df['Kód výrobku HS6'] = df['HS_ID'].astype(str)
    df['HS_Lookup'] = df['Kód výrobku HS6'] + " - " + df['Název']
    total_cz_export = USD_to_czk * CZE['ExportValue'].sum()
    total_cz_green_export = df['Český export ' + datayear + ' CZK'].sum()
    return df, total_cz_export, total_cz_green_export

# Define the default year_placeholder and get plotting lists
year_placeholder = " ‎"
plot_display_names, hover_display_data = get_plot_and_hover_display_names(year_placeholder)

# Sidebar selection boxes using display names
x_axis = col2.selectbox("Vyber osu X:", plot_display_names, index=0)
y_axis = col2.selectbox("Vyber osu Y:", plot_display_names, index=1)
markersize = col2.selectbox("Velikost dle:", plot_display_names, index=4)

# Load datasets for all years
df_2022, cz_export_22, cz_green_export_22 = load_data("2022")
df_2023, cz_export_23, cz_green_export_23 = load_data("2023")
df_2024, cz_export_24, cz_green_export_24 = load_data("2024")
df_by_year = {"2022": (df_2022, cz_export_22, cz_green_export_22),
              "2023": (df_2023, cz_export_23, cz_green_export_23),
              "2024": (df_2024, cz_export_24, cz_green_export_24)}
df, cz_total_export, cz_total_green_export = df_by_year[year]
df_prev, cz_export_prev, cz_green_export_prev = df_by_year[growth_from]
df_curr, cz_export_curr, cz_green_export_curr = df_by_year[growth_to]

# Initialize the session state for filtering by groups
if 'filtrovat_dle_skupin' not in st.session_state:
    st.session_state.filtrovat_dle_skupin = False

with col2:
    # Fixed label button, with a key
    if st.button("Přepnout zobrazení", use_container_width=True, key="toggle_filter_button"):
        st.session_state.filtrovat_dle_skupin = not st.session_state.filtrovat_dle_skupin

# **MOVE THE SESSION STATE FILTER MODE CHECK UP HERE** so that "color" is defined before filtering.
if st.session_state.filtrovat_dle_skupin:
    col2.markdown("**Aktuální zobrazení:** 🧩 Jednotlivé skupiny")
    color = 'Kategorie'
    # Use the current year's dataframe for group options.
    cur_df = df_by_year[year][0]
    skupiny = cur_df['Skupina'].unique()
    Skupina = col2.segmented_control('Skupina', skupiny, default=skupiny[5])
else:
    col2.markdown("**Aktuální zobrazení:** ✅ Všechny zelené produkty")
    color = 'Skupina'

# Define the filtering function
def apply_filters(df, year_str, x_axis, y_axis, color, markersize):
    filtered = df.copy()

    # If filtering by groups is active, assume Skupina is defined already.
    if st.session_state.filtrovat_dle_skupin:
        filtered = filtered[filtered['Skupina'].isin([Skupina])]

    for filter in st.session_state.filters:
        if filter['column'] is not None and filter['range'] is not None:
            colname = filter['column'].replace(year_placeholder, year_str)
            filtered = filtered[
                (filtered[colname] >= filter['range'][0]) &
                (filtered[colname] <= filter['range'][1])
            ]

    # Replace negative marker sizes with 0
    col_ms = markersize.replace(year_placeholder, year_str)
    filtered[col_ms] = filtered[col_ms].clip(lower=0)

    # Drop rows with missing values for plotting columns
    filtered = filtered.dropna(subset=[
        x_axis.replace(year_placeholder, year_str),
        y_axis.replace(year_placeholder, year_str),
        color,
        col_ms
    ])

    return filtered

# Ensure session state filters exist
if 'filters' not in st.session_state:
    st.session_state.filters = []

# Calculate filtered data for all years
filtered_df_2022 = apply_filters(df_2022, "2022", x_axis, y_axis, color, markersize)
filtered_df_2023 = apply_filters(df_2023, "2023", x_axis, y_axis, color, markersize)
filtered_df_2024 = apply_filters(df_2024, "2024", x_axis, y_axis, color, markersize)
filtered_by_year = {"2022": filtered_df_2022, "2023": filtered_df_2023, "2024": filtered_df_2024}
filtered_df = filtered_by_year[year]
filtered_df_prev = filtered_by_year[growth_from]
filtered_df_curr = filtered_by_year[growth_to]

# Filter control buttons
subcol1, subcol2 = col2.columns(2)
with subcol1:
    if st.button("Filtrování", use_container_width=True):
        st.session_state.filters.append({'column': None, 'range': None})
with subcol2:
    if st.button("Odstranit filtry", use_container_width=True):
        st.session_state.filters = []

# Display existing filters using display names
for i, filter in enumerate(st.session_state.filters):
    filter_col = col2.selectbox(f"Filtr {i+1}", plot_display_names, key=f"filter_col_{i}")
    filter_min, filter_max = df[filter_col.replace(year_placeholder, year)].min(), df[filter_col.replace(year_placeholder, year)].max()
    filter_range = col2.slider(
        f"Filtr {i+1}",
        float(filter_min),
        float(filter_max),
        (float(filter_min), float(filter_max)),
        key=f"filter_range_{i}"
    )
    st.session_state.filters[i]['column'] = filter_col
    st.session_state.filters[i]['range'] = filter_range

# Apply numerical filters (on already filtered_df)
for filter in st.session_state.filters:
    if filter['column'] is not None and filter['range'] is not None:
        filtered_df = filtered_df[
            (filtered_df[filter['column'].replace(year_placeholder, year)] >= filter['range'][0]) &
            (filtered_df[filter['column'].replace(year_placeholder, year)] <= filter['range'][1])
        ]

# Update axis names after replacing placeholder
markersize = markersize.replace(year_placeholder, year)
x_axis = x_axis.replace(year_placeholder, year)
y_axis = y_axis.replace(year_placeholder, year)

# Ensure no negative values and remove NA for plotting
filtered_df[markersize] = filtered_df[markersize].clip(lower=0)
filtered_df = filtered_df.dropna(subset=[x_axis, y_axis, color, markersize])

HS_select = topsubcol2.multiselect("Filtrovat jednotlivé produkty", filtered_df['HS_Lookup'])
st.divider()

hover_info = col2.multiselect("Co se zobrazí při najetí myší:", hover_display_data, default=['Název'])
hover_data = get_hover_data(year, year_placeholder, hover_info, x_axis, y_axis, markersize)

bottom_text = "Analýza je založená na obchodních datech UN COMTRADE, která jsou vyčištěna organizací CEPII a publikována každý rok jako dataset BACI"

if st.session_state.filtrovat_dle_skupin is False:
    if HS_select == []:
        chart_js = chartjs_plot(filtered_df, markersize, hover_data, color, x_axis, y_axis, year,
                                  chart_title="České zelené příležitosti", bottom_text=bottom_text)
    else:
        chart_js = chartjs_plot(filtered_df[filtered_df['HS_Lookup'].isin(HS_select)],
                                  markersize, hover_data, color, x_axis, y_axis, year,
                                  chart_title="České zelené příležitosti", bottom_text=bottom_text)
elif st.session_state.filtrovat_dle_skupin is True and Skupina is None:
    chart_js = None
elif st.session_state.filtrovat_dle_skupin is True and Skupina is not None:
    if HS_select == []:
        chart_js = chartjs_plot(filtered_df, markersize, hover_data, color, x_axis, y_axis, year,
                                  chart_title=Skupina, bottom_text=bottom_text)
    else:
        chart_js = chartjs_plot(filtered_df[filtered_df['HS_Lookup'].isin(HS_select)],
                                  markersize, hover_data, color, x_axis, y_axis, year,
                                  chart_title=Skupina, bottom_text=bottom_text)

# Render chart in main area
html_bytes = chart_js
with col1:
    components.html(chart_js, height=800,width=1500)

# Example: render the polar area chart in a Streamlit component
polar_js_skupiny = chart_highcharts_variable_pie(filtered_df_prev, filtered_df_curr, cz_export_prev,cz_export_curr,cz_green_export_prev,cz_green_export_curr,
                              group_field="Skupina",
                              chart_title="Růst exportu dle skupiny",
                              bottom_text=f"Šířka koláče vyjadřuje % z celkového českého exportu v roce {growth_to}<br>Vzdálenost dílu koláče od středu vyjadřuje růst skupiny mezi lety {growth_from} a {growth_to}",
                              usd_to_czk_22=USDtoCZKdefault(growth_from),
                              usd_to_czk_23=USDtoCZKdefault(growth_to),
                              year_from=growth_from, year_to=growth_to)
polar_js_kategorie = chart_highcharts_variable_pie(filtered_df_prev, filtered_df_curr, cz_export_prev,cz_export_curr,cz_green_export_prev,cz_green_export_curr,
                              group_field="Kategorie",
                              chart_title="Růst zeleného exportu dle kategorie",
                              bottom_text=f"Šířka koláče vyjadřuje % z českého zeleného exportu v roce {growth_to}<br>Vzdálenost dílu koláče od středu vyjadřuje růst kategorie mezi lety {growth_from} a {growth_to}",
                              usd_to_czk_22=USDtoCZKdefault(growth_from),
                              usd_to_czk_23=USDtoCZKdefault(growth_to),
                              relative_to_green_only=True,
                              year_from=growth_from, year_to=growth_to)


# Comparison columns - now you can compare metrics between 2022 and 2023
if HS_select == []:
    pie1,pie2 = st.columns(2)
    with pie1:
        st.components.v1.html(polar_js_skupiny, height=690,width=1500)
    with pie2:
        st.components.v1.html(polar_js_kategorie, height=690,width=1500)
    st.divider()
    mcol1, mcol2, mcol3, = st.columns(3)
    selected_CZ_growth = filtered_df_curr['Český export '+growth_to+' CZK'].sum() - filtered_df_prev['Český export '+growth_from+' CZK'].sum()
    selected_CZ_growth_perc = selected_CZ_growth / filtered_df_prev['Český export '+growth_from+' CZK'].sum()
    mcol1.metric("Vybraný český export za rok "+year+"", "{:,.0f}".format(sum(filtered_df['Český export '+year+' CZK'])/1e9),'miliard CZK' )
    mcol2.metric("Růst vybraného českého exportu mezi lety "+growth_from+" a "+growth_to, "{:,.0f}".format(selected_CZ_growth/1e9), "miliard CZK")
    mcol3.metric("Růst vybraného českého exportu mezi lety "+growth_from+" a "+growth_to, "{:,.1%}".format(selected_CZ_growth_perc), "%")


else:
    mcol1, mcol2, mcol3, = st.columns(3)
    lookup_year = filtered_df['HS_Lookup'].isin(HS_select)
    lookup_prev = filtered_df_prev['HS_Lookup'].isin(HS_select)
    lookup_curr = filtered_df_curr['HS_Lookup'].isin(HS_select)
    selected_CZ_growth = filtered_df_curr[lookup_curr]['Český export '+growth_to+' CZK'].sum() - filtered_df_prev[lookup_prev]['Český export '+growth_from+' CZK'].sum()
    selected_CZ_growth_perc = selected_CZ_growth / filtered_df_prev[lookup_prev]['Český export '+growth_from+' CZK'].sum()
    mcol1.metric("Vybraný český export za rok "+year+"", "{:,.0f}".format(sum(filtered_df[lookup_year]['Český export '+year+' CZK'])/1e9),'miliard CZK' )
    mcol2.metric("Růst vybraného českého exportu mezi lety "+growth_from+" a "+growth_to, "{:,.0f}".format(selected_CZ_growth/1e9), "miliard CZK")
    mcol3.metric("Růst vybraného českého exportu mezi lety "+growth_from+" a "+growth_to, "{:,.1%}".format(selected_CZ_growth_perc), "%")

total_CZ_growth = cz_export_curr - cz_export_prev
total_CZ_growth_perc = total_CZ_growth / cz_export_prev
mcol1.metric("Celkový český export za rok "+year+"", "{:,.0f}".format(cz_total_export/1e9),'miliard CZK' )
mcol2.metric("Růst celkového českého exportu mezi lety "+growth_from+" a "+growth_to, "{:,.0f}".format(total_CZ_growth/1e9), "miliard CZK")
mcol3.metric("Růst celkového českého exportu mezi lety "+growth_from+" a "+growth_to, "{:,.1%}".format(total_CZ_growth_perc), "%")
