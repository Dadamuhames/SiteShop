# Generated by Django 4.1 on 2022-10-12 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_wishlist_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='owner',
        ),
    ]
