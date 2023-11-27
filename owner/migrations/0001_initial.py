# Generated by Django 4.2.5 on 2023-10-15 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=120, unique=True)),
                ('author', models.CharField(max_length=80)),
                ('price', models.PositiveIntegerField()),
                ('copies', models.PositiveIntegerField()),
            ],
        ),
    ]
