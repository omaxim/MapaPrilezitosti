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
      
    Each data point (segment) now also carries additional fields:
      - export22: Export value for 2022.
      - export23: Export value for 2023.
      - growth_abs: Absolute difference (export23 - export22).
      - growth_frac: Growth as a fraction, used for the variable radius.
    
    The tooltip displays all these values, formatting the growth percentage with 1 decimal place.
    
    The chart includes:
      - A segment for non-green products (total minus filtered green) in gray.
      - One segment per green category (using group_field) with their own colors.
    
    Parameters:
      - filtered_df_2022, filtered_df_2023: DataFrames with green product exports.
      - total_export_22, total_export_23: Total exports (entire economy) for 2022 and 2023.
      - group_field: The column (e.g. 'Kategorie') to group green products.
      - chart_title: Title of the chart.
      - bottom_text: Subtitle or footer text.
    
    Returns:
      - A string of HTML/JS code for embedding the Highcharts variable pie chart.
    """
    # Calculate sums for green exports
    green_total_22 = filtered_df_2022['CZ Export 2022 CZK'].sum()
    green_total_23 = filtered_df_2023['CZ Export 2023 CZK'].sum()

    # Non-green export values
    non_green_22 = total_export_22 - green_total_22
    non_green_23 = total_export_23 - green_total_23

    # Growth for non-green (if non_green_22 > 0)
    growth_non_green = (non_green_23 - non_green_22) / non_green_22 if non_green_22 > 0 else 0

    # Build the data series list.
    data_series = []
    
    # First, the non-green segment (fixed gray) with additional properties
    data_series.append({
        "name": "Nenezelené produkty",
        "y": non_green_22,     # 2022 export share (for angle)
        "z": growth_non_green, # Growth fraction for radius
        "color": "#CCCCCC",    # Gray for non-green
        # Extra details for the tooltip:
        "export22": non_green_22,
        "export23": non_green_23,
        "growth_abs": non_green_23 - non_green_22,
        "growth_frac": growth_non_green
    })
    
    # Determine the set of green categories from both years.
    green_cats = sorted(list(set(filtered_df_2022[group_field].unique()).union(
                          set(filtered_df_2023[group_field].unique()))))
    
    color_map = get_color_discrete_map()  # Expecting a dict mapping category to color.
    fallback_colors = ["#E63946", "#F4A261", "#2A9D8F", "#264653", "#8A5AAB", "#D67D3E", "#1D3557"]
    fallback_cycle = itertools.cycle(fallback_colors)
    
    # Process each green category.
    for cat in green_cats:
        export_22 = filtered_df_2022[filtered_df_2022[group_field] == cat]['CZ Export 2022 CZK'].sum()
        export_23 = filtered_df_2023[filtered_df_2023[group_field] == cat]['CZ Export 2023 CZK'].sum()
        growth = (export_23 - export_22) / export_22 if export_22 > 0 else 0
        
        data_series.append({
            "name": cat,
            "y": export_22,  # 2022 export share
            "z": growth,     # Growth fraction for radius
            "color": color_map.get(cat, next(fallback_cycle)),
            # Extra details for tooltip:
            "export22": export_22,
            "export23": export_23,
            "growth_abs": export_23 - export_22,
            "growth_frac": growth
        })
    
    # Build the Highcharts configuration using the variable pie module.
    # The tooltip callback is updated to display all metrics formatted nicely.
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
                "function() { "
                "  var s = '<span style=\"color:' + this.color + '\">&#9679;</span> ' + this.name + ':<br/>' + "
                "          '2022: ' + Highcharts.numberFormat(this.export22, 0) + ' CZK<br/>' + "
                "          '2023: ' + Highcharts.numberFormat(this.export23, 0) + ' CZK<br/>' + "
                "          'Růst: ' + Highcharts.numberFormat(this.growth_abs, 0) + ' CZK (' + "
                "          Highcharts.numberFormat(this.growth_frac * 100, 1) + '%)'; "
                "  return s; "
                "}"
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
    
    # Convert the configuration to JSON.
    config_json = json.dumps(chart_config)
    
    # Generate HTML/JS snippet that loads Highcharts and renders the variable pie chart.
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
