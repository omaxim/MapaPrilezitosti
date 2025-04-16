import json
import itertools
from variable_names import get_color_discrete_map

def chart_highcharts_variable_pie(filtered_df_2022, filtered_df_2023, total_export_22, total_export_23,
                                  group_field, chart_title="Export růst mezi lety 2022 a 2023",
                                  bottom_text="Data: UN COMTRADE, CEPII, a další"):
    """
    Creates a Highcharts variable pie chart where:
      - Slice angle (y) represents the export share for 2022.
      - Slice radius (z) represents the percentage growth between 2022 and 2023.
      
    The chart displays:
      - A segment for non-green products (total exports minus green exports) in gray.
      - One segment per green category (as defined by group_field), using colors from your discrete map.
    
    The tooltip now shows the growth percentage with 1 decimal place.
    
    Parameters:
      - filtered_df_2022, filtered_df_2023: DataFrames with green product exports.
      - total_export_22, total_export_23: Total exports (for the entire economy) for 2022 and 2023.
      - group_field: Field name (e.g., 'Kategorie') to group green products.
      - chart_title: Title of the chart.
      - bottom_text: Subtitle or footer text displayed on the chart.
    
    Returns:
      - A string containing HTML/JS code to render the chart.
    """
    # Sum up green exports from filtered data
    green_total_22 = filtered_df_2022['CZ Export 2022 CZK'].sum()
    green_total_23 = filtered_df_2023['CZ Export 2023 CZK'].sum()

    # Non-green exports = Total - Green
    non_green_22 = total_export_22 - green_total_22
    non_green_23 = total_export_23 - green_total_23

    # Calculate growth for non-green as a fraction (e.g., 0.15 for 15%)
    growth_non_green = (non_green_23 - non_green_22) / non_green_22 if non_green_22 else 0

    # Begin building the data series: first element for non-green, then per green category.
    data_series = []
    
    # Non-green segment (displayed in gray)
    data_series.append({
        "name": "Nenezelené produkty",
        "y": non_green_22,  # Determines slice angle based on 2022 share
        "z": growth_non_green,  # Growth percentage for the radius
        "color": "#CCCCCC"
    })
    
    # Determine all green categories from both years
    green_cats = sorted(list(set(filtered_df_2022[group_field].unique()).union(
                          set(filtered_df_2023[group_field].unique()))))
    
    # Get color mapping and fallback colors
    color_map = get_color_discrete_map()  # Expected dict mapping category to color
    fallback_colors = ["#E63946", "#F4A261", "#2A9D8F", "#264653", "#8A5AAB", "#D67D3E", "#1D3557"]
    fallback_cycle = itertools.cycle(fallback_colors)
    
    for cat in green_cats:
        export_22 = filtered_df_2022[filtered_df_2022[group_field] == cat]['CZ Export 2022 CZK'].sum()
        export_23 = filtered_df_2023[filtered_df_2023[group_field] == cat]['CZ Export 2023 CZK'].sum()
        
        growth = (export_23 - export_22) / export_22 if export_22 else 0
        
        data_series.append({
            "name": cat,
            "y": export_22,
            "z": growth,
            "color": color_map.get(cat, next(fallback_cycle))
        })
    
    # Build the Highcharts configuration
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
            "pointFormatter": (
                "function() { return '<span style=\"color:' + this.color + '\">&#9679;</span> ' + "
                "this.name + ': ' + Highcharts.numberFormat(this.z * 100, 1) + '% růst'; }"
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
    
    # Convert configuration to JSON
    config_json = json.dumps(chart_config)
    
    # Produce the HTML/JS snippet with required Highcharts modules
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
