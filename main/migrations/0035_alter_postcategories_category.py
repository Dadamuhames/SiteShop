# Generated by Django 4.1 on 2022-11-02 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_categories_ctg_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcategories',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_ctg', to='main.categories'),
        ),
    ]
