from plotly import graph_objects as go
# from screeninfo import get_monitors


def get_x_y_data_label(df, csvcolumns):  # X軸、Y軸のデータとラベルを取得
    x_data, x_labels, y_data, y_labels = list(), list(), list(), list()

    for csvcolumn in csvcolumns:
        if csvcolumn.axis == 'X':
            x_data.append(df[csvcolumn.df_col_label])
            x_labels.append(csvcolumn.df_col_label)
        elif csvcolumn.axis == 'Y' and csvcolumn.df_col_label in df.columns:
            y_data.append(df[csvcolumn.df_col_label])
            y_labels.append(csvcolumn.df_col_label)

    return x_data, x_labels, y_data, y_labels


# ↓ グラフの種類ごとの処理

def line_charts(fig, df, csvcolumns):  # 折れ線グラフ
    x_data, x_labels, y_data, y_labels = get_x_y_data_label(df, csvcolumns)
    for i in range(len(y_data)):
        fig.add_trace(go.Scatter(
            x=x_data[0], y=y_data[i], mode='lines',
            line_shape='linear', name=y_labels[i],
            connectgaps=True,
        ))

    fig.update_layout(xaxis=dict(title=x_labels[0],),)


def weekday_charts(fig, df, csvcolumns):  # 曜日ごとの折れ線グラフ
    index_name = csvcolumns.filter(axis='X')[0].df_col_label
    df_i = df.set_index(index_name, drop=False)
    for i in range(7):
        weekday_df = df_i[df_i.index.weekday == i]
        x_data, x_labels, y_data, y_labels = get_x_y_data_label(
            weekday_df, csvcolumns)
        fig.add_trace(go.Scatter(
            x=x_data[0], y=y_data[0], mode='lines',
            line_shape='linear', name=weekday_df.index[0].day_name(),
            connectgaps=True,
        ))

    fig.update_layout(
        xaxis=dict(title=x_labels[0],),
        yaxis=dict(title=y_labels[0],),
    )


def get_sma(df, csvcolumns, window):  # SimpleMovingAverage 単純移動平均
    index_name = csvcolumns.filter(axis='X')[0].df_col_label
    df = df.reset_index().set_index(index_name, drop=False)
    # 'window'ごとに'mean'して'Nan'削除
    df = df.rolling(window).mean().dropna(how='any')
    return df


def sma_charts(fig, df, csvcolumns, window):
    x_data, x_labels, y_data, y_labels = get_x_y_data_label(df, csvcolumns)
    fig.add_trace(go.Scatter(
        x=x_data[0], y=y_data[0], mode='lines',
        line_shape='linear', name=f'{window}日移動平均',
        connectgaps=True,
    ))

    fig.update_layout(
        xaxis=dict(title=x_labels[0],),
        yaxis=dict(title=y_labels[0],),
    )


def bar_charts(fig, df, csvcolumns):  # 積み棒グラフ
    x_data, x_labels, y_data, y_labels = get_x_y_data_label(df, csvcolumns)

    for i in range(len(y_data)):
        fig.add_trace(go.Bar(
            x=x_data[0], y=y_data[i], name=y_labels[i],
        ))

    fig.update_layout(
        barmode='stack',
        xaxis=dict(title=x_labels[0],),
    )

# ↑ グラフの種類ごとの処理
# ↓ 共通レイアウト


def default_layout(fig, trg_model):
    # height = get_monitors()[0].height - 350
    fig.update_layout(
        title=trg_model.name,  # height=height,
        xaxis=dict(rangeslider=dict(visible=True),),  # レンジスライダー
        showlegend=True,
        margin=dict(l=50, r=50, t=50, b=50)
    )

# ↑ 共通レイアウト
