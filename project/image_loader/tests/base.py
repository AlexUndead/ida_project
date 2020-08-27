from django.test import TestCase
from image_loader.utils.image import generate_photo_file


class BaseTest(TestCase):
    """базовый класс тестов"""
    TEST_IMAGE_LINK_PATH = ('https://www.google.com/images/branding/'
                            'googlelogo/2x/')
    TEST_IMAGE_LINK_NAME = 'googlelogo_color_272x92dp.png'

    def _loading_image_throught_post(self) -> None:
        """загрузка изображения через пост запрос"""
        return self.client.post(
            '/loading_image/',
            data={'image': generate_photo_file()},
            format='multipart'
        )
