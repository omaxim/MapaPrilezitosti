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
        filtered_df["scaled_size"] = ((np.sqrt(filtered_df[markersize] + 1) - log_min) / (log_max - log_min)) * 20 + 2

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

        # Create the basic data point structure
        data_point = {
             "x": row[x_axis],
             "y": row[y_axis],
             "r": row["scaled_size"],
             "meta": {} # Initialize meta dictionary here
        }
        # Populate meta dictionary - *** MODIFIED LOGIC ***
        for key in hover_data:
             # Check if the key should be included (value is not False)
            if hover_data.get(key) is not False:
                # Format the value using your existing function
                value = format_hover_data(key, row[key])
                 # Store the value directly, preserving any <br> tags. NO MORE SPLITTING.
                data_point["meta"][key] = str(value) # Ensure it's a string
        # Sort meta dictionary alphabetically (optional, but good for consistency below title)
        # We will handle Název separately in JS, sorting affects the rest
        data_point["meta"] = dict(sorted(data_point["meta"].items()))
        # Add the complete data point to the correct group
        if color_category not in grouped_data:
            grouped_data[color_category] = {"data": [], "color": assigned_color, "_originalBackgroundColor": assigned_color} # Add original color store here too if not already done
        grouped_data[color_category]["data"].append(data_point)

    # Convert grouped data into Chart.js dataset format
    # --- Create datasets with default transparency ---
    default_alpha_hex = 'CC' # Set desired default alpha (~80% opaque). Try 'B3', '99', '80' etc.

    datasets = [
        {
            "label": category,
            "data": group_info["data"],
            "backgroundColor": group_info["color"] + default_alpha_hex,
            "borderColor": group_info["color"] + default_alpha_hex,
            "_originalBackgroundColor": group_info["color"] + default_alpha_hex, # <-- STORE ORIGINAL COLOR
            "borderWidth": 0,
            "hoverRadius": 5,
            "clip": 100
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
                        // Use callbacks for custom tooltip content
                        callbacks: {{
                            // ** Use the 'title' callback for 'Název' **
                            // It's typically bold by default.
                            title: function(tooltipItems) {{
                                // tooltipItems is an array, we usually use the first item
                                if (!tooltipItems.length) {{
                                    return '';
                                }}
                                const context = tooltipItems[0];
                                const data = context.dataset.data[context.dataIndex];

                                // Check if 'Název' exists in our meta data
                                if (data.meta && data.meta.hasOwnProperty('Název')) {{
                                    // Split the 'Název' string by '<br>' to create multiple lines
                                    // Chart.js handles an array return as multiple title lines
                                    return data.meta['Název'].split('<br>');
                                }}
                                return ''; // Return empty string if no 'Název'
                            }},

                            // ** Optional: Add space after title if Název existed **
                            afterTitle: function(tooltipItems) {{
                                const context = tooltipItems[0];
                                const data = context.dataset.data[context.dataIndex];
                                // Add space only if Název was shown and there are other items
                                if (data.meta && data.meta.hasOwnProperty('Název') && Object.keys(data.meta).length > 1) {{
                                     // Return an empty string or one with just space to force a line
                                    return ' '; // Creates visual separation
                                }}
                                return '';
                            }},


                            // ** Use 'beforeBody' to generate the Key: Value lines for other items **
                            // Returns an array of strings, each becoming a line in the tooltip body.
                            beforeBody: function(tooltipItems) {{
                                const context = tooltipItems[0];
                                const data = context.dataset.data[context.dataIndex];
                                const bodyLines = []; // Array to hold our custom body lines

                                if (data.meta) {{
                                    // Iterate through the keys (already sorted in Python)
                                    for (const key in data.meta) {{
                                        // Make sure the key is not 'Název' (already handled in title)
                                        if (key !== 'Název' && data.meta.hasOwnProperty(key)) {{
                                            // Format as "Key: Value"
                                            bodyLines.push(`${{key}}: ${{data.meta[key]}}`);
                                        }}
                                    }}
                                }}
                                return bodyLines; // Return the array of lines
                            }},

                            // ** Disable the default label **
                            // Since we are generating the body content in beforeBody,
                            // we don't need the default label (which usually shows dataset label & y-value).
                            label: function(context) {{
                                return null; // Returning null prevents the default label line
                            }},

                            // ** Optional: Hide the color swatch next to the label **
                            // Since we disabled the default label, you might not want the color box either.
                            labelColor: function(context) {{
                                return null; // Returning null hides the color box
                                // Alternative: return {{ borderColor: 'transparent', backgroundColor: 'transparent' }};
                            }}

                        }} // end callbacks
                    }} // end tooltip
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
