from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('loading_image/', views.LoadingImageView.as_view(), name='loading_image'),
    path('resize_image/<int:image_id>/', views.ResizeImageView.as_view(), name='resize_image'),
]
