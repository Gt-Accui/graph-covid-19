# Generated by Django 3.1.4 on 2021-01-14 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plotmode',
            name='mode',
            field=models.CharField(choices=[('lines', '折れ線グラフ'), ('bars', '積み棒グラフ')], default='lines', max_length=100, verbose_name='グラフの種類'),
        ),
    ]
