# Generated by Django 4.1 on 2022-09-21 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('palpay', '0007_orders_status_alter_orders_cash'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='order_img',
            field=models.FileField(blank=True, null=True, upload_to='static/main/img/order_img'),
        ),
    ]