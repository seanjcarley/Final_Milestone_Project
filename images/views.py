from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Image

# Create your views here.


def all_images(request):
    """ view to show all images """

    images = Image.objects.all()
    query = None
    # sort_name = None
    # sort_dir = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Please enter search details")
                return redirect(reverse('images'))

            queries = Q(img_title__icontains=query) \
                | Q(user_id__username__icontains=query) \
                | Q(img_data_id__country__icontains=query) \
                | Q(img_data_id__city__icontains=query) \
                | Q(img_data_id__model__icontains=query) \
                | Q(img_data_id__make__icontains=query)
            images = images.filter(queries)

    context = {
        'images': images,
        'search_term': query,
    }

    return render(request, 'images/images.html', context)


def top_10_images(request):
    """ view to show all images """
    images = Image.objects.order_by("-img_rating")[:5]

    context = {
        'images': images,
    }

    return render(request, 'images/images.html', context)


def user_images(request, user_id):
    """ view to show all images from a single user """
    images = Image.objects.all()
    query = user_id

    queries = Q(user_id__username=query)
    images = images.filter(queries)

    context = {
        'images': images,
        'user_id': user_id,
    }

    return render(request, 'images/user_images.html', context)
