# Generated by Django 2.2.4 on 2019-08-19 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190813_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='summary',
            field=models.CharField(blank=True, max_length=200, verbose_name='博客摘要'),
        ),
    ]