# Generated by Django 3.1.4 on 2021-02-14 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0012_auto_20210214_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='csv',
            field=models.FileField(max_length=300, unique=True, upload_to='csv/', verbose_name='CSV'),
        ),
    ]