# Generated by Django 4.1 on 2022-10-13 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('palpay', '0015_alter_orders_adres_alter_orders_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='price',
            field=models.FloatField(verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Performed', 'Performed'), ('Delivered', 'Delivered')], default='Accepted', max_length=255, verbose_name='Status'),
        ),
    ]
