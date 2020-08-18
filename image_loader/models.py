from django.db import models


class Image(models.Model):
    """модель загруженных изображенний"""
    image = models.ImageField(default='', upload_to='image')
    resized_image = models.TextField(default='')
