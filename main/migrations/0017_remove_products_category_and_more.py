# Generated by Django 4.1 on 2022-10-15 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_delete_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='category',
        ),
        migrations.RemoveField(
            model_name='products',
            name='post_category',
        ),
    ]
