import re
import io
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from PIL import Image as PILImage
from django.conf import settings
from django.core.files import File
from image_loader.models import Image as ImageModel

WRONG_FORMAT_STRING_ERROR = 'Неверный формат строки'


class Image:
    """класс работы с изображением"""
    def __init__(self, image_model: ImageModel) -> None:
        self.image_path = str(image_model.resized_image if
                              image_model.resized_image else
                              image_model.image)

        self.resized_image_name_postfix = '_resized'

    def resize(self, width: int = 0, height: int = 0) -> bool:
        """изменение размеров изображения"""
        try:
            full_image_path = settings.MEDIA_ROOT + '/' + self.image_path
            image = PILImage.open(full_image_path)
            resized_image = image.resize(
                self._get_sizes(
                    old_sizes=image.size,
                    width=width,
                    height=height
                )
            )
            self._set_resized_image_name(self.image_path)
            full_resized_image_path = (settings.MEDIA_ROOT + '/' +
                                       self.resized_image_name)
            resized_image.save(full_resized_image_path)

            return True
        except IOError:
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
            path, name, format = get_parts_image_path(image_path)
            self.resized_image_name = (path + '/' + name +
                                       self.resized_image_name_postfix +
                                       '.' + format)


class ImageException(Exception):
    """базовый класс исключений модуля Image"""
    pass


def get_parts_image_path(image_path: str) -> tuple:
    """получить путь, имя и формат изображения"""
    pattern = re.compile('(.*)/(.*)\.(jpg|jpeg|png)', re.IGNORECASE)
    coincidences = re.findall(pattern, image_path)
    if not coincidences:
        raise ImageException(WRONG_FORMAT_STRING_ERROR)
    pockets, *_ = coincidences

    return pockets


def generate_photo_file(name: str = 'test', format: str = 'png') -> io.BytesIO:
    """создание тесового файла"""
    file = io.BytesIO()
    image = PILImage.new(
        'RGBA',
        size=(100, 100),
        color=(155, 0, 0)
    )
    image.save(file, format)
    file.name = name + '.' + format
    file.seek(0)
    return file


def get_remote_image(url: str = '') -> File:
    """получить удаленное изображение"""
    try:
        temp_image = NamedTemporaryFile(dir=settings.MEDIA_ROOT + '/image/')
        _, name, format = get_parts_image_path(url)
        remote_image = urlopen(url).read()
        temp_image.write(remote_image)
        temp_image.flush()
        image = File(temp_image)
        image.name = name + '.' + format

        return image
    except Exception as error:
        raise ImageException(error)
