from django import forms
from .models import Image as ImageModel
from django.core.exceptions import ValidationError
from .additional_class.image import Image


class UploadImageForm(forms.Form):
    """форма загрузки изображения"""
    image = forms.ImageField(
        label='Файл',
        required=False,
        widget=forms.FileInput(
            attrs={
                'id': 'upload_image_file_input',
                'class': 'form-control-file',
            },
        )
    )
    link = forms.URLField(
        label='Ссылка',
        required=False,
        widget=forms.URLInput(
            attrs={
                'id': 'upload_image_link_input',
                'class': 'form-control-file',
            },
        )
    )

    def clean(self):
        """очистка данных из формы"""
        cleaned_data = super().clean()
        link = cleaned_data['link']
        image = cleaned_data['image']

        if link and image:
            raise ValidationError('Выберите одно значение')
        elif not link and not image:
            raise ValidationError('Необходимо заполнить хотя бы одно поле')

    def save(self):
        """сохранение данных из формы"""
        image = self.cleaned_data['image']
        link = self.cleaned_data['link']

        if link:
            image = Image.get_remote_image(link)
        new_image = ImageModel.objects.create(image=image)

        return new_image
