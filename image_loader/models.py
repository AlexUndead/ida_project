from django.db import models
from django.conf import settings


class Image(models.Model):
    """модель загруженных изображенний"""
    image = models.ImageField(
        default='',
        upload_to=settings.IMAGE_UPLOAD_FOLDER
    )
    resized_image = models.TextField(default='')
