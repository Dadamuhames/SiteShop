# Generated by Django 4.1 on 2022-09-10 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_answers'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswToAnsw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.answers')),
            ],
        ),
    ]