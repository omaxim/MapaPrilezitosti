# Standalone script version of ECIPCI.ipynb — generates CZE complexity outputs from BACI trade data.
# Usage: python ECIPCI.py (run from the BACI_analysis directory)
from ecomplexity import ecomplexity
from ecomplexity import proximity
import pandas as pd
EU_iso3  = ["AUT","BEL","BGR","HRV","CYP","CZE","DNK","EST","FIN","FRA","DEU","GRC","HUN","IRL","ITA","LVA","LTU","LUX","MLT","NLD","POL","PRT","ROU","SVK","SVN","ESP","SWE"]

# --- Load BACI data, aggregate exports and fill in ISO3 country codes ---

VERSION = 'V202601'
YEARS = [2022, 2023, 2024]

# Load and concatenate all years
frames = []
for year in YEARS:
    df = pd.read_csv(f'BACI_HS22_Y{year}_{VERSION}.csv')
    frames.append(df.groupby(['t', 'i', 'k'], as_index=False).agg({'v': 'sum', 'q': 'sum'}))
BACI_agg = pd.concat(frames, ignore_index=True)

country_codes = pd.read_csv(f'country_codes_{VERSION}.csv')
BACI_agg = BACI_agg.merge(country_codes, left_on='i', right_on='country_code')
data = pd.DataFrame({
    'time': BACI_agg['t'],
    'loc': BACI_agg['country_iso3'],
    'prod': BACI_agg['k'],
    'val': (BACI_agg['v'] * 1000)
})

# --- Use ecomplexity to get complexity values and proximity matrix ---

# Calculate complexity
trade_cols = {'time':'time', 'loc':'loc', 'prod':'prod', 'val':'val'}
cdata = ecomplexity(data, trade_cols)
# Calculate proximity matrix
prox_df = proximity(data, trade_cols)

# --- Add Czech names ---

CzechNames = pd.read_csv('CZ_HS6_codes.csv')
EnglishNames = pd.read_csv(f'product_codes_HS22_{VERSION}.csv')
EnglishNames['code'] = pd.to_numeric(EnglishNames['code'], errors="coerce")
classed_cdata = cdata.merge(CzechNames[['HS6','POPIS']],left_on='prod',right_on='HS6',how='left').drop('HS6',axis=1)
classed_cdata = classed_cdata.merge(EnglishNames,left_on='prod',right_on='code',how='left').drop('code',axis=1)
classed_cdata.loc[classed_cdata['POPIS'].isna(), 'POPIS'] = classed_cdata.loc[classed_cdata['POPIS'].isna(), 'description']

# --- Calculate product space values ---

# Function to calculate market concentration
def calculate_hhi(group):
    # Calculate market share of each country's export value for the product
    market_share = group["val"] / group["val"].sum()
    # Square the market shares and sum them to calculate HHI
    hhi = (market_share ** 2).sum()
    return hhi

def get_product_space(cdata):
    # Get EU only data
    EU_data = cdata[cdata['loc'].isin(EU_iso3)]

    # Calculate HHI in the world and in the EU
    hhi = cdata.groupby("prod").apply(calculate_hhi, include_groups=False).reset_index()
    euhhi = EU_data.groupby("prod").apply(calculate_hhi, include_groups=False).reset_index()
    hhi.rename(columns={0:'hhi'}, inplace=True)
    euhhi.rename(columns={0:'euhhi'}, inplace=True)

    # Calculate World and EU export
    WorldExport = cdata[['prod','val']].groupby('prod').agg('sum').reset_index()
    EUExport  = EU_data[['prod','val']].groupby('prod').agg('sum').reset_index()
    WorldExport.rename(columns={'val':'WorldExport'}, inplace=True)
    EUExport.rename(columns={'val':'EUExport'}, inplace=True)

    #Calculate top EU exporter
    EUTopExporter = EU_data.loc[EU_data.groupby('prod')['val'].idxmax(), ['prod', 'loc']].reset_index(drop=True)
    EUTopExporter.rename(columns={'loc':'EUTopExporter'}, inplace=True)

    #Merge all and calculate EU market share
    ProductSpace = WorldExport.merge(EUExport,left_on='prod',right_on='prod')
    ProductSpace = ProductSpace.merge(EUTopExporter,left_on='prod',right_on='prod')
    ProductSpace['EUWorldMarketShare'] = ProductSpace['EUExport']/ProductSpace['WorldExport']
    ProductSpace = ProductSpace.merge(hhi,left_on='prod',right_on='prod')
    ProductSpace = ProductSpace.merge(euhhi,left_on='prod',right_on='prod')
    return ProductSpace

# --- Calculate relatedness ---
# Using the OEC formula https://oec.world/en/resources/methods#relatedness

def get_relatedness(country_iso3, year, prox_df, cdata):
    # Step 1: Filter for the given year
    prox_filtered = prox_df[prox_df['time'] == year]
    cdata_filtered = cdata[cdata['time'] == year]

    # Step 2: Filter cdata by the country
    cdata_filtered = cdata_filtered[cdata_filtered['loc'] == country_iso3]

    # Step 3: Merge proximity data (prod_1 and prod_2) with cdata on 'prod_2' = 'prod'
    merged_df = pd.merge(cdata_filtered, prox_filtered, left_on='prod', right_on='prod_2')

    # Step 4: Group by HS6 code (prod_1) and calculate relatedness for each group
    def calculate_relatedness(group):
        return (group['mcp'] * group['proximity']).sum() / group['proximity'].sum()

    # Step 5: Calculate relatedness for each prod_1
    relatedness_results = merged_df.groupby('prod_1').apply(calculate_relatedness, include_groups=False)
    relatedness_df = relatedness_results.reset_index().rename(columns={'prod_1': 'prod', 0: 'relatedness'})
    return relatedness_df

# --- Combine all data to give a country overview ---

def get_country_data(country_iso3, year, prox_df, cdata):
    # Subset for year and location
    output = cdata[(cdata['time'] == year) & (cdata['loc'] == country_iso3)]

    # Calculate Relatedness and merge
    relatedness = get_relatedness(country_iso3, year, prox_df, cdata)
    output = output.merge(relatedness,left_on='prod',right_on='prod')

    # Merge with ProductSpaceInfo (filter to year so WorldExport is per-year, not summed across all years)
    ProductSpaceInfo = get_product_space(cdata[cdata['time'] == year])
    output = output.merge(ProductSpaceInfo,left_on='prod',right_on='prod')

    # Rename columns
    output = output.rename(columns={'val': 'ExportValue'})

    # Add World and EU Market Share
    output[country_iso3+'_WorldMarketShare'] = output['ExportValue']/output['WorldExport']

    # If country is in the EU calculate EU Market Share
    if country_iso3 in EU_iso3:
        output[country_iso3+'_EUMarketShare'] = output['ExportValue']/output['EUExport']
    return output

# --- Calculate for a given country ---

CZE_by_year = {}
for year in YEARS:
    CZE = get_country_data('CZE', year, prox_df, classed_cdata)

    CZE['PCI_Rank'] = CZE['pci'].rank(ascending=True)
    CZE['PCI_Percentile'] = CZE['pci'].rank(ascending=True, pct=True) * 100
    CZE['relatedness_Rank'] = CZE['relatedness'].rank(ascending=True)
    CZE['relatedness_Percentile'] = CZE['relatedness'].rank(ascending=True, pct=True) * 100
    # Compute CZE's world ranking for each product (rank 1 = top global exporter)
    year_all = cdata[cdata['time'] == year][['prod', 'loc', 'val']]
    world_ranks = year_all.groupby('prod')['val'].rank(ascending=False, method='min')
    cze_world_rank = year_all.assign(WorldRank=world_ranks).query("loc == 'CZE'")[['prod', 'WorldRank']]
    CZE = CZE.merge(cze_world_rank, on='prod', how='left')
    CZE['export_Rank'] = CZE['WorldRank'].fillna(0).astype(int)
    CZE = CZE.drop(columns=['WorldRank'])
    CZE['export_Percentile'] = CZE['export_Rank'].rank(ascending=True, pct=True) * 100

    CZE.to_csv(f'outputs/CZE_{year}.csv')
    CZE_by_year[year] = CZE
    print(f'Saved CZE_{year}.csv')

# Keep the latest year as CZE for downstream cells (Green Products etc.)
CZE = CZE_by_year[YEARS[-1]]

# --- Get Green Products ---

url = 'https://docs.google.com/spreadsheets/d/1M4_XVEXApUbnklbRwX1dqDVYIDStX4Uk/pub?gid=884468600&single=true&output=csv'
taxonomy = pd.read_csv(url)
GreenProducts = taxonomy.merge(CZE,how='left',left_on='HS_ID',right_on='prod')
# Calculate 2030 export value
GreenProducts['CountryExport2030'] = GreenProducts['ExportValue'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** 8
GreenProducts['EUExport2030'] = GreenProducts['EUExport'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** 8

# Calculate Total Export Value from 2025 to 2030
# We calculate for each year and sum up
GreenProducts['CountryExport_25_30'] = sum(GreenProducts['ExportValue'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** i for i in range(3, 9))
GreenProducts['EUExport_25_30'] = sum(GreenProducts['EUExport'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** i for i in range(3, 9))

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

# --- Get Full Product Database ---

products = get_product_space(classed_cdata)
products = products.merge(CzechNames[['HS6','POPIS']],left_on='prod',right_on='HS6',how='left').drop('HS6',axis=1)
products = products.merge(EnglishNames,left_on='prod',right_on='code',how='left').drop('code',axis=1)
products.to_csv('HS22_Products.csv',encoding='utf-8-sig')

import pandas as pd
products = pd.read_csv('HS22_Products.csv')
# Function to insert <br> after 6 words
def insert_br(text):
    if not isinstance(text, str):  # Check if the entry is not a string
        return text  # Return the value as it is (None, float, etc.)

    words = text.split()  # Split text into words
    new_text = []

    for i in range(0, len(words), 6):  # Iterate in steps of 6
        new_text.append(' '.join(words[i:i+6]))  # Join 6 words
        new_text.append('<br>')  # Add <br> tag

    return ''.join(new_text).rstrip('<br>')  # Join everything, remove last <br>

products['POPIS'] = products['POPIS'].apply(insert_br)
products.to_csv('HS22_Products_br.csv',encoding='utf-8-sig')
