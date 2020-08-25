from django.shortcuts import render

from images.models import Image

# Create your views here.


def index(request):
    """ view to return index.html"""

    images = Image.objects.filter(
        img_status=True).order_by(
            "-img_rating", "-vol_sold")[:5]

    context = {
        'images': images,
    }

    return render(request, 'home/index.html', context)
