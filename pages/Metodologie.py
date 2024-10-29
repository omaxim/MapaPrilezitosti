import streamlit as st

# Title
st.title("Economic Complexity Analysis Documentation")

# 1. Import Libraries and Define Constants
st.subheader("1. Import Libraries and Define Constants")
st.write("""
This section imports the necessary libraries for economic complexity analysis and defines the list of EU country codes, 
which will be used to filter relevant data later in the analysis.
""")
with st.expander("Code"):
    st.code("""
from ecomplexity import ecomplexity
from ecomplexity import proximity
import pandas as pd
EU_iso3  = ["AUT","BEL","BGR","HRV","CYP","CZE","DNK","EST","FIN","FRA","DEU","GRC","HUN","IRL","ITA","LVA","LTU","LUX","MLT","NLD","POL","PRT","ROU","SVK","SVN","ESP","SWE"]
    """, language="python")

# 2. Load and Aggregate Data
st.subheader("2. Load and Aggregate BACI Data")
st.write("""
This step loads the BACI 2022 trade dataset and aggregates export values by year (`t`), country (`i`), and product (`k`). 
ISO3 country codes are then added for easier identification.
""")
with st.expander("Code"):
    st.code("""
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
st.subheader("3. Calculate Complexity and Proximity Matrix")
st.write("""
Using the `ecomplexity` package, this section calculates the economic complexity values and the proximity matrix for each product.
""")
with st.expander("Code"):
    st.code("""
trade_cols = {'time': 'time', 'loc': 'loc', 'prod': 'prod', 'val': 'val'}
cdata = ecomplexity(data, trade_cols)
prox_df = proximity(data, trade_cols)
    """, language="python")

# 4. Add Czech Product Names
st.subheader("4. Add Czech Product Names")
st.write("""
Here, the Czech names for each product (HS6 codes) are merged with English names from the BACI database, filling any missing values.
""")
with st.expander("Code"):
    st.code("""
CzechNames = pd.read_csv('database_addons/CZ_HS6_codes.csv')
EnglishNames = pd.read_csv('BACI/H22/product_codes_HS22_V202401b.csv')
EnglishNames['code'] = pd.to_numeric(EnglishNames['code'], errors="coerce")
classed_cdata = cdata.merge(CzechNames[['HS6','POPIS']], left_on='prod', right_on='HS6', how='left').drop('HS6', axis=1)
classed_cdata = classed_cdata.merge(EnglishNames, left_on='prod', right_on='code', how='left').drop('code', axis=1)
classed_cdata['POPIS'].fillna(classed_cdata['description'], inplace=True)
    """, language="python")

# 5. Calculate Product Space Values
st.subheader("5. Calculate Product Space Values")
st.write("""
This section calculates market concentration (HHI) for products in the global and EU markets, the total export values, and the top EU exporters for each product.
""")
with st.expander("Code"):
    st.code("""
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
st.subheader("6. Calculate Relatedness")
st.write("""
The relatedness measure helps identify products that are similar based on trade patterns, using the methodology from the OEC.
""")
with st.expander("Code"):
    st.code("""
def get_relatedness(country_iso3, year, prox_df, cdata):
    prox_filtered = prox_df[prox_df['time'] == year]
    cdata_filtered = cdata[(cdata['time'] == year) & (cdata['loc'] == country_iso3)]
    merged_df = pd.merge(cdata_filtered, prox_filtered, left_on='prod', right_on='prod_2')
    relatedness_results = merged_df.groupby('prod_1').apply(lambda group: (group['mcp'] * group['proximity']).sum() / group['proximity'].sum())
    return relatedness_results.reset_index().rename(columns={'prod_1': 'prod', 0: 'relatedness'})
    """, language="python")

# Continue with remaining code blocks following the above format.

st.write("This concludes the primary sections of the documentation. The Streamlit application is now interactive, with each code block and its explanation in collapsible sections for ease of use.")
