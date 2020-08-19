from django.views import View
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .additional_class.image import Image
from .models import Image as ImageModel
from .forms import UploadImageForm


class IndexView(View):
    """Индексная страница"""
    def get(self, request: HttpRequest) -> HttpResponse:
        upload_images = ImageModel.objects.all()
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
    """Страница изменения размеров изображения"""
    def get(self, request: HttpRequest, image_id: int) -> HttpResponse:
        image = get_object_or_404(ImageModel, pk=image_id)
        return render(request, 'resize_image.html', context={'image': image})

    def post(self, request: HttpRequest, image_id: int) -> HttpResponse:
        image_model = get_object_or_404(ImageModel, pk=image_id)
        width = int(request.POST.get('width')) if request.POST.get('width') else 0
        height = int(request.POST.get('height')) if request.POST.get('height') else 0
        error_message = ''

        try:
            if width or height:
                image = Image(image_model)        
                if image.resize(width, height) and not image_model.resized_image:
                    image_model.resized_image = image.resized_image_name
                    image_model.save()
            else:
                error_message = 'Необходимо ввести хотя бы одно значение'
        except Exception as error:
            error_message = error
        finally:
            return render(
                request, 
                'resize_image.html', 
                context={'image': image_model, 'error': error_message}
            )
