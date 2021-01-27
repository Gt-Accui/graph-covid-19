from django.db import models
from os import path
from django.urls import reverse


class Source(models.Model):
    name = models.CharField(
        verbose_name='名称', max_length=200, unique=True,)
    source = models.CharField(
        verbose_name='出典', max_length=200, blank=True, null=True,)
    url = models.URLField(
        verbose_name='URL', max_length=300, blank=True, null=True,)
    csv = models.FileField(
        verbose_name='CSV', max_length=300, upload_to='csv/', unique=True,)
    ''' メモ欄追加するか '''
    created_at = models.DateTimeField(
        verbose_name='登録日', auto_now_add=True,)
    updated_at = models.DateTimeField(
        verbose_name='更新日', auto_now=True, blank=True, null=True,)

    def filename(self):  # ファイル名のみを返す
        return path.basename(self.csv.name)

    def save(self, *args, **kwargs):  # 既存CSVがあれば削除後に新規保存
        try:
            this = Source.objects.get(id=self.id)
            if this.csv != self.csv:
                this.csv.delete(save=False)
        except Exception:
            pass
        super(Source, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('update', kwargs={'pk': self.id})

    # 以下は管理サイト上の表示設定
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '参照ファイル'
        verbose_name_plural = '参照ファイル'


class CSVColumn(models.Model):
    source = models.ForeignKey(
        verbose_name='対象CSV', to=Source, on_delete=models.CASCADE,
        editable=False,)
    csv_col_num = models.PositiveSmallIntegerField(
        verbose_name='列番号', blank=True, null=True,)
    csv_col_label = models.CharField(
        verbose_name='ラベル', max_length=100, blank=True,
        null=True,)
    df_col_label = models.CharField(
        verbose_name='表示名', max_length=100, blank=True,
        null=True,)
    axislist = (('X', 'X'), ('Y', 'Y'),)
    axis = models.CharField(
        verbose_name='軸', choices=axislist, max_length=1, blank=True,
        null=True,)

    # 以下は管理サイト上の表示設定
    def __str__(self):
        return f'{self.source} - {self.csv_col_num} {self.csv_col_label}'

    class Meta:
        verbose_name = 'CSVからDFへの変換設定'
        verbose_name_plural = 'CSVからDFへの変換設定'


class PlotMode(models.Model):
    source = models.ForeignKey(
        verbose_name='対象CSV', to=Source, on_delete=models.CASCADE,
        editable=False,)
    modelist = (
        ('lines', '折れ線グラフ'),
        ('bars', '積み棒グラフ'),
    )
    mode = models.CharField(
        verbose_name='グラフの種類', choices=modelist, max_length=100,
        default='lines',)

    # 以下は管理サイト上の表示設定
    def __str__(self):
        return f'{self.source} - {self.mode}'

    class Meta:
        verbose_name = 'グラフの種類'
        verbose_name_plural = 'グラフの種類'
