from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_image, name='add_image'),
    path(
        'image_detail/<image_id>/<data_id>',
        views.image_detail,
        name='image_detail'),
]
