import io
from django.test import TestCase
from PIL import Image


class BaseTest(TestCase):
    """базовый класс тестов"""
    def _loading_image_throught_post(self) -> None:
        """загрузка изображения через пост запрос"""
        return self.client.post(
            '/loading_image/',
            data={'image': self._generate_photo_file()},
            format='multipart'
        )

    def _generate_photo_file(self) -> io.BytesIO:
        """создание тесового файла"""
        file = io.BytesIO()
        image = Image.new(
            'RGBA',
            size=(100, 100),
            color=(155, 0, 0)
        )
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file
