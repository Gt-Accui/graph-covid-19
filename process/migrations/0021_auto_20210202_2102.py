# Generated by Django 3.1.4 on 2021-02-02 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0020_process_data2_shift'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='data2_shift',
            field=models.SmallIntegerField(default=0, verbose_name='データ２のX軸シフト'),
        ),
    ]