import json
import itertools
from variable_names import get_color_discrete_map

def chart_chartjs_variable_pie(filtered_df_2022, filtered_df_2023, total_export_22, total_export_23,
                                green_total_22, green_total_23, group_field,
                                chart_title="Export růst mezi lety 2022 a 2023",
                                bottom_text="Data: UN COMTRADE, CEPII, a další"):

    green_total_22_filtered = filtered_df_2022['CZ Export 2022 CZK'].sum()
    green_total_23_filtered = filtered_df_2023['CZ Export 2023 CZK'].sum()

    non_green_22 = total_export_22 - green_total_22
    non_green_23 = total_export_23 - green_total_23

    other_green_22 = green_total_22 - green_total_22_filtered
    other_green_23 = green_total_23 - green_total_23_filtered

    def safe_growth(a, b):
        return (b - a) / a * 100 if a > 0 else 0

    labels = []
    data_2023 = []
    export22 = []
    export23 = []
    growthAbs = []
    growthPct = []
    backgroundColor = []
    outerRadii = []

    color_map = get_color_discrete_map()
    fallback_colors = ["#E63946", "#F4A261", "#2A9D8F", "#264653", "#8A5AAB", "#D67D3E", "#1D3557"]
    fallback_cycle = itertools.cycle(fallback_colors)

    # Get maximum value for radius scaling
    max_value = max([non_green_23, other_green_23, green_total_23_filtered] + 
                    [filtered_df_2023[filtered_df_2023[group_field] == cat]['CZ Export 2023 CZK'].sum()
                     for cat in set(filtered_df_2023[group_field].unique())])

    def compute_radius(value):
        return 80 + (value / max_value) * 60  # pixel radius

    # Non-green
    labels.append("Nezelené produkty")
    val = non_green_23
    export22.append(non_green_22 / 1e9)
    export23.append(val / 1e9)
    data_2023.append(val / 1e9)
    growthAbs.append((val - non_green_22) / 1e9)
    growthPct.append(safe_growth(non_green_22, val))
    backgroundColor.append("#CCCCCC")
    outerRadii.append(compute_radius(val))

    # Other green
    if other_green_22 > 0:
        labels.append("Ostatní zelené produkty")
        val = other_green_23
        export22.append(other_green_22 / 1e9)
        export23.append(val / 1e9)
        data_2023.append(val / 1e9)
        growthAbs.append((val - other_green_22) / 1e9)
        growthPct.append(safe_growth(other_green_22, val))
        backgroundColor.append("#B2BEB5")
        outerRadii.append(compute_radius(val))

    # Categories
    green_cats = sorted(set(filtered_df_2022[group_field].unique()).union(
                        set(filtered_df_2023[group_field].unique())))
    
    for cat in green_cats:
        exp22 = filtered_df_2022[filtered_df_2022[group_field] == cat]['CZ Export 2022 CZK'].sum()
        exp23 = filtered_df_2023[filtered_df_2023[group_field] == cat]['CZ Export 2023 CZK'].sum()
        labels.append(cat)
        export22.append(exp22 / 1e9)
        export23.append(exp23 / 1e9)
        data_2023.append(exp23 / 1e9)
        growthAbs.append((exp23 - exp22) / 1e9)
        growthPct.append(safe_growth(exp22, exp23))
        backgroundColor.append(color_map.get(cat, next(fallback_cycle)))
        outerRadii.append(compute_radius(exp23))

    chart_data = {
        "labels": labels,
        "datasets": [{
            "data": data_2023,
            "backgroundColor": backgroundColor,
            "export22": export22,
            "export23": export23,
            "growthAbs": growthAbs,
            "growthPct": growthPct
        }]
    }

    chart_config = {
        "type": "doughnut",
        "data": chart_data,
        "options": {
            "responsive": True,
            "cutout": "30%",
            "layout": {
                "padding": 40
            },
            "plugins": {
                "tooltip": {
                    "callbacks": {
                        "label": {
                            "function": """function(context) {
                                const i = context.dataIndex;
                                const d = context.dataset;
                                const l = context.label || '';
                                return [
                                    `${l}`,
                                    `2022: ${d.export22[i].toFixed(1)} mld CZK`,
                                    `2023: ${d.export23[i].toFixed(1)} mld CZK`,
                                    `Růst: ${d.growthAbs[i].toFixed(1)} mld CZK (${d.growthPct[i].toFixed(1)}%)`
                                ];
                            }"""
                        }
                    }
                },
                "title": {
                    "display": True,
                    "text": chart_title
                }
            },
            "animation": False,
            "hover": {
                "mode": "nearest"
            },
            "elements": {
                "arc": {
                    "hoverOffset": 0
                }
            }
        }
    }

    custom_plugin = f"""
    {{
      id: 'variableRadius',
      beforeDraw(chart) {{
        const {{"ctx", "chartArea", "data"}} = chart;
        const radiusData = {json.dumps(outerRadii)};
        const arcs = chart.getDatasetMeta(0).data;
        arcs.forEach((arc, i) => {{
          arc.outerRadius = radiusData[i];
          arc.innerRadius = chart._metasets[0].data[0].innerRadius;
        }});
      }}
    }}
    """

    glow_plugin = """
    {
      id: 'glowEffect',
      beforeDatasetDraw(chart, args, options) {
        const {ctx} = chart;
        ctx.save();
        ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
        ctx.shadowBlur = 10;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;
      },
      afterDatasetDraw(chart, args, options) {
        const {ctx} = chart;
        ctx.restore();
      }
    }
    """

    html = f'''
    <div style="width:100%; max-width:800px; margin:auto;">
      <canvas id="exportGrowthChart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.3.3/dist/chart.umd.js"></script>
    <script>
      const ctx = document.getElementById('exportGrowthChart').getContext('2d');
      const chartConfig = {json.dumps(chart_config)};
      chartConfig.options.plugins.tooltip.callbacks.label = eval('(' + chartConfig.options.plugins.tooltip.callbacks.label.function + ')');

      const variableRadiusPlugin = {custom_plugin};
      const glowEffect = {glow_plugin};

      new Chart(ctx, chartConfig, [variableRadiusPlugin, glowEffect]);
    </script>
    <div style="text-align:center; font-size:0.8em; color:#666;">{bottom_text}</div>
    '''

    return html
