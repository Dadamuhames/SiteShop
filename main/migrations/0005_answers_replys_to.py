# Generated by Django 4.1 on 2022-09-10 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_delete_answtoansw'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='replys_to',
            field=models.CharField(default='dsdsds', max_length=500, verbose_name='Replys to'),
            preserve_default=False,
        ),
    ]
