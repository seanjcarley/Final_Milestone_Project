from django.urls import path
from . import views

urlpatterns = [
    path('', views.top_10_images, name='top_10_images'),
]
