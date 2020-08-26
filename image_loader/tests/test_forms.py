import os
from django.conf import settings
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from image_loader.forms import UploadImageForm, ResizeImageForm, ALL_FIELDS_FILLED_ERROR, EMPTY_ITEMS_ERROR
from image_loader.additional_class.image import generate_photo_file, get_parts_image_path
from image_loader.models import Image
from .base import BaseTest


class UploadImageFormTest(BaseTest):
    """тест формы загрузки изображения"""
    def test_validation_for_empty_inputs(self) -> None:
        """отображение ошибки формы с пустыми полями"""
        form = UploadImageForm(data={'image': '', 'link': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], [EMPTY_ITEMS_ERROR])

    def test_validation_for_all_filled_inputs(self) -> None:
        """отображение ошибки если все поля заполнены"""
        upload_file = generate_photo_file()
        form = UploadImageForm(
            {'link': 'https://www.google.com/googlelogo_color_272x92dp.png'},
            {'image': SimpleUploadedFile(upload_file.name, upload_file.read())}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], [ALL_FIELDS_FILLED_ERROR])

    def test_success_link_upload(self) -> None:
        """успешная загрузка файла с помощью ссылки"""
        try:
            form = UploadImageForm(data={'link': self.TEST_LINK_IMAGE})
            if form.is_valid():
                new_uploaded_image = form.save()
                image_model = Image.objects.first()
                _, name, format = get_parts_image_path(self.TEST_LINK_IMAGE)
                self.assertEqual(image_model, new_uploaded_image)
                self.assertIn(name, self.TEST_LINK_IMAGE)
        finally:
            test_image_full_path = settings.MEDIA_ROOT + '/image/' + name + '.' + format 
            if os.path.exists(test_image_full_path):
                os.remove(test_image_full_path)


class ResizeImageFormTest(BaseTest):
    """тест формы изменения размеров изображения"""
    def test_validation_for_empty_inputs(self) -> None:
        """отображение ошибки формы с пустыми полями"""
        form = ResizeImageForm(data={'width': '', 'height': ''})
        self.assertFalse(form.is_valid())

    def test_success_resize_image(self) -> None:
        """успешное изменение размеров картинки"""
        try:
            self._loading_image_throught_post()
            image_model = Image.objects.first()
            resize_form = ResizeImageForm(
                data={'width': 300, 'height': 300},
                instance=image_model
            )
            print(resize_form.errors)
            if resize_form.is_valid():
               resize_form.save() 
            image_model.refresh_from_db()
            self.assertTrue(image_model.resized_image)
        finally:
            full_path_test_image = settings.MEDIA_ROOT +  '/image/test.png'
            full_path_test_image_resize = settings.MEDIA_ROOT + '/image/test_resized.png' 
            if os.path.exists(full_path_test_image):
                os.remove(full_path_test_image)
            if os.path.exists(full_path_test_image_resize):
                os.remove(full_path_test_image_resize)
