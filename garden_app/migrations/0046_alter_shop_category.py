# Generated by Django 5.1 on 2025-03-20 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden_app', '0045_alter_shop_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='category',
            field=models.CharField(choices=[('Nurseries & Plant Retailers', 'Nurseries & Plant Retailers'), ('Supply Stores', 'Supply Stores'), ('Specialty', 'Specialty')], max_length=100),
        ),
    ]
