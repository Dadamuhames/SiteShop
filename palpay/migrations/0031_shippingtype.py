# Generated by Django 4.1 on 2022-11-17 13:55

import django.core.validators
from django.db import migrations, models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('palpay', '0030_orderedproducts_variant'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(1.0)], verbose_name='Price')),
                ('img', easy_thumbnails.fields.ThumbnailerImageField(upload_to='shipping-img')),
            ],
        ),
    ]
