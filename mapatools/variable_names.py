def get_plot_and_hover_display_names(year_placeholder):
    plot_display_names = [
        'Percentil příbuznosti CZ '+year_placeholder+'',
        'Percentil komplexity '+year_placeholder+'',
        'Pořadí Česka na světovém trhu '+year_placeholder+'',
        'Komplexita výrobku (unikátnost) '+year_placeholder+'',
        'Český export '+year_placeholder+' CZK',
        'Český export '+year_placeholder+' USD',
        'Velikost světového trhu '+year_placeholder+' CZK',
        'Velikost světového trhu '+year_placeholder+' USD',
        'Podíl Česka na světovém trhu '+year_placeholder+' %',
        'Koncentrace světového trhu '+year_placeholder+'',
        'Koncentrace evropského exportu '+year_placeholder+'',
    ]

    hover_display_data = [
        'Kód výrobku HS6',
        'Skupina',
        'Podskupina',
        'Název',
        'Příbuznost CZ '+year_placeholder+'',
        'RCA '+year_placeholder+'',
        'EU Největší Exportér '+year_placeholder+'',
        'Komplexita výrobku (unikátnost) '+year_placeholder+'',
        'Český export '+year_placeholder+' CZK',
        'Český export '+year_placeholder+' USD',
        'Pořadí Česka na světovém trhu '+year_placeholder+'',
        'Velikost světového trhu '+year_placeholder+' CZK',
        'Velikost světového trhu '+year_placeholder+' USD',
        'Podíl Česka na světovém trhu '+year_placeholder+' %',
        'Percentil příbuznosti CZ '+year_placeholder+'',
        'Percentil komplexity '+year_placeholder+'',
        'Koncentrace světového trhu '+year_placeholder+'',
        'Koncentrace evropského exportu '+year_placeholder+'',
    ]
    return plot_display_names, hover_display_data


def get_hover_formatting(year):
    no_decimal = [
        'CZ Celkový Export 25-30 CZK',
        'Český export '+year+' CZK',
        'Český export '+year+' USD',
        'Velikost světového trhu '+year+' CZK',
        'Velikost světového trhu '+year+' USD',
        'Percentil příbuznosti CZ '+year+'',
        'Percentil komplexity '+year+'',
        'Pořadí Česka na světovém trhu '+year+''
    ]
    
    # Columns requiring three significant figures and percentage formatting
    two_sigfig = [
        'Příbuznost CZ '+year+'',
        'RCA '+year+'',
        'Koncentrace světového trhu '+year+'',
        'Koncentrace evropského exportu '+year+'',
        'Komplexita výrobku (unikátnost) '+year+'',
    ]
    
    # Columns that should show as percentages
    percentage = [
        'Podíl Česka na světovém trhu '+year+' %',
    ]
    
    texthover = [
        'Skupina',
        'Podskupina',
        'Název',
        'Kód výrobku HS6',
        'EU Největší Exportér '+year+''
    ]
    return no_decimal,two_sigfig,percentage,texthover

def get_hover_data(year,year_placeholder,hover_info,x_axis,y_axis,markersize):
    hover_data = {}
    no_decimal,two_sigfig,percentage,texthover = get_hover_formatting(year)
    
    # Iterate over the columns in hover_info
    hover_info_year = [text.replace(year_placeholder,year) for text in hover_info]
    for col in hover_info_year:
        # If the column is in no_decimal, format with no decimals and thousands separator
        if col in no_decimal:
            hover_data[col] = ':,.0f'  # No decimals, thousands separator
        # If the column is in three_sigfig, format with 3 decimal places
        elif col in two_sigfig:
            hover_data[col] = ':.2f'
        elif col in percentage:
            hover_data[col] = ':.1f'  # Three decimal places, with percentage symbol
        elif col in texthover:
            hover_data[col] = True
        else:
            hover_data[col] = False  # No formatting needed, just show the column
        
    # Ensure x_axis, y_axis, and markersize default to False if not explicitly provided in hover_info
    hover_data.setdefault(markersize, False)
    hover_data.setdefault(x_axis, False)
    hover_data.setdefault(y_axis, False)
    hover_data.setdefault('Skupina', False)
    hover_data.setdefault('Podskupina', False)
    hover_data.setdefault('Název', True)

    return hover_data
