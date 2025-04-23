import json
import itertools
from variable_names import get_color_discrete_map

def chart_highcharts_variable_pie(filtered_df_2022, filtered_df_2023,
                                  total_export_22, total_export_23,
                                  green_total_22, green_total_23,
                                  group_field,
                                  chart_title="Export růst mezi lety 2022 a 2023",
                                  bottom_text="Data: UN COMTRADE, CEPII, a další",
                                  relative_to_green_only=False):
    """
    Creates a Highcharts variable pie chart where:
      - The slice angle (y) represents the export share.
        - By default, relative to total exports.
        - If `relative_to_green_only=True` or total exports are None, relative to green exports only.
      - The slice radius (z) represents percentage growth between 2022 and 2023.

    Parameters:
      - filtered_df_2022, filtered_df_2023: DataFrames for green product exports.
      - total_export_22, total_export_23: Overall export values (can be None).
      - green_total_22, green_total_23: Total green export values.
      - group_field: Column used to group green products.
      - chart_title: Title of the chart.
      - bottom_text: Subtitle/footer.
      - relative_to_green_only: If True, slices are based only on green export totals.

    Returns:
      - HTML/JS string for rendering the chart.
    """

    green_total_22_filtered = filtered_df_2022['CZ Export 2022 CZK'].sum()
    green_total_23_filtered = filtered_df_2023['CZ Export 2023 CZK'].sum()

    data_series = []

    # Decide denominator
    use_green_relative = relative_to_green_only or (total_export_22 is None or total_export_23 is None)
    denominator = green_total_23 if use_green_relative else total_export_23

    if not use_green_relative:
        non_green_22 = total_export_22 - green_total_22
        non_green_23 = total_export_23 - green_total_23
        other_green_22 = green_total_22 - green_total_22_filtered
        other_green_23 = green_total_23 - green_total_23_filtered

        growth_non_green = (non_green_23 - non_green_22) / non_green_22 if non_green_22 > 0 else 0
        growth_other_green = (other_green_23 - other_green_22) / other_green_22 if other_green_22 > 0 else 0

        data_series.append({
            "name": "Nezelené produkty",
            "y": non_green_23 / denominator,
            "z": growth_non_green,
            "color": "#CCCCCC",
            "export22": non_green_22 / 1e9,
            "export23": non_green_23 / 1e9,
            "growth_abs": (non_green_23 - non_green_22) / 1e9,
            "growth_frac": growth_non_green
        })

        if other_green_22 != 0:
            data_series.append({
                "name": "Ostatní zelené produkty",
                "y": other_green_23 / denominator,
                "z": growth_other_green,
                "color": "#B2BEB5",
                "export22": other_green_22 / 1e9,
                "export23": other_green_23 / 1e9,
                "growth_abs": (other_green_23 - other_green_22) / 1e9,
                "growth_frac": growth_other_green
            })

    green_cats = sorted(list(set(filtered_df_2022[group_field].unique()).union(
                             set(filtered_df_2023[group_field].unique()))))

    color_map = get_color_discrete_map()
    fallback_colors = ["#E63946", "#F4A261", "#2A9D8F", "#264653", "#8A5AAB", "#D67D3E", "#1D3557"]
    fallback_cycle = itertools.cycle(fallback_colors)

    for cat in green_cats:
        export_22 = filtered_df_2022[filtered_df_2022[group_field] == cat]['CZ Export 2022 CZK'].sum()
        export_23 = filtered_df_2023[filtered_df_2023[group_field] == cat]['CZ Export 2023 CZK'].sum()
        growth = (export_23 - export_22) / export_22 if export_22 > 0 else 0

        data_series.append({
            "name": cat,
            "y": export_23 / denominator,
            "z": growth,
            "color": color_map.get(cat, next(fallback_cycle)),
            "export22": export_22 / 1e9,
            "export23": export_23 / 1e9,
            "growth_abs": (export_23 - export_22) / 1e9,
            "growth_frac": 100 * growth
        })

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
                '2022: {point.export22:,.1f} miliard CZK<br/>' +
                '2023: {point.export23:,.1f} miliard CZK<br/>' +
                'Růst: {point.growth_abs:,.1f} miliard CZK ({point.growth_frac:.2f}%)'
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
    <script src="https://code.highcharts.com/modules/variable-pie.js"></script>
    <script>
      document.addEventListener('DOMContentLoaded', function () {{
        Highcharts.chart('container', {config_json});
      }});
    </script>
    """

    return chart_html
