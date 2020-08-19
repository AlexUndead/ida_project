from django import forms
from django.forms import ModelForm, Form
from .models import Image


class UploadImageForm(ModelForm):
    """форма загрузки изображения"""
    image = forms.ImageField(
        required=True,
        label='Файл',
        widget=forms.FileInput(
            attrs={
                'id': 'upload_image_file_input',
                'class': 'form-control-file',
            },
        )
    )

    class Meta:
        model = Image
        fields = ['image']
