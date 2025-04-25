def get_plot_and_hover_display_names(year_placeholder):
    plot_display_names = [
        'Koncentrace světového trhu '+year_placeholder+'',
        'Koncentrace evropského exportu '+year_placeholder+'',
        'Percentil příbuznosti CZ '+year_placeholder+'',
        'Percentil komplexity '+year_placeholder+'',
        'Žebříček exportu CZ '+year_placeholder+'',
        'Žebříček příbuznosti CZ '+year_placeholder+'',
        'Žebříček komplexity '+year_placeholder+'',
        'Komplexita výrobku '+year_placeholder+'',
        'CZ Export '+year_placeholder+' CZK',
        'Světový export '+year_placeholder+' CZK',
        'EU Export '+year_placeholder+' CZK',
        'CZ Světový Podíl '+year_placeholder+' %',
        'CZ-EU Podíl '+year_placeholder+' %',
    ]

    hover_display_data = [
        'HS_ID',
        'Skupina',
        'Podskupina',
        'Název',
        'Příbuznost CZ '+year_placeholder+'',
        'Výhoda CZ '+year_placeholder+'',
        'Koncentrace světového trhu '+year_placeholder+'',
        'Koncentrace evropského exportu '+year_placeholder+'',
        'EU Největší Exportér '+year_placeholder+'',
        'Komplexita výrobku '+year_placeholder+'',
        'CZ Export '+year_placeholder+' CZK',
        'Žebříček exportu CZ '+year_placeholder+'',
        'Světový export '+year_placeholder+' CZK',
        'EU Export '+year_placeholder+' CZK',
        'EU Světový Podíl '+year_placeholder+' %',
        'CZ Světový Podíl '+year_placeholder+' %',
        'CZ-EU Podíl '+year_placeholder+' %',
        'Percentil příbuznosti CZ '+year_placeholder+'',
        'Percentil komplexity '+year_placeholder+'',
        'Žebříček příbuznosti CZ '+year_placeholder+'',
        'Žebříček komplexity '+year_placeholder+'',
    ]
    return plot_display_names, hover_display_data


def get_hover_formatting(year):
    no_decimal = [
        'HS_ID',
        'CZ Celkový Export 25-30 CZK',
        'CZ Export '+year+' CZK',
        'Světový export '+year+' CZK',
        'EU Export '+year+' CZK',
        'Žebříček příbuznosti CZ '+year+'',
        'Žebříček komplexity '+year+'',
        'Percentil příbuznosti CZ '+year+'',
        'Percentil komplexity '+year+'',
        'Žebříček exportu CZ '+year+''
    ]
    
    # Columns requiring three significant figures and percentage formatting
    two_sigfig = [
        'Příbuznost CZ '+year+'',
        'Výhoda CZ '+year+'',
        'Koncentrace světového trhu '+year+'',
        'Koncentrace evropského exportu '+year+'',
        'Komplexita výrobku '+year+'',
    ]
    
    # Columns that should show as percentages
    percentage = [
        'EU Světový Podíl '+year+' %',
        'CZ Světový Podíl '+year+' %',
        'CZ-EU Podíl '+year+' %',
    ]
    
    texthover = [
        'Skupina',
        'Podskupina',
        'Název',
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
