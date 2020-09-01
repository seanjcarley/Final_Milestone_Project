from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Image
from django.db.models.functions import Lower

# Create your views here.


def all_images(request):
    """ view to show all images """

    images = Image.objects.all().filter(img_status=True)
    query = None
    sort = None
    sort_dir = None

    if request.GET:
        if 'sort' in request.GET:
            sortKey = request.GET['sort']
            sort = sortKey
            if sortKey == 'img':
                sortKey = 'lower_title'
                images = images.annotate(lower_title=Lower('img_title'))
            if 'direction' in request.GET:
                sort_dir = request.GET['direction']
                if sort_dir == 'desc':
                    sortKey = f'-{sortKey}'
            images = images.order_by(sortKey)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Please enter search details")
                return redirect(reverse('all_images'))

            queries = Q(img_title__icontains=query) \
                | Q(user_id__username__icontains=query) \
                | Q(img_data_id__country__icontains=query) \
                | Q(img_data_id__city__icontains=query) \
                | Q(img_data_id__model__icontains=query) \
                | Q(img_data_id__make__icontains=query)
            images = images.filter(queries).filter(img_status=True)

    if sort == "img_title":
        if sort_dir == 'asc':
            current_sorting = 'Image Title A-Z'
        else:
            current_sorting = 'Image Title Z-A'
    elif sort == "img_rating":
        if sort_dir == 'asc':
            current_sorting = 'Image Rating Low - High'
        else:
            current_sorting = 'Image Rating High - Low'
    elif sort == "base_price":
        if sort_dir == 'asc':
            current_sorting = 'Image Price Low - High'
        else:
            current_sorting = 'Image Price High - Low'
    else:
        current_sorting = 'None_None'

    context = {
        'images': images,
        'search_term': query,
        'current_sorting': current_sorting,
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
