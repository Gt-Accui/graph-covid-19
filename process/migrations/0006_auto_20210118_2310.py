# Generated by Django 3.1.4 on 2021-01-18 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0002_auto_20210114_2207'),
        ('process', '0005_auto_20210118_2255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='data1_name',
        ),
        migrations.RemoveField(
            model_name='process',
            name='data2_name',
        ),
        migrations.AlterField(
            model_name='process',
            name='calc',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='データ１、２の演算'),
        ),
        migrations.RemoveField(
            model_name='process',
            name='data1_col',
        ),
        migrations.AddField(
            model_name='process',
            name='data1_col',
            field=models.ManyToManyField(default='default', related_name='data1_col', to='graph.CSVColumn', verbose_name='データ１'),
        ),
        migrations.RemoveField(
            model_name='process',
            name='data2_col',
        ),
        migrations.AddField(
            model_name='process',
            name='data2_col',
            field=models.ManyToManyField(default='default', related_name='data2_col', to='graph.CSVColumn', verbose_name='データ２'),
        ),
        migrations.AlterField(
            model_name='process',
            name='process',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='曜日ごと、７日平均'),
        ),
    ]
