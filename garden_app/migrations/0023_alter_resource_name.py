# Generated by Django 5.1 on 2024-11-16 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden_app', '0022_resource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden_app.prof_reg'),
        ),
    ]
