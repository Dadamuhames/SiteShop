# Generated by Django 4.1 on 2022-09-25 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('palpay', '0012_alter_orders_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedproducts',
            name='img',
            field=models.FileField(blank=True, null=True, upload_to='static/main/img/order_prod_img'),
        ),
    ]
