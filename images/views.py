from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Image, Image_Data

# Create your views here.


def all_images(request):
    """ view to show all images """
    images = Image.objects.all()
    query = None
    # sort = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Please enter search details")
                return redirect(reverse('images'))

        queries = Q(img_title__icontains=query) | Q(user_id__icontains=query)
        images = images.filter(queries)

    context = {
        'images': images,
        'search_term': query,
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
