# Generated by Django 4.1 on 2022-09-03 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_profile_instagram_alter_profile_prof_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='prof_img',
            field=models.ImageField(blank=True, null=True, upload_to='static/account/profile', verbose_name='Аватарка'),
        ),
    ]
