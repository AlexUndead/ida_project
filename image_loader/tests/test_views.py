import os
import io
from PIL import Image as PILImage
from django.test import TestCase
from image_loader.models import Image


class HomePageTest(TestCase):
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


class LoadingImagePageTest(TestCase):
    """тест страницы загрузки изображения"""
    def test_page_uses_upload_image_template(self) -> None:
        """используется шаблон страницы загрузки изображения"""
        response = self.client.get('/loading_image/')
        self.assertTemplateUsed(response, 'loading_image.html')
        self.assertContains(response, 'Новое изображение')

    def test_redirects_after_POST(self):
        """переадресует после post"""
        response = self.client.post(
            '/loading_image/', 
            data={'path': self._generate_photo_file()},
            format='multipart'
        )
        new_image = Image.objects.first()
        self.assertRedirects(response, f'/resize_image/{new_image.id}/')
        os.remove(os.getcwd() + '/image/test.png')

    def test_for_invalid_input_without_file(self):
        """недопустимый ввод: пустое поле загрузки файла"""
        response = self.client.post(
            '/loading_image/', 
            format='multipart'
        )
        self.assertContains(response, 'This field is required')

    def _generate_photo_file(self) -> io.BytesIO:
        """создание тесового файла"""
        file = io.BytesIO()
        image = PILImage.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file


class ResizeImagePageTest(TestCase):
    """тест страницы изменения размеров изображения"""
    def test_page_uses_resize_image_template(self) -> None:
        """используется шаблон страницы изменения размеров изображения"""
        new_image = Image.objects.create(path='test_path')
        response = self.client.get(f'/resize_image/{new_image.id}/')
        self.assertTemplateUsed(response, 'resize_image.html')
