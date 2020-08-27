from django.core.files.uploadedfile import SimpleUploadedFile
from image_loader.forms import (UploadImageForm, ResizeImageForm,
                                ALL_FIELDS_FILLED_ERROR, EMPTY_ITEMS_ERROR)
from image_loader.models import Image
from image_loader.utils.decorators import remove_image_after_test
from image_loader.utils.image import generate_photo_file, get_parts_image_path
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

    @remove_image_after_test([BaseTest.TEST_IMAGE_LINK_NAME])
    def test_success_link_upload(self) -> None:
        """успешная загрузка файла с помощью ссылки"""
        test_image_full_link = (self.TEST_IMAGE_LINK_PATH +
                                self.TEST_IMAGE_LINK_NAME)
        form = UploadImageForm(data={'link': test_image_full_link})
        if form.is_valid():
            new_uploaded_image = form.save()
            image_model = Image.objects.first()
            _, name, _ = get_parts_image_path(test_image_full_link)
            self.assertEqual(image_model, new_uploaded_image)
            self.assertIn(name, test_image_full_link)


class ResizeImageFormTest(BaseTest):
    """тест формы изменения размеров изображения"""
    def test_validation_for_empty_inputs(self) -> None:
        """отображение ошибки формы с пустыми полями"""
        form = ResizeImageForm(data={'width': '', 'height': ''})
        self.assertFalse(form.is_valid())

    @remove_image_after_test(['test.png', 'test_resized.png'])
    def test_success_resize_image(self) -> None:
        """успешное изменение размеров картинки"""
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
