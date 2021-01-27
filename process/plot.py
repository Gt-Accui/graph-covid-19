from plotly import graph_objects as go
import pandas as pd

import sys
sys.path.append('../')
from graph.charts import line_charts, weekday_charts, get_sma, sma_charts
from graph.charts import default_layout
from graph.csvdf import csv_to_df, get_csvcolumns


def df_calc(fig, df1, df2, process):
    calc = process.calc
    calc_dic = {'add': df1.add, 'sub': df1.sub, 'mul': df1.mul, 'div': df1.div}
    df_list = list()
    if calc:
        df_list.append(calc_dic[calc](df2))
    else:
        df_list.extend([df1, df2])
    return df_list


def update_y_title(fig, process):
    calc = process.calc
    symbol_dic = {'add': '+', 'sub': '-', 'mul': '×', 'div': '÷', None: ' '}
    calc_symbol = symbol_dic[calc]
    fig.update_layout(yaxis=dict(
        title=f'{process.data1_col} {calc_symbol} {process.data2_col}',
    ),)


def set_mode(fig, df1, df2, process):
    csvcolumns = get_csvcolumns(process)
    if process.weekday:  # 曜日ごと
        df_list = df_calc(fig, df1, df2, process)
        for df in df_list:
            weekday_charts(fig, df.reset_index(), csvcolumns)
    elif process.sma_num:  # 単純移動平均
        window = process.sma_num
        df1_sma = get_sma(df1, csvcolumns, window)
        df2_sma = get_sma(df2, csvcolumns, window)
        df_list = df_calc(fig, df1_sma, df2_sma, process)
        for df in df_list:
            sma_charts(fig, df.reset_index(), csvcolumns, window)
    else:
        df_list = df_calc(fig, df1, df2, process)
        for df in df_list:
            line_charts(fig, df.reset_index(), csvcolumns)
    update_y_title(fig, process)


def plot(process):
    fig = go.Figure()

    err_list = list()
    df1 = csv_to_df(process.data1_col, err_list)
    df2 = csv_to_df(process.data2_col, err_list)
    if len(err_list) > 0:  # 'データ１、２のX軸がいずれも1つ'以外の時
        fig.update_layout(xaxis=dict(title=' '.join(err_list),))
        return fig.to_html(include_plotlyjs=False)
    # elif  # X軸の型が一致しないときの処理

    default_layout(fig, process)
    set_mode(fig, df1, df2, process)

    return fig.to_html(include_plotlyjs=False)
