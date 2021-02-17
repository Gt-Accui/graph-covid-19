# Generated by Django 3.1.4 on 2021-02-13 11:46

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0009_source_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source',
            name='image',
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('source', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='graph.source', verbose_name='対象CSV')),
            ],
            options={
                'verbose_name': '画像',
                'verbose_name_plural': '画像',
            },
        ),
    ]