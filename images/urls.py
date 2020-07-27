from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_images, name='all_images'),
    path('<user_id>/', views.user_images, name='user_images'),
]
