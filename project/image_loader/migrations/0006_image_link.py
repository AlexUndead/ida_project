# Generated by Django 3.1 on 2020-08-20 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_loader', '0005_auto_20200815_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='link',
            field=models.URLField(default=''),
        ),
    ]
