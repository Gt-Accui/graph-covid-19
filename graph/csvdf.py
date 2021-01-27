import pandas as pd
from django.db.models import Q

from .models import CSVColumn


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
            except Exception:
                pass
        df_labels.append(csvcolumn.df_col_label)

    return df_labels

# ↑ 'CSV登録'で使用
# ↓ 'CSV組合せ'で使用


def get_x_label(data_source, err_list):
    try:
        csvcolumn_x = CSVColumn.objects.get(source=data_source, axis='X')
        data_x_csv = csvcolumn_x.csv_col_label
        data_x_df = csvcolumn_x.df_col_label
    except Exception as e_data1_x:
        print('e_data1_x', e_data1_x)
        err_list.append(f'CSV登録で、{data_source}のX軸を1つだけ設定してください。')
        return '', ''
    return data_x_csv, data_x_df


def csv_to_df(data_col, err_list):
    data_source = data_col.source
    data_x_csv, data_x_df = get_x_label(data_source, err_list)
    if data_x_csv + data_x_df == '':
        return pd.DataFrame  # X軸が1つ以外なら空のDFを返す
    data_y_csv = data_col.csv_col_label

    data_csv = pd.read_csv(data_source.csv, encoding='UTF8',)[
        [data_x_csv, data_y_csv]]

    data_csvcolumns = CSVColumn.objects.filter(
        Q(source=data_source) & Q(axis='X') |
        Q(source=data_source) & Q(csv_col_num=data_col.csv_col_num)
    )
    data_csv.columns = get_df_labels(data_csvcolumns, data_csv)
    data_df = data_csv.set_index(data_x_df)

    return data_df


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
