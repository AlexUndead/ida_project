from django import forms
from django.forms import ModelForm, Form
from .models import Image


class UploadImageForm(ModelForm):
    """форма загрузки изображения"""
    path = forms.ImageField(
        widget=forms.FileInput(attrs={'id': 'upload_image_file_input'})
    )

    class Meta:
        model = Image
        fields = ['path']
