# Generated by Django 5.1 on 2024-10-28 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden_app', '0016_alter_cart_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='img',
        ),
        migrations.AddField(
            model_name='prof_reg',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='user_reg',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
