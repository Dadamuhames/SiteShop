# Generated by Django 4.1 on 2022-09-08 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0012_alter_profile_prof_img'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100, verbose_name='Category name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_name', models.CharField(max_length=250, verbose_name='Product name')),
                ('price', models.CharField(max_length=250, verbose_name='Price')),
                ('deskription', models.TextField(max_length=1000, verbose_name='Product description')),
                ('information', models.TextField(max_length=800, verbose_name='Product details')),
                ('category', models.CharField(choices=[("Men's wear", "Men's wear"), ("Women's wear", "Women's wear"), ('Unisex', 'Unisex'), ("Children's wear", "Children's wear"), ('Accessories', 'Accessories'), ('Hats', 'Hats')], max_length=500, verbose_name='Category')),
                ('post_category', models.CharField(choices=[("Men's Shirts", "Men's Shirts"), ("Men's Blazers", "Men's Blazers"), ('Underwear', 'Underwear'), ('Underwear', 'Underwear'), ('Underwear', 'Underwear'), ("women's Blazers", "women's Blazers"), ('skirt', 'skirt'), ('Shoes', 'Shoes'), ("Women's shirts", "Women's shirts"), ('Pijamas', 'Pijamas'), ('Hoodies', 'Hoodies'), ('Caps', 'Caps'), ('Panama hats', 'Panama hats'), ('Rings', 'Rings'), ('Bracelets', 'Bracelets'), ('Wristwatch', 'Wristwatch'), ('Jeans', 'Jeans')], max_length=500, verbose_name='Post_category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Subscribes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=300, verbose_name='Email')),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.products')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_category', models.CharField(max_length=100, verbose_name='Post Category')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.categories')),
            ],
            options={
                'verbose_name': 'Post category',
                'verbose_name_plural': 'Post categories',
            },
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='static/main/img/prod-imgs', verbose_name='Файл')),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.products')),
            ],
            options={
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000, verbose_name='Comment')),
                ('likes', models.IntegerField(verbose_name='Likes')),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.products')),
                ('prof', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prim_key', models.IntegerField(verbose_name='Product ID')),
                ('name', models.CharField(max_length=500, verbose_name='Prod Name')),
                ('price', models.CharField(max_length=500, verbose_name='Price')),
                ('size', models.CharField(choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')], max_length=100, verbose_name='Size')),
                ('quantity', models.IntegerField(default='1', verbose_name='Quantity')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cart item',
                'verbose_name_plural': 'Cart items',
            },
        ),
    ]
