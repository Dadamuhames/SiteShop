# Generated by Django 4.1 on 2022-11-04 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('palpay', '0022_alter_orderedproducts_img_alter_orders_order_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderedproducts',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='palpay.orders'),
        ),
    ]