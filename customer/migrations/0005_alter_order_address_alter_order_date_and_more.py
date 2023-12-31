# Generated by Django 4.2.5 on 2023-11-10 10:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(max_length=120),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='expected_delivery_date',
            field=models.DateField(default=datetime.datetime(2023, 11, 15, 15, 45, 38, 203382), null=True),
        ),
    ]
