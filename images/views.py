from django.shortcuts import render
from .models import Image

# Create your views here.


def all_images(request):
    """ view to show all images """
    images = Image.objects.all()
    print(images)

    context = {
        'images': images,
    }

    return render(request, 'images/images.html', context)


def top_10_images(request):
    """ view to show all images """
    images = Image.objects.order_by("-img_rating")[:5]
    print(images)

    context = {
        'images': images,
    }

    return render(request, 'images/images.html', context)
