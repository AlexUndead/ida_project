from django.db import models


class Image(models.Model):
    """модель загруженных изображенний"""
    path = models.ImageField(default='', upload_to='image')
