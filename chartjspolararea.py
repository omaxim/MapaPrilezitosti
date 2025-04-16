import json
import itertools
from variable_names import get_color_discrete_map

def chart_highcharts_variable_pie(filtered_df_2022, filtered_df_2023, total_export_22, total_export_23,
                                  group_field, chart_title="Export růst mezi lety 2022 a 2023",
                                  bottom_text="Data: UN COMTRADE, CEPII, a další"):
    """
    Creates a Highcharts variable pie chart where:
      - The slice angle (y) represents the 2022 export share (for that segment, in CZK).
      - The slice radius (z) represents the percentage growth between 2022 and 2023.
    
    The chart includes:
      - A segment for non-green products (calculated as total exports minus green exports)
        shown in gray.
      - One segment per green category defined by 'group_field'. Colors for these segments are
        drawn from get_color_discrete_map() (with fallback colors if not defined).
      
    Parameters:
      - filtered_df_2022, filtered_df_2023: DataFrames with green product exports.
      - total_export_22, total_export_23: Total exports (for the entire economy) for 2022 and 2023.
      - group_field: Field in the filtered DataFrames (e.g. 'Kategorie') for grouping green products.
      - chart_title: Title of the chart.
      - bottom_text: Subtitle or additional info displayed on the chart.
    
    Returns:
      - A string of HTML/JS code to be rendered by st.components.v1.html().
    """
    # Calculate sums for green products
    green_total_22 = filtered_df_2022['CZ Export 2022 CZK'].sum()
    green_total_23 = filtered_df_2023['CZ Export 2023 CZK'].sum()

    # Non-green exports = Total - Green subset
    non_green_22 = total_export_22 - green_total_22
    non_green_23 = total_export_23 - green_total_23

    # Growth calculation for non-green:
    # Use percentage growth (e.g., 0.15 meaning 15% growth)
    if non_green_22 > 0:
        growth_non_green = (non_green_23 - non_green_22) / non_green_22
    else:
        growth_non_green = 0

    # Build data for variable pie: first segment for non-green, then one per green category.
    data_series = []
    
    # Non-green data point:
    data_series.append({
        "name": "Nenezelené produkty",
        "y": non_green_22,  # Angle determined by the 2022 non-green export share
        "z": growth_non_green,  # Growth as percentage (used to adjust the radius)
        "color": "#CCCCCC"  # Fixed grey color
    })
    
    # Get the set of green categories (union from both years)
    green_cats = sorted(list(set(filtered_df_2022[group_field].unique()).union(
                          set(filtered_df_2023[group_field].unique()))))
    
    # Create a color map from your helper function and a fallback cycle
    color_map = get_color_discrete_map()  # Expecting: { category: color }
    fallback_colors = ["#E63946", "#F4A261", "#2A9D8F", "#264653", "#8A5AAB", "#D67D3E", "#1D3557"]
    fallback_cycle = itertools.cycle(fallback_colors)

    for cat in green_cats:
        # Sum exports for this category in 2022 and 2023:
        export_22 = filtered_df_2022[filtered_df_2022[group_field] == cat]['CZ Export 2022 CZK'].sum()
        export_23 = filtered_df_2023[filtered_df_2023[group_field] == cat]['CZ Export 2023 CZK'].sum()
        
        # Calculate growth for the green category
        if export_22 > 0:
            growth = (export_23 - export_22) / export_22
        else:
            growth = 0
        
        # Append the data point
        data_series.append({
            "name": cat,
            "y": export_22,  # Slice's angle determined by its share of 2022 exports
            "z": growth,     # Growth percentage determines the extra dimension (slice radius)
            "color": color_map.get(cat, next(fallback_cycle))
        })
    
    # Build the Highcharts configuration using the variable pie module.
    # (Highcharts requires highcharts.js, highcharts-more.js, and modules/variable-pie.js)
    chart_config = {
        "chart": {
            "type": "variablepie",
            "height": "700px"
        },
        "title": {
            "text": chart_title,
            "style": {
                "fontSize": "25px"
            }
        },
        "subtitle": {
            "text": bottom_text,
            "align": "center",
            "style": {
                "fontSize": "14px"
            }
        },
        "tooltip": {
            "pointFormatter": (
                "function() { return '<span style=\"color:' + this.color + '\">&#9679;</span> ' +"
                " this.name + ': ' + Highcharts.numberFormat(this.z * 100, 1) + '% růst'; }"
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
    
    # Convert the configuration to JSON
    config_json = json.dumps(chart_config)
    
    # Generate the HTML/JS snippet (including required Highcharts scripts)
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
