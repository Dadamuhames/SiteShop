# Generated by Django 4.1 on 2022-11-19 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('palpay', '0031_shippingtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='ship_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='palpay.shippingtype'),
        ),
    ]