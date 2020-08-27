from django import forms
from django.core.exceptions import ValidationError
from .models import Image as ImageModel
from .utils.image import Image, ImageException, get_remote_image

ALL_FIELDS_FILLED_ERROR = 'Выберите одно значение'
EMPTY_ITEMS_ERROR = 'Необходимо заполнить хотя бы одно поле'
RESIZE_IMAGE_ERROR = 'Не удалось изменить размеры изображения'


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

    field_order = ['link', 'image']

    def clean(self) -> None:
        """очистка данных из формы"""
        cleaned_data = super().clean()
        for error in self.errors:
            raise ValidationError(self.errors[error])
        link = cleaned_data.get('link')
        image = cleaned_data.get('image')

        if link and image:
            raise ValidationError(ALL_FIELDS_FILLED_ERROR)
        if not link and not image:
            raise ValidationError(EMPTY_ITEMS_ERROR)
        if link:
            try:
                cleaned_data['image'] = get_remote_image(link)
            except ImageException as error:
                raise ValidationError(error)

    def save(self) -> ImageModel:
        """сохранение данных из формы"""
        image = self.cleaned_data['image']

        return ImageModel.objects.create(image=image)


class ResizeImageForm(forms.Form):
    """форма изменения размеров изображенния"""
    def __init__(self, *args, instance=None, **kwargs) -> None:
        if instance:
            self.instance = instance
        super().__init__(*args, **kwargs)

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

    def clean(self) -> None:
        """очистка данных из формы"""
        cleaned_data = super().clean()
        for error in self.errors:
            raise ValidationError(self.errors[error])
        width = cleaned_data.get('width')
        height = cleaned_data.get('height')

        if not width and not height:
            raise ValidationError(EMPTY_ITEMS_ERROR)
        try:
            image_model = self.instance
            image = Image(image_model)
            if image.resize(width, height):
                cleaned_data['resized_image'] = image.resized_image_name
        except Exception:
            raise ValidationError(RESIZE_IMAGE_ERROR)

    def save(self) -> ImageModel:
        """сохранение данных из формы"""
        image_model = self.instance
        image_model.resized_image = self.cleaned_data['resized_image']
        image_model.save()
        return image_model
