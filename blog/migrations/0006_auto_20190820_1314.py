# Generated by Django 2.2.4 on 2019-08-20 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20190820_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='summary',
            field=models.TextField(blank=True, max_length=200, verbose_name='摘要'),
        ),
    ]
