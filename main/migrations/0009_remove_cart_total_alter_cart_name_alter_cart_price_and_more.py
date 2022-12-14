# Generated by Django 4.1 on 2022-10-12 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_cart_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total',
        ),
        migrations.AlterField(
            model_name='cart',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Prod Name'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.FloatField(verbose_name='Total'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='prim_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.products'),
        ),
    ]
