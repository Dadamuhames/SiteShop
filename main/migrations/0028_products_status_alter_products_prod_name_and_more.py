# Generated by Django 4.1 on 2022-10-29 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_products_qty_alter_products_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Published', 'Published')], default='Published', max_length=255, verbose_name='Status'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='products',
            name='prod_name',
            field=models.CharField(max_length=255, verbose_name='Product name'),
        ),
        migrations.AlterField(
            model_name='products',
            name='qty',
            field=models.PositiveIntegerField(default=1, verbose_name='Product quntity'),
        ),
    ]
