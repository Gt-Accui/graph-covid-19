from plotly import graph_objects as go


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

def line_charts(fig, df, csvcolumns, y_axis):  # 折れ線グラフ
    x_data, x_labels, y_data, y_labels = get_x_y_data_label(df, csvcolumns)
    for i in range(len(y_data)):
        fig.add_trace(go.Scatter(
            x=x_data[0], y=y_data[i], yaxis=y_axis, mode='lines',
            name=y_labels[i], line_shape='linear',
            connectgaps=True,
        ))

    fig.update_layout(xaxis=dict(title=x_labels[0],),)


def weekday_charts(fig, df, csvcolumns, y_axis):  # 曜日ごとの折れ線グラフ
    index_name = csvcolumns.filter(axis='X')[0].df_col_label
    df_i = df.set_index(index_name, drop=False)
    if y_axis == 'y2': dash = 'dot'
    else: dash = 'solid'

    for i in range(7):
        weekday_df = df_i[df_i.index.weekday == i]
        x_data, x_labels, y_data, y_labels = \
            get_x_y_data_label(weekday_df, csvcolumns)
        fig.add_trace(go.Scatter(
            x=x_data[0], y=y_data[0], yaxis=y_axis, mode='lines',
            name=weekday_df.index[0].strftime('%a'),
            line_shape='linear', line_dash=dash,
            connectgaps=True,
        ))

    fig.update_layout(xaxis=dict(title=x_labels[0],),)
    if y_axis == 'y1':
        fig.update_layout(
            yaxis=dict(title=y_labels[0],),)
    elif y_axis == 'y2':
        fig.update_layout(
            xaxis=dict(title='',),
            yaxis2=dict(
                title='･･･ : '+y_labels[0], side='right', overlaying='y'),
            legend=dict(orientation='h', x=0, yanchor='top', y=-0.5),)


def get_sma(df, csvcolumns, window):  # SimpleMovingAverage 単純移動平均
    index_name = csvcolumns.filter(axis='X')[0].df_col_label
    df = df.reset_index().set_index(index_name, drop=False)
    # 'window'ごとに'mean'して'Nan'削除
    df = df.rolling(window).mean().dropna(how='any')
    return df


def sma_charts(fig, df, csvcolumns, y_axis, window):
    x_data, x_labels, y_data, y_labels = get_x_y_data_label(df, csvcolumns)
    if y_axis == 'y': y_labels = [f'SMA-{window}']
    fig.add_trace(go.Scatter(
        x=x_data[0], y=y_data[0], yaxis=y_axis, mode='lines',
        name=y_labels[0], line_shape='linear',
        connectgaps=True,
    ))

    fig.update_layout(xaxis=dict(title=x_labels[0],),)
    if y_axis == 'y1':
        fig.update_layout(
            yaxis=dict(title=y_labels[0],),)
    elif y_axis == 'y2':
        fig.update_layout(
            yaxis2=dict(title=y_labels[0], side='right', overlaying='y'),
            legend=dict(orientation='h', x=0, yanchor='top', y=-0.5),)


def bar_charts(fig, df, csvcolumns, y_axis):  # 積み棒グラフ
    x_data, x_labels, y_data, y_labels = get_x_y_data_label(df, csvcolumns)

    for i in range(len(y_data)):
        fig.add_trace(go.Bar(
            x=x_data[0], y=y_data[i], yaxis=y_axis, name=y_labels[i],
        ))

    fig.update_layout(
        barmode='stack',
        xaxis=dict(title=x_labels[0],),
    )

# ↑ グラフの種類ごとの処理
# ↓ 共通レイアウト


def default_layout(fig, trg_model):
    fig.update_layout(
        title=trg_model.name,
        xaxis=dict(rangeslider=dict(visible=True),),  # レンジスライダー
        showlegend=True,
        margin=dict(l=50, r=50, t=50, b=50),
    )


def image_default(fig, trg_model):  # 一覧表示用
    fig.update_layout(
        xaxis=dict(title=''),
        margin=dict(l=50, r=5, t=5, b=20),
        legend=dict(orientation='h', x=0, yanchor='top', y=-0.1),
    )

# ↑ 共通レイアウト
