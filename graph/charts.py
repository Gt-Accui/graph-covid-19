from plotly import graph_objects as go
# from win32 import win32gui


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


'''def plot_size():  # 描画エリアのサイズ（px）を設定
    def get_rect(hwnd):  # 幅と高さを取得
        rect = win32gui.GetWindowRect(hwnd)
        w = rect[2] - rect[0]
        h = rect[3] - rect[1]
        return [w, h]

    fore_size = get_rect(win32gui.GetForegroundWindow())  # ウィンドウ
    desk_size = get_rect(win32gui.GetDesktopWindow())  # デスクトップ
    print(fore_size, desk_size)
    temp_size = [400, 400]  # 最小値を初期値として設定
    twk = 11  # 微調整（tweak）用

    for i in range(2):
        if temp_size[i] < fore_size[i] * 0.96 - twk:
            temp_size[i] = int(fore_size[i] * 0.96 - twk)
            if temp_size[i] > desk_size[i] * 0.96 - twk:
                temp_size[i] = int(desk_size[i] * 0.96 - twk)
            if temp_size[i] > 700:
                temp_size[i] -= i * 200

    if sum(temp_size) > 800:  # 縦横比を調整
        for i in range(2):  # タブボタン等の分、縦を短めに設定
            if temp_size[i] > temp_size[1-i] * (1.5 + (1-i) * 0.7):
                temp_size[i] = int(temp_size[1-i] * (1.5 + (1-i) * 0.7))

    result = temp_size
    return result'''


def default_layout(fig, trg_model):
    # plotsize = plot_size()
    fig.update_layout(
        title=trg_model.name,  # width=plotsize[0], height=plotsize[1],
        xaxis=dict(rangeslider=dict(visible=True),),  # レンジスライダー
        showlegend=True,
        margin=dict(l=50, r=50, t=50, b=50)
    )

# ↑ 共通レイアウト
