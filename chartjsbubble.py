import pandas as pd
import json
import itertools
import numpy as np
# Assuming get_hover_formatting and get_color_discrete_map are defined elsewhere
from variable_names import get_hover_formatting, get_color_discrete_map

def chartjs_plot(filtered_df, markersize, hover_data, color, x_axis, y_axis, year):
    # Min-Max scaling for markersize (normalize to range like 2-32)
    min_size = filtered_df[markersize].min()
    max_size = filtered_df[markersize].max()


    # Avoid division by zero in case all values are the same
    if max_size == min_size:
        filtered_df["scaled_size"] = 10  # Assign a medium default size
    else:
        # Apply log scaling: map input range to output range [2, 32]
        # Use np.log to apply log scaling
        log_min = np.sqrt(min_size + 1)  # Adding 1 to avoid 10(0) if min_size is 0
        log_max = np.sqrt(max_size + 1)

        # Scale the size based on the log of the values
        filtered_df["scaled_size"] = ((np.sqrt(filtered_df[markersize] + 1) - log_min) / (log_max - log_min)) * 40 + 1

    color_discrete_map = get_color_discrete_map() # Assume this returns a dict
    fallback_colors = [
        "#E63946", "#F4A261", "#2A9D8F", "#264653", "#8A5AAB", "#D67D3E", "#1D3557"
    ]
    color_cycle = itertools.cycle(fallback_colors)

    # --- Assume get_hover_formatting returns dictionaries like before ---
    no_decimal, two_sigfig, percentage, texthover = get_hover_formatting(year)

    # --- Assume format_hover_data function is defined as before ---

    def format_hover_data(key, value):

        if key in no_decimal:
            return "{:,.0f}".format(value) # No decimals, thousands separator
        elif key in two_sigfig:
            return "{:.2f}".format(value) # 2 decimal places
        elif key in percentage:
            return "{:.1f}%".format(value * 100) # Convert to percentage
        elif key in texthover:
            return str(value)
        else:
            return value # No special formatting
    
    grouped_data = {}
    for _, row in filtered_df.iterrows():
        color_category = row[color]
        assigned_color = color_discrete_map.get(color_category, next(color_cycle))

        # --- Assume hover data formatting logic is correct ---
        meta_data = {key: format_hover_data(key, row[key]) for key in hover_data if hover_data.get(key) is not False}
        # Handle <br> splitting if necessary (your existing logic here)
        # ...
        # Sort meta dictionary alphabetically
        sorted_meta = dict(sorted(meta_data.items()))


        data_point = {
            "x": row[x_axis],
            "y": row[y_axis],
            "r": row["scaled_size"],
            "meta": sorted_meta
        }

        if color_category not in grouped_data:
            grouped_data[color_category] = {"data": [], "color": assigned_color}

        grouped_data[color_category]["data"].append(data_point)

    # Convert grouped data into Chart.js dataset format
    datasets = [
        {
            "label": category,
            "data": group_info["data"],
            "backgroundColor": group_info["color"],
            "borderColor": group_info["color"],
            "_originalBackgroundColor": group_info["color"], # <-- STORE ORIGINAL COLOR
            "borderWidth": 0,
            "hoverRadius": 2
        }
        for category, group_info in grouped_data.items()
    ]

    # Convert datasets to JSON
    # Use a custom encoder if you have non-standard types (like lambdas, though they won't serialize)


    datasets_json = json.dumps(datasets)
    x_label = json.dumps(x_axis)
    y_label = json.dumps(y_axis)

    # Generate the JavaScript chart code
    chart_js = f"""
    <div style="width:100%; height:700px;">
        <canvas id="myBubbleChart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        var ctx = document.getElementById('myBubbleChart').getContext('2d');
        var datasets = {datasets_json}; // Load datasets from Python

        // --- Optional: Add original color back if needed post-JSON parsing ---
        // Not strictly necessary if we use the _originalBackgroundColor added above

        var myBubbleChart = new Chart(ctx, {{
            type: 'bubble',
            data: {{
                datasets: datasets // Use the datasets variable
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ title: {{ display: true, text: {x_label} }} }},
                    y: {{ title: {{ display: true, text: {y_label} }} }}
                }},
                animation: {{ duration: 500 }}, // Disable default animations if hover is jerky
                transitions: {{
                    active: {{ animation: {{ duration: 500 }} }} // Faster response on hover
                }},
                // *** REVISED onHover LOGIC ***
                onHover: (event, elements, chart) => {{
                    // 1. Reset all datasets to their original colors first
                    chart.data.datasets.forEach(dataset => {{
                        // Ensure _originalBackgroundColor exists, otherwise use current color as fallback
                        const originalColor = dataset._originalBackgroundColor || dataset.backgroundColor;
                        // Only reset if it was potentially modified (ends with '0D' alpha)
                        if (typeof dataset.backgroundColor === 'string' && dataset.backgroundColor.length === 9) {{
                             dataset.backgroundColor = originalColor;
                             dataset.borderColor = originalColor;
                        }} else if (!dataset.backgroundColor.startsWith('#')) {{
                            // If it's not a hex string (maybe reset from transparent state error)
                            dataset.backgroundColor = originalColor;
                            dataset.borderColor = originalColor;
                        }}
                         // If already original, this does nothing harmful
                         dataset.backgroundColor = originalColor;
                         dataset.borderColor = originalColor;
                    }});

                    // 2. If hovering over an element, apply transparency to OTHERS
                    if (elements.length > 0) {{
                        const hoveredDatasetIndex = elements[0].datasetIndex;
                        chart.data.datasets.forEach((dataset, index) => {{
                            if (index !== hoveredDatasetIndex) {{
                                // Make sure we have a valid original color string to modify
                                const originalColor = dataset._originalBackgroundColor || dataset.backgroundColor;
                                if (typeof originalColor === 'string' && originalColor.startsWith('#') && originalColor.length === 7) {{ // Only modify #RRGGBB
                                    dataset.backgroundColor = originalColor + '0D'; // Add low alpha hex
                                    dataset.borderColor = originalColor + '0D';
                                }}
                                // Handle potential RGBA or other formats if necessary
                            }}
                        }});
                    }}
                    // 3. Update the chart
                    chart.update(); // Use 'none' or 0 for mode to prevent animation conflicts
                }},
                plugins: {{
                    legend: {{
                        // --- Your existing legend onClick logic ---
                        onClick: (event, item, legend) => {{
                            const datasetIndex = item.datasetIndex;
                            const chart = legend.chart;
                            if (chart._isolatedDatasetIndex === undefined) {{
                                chart._isolatedDatasetIndex = null;
                            }}
                            if (chart._isolatedDatasetIndex === datasetIndex) {{
                                chart.data.datasets.forEach((ds, index) => {{
                                    chart.setDatasetVisibility(index, true);
                                     // Restore original colors when un-isolating
                                    if(ds._originalBackgroundColor) {{
                                        ds.backgroundColor = ds._originalBackgroundColor;
                                        ds.borderColor = ds._originalBackgroundColor;
                                    }}
                                }});
                                chart._isolatedDatasetIndex = null;
                            }} else {{
                                chart.data.datasets.forEach((ds, index) => {{
                                    chart.setDatasetVisibility(index, index === datasetIndex);
                                     // Restore original colors before hiding/showing
                                     if(ds._originalBackgroundColor) {{
                                        ds.backgroundColor = ds._originalBackgroundColor;
                                        ds.borderColor = ds._originalBackgroundColor;
                                    }}
                                }});
                                chart._isolatedDatasetIndex = datasetIndex;
                            }}
                            chart.update();
                        }},
                        labels: {{ usePointStyle: true, padding: 10 }}
                    }},
                    tooltip: {{
                        callbacks: {{
                            // --- Your existing tooltip label callback ---
                            label: function(context) {{
                                let data = context.dataset.data[context.dataIndex];
                                if (!data.meta) return [];
                                return Object.entries(data.meta).map(([key, value]) => `${{key}}: ${{value}}`);
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Optional: Add logic to reset hover state if mouse leaves canvas
        ctx.canvas.addEventListener('mouseout', () => {{
             myBubbleChart.data.datasets.forEach(dataset => {{
                const originalColor = dataset._originalBackgroundColor || dataset.backgroundColor;
                 dataset.backgroundColor = originalColor;
                 dataset.borderColor = originalColor;
            }});
            myBubbleChart.update('none');
        }});

    </script>
    """
    return chart_js
