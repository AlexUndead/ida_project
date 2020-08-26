from typing import Union
from django import forms
from django.core.exceptions import ValidationError
from .models import Image as ImageModel
from .additional_class.image import Image, get_remote_image

ALL_FIELDS_FILLED_ERROR = 'Выберите одно значение'
EMPTY_ITEMS_ERROR = 'Необходимо заполнить хотя бы одно поле'


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
            raise ValidationError(ALL_FIELDS_FILLED_ERROR)
        elif not link and not image:
            raise ValidationError(EMPTY_ITEMS_ERROR)

    def save(self):
        """сохранение данных из формы"""
        image = self.cleaned_data['image']
        link = self.cleaned_data['link']

        if link:
            image = get_remote_image(link)
        return ImageModel.objects.create(image=image)
         

class ResizeImageForm(forms.Form):
    """форма изменения размеров изображенния"""
    width = forms.DecimalField(
        label='Ширина',
        required=False,
        widget=forms.NumberInput(
            attrs={
                'id': 'change_width_image_input',
                'class': 'form-control-file',
            },
        )
    )
    
    height = forms.DecimalField(
        label='Высота',
        required=False,
        widget=forms.NumberInput(
            attrs={
                'id': 'change_height_image_input',
                'class': 'form-control-file',
            },
        )
    )
    
    def __init__(self, instance=None, *args, **kwargs) -> None:
        if instance:
            self.instance = instance
        super().__init__(*args, **kwargs)

    def clean(self) -> Union[None, ValidationError]:
        """
        возвращать ошибку только если оба 
        поля изменения изоброжения пусты
        """
        cleaned_data = super().clean()
        width = cleaned_data['width']
        height = cleaned_data['height']

        if not width and not height:
            raise ValidationError(EMPTY_ITEMS_ERROR)

    def save(self) -> None:
        """сохранение данных из формы"""
        width = self.cleaned_data['width']
        height = self.cleaned_data['height']
        image_model = self.instance
        path = str(image_model.resized_image 
            if image_model.resized_image else image_model.image)
        image = Image(path)
        if image.resize(width, height): 
            image_model.resized_image = image.resized_image_name
            image_model.save()
            return image_model
