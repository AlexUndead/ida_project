# Generated by Django 3.1 on 2020-08-20 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_loader', '0006_image_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='link',
        ),
    ]
