from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_image, name='add_image'),
    path(
        'image_detail/<image_id>/<data_id>',
        views.image_detail,
        name='image_detail'),
    path('user_images/', views.all_user_images, name='all_user_images'),
    path('delete_image/<image_id>', views.delete_image, name='delete_image'),
]
