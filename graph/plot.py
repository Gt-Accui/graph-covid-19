from plotly import graph_objects as go
import pandas as pd
import io

from .models import CSVColumn, CSVData, PlotMode
from .charts import line_charts, weekday_charts, get_sma, sma_charts
from .charts import bar_charts, default_layout
from .csvdf import get_df_labels


def set_mode(fig, df, csvcolumns, source):
    x_len = len(csvcolumns.filter(axis='X'))
    y_len = len(csvcolumns.filter(axis='Y'))
    y_axis = 'y'
    if x_len == 1 and y_len > 0:  # グラフの種類ごとで変えるか
        mode = PlotMode.objects.get(source=source).mode
        if mode == 'lines':
            if y_len == 1:  # 折れ線グラフでY軸が１つのとき
                try:  # X軸が日付なら'曜日ごと'と'７日平均'をplot
                    weekday_charts(fig, df, csvcolumns, y_axis)
                    window = 7
                    df_sma = get_sma(df, csvcolumns, window).reset_index()
                    sma_charts(fig, df_sma, csvcolumns, y_axis, window)
                except Exception:
                    line_charts(fig, df, csvcolumns, y_axis)
            else:
                line_charts(fig, df, csvcolumns, y_axis)
        elif mode == 'bars':
            bar_charts(fig, df, csvcolumns, y_axis)
    else:
        if x_len != 1:
            fig.update_layout(xaxis=dict(title='X軸は1つだけ選択してください。',))
        if y_len == 0:
            fig.update_layout(yaxis=dict(title='Y軸は1つ以上選択してください。',))


def plot(source):
    fig = go.Figure()
    default_layout(fig, source)

    csvcolumns = CSVColumn.objects.filter(source=source)
    csv_str = CSVData.objects.get(source=source).csv_str
    df = pd.read_csv(io.StringIO(csv_str))  # , encoding='UTF8',)
    df.columns = get_df_labels(csvcolumns, df)
    set_mode(fig, df, csvcolumns, source)

    return fig.to_html(include_plotlyjs=False)
