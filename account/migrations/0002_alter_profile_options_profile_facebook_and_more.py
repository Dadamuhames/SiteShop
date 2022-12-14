# Generated by Django 4.1 on 2022-09-02 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
        migrations.AddField(
            model_name='profile',
            name='facebook',
            field=models.CharField(default='none', max_length=1000, verbose_name='Facebook'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram',
            field=models.CharField(default='none', max_length=1000, verbose_name='Instagram'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter',
            field=models.CharField(default='none', max_length=1000, verbose_name='Twitter'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='wk',
            field=models.CharField(default='none', max_length=1000, verbose_name='WK'),
            preserve_default=False,
        ),
    ]
