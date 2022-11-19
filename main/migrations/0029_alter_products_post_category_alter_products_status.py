# Generated by Django 4.1 on 2022-10-29 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_products_status_alter_products_prod_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='post_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.postcategories'),
        ),
        migrations.AlterField(
            model_name='products',
            name='status',
            field=models.CharField(choices=[('Scheduled', 'Scheduled'), ('Inactive', 'Inactive'), ('Published', 'Published')], max_length=255, verbose_name='Status'),
        ),
    ]
