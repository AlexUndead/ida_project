import re
from PIL import Image
from django.conf import settings

class BaseImage:
    """класс работы с изображением"""
    @staticmethod
    def resize_image(image_path: str = '', width: int = 0, height: int = 0) -> str:
        """изменение размеров изображения"""
        image_name_postfix = '_resized'
        image = Image.open(settings.MEDIA_ROOT + '/' + image_path)
        old_width, old_height = image.size
        weight = height * old_width // old_height if not width else width
        height = weight * old_height // old_width if not height else height
        resized_image = image.resize((weight, height))
        # паттерн для отрезания формата изображения из полного пути
        # чтобы переименновать изображение
        pattern = re.compile('(.*)\.(jpg|jpeg|png)', re.IGNORECASE)
        image_name, image_format = re.findall(pattern, image_path)[0]
        new_image_name = image_name + image_name_postfix + '.' + image_format
        resize_image_path = settings.MEDIA_ROOT + '/' + new_image_name
        resized_image.save(resize_image_path)

        return new_image_name
