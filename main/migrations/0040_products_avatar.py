# Generated by Django 4.1 on 2022-11-07 10:48

from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_alter_comments_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='avatar',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='prod-avatar'),
        ),
    ]
