# Generated by Django 4.1 on 2022-10-13 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('palpay', '0016_alter_orders_price_alter_orders_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Price'),
        ),
    ]
