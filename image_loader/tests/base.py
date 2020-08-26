from django.test import TestCase
from image_loader.additional_class.image import generate_photo_file


class BaseTest(TestCase):
    """базовый класс тестов"""
    TEST_LINK_IMAGE = ('https://www.google.com/images/branding/'
        'googlelogo/2x/googlelogo_color_272x92dp.png')

    def _loading_image_throught_post(self) -> None:
        """загрузка изображения через пост запрос"""
        return self.client.post(
            '/loading_image/',
            data={'image': generate_photo_file()},
            format='multipart'
        )
