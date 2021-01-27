# Generated by Django 3.1.4 on 2021-01-19 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0002_auto_20210114_2207'),
        ('process', '0009_auto_20210119_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='data1_col',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='data1_col', to='graph.csvcolumn', verbose_name='データ１'),
        ),
        migrations.AlterField(
            model_name='process',
            name='data2_col',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='data2_col', to='graph.csvcolumn', verbose_name='データ２'),
        ),
    ]