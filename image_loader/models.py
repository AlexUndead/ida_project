from django.db import models


class Image(models.Model):
    """модель загруженных изображенний"""
    image = models.ImageField(default='', upload_to='image')
    resized_image = models.TextField(default='')

    #def save(self, *args, **kwargs) -> None:
    #    """метод сохранения данных"""
    #    if self.link:
    #        image_name, _ = AdditImage.get_image_name_and_format(self.link)
    #        image_file = AdditImage.get_remote_image(self.link)
    #        self.image.save(image_name, image_file)
    #    super().save(*args, **kwargs)
