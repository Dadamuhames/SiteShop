# Generated by Django 4.1 on 2022-10-12 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0010_rename_prim_key_cart_product_alter_cart_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='name',
        ),
        migrations.AlterField(
            model_name='cart',
            name='size',
            field=models.CharField(choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')], max_length=255, verbose_name='Size'),
        ),
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.FloatField(verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.products'),
        ),
    ]
