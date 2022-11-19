# Generated by Django 4.1 on 2022-11-05 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='facebook',
            field=models.CharField(default='#', max_length=1000, verbose_name='Facebook'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='tel',
            field=models.CharField(default='#', max_length=13, verbose_name='Tel Nbm'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='twitter',
            field=models.CharField(default='#', max_length=1000, verbose_name='Twitter'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='wk',
            field=models.CharField(default='#', max_length=1000, verbose_name='WK'),
        ),
    ]