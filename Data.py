import streamlit as st
import pandas as pd

from chartjsbubble import chartjs_plot
from variable_names import get_color_discrete_map, get_plot_and_hover_display_names, get_hover_data
import streamlit.components.v1 as components
from visualsetup import load_visual_identity

st.set_page_config(
    page_title="Mapa Příležitostí",
    page_icon="logo_notext.svg",
    layout="wide"
)
#Loading loads of custom css in markdown
load_visual_identity("header.jpg")

st.logo('logo_notext.svg',size='large',icon_image='logo_notext.svg')
logocol1,logocol2 = st.columns([2,3])
logocol1.image('logo_text.svg',use_container_width=True)
logocol2.text("")
logocol2.text("")
p1,p2,p3,p4,p5,p6,p7 = logocol2.columns(7)
p1.image('partners/01.png',use_container_width=True)
p2.image('partners/02.png',use_container_width=True)
p3.image('partners/03.png',use_container_width=True)
p4.image('partners/04.png',use_container_width=True)
p5.image('partners/05.png',use_container_width=True)
p6.image('partners/06.png',use_container_width=True)
p7.image('partners/07.png',use_container_width=True)

col1,col2, = st.columns([12,4])
col1.subheader("")
col2.subheader("")
col2.subheader("Nastavení grafu")



year = col2.segmented_control("Rok",["2022","2023"],default="2023")
def USDtoCZKdefault(year):
    if year=="2022":
        return 23.360
    elif year=="2023":
        return 22.21

# Load data
@st.cache_data
def load_data(datayear):
    USD_to_czk = USDtoCZKdefault(datayear)
    # Replace with the path to your data file
    #df                          = pd.read_csv('GreenComplexity_CZE_2022.csv')
    url = 'https://docs.google.com/spreadsheets/d/1mhv7sJC5wSqJRXdfyFaWtBuEpX6ENj2c/gviz/tq?tqx=out:csv'
    taxonomy = pd.read_csv(url)
    CZE = pd.read_csv('CZE_'+datayear+'.csv')
    GreenProducts = taxonomy.merge(CZE,how='left',left_on='HS_ID',right_on='prod')
    # Calculate 2030 export value
    GreenProducts['CountryExport2030'] = GreenProducts['ExportValue'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** 8
    GreenProducts['EUExport2030'] = GreenProducts['EUExport'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** 8

    # Calculate Total Export Value from 2025 to 2030
    # We calculate for each datayear and sum up
    GreenProducts['CountryExport_25_30'] = sum(GreenProducts['ExportValue'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** i for i in range(3, 9))
    GreenProducts['EUExport_25_30'] = sum(GreenProducts['EUExport'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** i for i in range(3, 9))

    df = GreenProducts.rename(columns={'ExportValue': 'CZ Export '+datayear+' CZK',
                               'export_Rank':'Žebříček exportu CZ '+datayear+'',
                               'pci': 'Komplexita výrobku '+datayear+'',
                               'relatedness': 'Příbuznost CZ '+datayear+'',
                               'PCI_Rank':'Žebříček komplexity '+datayear+'',
                               'PCI_Percentile':'Percentil komplexity '+datayear+'',
                               'relatedness_Rank':'Žebříček příbuznosti CZ '+datayear+'',
                               'relatedness_Percentile':'Percentil příbuznosti CZ '+datayear+'',
                               'WorldExport':'Světový export '+datayear+' CZK',
                               'EUExport':'EU Export '+datayear+' CZK',
                               'EUWorldMarketShare':'EU Světový Podíl '+datayear+' %',
                               'euhhi':'Koncentrace evropského exportu '+datayear+'',
                               'hhi':'Koncentrace světového trhu '+datayear+'',
                               'CZE_WorldMarketShare':'CZ Světový Podíl '+datayear+' %',
                               'CZE_EUMarketShare':'CZ-EU Podíl '+datayear+' %',
                               'rca':'Výhoda CZ '+datayear+'',
                               'EUTopExporter':'EU Největší Exportér '+datayear+'',
                               'CZ_Nazev':'Název',
                               'CountryExport2030':'CZ 2030 Export CZK',
                               'EUExport2030':'EU 2030 Export CZK',
                               'CountryExport_25_30':'CZ Celkový Export 25-30 CZK',
                               'EUExport_25_30':'EU Celkový Export 25-30 CZK',
                               'CAGR_2022_30_FORECAST':'CAGR 2022-2030 Předpověď'
                               })
    df                          = df[df.Included == "IN"]
    df['stejna velikost']       = 0.02
    df['CZ-EU Podíl '+datayear+' %']      = 100 * df['CZ-EU Podíl '+datayear+' %'] 
    df['EU Světový Podíl '+datayear+' %'] = 100 * df['EU Světový Podíl '+datayear+' %'] 
    df['CZ Světový Podíl '+datayear+' %'] = 100 * df['CZ Světový Podíl '+datayear+' %'] 
    df['CZ Export '+datayear+' CZK']        = USD_to_czk*df['CZ Export '+datayear+' CZK'] 
    df['Světový export '+datayear+' CZK']      = USD_to_czk*df['Světový export '+datayear+' CZK'] 
    df['EU Export '+datayear+' CZK']        = USD_to_czk*df['EU Export '+datayear+' CZK'] 
    df['EU Celkový Export 25-30 CZK'] = USD_to_czk*df['EU Celkový Export 25-30 CZK'] 
    df['CZ Celkový Export 25-30 CZK'] = USD_to_czk*df['CZ Celkový Export 25-30 CZK'] 
    df['EU 2030 Export CZK']        = USD_to_czk*df['EU 2030 Export CZK'] 
    df['CZ 2030 Export CZK']        = USD_to_czk*df['CZ 2030 Export CZK'] 
    df['HS_ID']                 = df['HS_ID'].astype(str)
    df['HS_Lookup']              = df['HS_ID']+" - "+df['Název']
    
    st.sidebar.info(str(GreenProducts.shape[0]) + " HS6 načteno, z toho " +str(df.shape[0])+" je IN")
    return df


# Create lists of display names for the sidebar
year_placeholder = " ‎"
plot_display_names, hover_display_data = get_plot_and_hover_display_names(year_placeholder)
# Sidebar selection boxes using display names
x_axis      = col2.selectbox("Vyber osu X:", plot_display_names, index=4)
y_axis      = col2.selectbox("Vyber osu Y:", plot_display_names, index=5)
markersize  = col2.selectbox("Velikost dle:", plot_display_names, index=10)

df_2022 = load_data("2022")
df_2023 = load_data("2023")

if year=="2022":
    df = df_2022
if year=="2023":
    df = df_2023

# Apply filters to dataframe
filtered_df = df.copy()

# Initialize session state
if 'filtrovat_dle_skupin' not in st.session_state:
    st.session_state.filtrovat_dle_skupin = False
    skupiny = df['Skupina'].unique()

# Handle initial value for selected Skupina
if 'selected_skupina' not in st.session_state or st.session_state.selected_skupina not in skupiny:
    st.session_state.selected_skupina = skupiny[5]

with col2:
    # Show current filter mode as a label
    current_mode = "✅ Všechny zelené produkty" if st.session_state.filtrovat_dle_skupin else "🧩 Jednotlivé skupiny"
    st.markdown(f"**Aktuální režim:** {current_mode}")

    # Fixed label button, with a key
    if st.button("Přepnout režim", use_container_width=True, key="toggle_filter_button"):
        st.session_state.filtrovat_dle_skupin = not st.session_state.filtrovat_dle_skupin

if st.session_state.filtrovat_dle_skupin:
    color       = 'Kategorie'
    Skupina = col2.segmented_control(
    'Skupina',
    skupiny,
    default=skupiny.tolist().index(st.session_state.selected_skupina),
    key='selected_skupina')
    filtered_df = filtered_df[filtered_df['Skupina'].isin([Skupina])]
    # Assign it back to session_state to persist between reruns
    st.session_state.selected_skupina = Skupina
else:
    color       = 'Skupina'


hover_info  = col2.multiselect("Co se zobrazí při najetí myší:", hover_display_data, default=['Název'])
col2.divider()
# Filter section
if 'filters' not in st.session_state:
    st.session_state.filters = []

subcol1, subcol2 = col2.columns(2)
with subcol1:
    if st.button("Filtrování hodnot", use_container_width=True):
        st.session_state.filters.append({'column': None, 'range': None})
with subcol2:
    if st.button("Odstranit filtry", use_container_width=True):
        st.session_state.filters = []

# Display existing filters using display names
for i, filter in enumerate(st.session_state.filters):
    filter_col= col2.selectbox(f"Filtr {i+1}", plot_display_names, key=f"filter_col_{i}")
    filter_min, filter_max = df[filter_col.replace(year_placeholder,year)].min(), df[filter_col.replace(year_placeholder,year)].max()
    filter_range = col2.slider(f"Filtr {i+1}", float(filter_min), float(filter_max), (float(filter_min), float(filter_max)), key=f"filter_range_{i}")
    st.session_state.filters[i]['column'] = filter_col
    st.session_state.filters[i]['range'] = filter_range

# Apply numerical filters
for filter in st.session_state.filters:
    if filter['column'] is not None and filter['range'] is not None:
        filtered_df = filtered_df[
            (filtered_df[filter['column'].replace(year_placeholder,year)] >= filter['range'][0]) &
            (filtered_df[filter['column'].replace(year_placeholder,year)] <= filter['range'][1])
        ]

markersize = markersize.replace(year_placeholder,year)
x_axis = x_axis.replace(year_placeholder,year)
y_axis = y_axis.replace(year_placeholder,year)

# Replace negative values in markersize column with zero
filtered_df[markersize] = filtered_df[markersize].clip(lower=0)

# Remove NA values
filtered_df = filtered_df.dropna(subset=[x_axis, y_axis, color, markersize])


HS_select = st.multiselect("Filtrovat HS6 kódy",filtered_df['HS_Lookup'])

# Create a button in the sidebar that clears the cache
if st.sidebar.button('Obnovit Data'):
    load_data.clear()  # This will clear the cache for the load_data function
    st.sidebar.write("Sušenky vyčištěny!")
# Initialize the hover_data dictionary with default values of False for x, y, and markersize
#hover_data = {col: True for col in hover_info}
hover_data = get_hover_data(year,year_placeholder,hover_info,x_axis,y_axis,markersize)

bottom_text =  "Analýza je založená na obchodních datech UN COMTRADE, která jsou vyčištěna organizací CEPII a publikována každý rok jako dataset BACI"
if st.session_state.filtrovat_dle_skupin is False:
    if HS_select == []:
        chart_js = chartjs_plot(filtered_df,markersize,hover_data,color,x_axis,y_axis,year,chart_title="České zelené příležitosti", bottom_text=bottom_text)
    else:
        chart_js = chartjs_plot(filtered_df[filtered_df['HS_Lookup'].isin(HS_select)],markersize,hover_data,color,x_axis,y_axis,year,chart_title="České zelené příležitosti", bottom_text=bottom_text)
elif st.session_state.filtrovat_dle_skupin is True and Skupina is None:
    chart_js = None
elif st.session_state.filtrovat_dle_skupin is True and Skupina is not None:
    if HS_select == []:
        chart_js = chartjs_plot(filtered_df,markersize,hover_data,color,x_axis,y_axis,year,chart_title=Skupina, bottom_text=bottom_text)
    else:
        chart_js = chartjs_plot(filtered_df[filtered_df['HS_Lookup'].isin(HS_select)],markersize,hover_data,color,x_axis,y_axis,year,chart_title=Skupina, bottom_text=bottom_text)

# Render the chart in Streamlit
html_bytes=chart_js
with col1:
    components.html(chart_js, height=800)

mcol1, mcol2, mcol3 = st.columns(3)
if HS_select == []:
    mcol1.metric("Vybraný český export za rok "+year+"", "{:,.0f}".format(sum(filtered_df['CZ Export '+year+' CZK'])/1000000000),'miliard CZK' )
    mcol2.metric("Vybraný český export 2025 až 2030", "{:,.0f}".format(sum(filtered_df['CZ Celkový Export 25-30 CZK'])/1000000000), "miliard CZK")
    mcol3.metric("Vybraný evropský export 2025 až 2030", "{:,.0f}".format(sum(filtered_df['EU Celkový Export 25-30 CZK'])/1000000000), "miliard CZK")

else:
    mcol1.metric("Vybraný český export za rok "+year+"", "{:,.0f}".format(sum(filtered_df[filtered_df['HS_Lookup'].isin(HS_select)]['CZ Export '+year+' CZK'])/1000000),'milionů CZK' )
    mcol2.metric("Vybraný český export 2025 až 2030", "{:,.0f}".format(sum(filtered_df[filtered_df['HS_Lookup'].isin(HS_select)]['CZ Celkový Export 25-30 CZK'])/1000000), "milionů CZK")
    mcol3.metric("Vybraný evropský export 2025 až 2030", "{:,.0f}".format(sum(filtered_df[filtered_df['HS_Lookup'].isin(HS_select)]['EU Celkový Export 25-30 CZK'])/1000000), "milionů CZK")



if st.session_state.filtrovat_dle_skupin is True and Skupina is None:
    pass
else:    
    col2.download_button(
        label = "Stáhnout HTML",
        data = html_bytes,
        file_name = "plot.html",
        mime="text/html",
        use_container_width=True
    )

