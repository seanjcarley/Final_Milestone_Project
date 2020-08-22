from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AddSellerImage, AddSellerImageData
from images.models import Image, Image_Data
from user_profile.models import UserProfile
from django.db.models import Q


# Create your views here.
@login_required
def add_image(request):
    """ handle user adding image to site """
    if request.method == 'POST':

        dform_data = {
            'make': request.POST['make'],
            'model': request.POST['model'],
            'focal_length': request.POST['focal_length'],
            'aperture': request.POST['aperture'],
            'shutter_speed_sec': request.POST['shutter_speed_sec'],
            'iso': request.POST['iso'],
            'country': request.POST['country'],
            'city': request.POST['city'],
        }

        iform = AddSellerImage(request.POST, request.FILES)
        dform = AddSellerImageData(dform_data)
        if iform.is_valid() and dform.is_valid():
            image = iform.save(commit=False)
            data = dform.save()
            profile = UserProfile.objects.get(user=request.user)
            username = profile.user
            image.user = username
            image.user_id = username
            image.img_data_id = data
            image.save()
            return redirect(reverse('image_detail', args=[image.id, data.id]))
        else:
            messages.error(request, 'Image not uploaded. Please check form.')
    else:
        iform = AddSellerImage()
        dform = AddSellerImageData()

    template = 'seller_upload/upload.html'
    context = {
        'iform': iform,
        'dform': dform,
    }
    return render(request, template, context)


def image_detail(request, image_id, data_id):
    image = Image.objects.get(pk=image_id)
    data = Image_Data.objects.get(pk=data_id)

    if request.user == image.user_id:
        template = 'seller_upload/image_detail.html'
        context = {
            'image': image,
            'data': data,
        }
    else:
        template = 'seller_upload/image_detail.html'
        context = {}

    return render(request, template, context)


def all_user_images(request):
    """ view to show user's images """
    uname = request.user
    query = Q(user_id__username=uname)
    images = Image.objects.filter(query)

    context = {
        'images': images,
    }

    return render(request, 'seller_upload/seller_show_images.html', context)
