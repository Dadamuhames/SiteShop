# Generated by Django 4.1 on 2022-11-17 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0057_products_colors'),
        ('palpay', '0029_alter_orders_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedproducts',
            name='variant',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='main.productvariants'),
            preserve_default=False,
        ),
    ]
