# Generated by Django 3.1.4 on 2021-01-29 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0003_auto_20210119_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='csv',
            field=models.CharField(max_length=300, unique=True, verbose_name='CSV'),
        ),
    ]