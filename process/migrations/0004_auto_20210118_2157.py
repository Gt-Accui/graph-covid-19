# Generated by Django 3.1.4 on 2021-01-18 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0002_auto_20210114_2207'),
        ('process', '0003_auto_20210117_2122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='data1_name',
        ),
        migrations.AddField(
            model_name='process',
            name='data1_name',
            field=models.ManyToManyField(default='default', to='graph.Source', verbose_name='データ１'),
        ),
    ]
