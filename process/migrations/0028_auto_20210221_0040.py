# Generated by Django 3.1.4 on 2021-02-20 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0027_auto_20210220_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='画像URL'),
        ),
        migrations.CreateModel(
            name='Memo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='メモ')),
                ('process', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='memo', to='process.process', verbose_name='対象CSV')),
            ],
            options={
                'verbose_name': '処理・加工_メモ',
                'verbose_name_plural': '処理・加工_メモ',
            },
        ),
    ]
