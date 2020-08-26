from django.views import View
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Image
from .forms import UploadImageForm, ResizeImageForm


class IndexView(View):
    """Индексная страница"""
    def get(self, request: HttpRequest) -> HttpResponse:
        upload_images = Image.objects.all()
        return render(request, 'index.html', context={'upload_images': upload_images})


class LoadingImageView(View):
    """Страница загрузки изображения"""
    def get(self, request: HttpRequest) -> HttpResponse:
        upload_image_form = UploadImageForm()
        return render(
            request,
            'loading_image.html',
            context={'upload_image_form': upload_image_form}
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        upload_image_form = UploadImageForm(
            data=request.POST,
            files=request.FILES
        )
        if upload_image_form.is_valid():
            image_model = upload_image_form.save()
            return redirect('resize_image', image_model.id)
        return render(
            request,
            'loading_image.html',
            context={'upload_image_form': upload_image_form}
        )


class ResizeImageView(View):
    """Страница изменения размеров изображения"""
    def get(self, request: HttpRequest, image_id: int) -> HttpResponse:
        image = get_object_or_404(Image, pk=image_id)
        resize_form = ResizeImageForm()
        return render(request, 'resize_image.html', context={'image': image, 'resize_form': resize_form})

    def post(self, request: HttpRequest, image_id: int) -> HttpResponse:
        image = get_object_or_404(Image, pk=image_id)
        resize_form = ResizeImageForm(data=request.POST, instance=image)
        if resize_form.is_valid():
            resize_form.save()
        return render(request, 'resize_image.html', context={'image': image, 'resize_form': resize_form})
