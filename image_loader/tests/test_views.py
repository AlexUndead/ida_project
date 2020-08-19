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
            os.remove(settings.MEDIA_ROOT + '/image/test.png')

    def test_succesful_image_upload(self) -> None:
        """успешная загрузка картинки"""
        response = self.client.post(
            '/loading_image/',
            data={'image': self._generate_photo_file()},
            format='multipart',
        )
        image_model = Image.objects.first()
        self.assertEqual(image_model.image, 'image/test.png')

    def test_succesful_image_link_upload(self) -> None:
        """успешная загрузка картинки с помощью ссылки"""
        response = self.client.post(
            '/loading_image/',
            data={'link': 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'},
            format='multipart',
        )
        image_model = Image.objects.first()
        self.assertEqual(image_model.image, 'image/googlelogo_color_272x92dp.png')


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
            os.remove(settings.MEDIA_ROOT + '/image/test.png')

    def test_list_upload_images(self) -> None:
        """список успешно загруженных изображений"""
        self._loading_image_throught_post()
        model_image = Image.objects.first()
        response = self.client.get('/')
        self.assertContains(response, model_image.image)
