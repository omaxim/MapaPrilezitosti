import streamlit as st
#st.set_page_config(
#    page_title="Mapa Příležitostí",
#    page_icon="favicon.png")
st.logo('logo.svg')
col0,col1, colx = st.columns([1,4, 1])

# Title
col1.title("Economic Complexity Analysis Documentation")

# 1. Import Libraries and Define Constants
col1.subheader("1. Import Libraries and Define Constants")
col1.write("""
This section imports the necessary libraries for economic complexity analysis and defines the list of EU country codes, 
which will be used to filter relevant data later in the analysis.
""")
with col1.expander("Code"):
    col1.code("""
from ecomplexity import ecomplexity
from ecomplexity import proximity
import pandas as pd
EU_iso3  = ["AUT","BEL","BGR","HRV","CYP","CZE","DNK","EST","FIN","FRA","DEU","GRC","HUN","IRL","ITA","LVA","LTU","LUX","MLT","NLD","POL","PRT","ROU","SVK","SVN","ESP","SWE"]
    """, language="python")

# 2. Load and Aggregate Data
col1.subheader("2. Load and Aggregate BACI Data")
col1.write("""
This step loads the BACI 2022 trade dataset and aggregates export values by year (`t`), country (`i`), and product (`k`). 
ISO3 country codes are then added for easier identification.
""")
with col1.expander("Code"):
    col1.code("""
BACI_2022 = pd.read_csv('BACI/H22/BACI_HS22_Y2022_V202401b.csv')
BACI_2022_agg = BACI_2022.groupby(['t', 'i', 'k'], as_index=False).agg({'v': 'sum', 'q': 'sum'})
country_codes = pd.read_csv('BACI/H22/country_codes_V202401b.csv')
BACI_2022_agg = BACI_2022_agg.merge(country_codes, left_on='i', right_on='country_code')
data = pd.DataFrame({
    'time': BACI_2022_agg['t'],
    'loc': BACI_2022_agg['country_iso3'],
    'prod': BACI_2022_agg['k'],
    'val': BACI_2022_agg['v'] * 1000  # Convert to dollars
})
    """, language="python")

# 3. Calculate Complexity and Proximity
col1.subheader("3. Calculate Complexity and Proximity Matrix")
col1.write("""
Using the `ecomplexity` package, this section calculates the economic complexity values and the proximity matrix for each product.
""")
with col1.expander("Code"):
    col1.code("""
trade_cols = {'time': 'time', 'loc': 'loc', 'prod': 'prod', 'val': 'val'}
cdata = ecomplexity(data, trade_cols)
prox_df = proximity(data, trade_cols)
    """, language="python")

# 4. Add Czech Product Names
col1.subheader("4. Add Czech Product Names")
col1.write("""
Here, the Czech names for each product (HS6 codes) are merged with English names from the BACI database, filling any missing values.
""")
with col1.expander("Code"):
    col1.code("""
CzechNames = pd.read_csv('database_addons/CZ_HS6_codes.csv')
EnglishNames = pd.read_csv('BACI/H22/product_codes_HS22_V202401b.csv')
EnglishNames['code'] = pd.to_numeric(EnglishNames['code'], errors="coerce")
classed_cdata = cdata.merge(CzechNames[['HS6','POPIS']], left_on='prod', right_on='HS6', how='left').drop('HS6', axis=1)
classed_cdata = classed_cdata.merge(EnglishNames, left_on='prod', right_on='code', how='left').drop('code', axis=1)
classed_cdata['POPIS'].fillna(classed_cdata['description'], inplace=True)
    """, language="python")

# 5. Calculate Product Space Values
col1.subheader("5. Calculate Product Space Values")
col1.write("""
This section calculates market concentration (HHI) for products in the global and EU markets, the total export values, and the top EU exporters for each product.
""")
with col1.expander("Code"):
    col1.code("""
def calculate_hhi(group):
    market_share = group["val"] / group["val"].sum()
    hhi = (market_share ** 2).sum()
    return hhi

def get_product_space(cdata):
    EU_data = cdata[cdata['loc'].isin(EU_iso3)]
    hhi = cdata.groupby("prod").apply(calculate_hhi).reset_index()
    euhhi = EU_data.groupby("prod").apply(calculate_hhi).reset_index()
    hhi.rename(columns={0: 'hhi'}, inplace=True)
    euhhi.rename(columns={0: 'euhhi'}, inplace=True)
    WorldExport = cdata[['prod', 'val']].groupby('prod').agg(sum).reset_index().rename(columns={'val': 'WorldExport'})
    EUExport = EU_data[['prod', 'val']].groupby('prod').agg(sum).reset_index().rename(columns={'val': 'EUExport'})
    EUTopExporter = EU_data.loc[EU_data.groupby('prod')['val'].idxmax(), ['prod', 'loc']].reset_index(drop=True).rename(columns={'loc': 'EUTopExporter'})
    ProductSpace = WorldExport.merge(EUExport, on='prod').merge(EUTopExporter, on='prod').merge(hhi, on='prod').merge(euhhi, on='prod')
    ProductSpace['EUWorldMarketShare'] = ProductSpace['EUExport'] / ProductSpace['WorldExport']
    return ProductSpace
    """, language="python")

# 6. Calculate Relatedness
col1.subheader("6. Calculate Relatedness")
col1.write("""
The relatedness measure helps identify products that are similar based on trade patterns, using the methodology from the OEC.
""")
with col1.expander("Code"):
    col1.code("""
def get_relatedness(country_iso3, year, prox_df, cdata):
    prox_filtered = prox_df[prox_df['time'] == year]
    cdata_filtered = cdata[(cdata['time'] == year) & (cdata['loc'] == country_iso3)]
    merged_df = pd.merge(cdata_filtered, prox_filtered, left_on='prod', right_on='prod_2')
    relatedness_results = merged_df.groupby('prod_1').apply(lambda group: (group['mcp'] * group['proximity']).sum() / group['proximity'].sum())
    return relatedness_results.reset_index().rename(columns={'prod_1': 'prod', 0: 'relatedness'})
    """, language="python")

# 7. Combine All Data for Country Overview
col1.subheader("7. Combine All Data to Give a Country Overview")
col1.write("""
This function retrieves the economic complexity, market share, relatedness, and product space data for a specific country 
and year. It combines all the calculated values, including world and EU market shares, to give a comprehensive overview.
""")
with col1.expander("Code"):
    col1.code("""
def get_country_data(country_iso3, year, prox_df, cdata):
    output = cdata[(cdata['time'] == year) & (cdata['loc'] == country_iso3)]
    relatedness = get_relatedness(country_iso3, year, prox_df, cdata)
    output = output.merge(relatedness, on='prod')
    ProductSpaceInfo = get_product_space(cdata)
    output = output.merge(ProductSpaceInfo, on='prod').rename(columns={'val': 'ExportValue'})
    output[country_iso3 + '_WorldMarketShare'] = output['ExportValue'] / output['WorldExport']
    
    if country_iso3 in EU_iso3:
        output[country_iso3 + '_EUMarketShare'] = output['ExportValue'] / output['EUExport']
    return output
    """, language="python")

# 8. Calculate Data for Specific Country
col1.subheader("8. Calculate Data for a Specific Country")
col1.write("""
In this example, the `get_country_data` function is used to retrieve data for the Czech Republic (ISO3 code: 'CZE') for the year 2022.
Additional calculations for PCI (Product Complexity Index) ranks and relatedness ranks are added to give further insights.
""")
with col1.expander("Code"):
    col1.code("""
CZE = get_country_data('CZE', 2022, prox_df, classed_cdata)
CZE['PCI_Rank'] = CZE['pci'].rank(ascending=True)
CZE['PCI_Percentile'] = CZE['pci'].rank(ascending=True, pct=True) * 100
CZE['relatedness_Rank'] = CZE['relatedness'].rank(ascending=True)
CZE['relatedness_Percentile'] = CZE['relatedness'].rank(ascending=True, pct=True) * 100
    """, language="python")

# 9. Export Country Data to CSV
col1.subheader("9. Export Country Data to CSV")
col1.write("""
This block exports the Czech Republic's data to a CSV file (`CZE.csv`) for further analysis or record-keeping.
""")
with col1.expander("Code"):
    col1.code("""
CZE.to_csv('CZE.csv')
    """, language="python")

# 10. Import and Merge Green Products Taxonomy
col1.subheader("10. Import and Merge Green Products Taxonomy")
col1.write("""
A taxonomy of green products is loaded from a Google Sheets link, and merged with Czech Republic's export data.
Future export values (2030) are forecasted based on Compound Annual Growth Rate (CAGR) from 2022 to 2030.
""")
with col1.expander("Code"):
    col1.code("""
url = 'https://docs.google.com/spreadsheets/d/1M4_XVEXApUbnklbRwX1dqDVYIDStX4Uk/pub?gid=884468600&single=true&output=csv'
taxonomy = pd.read_csv(url)
GreenProducts = taxonomy.merge(CZE, how='left', left_on='HS_ID', right_on='prod')
GreenProducts['CountryExport2030'] = GreenProducts['ExportValue'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** 8
GreenProducts['EUExport2030'] = GreenProducts['EUExport'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** 8
GreenProducts['CountryExport_25_30'] = sum(GreenProducts['ExportValue'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** i for i in range(3, 9))
GreenProducts['EUExport_25_30'] = sum(GreenProducts['EUExport'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** i for i in range(3, 9))
    """, language="python")

# 11. Rename Columns and Export Green Products Data
col1.subheader("11. Rename Columns and Export Green Products Data")
col1.write("""
For ease of understanding, column names are changed to descriptive labels in Czech. 
The final dataset is exported as `GreenComplexity_CZE_2022.csv`.
""")
with col1.expander("Code"):
    col1.code("""
GreenProducts.rename(columns={'ExportValue': 'CZ Export 2022 CZK',
                              'pci': 'Komplexita výrobku 2022',
                              'relatedness': 'Příbuznost CZ 2022',
                              'WorldExport':'Světový export 2022 CZK',
                              'EUExport':'EU Export 2022 CZK',
                              'EUWorldMarketShare':'EU Světový Podíl 2022 %',
                              'euhhi':'Koncentrace evropského exportu 2022',
                              'hhi':'Koncentrace světového trhu 2022',
                              'CZE_WorldMarketShare':'CZ Světový Podíl 2022 %',
                              'CZE_EUMarketShare':'CZ-EU Podíl 2022 %',
                              'rca':'Výhoda CZ 2022',
                              'EUTopExporter':'EU Největší Exportér 2022',
                              'POPIS':'Název Produktu',
                              'CountryExport2030':'CZ 2030 Export CZK',
                              'EUExport2030':'EU 2030 Export CZK',
                              'CountryExport_25_30':'CZ Celkový Export 25-30 CZK',
                              'EUExport_25_30':'EU Celkový Export 25-30 CZK',
                              'CAGR_2022_30_FORECAST':'CAGR 2022-2030 Předpověď'
                              }).to_csv('GreenComplexity_CZE_2022.csv')
    """, language="python")

# 12. Create Full Product Database
col1.subheader("12. Create Full Product Database")
col1.write("""
This section merges the product space data with Czech and English product names for a complete product database.
The database is then exported to `HS22_Products.csv`.
""")
with col1.expander("Code"):
    col1.code("""
products = get_product_space(classed_cdata)
products = products.merge(CzechNames[['HS6', 'POPIS']], left_on='prod', right_on='HS6', how='left').drop('HS6', axis=1)
products = products.merge(EnglishNames, left_on='prod', right_on='code', how='left').drop('code', axis=1)
products.to_csv('HS22_Products.csv', encoding='utf-8-sig')
    """, language="python")

# 13. Format Descriptions for Display
col1.subheader("13. Format Descriptions for Display")
col1.write("""
In this section, descriptions in the product database are formatted to include line breaks after every 6 words 
to enhance readability. The formatted database is exported as `HS22_Products_br.csv`.
""")
with col1.expander("Code"):
    col1.code("""
def insert_br(text):
    if not isinstance(text, str):
        return text
    words = text.split()
    new_text = []
    for i in range(0, len(words), 6):
        new_text.append(' '.join(words[i:i+6]))
        new_text.append('<br>')
    return ''.join(new_text).rstrip('<br>')

products['POPIS'] = products['POPIS'].apply(insert_br)
products.to_csv('HS22_Products_br.csv', encoding='utf-8-sig')
    """, language="python")