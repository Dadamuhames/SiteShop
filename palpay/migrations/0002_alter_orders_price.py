# Generated by Django 4.1 on 2022-09-17 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('palpay', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Price'),
        ),
    ]