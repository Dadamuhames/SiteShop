# Generated by Django 4.1 on 2022-10-23 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_alter_profile_tel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='prof_img',
            field=models.FileField(blank=True, null=True, upload_to='avatars'),
        ),
    ]
