# Generated by Django 5.1 on 2024-11-16 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden_app', '0020_pay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='quantity',
            field=models.IntegerField(max_length=100),
        ),
    ]
