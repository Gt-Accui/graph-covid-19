from django.db import models
from django.urls import reverse

import sys
sys.path.append('../')
from graph.models import CSVColumn


class Process(models.Model):
    name = models.CharField(
        verbose_name='名称', max_length=200, unique=True,)

    data1_col = models.ForeignKey(
        verbose_name='データ１', to=CSVColumn, on_delete=models.CASCADE,
        related_name='data1_col',
    )
    data2_col = models.ForeignKey(
        verbose_name='データ２', to=CSVColumn, on_delete=models.CASCADE,
        related_name='data2_col',
    )

    process_list = (
        ('shift', '差分'), ('pct_change', '変化率'),
    )
    data1_process = models.CharField(
        verbose_name='データ１の処理', choices=process_list,
        max_length=100, blank=True, null=True, default='')
    data1_periods = models.SmallIntegerField(
        verbose_name='データ１の処理間隔', default=0)
    data2_process = models.CharField(
        verbose_name='データ２の処理', choices=process_list,
        max_length=100, blank=True, null=True, default='')
    data2_periods = models.SmallIntegerField(
        verbose_name='データ２の処理間隔', default=0)

    calc_list = (
        ('1-axis', 'なし（１軸）'), ('2-axis', 'なし（２軸）'),
        ('add', 'たし算： データ１ + データ２'), ('sub', 'ひき算： データ１ − データ２'),
        ('mul', 'かけ算： データ１ × データ２'), ('div', 'わり算： データ１ ÷ データ２'),
    )
    calc = models.CharField(
        verbose_name='データ１、２の演算', choices=calc_list,
        max_length=100, default='1-axis')

    weekday = models.BooleanField(
        verbose_name='曜日ごと(移動平均無効)', default=False)
    sma_num = models.PositiveSmallIntegerField(
        verbose_name='単純移動平均', default=7)

    created_at = models.DateTimeField(
        verbose_name='登録日', auto_now_add=True,)
    updated_at = models.DateTimeField(
        verbose_name='更新日', auto_now=True, blank=True, null=True,)

    def get_absolute_url(self):
        return reverse('process_update', kwargs={'pk': self.id})

    # 以下は管理サイト上の表示設定
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '処理・加工'
        verbose_name_plural = '処理・加工'
