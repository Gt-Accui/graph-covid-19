# Generated by Django 3.1.4 on 2021-01-23 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0014_auto_20210123_1610'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='process',
        ),
        migrations.AddField(
            model_name='process',
            name='曜日ごと',
            field=models.BooleanField(default=False, verbose_name='曜日ごと'),
        ),
        migrations.AddField(
            model_name='process',
            name='７日平均',
            field=models.BooleanField(default=False, verbose_name='７日平均'),
        ),
    ]