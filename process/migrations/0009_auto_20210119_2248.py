# Generated by Django 3.1.4 on 2021-01-19 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0008_auto_20210119_0051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='data1_col',
        ),
        migrations.AddField(
            model_name='process',
            name='data1_col',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='データ１'),
        ),
        migrations.RemoveField(
            model_name='process',
            name='data2_col',
        ),
        migrations.AddField(
            model_name='process',
            name='data2_col',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='データ２'),
        ),
    ]
