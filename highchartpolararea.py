import json
import itertools
from variable_names import get_color_discrete_map

def chart_highcharts_variable_pie(filtered_df_2022, filtered_df_2023,
                                  total_export_22, total_export_23,
                                  green_total_22, green_total_23,
                                  group_field,
                                  usd_to_czk_22=23.360,
                                  usd_to_czk_23=22.21,
                                  chart_title="Export růst mezi lety 2022 a 2023",
                                  bottom_text="Data: UN COMTRADE, CEPII, a další",
                                  relative_to_green_only=False):
    """
    Creates a Highcharts variable pie chart showing green export growth.
    Includes both filtered green categories and (optionally) non-green and unclassified green.

    If `relative_to_green_only` is True or total_export_22/23 are None, then
    slice angles (y) are calculated as share of green exports only.
    """

    # Base green export totals from filtered subset and convert to USD
    total_export_22 = total_export_22/usd_to_czk_22
    total_export_23 = total_export_23/usd_to_czk_23
    green_total_22 = green_total_22/usd_to_czk_22
    green_total_23 = green_total_23/usd_to_czk_23
    green_total_22_filtered = filtered_df_2022['CZ Export 2022 CZK'].sum()/usd_to_czk_22
    green_total_23_filtered = filtered_df_2023['CZ Export 2023 CZK'].sum()/usd_to_czk_23

    # Compute unfiltered other-green portion
    other_green_22 = green_total_22 - green_total_22_filtered
    other_green_23 = green_total_23 - green_total_23_filtered
    growth_other_green = (other_green_23 - other_green_22) / other_green_22 if other_green_22 > 0 else 0

    # Decide what denominator to use for slice angles (y)
    use_green_only = relative_to_green_only or total_export_22 is None or total_export_23 is None
    denominator = green_total_23 if use_green_only else total_export_23

    data_series = []

    # Add non-green slice if using total exports as denominator
    if not use_green_only:
        non_green_22 = total_export_22 - green_total_22
        non_green_23 = total_export_23 - green_total_23
        growth_non_green = (non_green_23 - non_green_22) / non_green_22 if non_green_22 > 0 else 0

        data_series.append({
            "name": "Nezelené produkty",
            "y": non_green_23 / denominator,
            "z": growth_non_green,
            "color": "#CCCCCC",
            "export22": non_green_22 / 1e9,
            "export23": non_green_23 / 1e9,
            "growth_abs": (non_green_23 - non_green_22) / 1e9,
            "growth_frac": 100 * growth_non_green
        })

    # Add other-green slice if it exists
    if other_green_22 > 0 or other_green_23 > 0:
        data_series.append({
            "name": "Ostatní zelené produkty",
            "y": other_green_23 / denominator,
            "z": growth_other_green,
            "color": "#B2BEB5",
            "export22": other_green_22 / 1e9,
            "export23": other_green_23 / 1e9,
            "growth_abs": (other_green_23 - other_green_22) / 1e9,
            "growth_frac": 100 * growth_other_green
        })

    # Add each filtered green category
    green_cats = sorted(set(filtered_df_2022[group_field]) | set(filtered_df_2023[group_field]))
    color_map = get_color_discrete_map()
    fallback_colors = ["#E63946", "#F4A261", "#2A9D8F", "#264653", "#8A5AAB", "#D67D3E", "#1D3557"]
    fallback_cycle = itertools.cycle(fallback_colors)

    for cat in green_cats:
        export_22 = filtered_df_2022.loc[filtered_df_2022[group_field] == cat, 'CZ Export 2022 CZK'].sum()/usd_to_czk_22
        export_23 = filtered_df_2023.loc[filtered_df_2023[group_field] == cat, 'CZ Export 2023 CZK'].sum()/usd_to_czk_23
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

    # Highcharts config
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
                '2022: {point.export22:,.1f} miliard USD<br/>' +
                '2023: {point.export23:,.1f} miliard USD<br/>' +
                'Růst: {point.growth_abs:,.1f} miliard USD ({point.growth_frac:.2f}%)'
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
