# Generated by Django 4.1 on 2022-10-13 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('palpay', '0017_alter_orders_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='price',
            field=models.FloatField(verbose_name='Price'),
        ),
    ]
