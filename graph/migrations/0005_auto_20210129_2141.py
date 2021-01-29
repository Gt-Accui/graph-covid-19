# Generated by Django 3.1.4 on 2021-01-29 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0004_auto_20210129_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='csv_data',
            field=models.TextField(blank=True, null=True, verbose_name='CSVデータ'),
        ),
        migrations.AlterField(
            model_name='source',
            name='csv',
            field=models.FileField(max_length=300, unique=True, upload_to='csv/', verbose_name='CSV'),
        ),
    ]