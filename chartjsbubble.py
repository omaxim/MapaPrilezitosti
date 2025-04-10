import pandas as pd
import json
import itertools
from variable_names import get_hover_formatting, get_color_discrete_map
def hex_to_rgba(hex_color, alpha=1.0):
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"

def chartjs_plot(filtered_df,markersize,hover_data,color,x_axis,y_axis,year):

    # Min-Max scaling for markersize (normalize to 0-100)
    min_size = filtered_df[markersize].min()
    max_size = filtered_df[markersize].max()

    # Avoid division by zero in case all values are the same
    if max_size == min_size:
        filtered_df["scaled_size"] = 2  # Default all to medium size
    else:
        filtered_df["scaled_size"] = (filtered_df[markersize].copy() - min_size) / (max_size - min_size)  * 30 + 2

    color_discrete_map = get_color_discrete_map()
    fallback_colors = [
        "#E63946", "#F4A261", "#2A9D8F", "#264653", "#8A5AAB", "#D67D3E", "#1D3557"
    ]  # Example palette (you can use more)

    color_cycle = itertools.cycle(fallback_colors)  # Cycles through colors

    no_decimal,two_sigfig,percentage,texthover = get_hover_formatting(year)
    # Function to format values based on the hover_data rules
    def format_hover_data(key, value):
        if key in no_decimal:
            return "{:,.0f}".format(value)  # No decimals, thousands separator
        elif key in two_sigfig:
            return "{:.2f}".format(value)  # 2 decimal places
        elif key in percentage:
            return "{:.1f}%".format(value * 100)  # Convert to percentage
        elif key in texthover:
            return str(value)
        else:
            return value  # No special formatting
    # Group data by color category
    grouped_data = {}
    for _, row in filtered_df.iterrows():

        color_category = row[color]

        # Use mapped color or fallback if missing
        raw_color = color_discrete_map.get(color_category, next(color_cycle))
        assigned_color = hex_to_rgba(raw_color, alpha=1.0)

        data_point = {
            "x": row[x_axis],
            "y": row[y_axis],
            "r": row["scaled_size"],
            "meta": {key: format_hover_data(key, row[key]) for key in hover_data if hover_data[key] is not False}
        }

        if color_category not in grouped_data:
            grouped_data[color_category] = {"data": [], "color": assigned_color}
            
        for key in hover_data:
            if hover_data[key] is not False:
                value = format_hover_data(key, row[key])
                if "<br>" in value:
                    parts = value.split("<br>")
                    for i, part in enumerate(parts):
                        new_key = f"{key} {i+1}" if i > 0 else key  # Append (1), (2), etc.
                        data_point["meta"][new_key] = part
                else:
                    data_point["meta"][key] = value
        # Sort meta dictionary alphabetically
        data_point["meta"] = dict(sorted(data_point["meta"].items()))
        grouped_data[color_category]["data"].append(data_point)


    # Convert grouped data into Chart.js dataset format
    datasets = [
        {
            "label": category,
            "data": group_info["data"],
            "backgroundColor": group_info["color"],
            "borderColor": group_info["color"],
            "borderWidth": 1,
            "hoverRadius": 10,  # Increase size on hover
        }
        for category, group_info in grouped_data.items()
    ]
    # Convert datasets to JSON
    datasets_json = json.dumps(datasets)
    x_label = json.dumps(x_axis)  # Convert to JSON for safe JS use
    y_label = json.dumps(y_axis)

    # Generate the JavaScript chart code
    chart_js = f"""
    <div style="width:100%; height:700px;">
        <canvas id="myBubbleChart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        const originalColors = [];

        var ctx = document.getElementById('myBubbleChart').getContext('2d');
        var myBubbleChart = new Chart(ctx, {{
            type: 'bubble',
            data: {{
                datasets: {datasets_json}
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{
                        title: {{
                            display: true,
                            text: {x_label}
                        }}
                    }},
                    y: {{
                        title: {{
                            display: true,
                            text: {y_label}
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        labels: {{
                            usePointStyle: true
                        }}
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                let data = context.dataset.data[context.dataIndex]; 
                                if (!data.meta) return [];
                                return Object.entries(data.meta).map(([key, value]) => `${{key}}: ${{value}}`);
                            }}
                        }}
                    }}
                }},
                hover: {{
                    mode: 'nearest',
                    intersect: true,
                    onHover: function(event, elements) {{
                        if (elements.length > 0) {{
                            const hoveredDatasetIndex = elements[0].datasetIndex;

                            // Store original colors if not already stored
                            if (originalColors.length === 0) {{
                                myBubbleChart.data.datasets.forEach(ds => {{
                                    originalColors.push(ds.backgroundColor);
                                }});
                            }}

                            myBubbleChart.data.datasets.forEach((ds, idx) => {{
                                ds.backgroundColor = idx === hoveredDatasetIndex
                                    ? originalColors[idx]
                                    : originalColors[idx].replace(/rgba?\\(([^,]+),([^,]+),([^,]+)(?:,[^)]+)?\\)/, 'rgba($1,$2,$3,0.1)');
                            }});

                            myBubbleChart.update();
                        }}
                    }},
                    onLeave: function(event) {{
                        myBubbleChart.data.datasets.forEach((ds, idx) => {{
                            ds.backgroundColor = originalColors[idx];
                        }});
                        myBubbleChart.update();
                    }}
                }}
            }}
        }});
    </script>
    """
    return chart_js.replace("Název 3: ", "").replace("Název 2: ", "").replace("Název: ", "")

