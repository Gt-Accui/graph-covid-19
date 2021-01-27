# Generated by Django 3.1.4 on 2021-01-26 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0017_auto_20210123_1728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='sevendays',
        ),
        migrations.AddField(
            model_name='process',
            name='sma_num',
            field=models.PositiveSmallIntegerField(default=7, verbose_name='単純移動平均'),
        ),
        migrations.AlterField(
            model_name='process',
            name='calc',
            field=models.CharField(blank=True, choices=[('add', 'たし算： データ１ + データ２'), ('sub', 'ひき算： データ１ − データ２'), ('mul', 'かけ算： データ１ × データ２'), ('div', 'わり算： データ１ ÷ データ２')], default='', max_length=100, null=True, verbose_name='データ１、２の演算'),
        ),
    ]
