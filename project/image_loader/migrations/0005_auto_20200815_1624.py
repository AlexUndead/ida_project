# Generated by Django 3.1 on 2020-08-15 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_loader', '0004_image_image_resized'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='image_resized',
            new_name='resized_image',
        ),
    ]
