# Generated by Django 4.1 on 2022-09-19 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('palpay', '0003_alter_orderedproducts_product_alter_orders_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedproducts',
            name='quantity',
            field=models.IntegerField(default='1', verbose_name='Quantity'),
        ),
        migrations.AddField(
            model_name='orderedproducts',
            name='size',
            field=models.CharField(default='small', max_length=100, verbose_name='Size'),
            preserve_default=False,
        ),
    ]
