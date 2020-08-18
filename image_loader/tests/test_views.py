import os
from django.conf import settings
from image_loader.models import Image
from .base import BaseTest


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
            os.remove(str(settings.BASE_DIR) + '/media/image/test.png')

    def test_for_invalid_input_without_file(self) -> None:
        """недопустимый ввод: пустое поле загрузки файла"""
        response = self.client.post(
            '/loading_image/', 
            format='multipart'
        )
        self.assertContains(response, 'This field is required')


class ResizeImagePageTest(BaseTest):
    """тест страницы изменения размеров изображения"""
    def test_page_uses_resize_image_template(self) -> None:
        """используется шаблон страницы изменения размеров изображения"""
        new_image = Image.objects.create(image='test_path')
        response = self.client.get(f'/resize_image/{new_image.id}/')
        self.assertTemplateUsed(response, 'resize_image.html')

    def test_succesful_image_resize(self):
        """успешное изенение размеров изображения"""
        self._loading_image_throught_post()
        new_image = Image.objects.first()
        response = self.client.post(
            f'/resize_image/{new_image.id}',
            data={'weight':100, 'height':100}
        )
        self.assertTrue(new_image.resized_image)
