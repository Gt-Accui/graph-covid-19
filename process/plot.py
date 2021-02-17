import plotly.graph_objects as go
import cloudinary
import cloudinary.uploader
import cloudinary.api

import sys
sys.path.append('../')
from graph.charts import line_charts, weekday_charts, get_sma, sma_charts
from graph.charts import default_layout, image_default
from graph.csvdf import csv_to_df, df_process, get_csvcolumns, df_slice


def df_calc(fig, df1, df2, process):
    calc = process.calc
    calc_dic = {'add': df1.add, 'sub': df1.sub, 'mul': df1.mul, 'div': df1.div}
    df_list = list()
    if calc and 'axis' not in calc:
        df2.columns = df1.columns
        df_list.append(calc_dic[calc](df2))
    else:
        df_list.extend([df1, df2])
    return df_list


def update_y_title(fig, process):
    calc = process.calc
    if calc and 'axis' not in calc:
        symbol_dic = {
            'add': '+', 'sub': '-', 'mul': '×', 'div': '÷', None: ' '}
        calc_symbol = symbol_dic[calc]
        fig.update_layout(
            yaxis=dict(title=f'{process.data1_col}<br>{calc_symbol}  {process.data2_col}'),
            showlegend=False)
    else:
        fig.update_layout(
            yaxis=dict(showgrid=False),
            yaxis2=dict(showgrid=False),
        )


def set_mode(fig, df1, df2, process):
    csvcolumns = get_csvcolumns(process)
    y_axis = 'y1'
    calc = process.calc
    if process.weekday:  # 曜日ごと
        df_list = df_calc(fig, df1, df2, process)
        for df in df_list:
            weekday_charts(fig, df.reset_index(), csvcolumns, y_axis)
            if calc == '2-axis': y_axis = 'y2'  # ２軸のとき df2 を右の軸に
    elif process.sma_num:  # 単純移動平均
        window = process.sma_num
        df1_sma = get_sma(df1, csvcolumns, window)
        df2_sma = get_sma(df2, csvcolumns, window)
        df_list = df_calc(fig, df1_sma, df2_sma, process)
        for df in df_list:
            sma_charts(fig, df.reset_index(), csvcolumns, y_axis, window)
            if calc == '2-axis': y_axis = 'y2'
    else:
        df_list = df_calc(fig, df1, df2, process)
        for df in df_list:
            line_charts(fig, df.reset_index(), csvcolumns, y_axis)
            if calc == '2-axis': y_axis = 'y2'
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
    df1 = df_process(df1, process.data1_process, process.data1_periods)
    df2 = df_process(df2, process.data2_process, process.data2_periods)

    default_layout(fig, process)
    set_mode(fig, df1, df2, process)

    return fig.to_html(include_plotlyjs=False)


def plot_image(process):
    fig = go.Figure()

    err_list = list()
    df1 = csv_to_df(process.data1_col, err_list)
    df2 = csv_to_df(process.data2_col, err_list)
    if len(err_list) > 0:
        fig.update_layout(xaxis=dict(title=' '.join(err_list),))
        return fig.to_html(include_plotlyjs=False)
    df1 = df_process(df1, process.data1_process, process.data1_periods)
    df2 = df_process(df2, process.data2_process, process.data2_periods)
    rows = 189
    df1 = df_slice(df1, rows)
    df2 = df_slice(df2, rows)

    set_mode(fig, df1, df2, process)
    image_default(fig, process)

    image_name = './process/static/process/image/' + process.name + '.svg'
    fig.write_image(image_name, scale=0.5, engine='kaleido')
    res = cloudinary.uploader.upload(
        open(image_name, 'rb'), public_id=process.name)
    return res['secure_url']
