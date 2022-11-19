# Generated by Django 4.1 on 2022-09-17 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_answers_replys_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Your name')),
                ('price', models.IntegerField(verbose_name='Price')),
                ('city', models.CharField(choices=[('Ташкент', 'Ташкент'), ('Самарканд', 'Самарканд'), ('Бухара', 'Бухара'), ('Хива', 'Хива'), ('Шахрисабз', 'Шахрисабз'), ('Муйнак', 'Муйнак'), ('Заамин', 'Заамин'), ('Термез', 'Термез'), ('Термез', 'Термез'), ('Гулистан', 'Гулистан'), ('Нукус', 'Нукус'), ('Наманган', 'Наманган'), ('Карши', 'Карши'), ('Навои', 'Навои'), ('Коканд', 'Коканд'), ('Андижан', 'Андижан'), ('Фергана', 'Фергана')], max_length=500, verbose_name='Country')),
                ('adres', models.CharField(max_length=500, verbose_name='Your adress')),
                ('your_number', models.CharField(max_length=13, verbose_name='Tel. number')),
                ('date', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderedProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palpay.orders')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cart')),
            ],
        ),
    ]