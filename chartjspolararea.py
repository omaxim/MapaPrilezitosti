import json
import itertools
from variable_names import get_color_discrete_map

def chart_highcharts_variable_pie(filtered_df_2022, filtered_df_2023, total_export_22, total_export_23,
                                  group_field, chart_title="Export růst mezi lety 2022 a 2023",
                                  bottom_text="Data: UN COMTRADE, CEPII, a další"):
    """
    Creates a Highcharts variable pie chart where:
      - Slice angle (y) represents the export share in 2022.
      - Slice radius (z) represents the percentage growth between 2022 and 2023.
    
    Each data point carries extra fields:
      - export22: Export value for 2022.
      - export23: Export value for 2023.
      - growth_abs: Absolute export difference (export23 - export22).
      - growth_frac: Growth fraction (used for slice radius).
    
    The tooltip displays these values, formatted nicely (growth percentage with one decimal place).
    
    Parameters:
      - filtered_df_2022, filtered_df_2023: DataFrames containing green product exports.
      - total_export_22, total_export_23: Total exports for the entire economy in 2022 and 2023.
      - group_field: Field name (e.g., 'Kategorie') to group green products.
      - chart_title: Title of the chart.
      - bottom_text: Subtitle/footer text for the chart.
    
    Returns:
      - A string containing the HTML/JS snippet to render the Highcharts variable pie chart.
    """
    # Calculate totals for green exports
    green_total_22 = filtered_df_2022['CZ Export 2022 CZK'].sum()
    green_total_23 = filtered_df_2023['CZ Export 2023 CZK'].sum()
    
    # Calculate non-green exports
    non_green_22 = total_export_22 - green_total_22
    non_green_23 = total_export_23 - green_total_23
    
    # Calculate growth for non-green segment (if denominator > 0)
    growth_non_green = (non_green_23 - non_green_22) / non_green_22 if non_green_22 > 0 else 0
    
    # Build the data series. First element for non-green products.
    data_series = []
    
    data_series.append({
        "name": "Nenezelené produkty",
        "y": non_green_22,     # Slice angle determined by 2022 value.
        "z": growth_non_green, # Growth fraction.
        "color": "#CCCCCC",    # Gray.
        # Extra details for tooltip:
        "export22": non_green_22,
        "export23": non_green_23,
        "growth_abs": non_green_23 - non_green_22,
        "growth_frac": growth_non_green
    })
    
    # Build list of green categories from filtered data (both years)
    green_cats = sorted(list(set(filtered_df_2022[group_field].unique()).union(
                          set(filtered_df_2023[group_field].unique()))))
    
    color_map = get_color_discrete_map()  # Expects a dict mapping category -> color.
    fallback_colors = ["#E63946", "#F4A261", "#2A9D8F", "#264653", "#8A5AAB", "#D67D3E", "#1D3557"]
    fallback_cycle = itertools.cycle(fallback_colors)
    
    for cat in green_cats:
        export_22 = filtered_df_2022[filtered_df_2022[group_field] == cat]['CZ Export 2022 CZK'].sum()
        export_23 = filtered_df_2023[filtered_df_2023[group_field] == cat]['CZ Export 2023 CZK'].sum()
        growth = (export_23 - export_22) / export_22 if export_22 > 0 else 0
        
        data_series.append({
            "name": cat,
            "y": export_22,
            "z": growth,
            "color": color_map.get(cat, next(fallback_cycle)),
            "export22": export_22,
            "export23": export_23,
            "growth_abs": export_23 - export_22,
            "growth_frac": growth
        })
    
    # Highcharts configuration with tooltip formatted per the example.
    chart_config = {
        "chart": {
            "type": "variablepie",
            "height": "700px"
        },
        "title": {
            "text": chart_title,
            "style": {"fontSize": "25px"}
        },
        "subtitle": {
            "text": bottom_text,
            "align": "center",
            "style": {"fontSize": "14px"}
        },
        "tooltip": {
            "headerFormat": "",
            "pointFormat": (
                '<span style="color:{point.color}">\u25CF</span> <b>{point.name}</b><br/>' +
                '2022: {point.export22:,.0f} CZK<br/>' +
                '2023: {point.export23:,.0f} CZK<br/>' +
                'Růst: {point.growth_abs:,.0f} CZK ({point.growth_frac:.1%})'
            )
        },
        "series": [{
            "minPointSize": 10,
            "innerSize": "20%",
            "zMin": 0,
            "name": "Export",
            "data": data_series
        }]
    }
    
    config_json = json.dumps(chart_config)
    
    chart_html = f"""
    <div id="container" style="width: 100%; height: 700px;"></div>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/highcharts-more.js"></script>
    <script src="https://code.highcharts.com/modules/variable-pie.js"></script>
    <script>
      document.addEventListener('DOMContentLoaded', function () {{
        Highcharts.chart('container', {config_json});
      }});
    </script>
    """
    
    return chart_html
