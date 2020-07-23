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
