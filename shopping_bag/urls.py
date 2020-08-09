from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_bag, name='show_bag'),
    path('add/<image_id>/', views.add_to_bag, name='add_to_bag'),
    path('remove/<image_id>/', views.remove_from_bag, name='remove_from_bag'),
]
