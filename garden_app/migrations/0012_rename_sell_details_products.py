# Generated by Django 5.1 on 2024-09-28 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garden_app', '0011_sell_details_delete_reminder'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='sell_details',
            new_name='products',
        ),
    ]
