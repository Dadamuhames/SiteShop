# Generated by Django 4.1 on 2022-10-13 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('palpay', '0018_alter_orders_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderedproducts',
            name='img',
            field=models.FileField(blank=True, null=True, upload_to='static/main/img/order_img'),
        ),
    ]
