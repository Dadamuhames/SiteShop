# Generated by Django 4.1 on 2022-11-13 13:52

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_colors_productvariants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colors',
            name='hex',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=18, samples=None),
        ),
    ]
