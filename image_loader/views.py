from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Image
from .forms import UploadImageForm


class IndexView(View):
    """Индексная страница"""
    def get(self, request: HttpRequest) -> HttpResponse:
        images = Image.objects.all()
        return render(request, 'index.html', context={'images': images})


class LoadingImageView(View):
    """Страницы загрузки изображения"""
    def get(self, request: HttpRequest) -> HttpResponse:
        upload_image_form = UploadImageForm()
        return render(
            request,
            'loading_image.html',
            context={'upload_image_form': upload_image_form}
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        upload_image_form = UploadImageForm(files=request.FILES)
        if upload_image_form.is_valid():
            image = upload_image_form.save()
            return redirect('resize_image', image.id)
        return render(
            request,
            'loading_image.html',
            context={'upload_image_form': upload_image_form}
        )


class ResizeImageView(View):
    """Страницы изменения размеров изображения"""
    def get(self, request: HttpRequest, image_id: int) -> HttpResponse:
        image = get_object_or_404(Image, pk=image_id)
        return render(request, 'resize_image.html', context={'image': image})
