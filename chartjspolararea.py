import json
import itertools
import numpy as np
from variable_names import get_color_discrete_map  # Assumes this returns a dict mapping category to color

def chartjs_polar_area(filtered_df_2022, filtered_df_2023, group_field, chart_title="Export růst mezi lety 2022 a 2023", bottom_text="Data: UN COMTRADE, CEPII, a další"):
    """
    Create a polar area chart in Chart.js showing growth in % for total export and by category.
    
    Parameters:
    - filtered_df_2022, filtered_df_2023: DataFrames for the two years.
    - group_field: Column name used for grouping (e.g., 'Kategorie' or 'Skupina').
    - chart_title: Title for the chart.
    - bottom_text: Subtitle or bottom text.
    
    Returns:
    - A string containing HTML + JS code for embedding in Streamlit.
    """
    # Total export values and growth percentage
    total_export_22 = filtered_df_2022['CZ Export 2022 CZK'].sum()
    total_export_23 = filtered_df_2023['CZ Export 2023 CZK'].sum()
    total_growth = total_export_23 - total_export_22
    total_growth_perc = total_growth / total_export_22 if total_export_22 else 0

    # Get the union of groups from both dataframes for robustness
    groups = list(set(filtered_df_2022[group_field].unique()).union(set(filtered_df_2023[group_field].unique())))
    groups.sort()

    # Calculate growth percentage for each category
    category_growth = {}
    for grp in groups:
        export_22 = filtered_df_2022[filtered_df_2022[group_field] == grp]['CZ Export 2022 CZK'].sum()
        export_23 = filtered_df_2023[filtered_df_2023[group_field] == grp]['CZ Export 2023 CZK'].sum()
        if export_22 > 0:
            growth_perc = (export_23 - export_22) / export_22
        else:
            growth_perc = 0
        category_growth[grp] = growth_perc

    # Build chart labels and data.
    # The first segment represents the total export growth.
    labels = ["Celkový export"] + list(category_growth.keys())
    data_values = [total_growth_perc] + list(category_growth.values())

    # Set colors. Fixed color for total export (not green; here, a shade of gray),
    # and for each category, use your provided discrete color mapping.
    fixed_total_color = "#CCCCCC"  # Fixed, non-green color
    colors = [fixed_total_color]
    color_map = get_color_discrete_map()  # This function should return a dict mapping group to color
    fallback_colors = ["#E63946", "#F4A261", "#2A9D8F", "#264653", "#8A5AAB", "#D67D3E", "#1D3557"]
    color_cycle = itertools.cycle(fallback_colors)
    for grp in category_growth.keys():
        grp_color = color_map.get(grp, next(color_cycle))
        colors.append(grp_color)

    # Create the Chart.js data and options objects.
    chart_data = {
        "labels": labels,
        "datasets": [{
            "data": data_values,
            "backgroundColor": colors,
            "borderColor": colors,
            "borderWidth": 1
        }]
    }
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
                    # Display tooltip as "Label: XX.X% growth"
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

    # Convert the Python dictionaries to JSON for Chart.js.
    datasets_json = json.dumps(chart_data)
    options_json = json.dumps(chart_options)

    # Generate the HTML/JS code
    chart_js = f"""
    <div style="width:100%; height:700px;">
        <canvas id="polarChart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        var ctx = document.getElementById('polarChart').getContext('2d');
        var data = {datasets_json};
        var options = {options_json};
        new Chart(ctx, {{
            type: 'polarArea',
            data: data,
            options: options
        }});
    </script>
    """
    return chart_js
