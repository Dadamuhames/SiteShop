# Generated by Django 4.1 on 2022-09-04 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_profile_prof_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='prof_img',
            field=models.FileField(blank=True, null=True, upload_to='media/static/accounts/profile'),
        ),
    ]
