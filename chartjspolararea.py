import json
import itertools
from variable_names import get_color_discrete_map

def chartjs_polar_area(filtered_df_2022, filtered_df_2023, total_export_22, total_export_23, 
                       group_field, chart_title="Export růst mezi lety 2022 a 2023", 
                       bottom_text="Data: UN COMTRADE, CEPII, a další"):
    """
    Create a polar area chart using Chart.js that compares export growth (% difference relative to total 2022 exports)
    for non-green products versus green products per category (as defined by group_field).

    Parameters:
      - filtered_df_2022, filtered_df_2023: DataFrames containing the green product subset for years 2022 and 2023.
      - total_export_22, total_export_23: Totals (for the entire economy) for the years 2022 and 2023, respectively.
      - group_field: The column name to group filtered_df (e.g. 'Kategorie' or 'Skupina').
      - chart_title: Title to display on the chart.
      - bottom_text: Subtitle text to display on the chart.

    The function calculates growth as:
         (value_2023 - value_2022) / total_export_22

    It computes this separately for:
      1) Non-green: total exports minus green exports.
      2) Each green category present in the filtered datasets.
      
    Returns:
      - HTML/JS code (as a string) for embedding the Chart.js polar area chart.
    """
    # Sum of green exports from filtered data in each year
    green_total_22 = filtered_df_2022['CZ Export 2022 CZK'].sum()
    green_total_23 = filtered_df_2023['CZ Export 2023 CZK'].sum()

    # Non-green exports for each year
    non_green_22 = total_export_22 - green_total_22
    non_green_23 = total_export_23 - green_total_23

    # Calculate growth for non-green segment (relative to total_export_22)
    growth_non_green = (non_green_23 - non_green_22) / total_export_22 if total_export_22 else 0

    # Build set of green categories from filtered data (union of both years)
    categories = sorted(list(set(filtered_df_2022[group_field].unique()).union(
                               set(filtered_df_2023[group_field].unique()))))
    
    # For each green category, compute the export volumes and growth percentage
    cat_growth = {}
    for cat in categories:
        export_22 = filtered_df_2022[filtered_df_2022[group_field] == cat]['CZ Export 2022 CZK'].sum()
        export_23 = filtered_df_2023[filtered_df_2023[group_field] == cat]['CZ Export 2023 CZK'].sum()
        # Growth is calculated relative to total_export_22; if no baseline then use 0
        growth = (export_23 - export_22) / total_export_22 if total_export_22 else 0
        cat_growth[cat] = growth

    # Build labels and data; first element is for non-green, then the green categories.
    labels = ["Nenezelené produkty"] + list(cat_growth.keys())
    data_values = [growth_non_green] + [cat_growth[cat] for cat in cat_growth]

    # Colors: use a fixed color for non-green (grey) and then one color per green category.
    non_green_color = "#CCCCCC"  # Grey for non-green
    colors = [non_green_color]
    color_map = get_color_discrete_map()  # Returns a dict mapping group -> color
    fallback_colors = ["#E63946", "#F4A261", "#2A9D8F", "#264653", "#8A5AAB", "#D67D3E", "#1D3557"]
    fallback_cycle = itertools.cycle(fallback_colors)

    for cat in cat_growth:
        cat_color = color_map.get(cat, next(fallback_cycle))
        colors.append(cat_color)

    # Build the Chart.js data structure.
    chart_data = {
        "labels": labels,
        "datasets": [{
            "data": data_values,
            "backgroundColor": colors,
            "borderColor": colors,
            "borderWidth": 1
        }]
    }
    
    # Chart options with a tooltip that will show the label and value in percentage format.
    chart_options = {
        "responsive": True,
        "maintainAspectRatio": False,
        "plugins": {
            "title": {
                "display": True,
                "text": chart_title,
                "font": {"size": 25}
            },
            "subtitle": {
                "display": True,
                "text": bottom_text,
                "position": "bottom",
                "padding": {"top": 10},
                "font": {"size": 14}
            },
            "tooltip": {
                "callbacks": {
                    "label": (
                        "function(context) {"
                        "   var label = context.label || '';"
                        "   var value = context.parsed;"
                        "   return label + ': ' + (value*100).toFixed(1) + '% růst';"
                        "}"
                    )
                }
            }
        }
    }
    
    # Convert Python dictionaries to JSON.
    data_json = json.dumps(chart_data)
    options_json = json.dumps(chart_options)
    
    # Generate the HTML/JS snippet for Chart.js polar area chart.
    chart_js = f"""
    <div style="width:100%; height:700px;">
        <canvas id="polarChart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        var ctx = document.getElementById('polarChart').getContext('2d');
        var data = {data_json};
        var options = {options_json};
        new Chart(ctx, {{
            type: 'polarArea',
            data: data,
            options: options
        }});
    </script>
    """
    return chart_js
