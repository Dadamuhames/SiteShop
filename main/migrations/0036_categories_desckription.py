# Generated by Django 4.1 on 2022-11-03 11:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_alter_postcategories_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='desckription',
            field=models.TextField(default=django.utils.timezone.now, verbose_name='Desckription'),
            preserve_default=False,
        ),
    ]
