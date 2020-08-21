import os
import re
from urllib.request import urlopen, urlretrieve
from PIL import Image as PILImage
from django.conf import settings
from django.core.files import File
from tempfile import NamedTemporaryFile
from django.core.files import File

class Image:
    """класс работы с изображением"""
    def __init__(self, image_path: str) -> None:
        self.image_path = image_path
        self.resized_image_name_postfix = '_resized'

    def resize(self, width: int = 0, height: int = 0) -> bool:
        """изменение размеров изображения"""
        try:
            image = PILImage.open(settings.MEDIA_ROOT + '/' + self.image_path)
            resized_image = image.resize(self._get_sizes(image.size, width, height))
            self._set_resized_image_name(self.image_path)
            resized_image.save(settings.MEDIA_ROOT + '/' + self.resized_image_name)

            return True
        except Exception as error:
            return False
    
    @staticmethod
    def get_parts_image_path(image_path: str) -> tuple:
        """получить путь, имя и формат изображения"""
        pattern = re.compile('(.*)/(.*)\.(jpg|jpeg|png)', re.IGNORECASE)
        coincidences, *_ = re.findall(pattern, image_path)

        return coincidences

    @staticmethod
    def get_remote_image(url: str = '') -> File:
        """получить удаленное изображение"""
        temp_image = NamedTemporaryFile(dir=settings.MEDIA_ROOT + '/image/')
        _, name, format = Image.get_parts_image_path(url)
        remote_image = urlopen(url).read()
        temp_image.write(remote_image)
        temp_image.flush()
        image = File(temp_image)
        image.name = name + '.' + format

        return image

    def _get_sizes(self, old_sizes: tuple, width: int, height: int) -> tuple:
        """получить пропорциональную ширину и высоту изображения"""
        old_width, old_height = old_sizes
        width = height * old_width // old_height if not width else width
        height = width * old_height // old_width if not height else height

        return (width, height)

    def _set_resized_image_name(self, image_path: str) -> None:
        """получить имя изображения с измененными размерами"""
        if image_path.rfind(self.resized_image_name_postfix) > 0:
            self.resized_image_name = image_path
        else:
            path, name, format = Image.get_parts_image_path(image_path)
            self.resized_image_name = (path + '/' +
                name + self.resized_image_name_postfix + '.' + format)


class ImageException(Exception):
    """базовый класс исключений класса Image"""
    pass
