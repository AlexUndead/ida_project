import re
from PIL import Image as PILImage
from django.conf import settings
from image_loader.models import Image

class Image:
    """класс работы с изображением"""
    def __init__(self, ImageModel: Image) -> None:
        self.image_path = str(ImageModel.image)
        self.resized_image_path = str(ImageModel.resized_image)
        self.resized_image_name_postfix = '_resized'

    def resize(self, width: int = 0, height: int = 0) -> bool:
        """изменение размеров изображения"""
        try:
            image_path = self.resized_image_path if self.resized_image_path else self.image_path
            image = PILImage.open(settings.MEDIA_ROOT + '/' + image_path)
            resized_image = image.resize(self._get_sizes(image.size, width, height))
            self._set_resized_image_name(image_path)
            resized_image.save(settings.MEDIA_ROOT + '/' + self.resized_image_name)

            return True
        except Exception as error:
            return False

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
            # паттерн для отрезания формата изображения из полного пути
            # чтобы переименновать изображение
            pattern = re.compile('(.*)\.(jpg|jpeg|png)', re.IGNORECASE)
            coincidences, *_ = re.findall(pattern, image_path)
            image_name, image_format = coincidences
            self.resized_image_name = image_name + self.resized_image_name_postfix + '.' + image_format
