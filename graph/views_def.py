import pandas as pd
import io

from .models import Source, CSVData, Image, CSVColumn
from .plot import plot_image


def update_csv(pk, csv):
    Source.objects.update_or_create(
        pk=pk,
        defaults={'csv': csv.name},)


def csv_str(source, csv):
    csv_str = ''
    for line in csv:  # csvを列ごとに取り出し、文字列として結合
        try: line = line.decode(encoding='UTF8')
        except Exception: pass
        csv_str += line

    CSVData.objects.update_or_create(
        source=source,
        defaults={'csv_str': csv_str},)


def updated(pk, last_modified):
    Source.objects.update_or_create(
        pk=pk,
        defaults={'updated_at': last_modified},)


def up_image(source):
    url = plot_image(source)

    Image.objects.update_or_create(
        source=source,
        defaults={'url': url},
    )


def csv_col_def(source):  # CSVの列ラベルをテーブル'CSVColumn'に保存
    csv_str = CSVData.objects.get(source=source).csv_str
    df = pd.read_csv(io.StringIO(csv_str))
    columns = list(df.columns)

    for column in columns:  # 数値はY軸、その他はX軸をデフォルトとする
        if not column.startswith('Unnamed: '):
            col_num = columns.index(column)
            axis = 'Y'
            try: df.iloc[[0], [col_num]].values[0] / 1  # 日付はエラーと判定される
            except Exception: axis = 'X'

            CSVColumn.objects.update_or_create(
                source=source, csv_col_num=col_num, csv_col_label=column,
                defaults={'df_col_label': column, 'axis': axis},
                )
