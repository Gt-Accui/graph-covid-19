# Generated by Django 3.1.4 on 2021-02-23 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0028_auto_20210221_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='更新日'),
        ),
    ]
