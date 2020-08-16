from django.shortcuts import render

from images.models import Image, Image_Data

# Create your views here.


def index(request):
    """ view to return index.html"""

    images = Image.objects.order_by("-img_rating")[:5]

    context = {
        'images': images,
    }

    return render(request, 'home/index.html', context)
