import streamlit as st
import pandas as pd

from mapatools.chartjsbubble import chartjs_plot
from mapatools.highchartpolararea import chart_highcharts_variable_pie
from mapatools.variable_names import get_color_discrete_map, get_plot_and_hover_display_names, get_hover_data
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
year = col2.segmented_control("Rok", ["2022", "2023"], default="2023")
topsubcol2 = col2.container()
def USDtoCZKdefault(year):
    if year == "2022":
        return 23.360
    elif year == "2023":
        return 22.21

@st.cache_data
def load_data(datayear):
    USD_to_czk = USDtoCZKdefault(datayear)
    url = 'https://docs.google.com/spreadsheets/d/1mhv7sJC5wSqJRXdfyFaWtBuEpX6ENj2c/gviz/tq?tqx=out:csv'
    taxonomy = pd.read_csv(url)
    CZE = pd.read_csv('BACI_analysis/outputs/CZE_' + datayear + '.csv')
    GreenProducts = taxonomy.merge(CZE, how='left', left_on='HS_ID', right_on='prod')
    # Calculate export forecasts
    GreenProducts['CountryExport2030'] = GreenProducts['ExportValue'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** 8
    GreenProducts['EUExport2030'] = GreenProducts['EUExport'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** 8
    GreenProducts['CountryExport_25_30'] = sum(GreenProducts['ExportValue'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** i for i in range(3, 9))
    GreenProducts['EUExport_25_30'] = sum(GreenProducts['EUExport'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** i for i in range(3, 9))
    
    df = GreenProducts.rename(columns={
        'ExportValue': 'CZ Export ' + datayear + ' CZK',
        'export_Rank': 'Žebříček exportu CZ ' + datayear,
        'pci': 'Komplexita výrobku ' + datayear,
        'relatedness': 'Příbuznost CZ ' + datayear,
        'PCI_Rank': 'Žebříček komplexity ' + datayear,
        'PCI_Percentile': 'Percentil komplexity ' + datayear,
        'relatedness_Rank': 'Žebříček příbuznosti CZ ' + datayear,
        'relatedness_Percentile': 'Percentil příbuznosti CZ ' + datayear,
        'WorldExport': 'Světový export ' + datayear + ' CZK',
        'EUExport': 'EU Export ' + datayear + ' CZK',
        'EUWorldMarketShare': 'EU Světový Podíl ' + datayear + ' %',
        'euhhi': 'Koncentrace evropského exportu ' + datayear,
        'hhi': 'Koncentrace světového trhu ' + datayear,
        'CZE_WorldMarketShare': 'CZ Světový Podíl ' + datayear + ' %',
        'CZE_EUMarketShare': 'CZ-EU Podíl ' + datayear + ' %',
        'rca': 'Výhoda CZ ' + datayear,
        'EUTopExporter': 'EU Největší Exportér ' + datayear,
        'CZ_Nazev': 'Název',
        'CountryExport2030': 'CZ 2030 Export CZK',
        'EUExport2030': 'EU 2030 Export CZK',
        'CountryExport_25_30': 'CZ Celkový Export 25-30 CZK',
        'EUExport_25_30': 'EU Celkový Export 25-30 CZK',
        'CAGR_2022_30_FORECAST': 'CAGR 2022-2030 Předpověď'
    })
    df = df[df.Included == "IN"]
    df['CZ-EU Podíl ' + datayear + ' %'] = 100 * df['CZ-EU Podíl ' + datayear + ' %']
    df['EU Světový Podíl ' + datayear + ' %'] = 100 * df['EU Světový Podíl ' + datayear + ' %']
    df['CZ Světový Podíl ' + datayear + ' %'] = 100 * df['CZ Světový Podíl ' + datayear + ' %']
    df['CZ Export ' + datayear + ' CZK'] = USD_to_czk * df['CZ Export ' + datayear + ' CZK']
    df['Světový export ' + datayear + ' CZK'] = USD_to_czk * df['Světový export ' + datayear + ' CZK']
    df['EU Export ' + datayear + ' CZK'] = USD_to_czk * df['EU Export ' + datayear + ' CZK']
    df['EU Celkový Export 25-30 CZK'] = USD_to_czk * df['EU Celkový Export 25-30 CZK']
    df['CZ Celkový Export 25-30 CZK'] = USD_to_czk * df['CZ Celkový Export 25-30 CZK']
    df['EU 2030 Export CZK'] = USD_to_czk * df['EU 2030 Export CZK']
    df['CZ 2030 Export CZK'] = USD_to_czk * df['CZ 2030 Export CZK']
    df['HS_ID'] = df['HS_ID'].astype(str)
    df['HS_Lookup'] = df['HS_ID'] + " - " + df['Název']
    total_cz_export = USD_to_czk * CZE['ExportValue'].sum()
    total_cz_green_export = df['CZ Export ' + datayear + ' CZK'].sum()
    return df, total_cz_export, total_cz_green_export

# Define the default year_placeholder and get plotting lists
year_placeholder = " ‎"
plot_display_names, hover_display_data = get_plot_and_hover_display_names(year_placeholder)

# Sidebar selection boxes using display names
x_axis = col2.selectbox("Vyber osu X:", plot_display_names, index=2)
y_axis = col2.selectbox("Vyber osu Y:", plot_display_names, index=3)
markersize = col2.selectbox("Velikost dle:", plot_display_names, index=8)

# Load datasets for both years
df_2022, cz_export_22, cz_green_export_22 = load_data("2022")
df_2023, cz_export_23, cz_green_export_23 = load_data("2023")
if year == "2022":
    df = df_2022
    cz_total_export = cz_export_22
    cz_total_green_export = cz_export_22
else:
    df = df_2023
    cz_total_export = cz_export_23
    cz_total_green_export = cz_export_23
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
    cur_df = df_2022 if year == "2022" else df_2023
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

# Calculate filtered data for both years
filtered_df_2022 = apply_filters(df_2022, "2022", x_axis, y_axis, color, markersize)
filtered_df_2023 = apply_filters(df_2023, "2023", x_axis, y_axis, color, markersize)
filtered_df = filtered_df_2022 if year == "2022" else filtered_df_2023

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
    components.html(chart_js, height=800)

# Example: render the polar area chart in a Streamlit component
polar_js_skupiny = chart_highcharts_variable_pie(filtered_df_2022, filtered_df_2023, cz_export_22,cz_export_23,cz_green_export_22,cz_green_export_23,
                              group_field="Skupina",
                              chart_title="Růst exportu dle skupiny",
                              bottom_text="Šířka koláče vyjadřuje % z celkového českého exportu v roce 2023<br>Vzdálenost dílu koláče od středu vyjadřuje růst skupiny mezi lety 2022 a 2023",
                              usd_to_czk_22=USDtoCZKdefault("2022"),
                              usd_to_czk_23=USDtoCZKdefault("2023"))
polar_js_kategorie = chart_highcharts_variable_pie(filtered_df_2022, filtered_df_2023, cz_export_22,cz_export_23,cz_green_export_22,cz_green_export_23,
                              group_field="Kategorie",
                              chart_title="Růst zeleného exportu dle kategorie",
                              bottom_text="Šířka koláče vyjadřuje % z českého zeleného exportu v roce 2023<br>Vzdálenost dílu koláče od středu vyjadřuje růst kategorie mezi lety 2022 a 2023",
                              usd_to_czk_22=USDtoCZKdefault("2022"),
                              usd_to_czk_23=USDtoCZKdefault("2023"),
                              relative_to_green_only=True)


# Comparison columns - now you can compare metrics between 2022 and 2023
if HS_select == []:
    pie1,pie2 = st.columns(2)
    with pie1:
        st.components.v1.html(polar_js_skupiny, height=690)
    with pie2:
        st.components.v1.html(polar_js_kategorie, height=690)
    st.divider()
    mcol1, mcol2, mcol3, = st.columns(3)
    selected_CZ_growth = filtered_df_2023['CZ Export 2023 CZK'].sum()/USDtoCZKdefault("2023") - filtered_df_2022['CZ Export 2022 CZK'].sum()/USDtoCZKdefault("2022")
    selected_CZ_growth_perc = selected_CZ_growth/(filtered_df_2022['CZ Export 2022 CZK'].sum()/USDtoCZKdefault("2022"))
    mcol1.metric("Vybraný český export za rok "+year+"", "{:,.0f}".format(sum(filtered_df['CZ Export '+year+' CZK'])/1e9),'miliard CZK' )
    mcol2.metric("Růst vybraného českého exportu mezi lety 2022 a 2023", "{:,.0f}".format(selected_CZ_growth/1e6), "milionů USD")
    mcol3.metric("Růst vybraného českého exportu mezi lety 2022 a 2023", "{:,.1%}".format(selected_CZ_growth_perc), "%")


else:
    mcol1, mcol2, mcol3, = st.columns(3)
    lookup_year = filtered_df['HS_Lookup'].isin(HS_select)
    lookup_22 = filtered_df_2022['HS_Lookup'].isin(HS_select)
    lookup_23 = filtered_df_2023['HS_Lookup'].isin(HS_select)
    selected_CZ_growth = filtered_df_2023[lookup_23]['CZ Export 2023 CZK'].sum()/USDtoCZKdefault("2023") - filtered_df_2022[lookup_22]['CZ Export 2022 CZK'].sum()/USDtoCZKdefault("2022")
    selected_CZ_growth_perc = selected_CZ_growth/(filtered_df_2022[lookup_22]['CZ Export 2022 CZK'].sum()/USDtoCZKdefault("2022"))
    mcol1.metric("Vybraný český export za rok "+year+"", "{:,.0f}".format(sum(filtered_df[lookup_year]['CZ Export '+year+' CZK'])/1e6),'milionů CZK' )
    mcol2.metric("Růst vybraného českého exportu mezi lety 2022 a 2023", "{:,.0f}".format(selected_CZ_growth/1e6), "milionů USD")
    mcol3.metric("Růst vybraného českého exportu mezi lety 2022 a 2023", "{:,.1%}".format(selected_CZ_growth_perc), "%")

total_CZ_growth = cz_export_23/USDtoCZKdefault("2023") - cz_export_22/USDtoCZKdefault("2022")
total_CZ_growth_perc = total_CZ_growth/(cz_export_22/USDtoCZKdefault("2022"))
mcol1.metric("Celkový český export za rok "+year+"", "{:,.0f}".format(cz_total_export/1e9),'miliard CZK' )
mcol2.metric("Růst celkového českého exportu mezi lety 2022 a 2023", "{:,.0f}".format(total_CZ_growth/1e9), "miliard USD")
mcol3.metric("Růst celkového českého exportu mezi lety 2022 a 2023", "{:,.1%}".format(total_CZ_growth_perc), "%")
