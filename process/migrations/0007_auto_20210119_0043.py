# Generated by Django 3.1.4 on 2021-01-18 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0006_auto_20210118_2310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='data1_col',
        ),
        migrations.AddField(
            model_name='process',
            name='data1_col',
            field=models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='データ１'),
        ),
        migrations.RemoveField(
            model_name='process',
            name='data2_col',
        ),
        migrations.AddField(
            model_name='process',
            name='data2_col',
            field=models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='データ２'),
        ),
    ]
