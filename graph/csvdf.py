import pandas as pd
from django.db.models import Q
import io

from .models import CSVColumn, CSVData
# from copy import deepcopy


# ↓ 'CSV登録'で使用

def get_df_labels(csvcolumns, csv):
    df_labels = list()
    for csvcolumn in csvcolumns:
        csv_col_label = csvcolumn.csv_col_label
        try:  # 数値（1で割れる）か判定
            csv[csv_col_label][0] / 1
        except Exception:  # エラーなら
            try:  # 日時に変換、上書きしてみるテスト ← try tryの目的
                csv[csv_col_label] = pd.to_datetime(csv[csv_col_label])
            except Exception: pass
        df_labels.append(csvcolumn.df_col_label)

    return df_labels

# ↑ 'CSV登録'で使用
# ↓ 'CSV組合せ'で使用


def get_x_label(data_source, err_list):
    try:
        csvcolumn_x = CSVColumn.objects.get(source=data_source, axis='X')
        data_x_csv = csvcolumn_x.csv_col_label
        data_x_df = csvcolumn_x.df_col_label
    except Exception:
        err_list.append(f'CSV登録で、{data_source}のX軸を1つだけ設定してください。')
        return '', ''
    return data_x_csv, data_x_df


def csv_to_df(data_col, err_list):
    data_source = data_col.source
    data_x_csv, data_x_df = get_x_label(data_source, err_list)
    if data_x_csv + data_x_df == '':
        return pd.DataFrame  # X軸が1つ以外なら空のDFを返す
    data_y_csv = data_col.csv_col_label

    csv_str = CSVData.objects.get(source=data_source).csv_str
    df = obj_to_col(pd.read_csv(io.StringIO(csv_str)))
    data_csv = df[[data_x_csv, data_y_csv]]

    data_csvcolumns = CSVColumn.objects.filter(
        Q(source=data_source) & Q(axis='X') |
        Q(source=data_source) & Q(csv_col_num=data_col.csv_col_num)
    )
    data_csv.columns = get_df_labels(data_csvcolumns, data_csv)
    data_df = data_csv.set_index(data_x_df)

    return data_df


def df_process(df, process, periods):
    if process and periods:
        try:  # index が日付のとき
            periods_str = f'{periods}D'
            if process == 'shift': return df.shift(freq=periods_str)
            elif process == 'difference': return df - df.shift(freq=periods_str)
            elif process == 'pct_change': return df.pct_change(freq=periods_str)
            else: return df
        except Exception:
            if process == 'shift': return df.shift(periods)
            elif process == 'difference': return df.diff(periods)
            elif process == 'pct_change': return df.pct_change(periods)
            else: return df
    else:
        return df


def get_csvcolumns(process):
    data_source = process.data1_col.source
    data1_col = process.data1_col
    data2_col = process.data2_col
    csvcolumns = CSVColumn.objects.select_related().filter(
        Q(source=data_source) & Q(axis='X') |
        Q(source=data1_col.source) & Q(csv_col_num=data1_col.csv_col_num) |
        Q(source=data2_col.source) & Q(csv_col_num=data2_col.csv_col_num)
    )  # .distinct()  # 重複削除

    return csvcolumns

# ↑ 'CSV組合せ'で使用
# ↓ 共用


def obj_to_col(df, col_num=3):
    df_col = len(df.columns)
    for i, col in enumerate(df.columns):
        if not i:
            df_i = df.set_index(col, drop=False)
            res = df_i[col].drop_duplicates()
            df_i = df_i.drop(columns=col)
            continue
        if type(df_i[col][0]) == str and df_i[col][0] != '0':
            groups = df_i.groupby(col, as_index=False)
            for group in groups.groups:
                tmp = groups.get_group(group).drop(columns=col)
                if df_col == col_num: tmp.columns = [group]
                else: tmp = tmp.add_prefix(group + '_')
                res = pd.concat([res, tmp], axis=1)
            return res
    return df


def df_slice(df, rows):  # 一覧表示で使用
    df_rows = len(df)
    if df_rows > rows:
        df = df[df_rows - rows:df_rows]
    return df

# ↑ 共用
