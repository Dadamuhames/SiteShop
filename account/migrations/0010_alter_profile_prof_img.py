# Generated by Django 4.1 on 2022-09-03 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_profile_prof_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='prof_img',
            field=models.ImageField(blank=True, null=True, upload_to='static/accounts/profile'),
        ),
    ]