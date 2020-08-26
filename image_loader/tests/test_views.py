import os
from django.conf import settings
from .base import BaseTest
from image_loader.additional_class.image import get_parts_image_path
from image_loader.models import Image


class HomePageTest(BaseTest):
    """тест домашней страницы"""

    def test_page_uses_index_template(self) -> None:
        """используется шаблон индексной страницы"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Список изображений')

    def test_correct_index_message_without_images(self) -> None:
        """
        корректное сообщение на индексной странице 
        если нет загруженных картинок
        """
        first_uploaded_image = Image.objects.first()
        if not first_uploaded_image:
            response = self.client.get('/')
            self.assertContains(response, 'Нет доступных изображений')


class LoadingImagePageTest(BaseTest):
    """тест страницы загрузки изображения"""
    def test_page_uses_upload_image_template(self) -> None:
        """используется шаблон страницы загрузки изображения"""
        response = self.client.get('/loading_image/')
        self.assertTemplateUsed(response, 'loading_image.html')
        self.assertContains(response, 'Новое изображение')

    def test_redirects_after_POST(self) -> None:
        """переадресует после post"""
        try:
            response = self._loading_image_throught_post()
            new_image = Image.objects.first()
            self.assertRedirects(response, f'/resize_image/{new_image.id}/')
        finally:
            full_path_test_image = settings.MEDIA_ROOT +  '/image/test.png'
            if os.path.exists(full_path_test_image):
                os.remove(full_path_test_image)

    def test_succesful_image_upload(self) -> None:
        """успешная загрузка картинки"""
        try:
            response = self._loading_image_throught_post()
            image_model = Image.objects.first()
            self.assertEqual(image_model.image, 'image/test.png')
        finally:
            full_path_test_image = settings.MEDIA_ROOT +  '/image/test.png'
            if os.path.exists(full_path_test_image):
                os.remove(full_path_test_image)

    def test_succesful_image_link_upload(self) -> None:
        """успешная загрузка картинки с помощью ссылки"""
        try:
            response = self.client.post(
                '/loading_image/',
                data={'link': self.TEST_LINK_IMAGE},
            )
            _, name, format = get_parts_image_path(self.TEST_LINK_IMAGE)
            image_model = Image.objects.first()
            self.assertIn(name + '.' + format, str(image_model.image))
        finally:
            full_path_test_image = settings.MEDIA_ROOT + '/image/' + name + '.' + format 
            if os.path.exists(full_path_test_image):
                os.remove(full_path_test_image)


class ResizeImagePageTest(BaseTest):
    """тест страницы изменения размеров изображения"""
    def test_page_uses_resize_image_template(self) -> None:
        """используется шаблон страницы изменения размеров изображения"""
        new_image = Image.objects.create(image='test_path')
        response = self.client.get(f'/resize_image/{new_image.id}/')
        self.assertTemplateUsed(response, 'resize_image.html')

    def test_succesful_image_resize(self) -> None:
        """успешное изенение размеров изображения"""
        try:
            self._loading_image_throught_post()
            image_model = Image.objects.first()
            response = self.client.post(
                f'/resize_image/{image_model.id}/',
                data={'width':400, 'height':400}
            )
            image_model.refresh_from_db()
            self.assertTrue(image_model.resized_image)
        finally:
            full_path_test_image = settings.MEDIA_ROOT +  '/image/test.png'
            full_path_test_image_resize = settings.MEDIA_ROOT + '/image/test_resized.png' 
            if os.path.exists(full_path_test_image):
                os.remove(full_path_test_image)
            elif os.path.exists(full_path_test_image_resize):
                os.remove(full_path_test_image_resize)

    def test_list_upload_images(self) -> None:
        """список успешно загруженных изображений"""
        try:
            self._loading_image_throught_post()
            model_image = Image.objects.first()
            response = self.client.get('/')
            self.assertContains(response, model_image.image)
        finally:
            full_path_test_image = settings.MEDIA_ROOT +  '/image/test.png'
            if os.path.exists(full_path_test_image):
                os.remove(full_path_test_image)
