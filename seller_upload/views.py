from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AddSellerImage, AddSellerImageData
from images.models import Image, Image_Data
from user_profile.models import UserProfile


# Create your views here.
@login_required
def add_image(request):
    """ handle user adding image to site """
    if request.method == 'POST':
        username = request.user
        iform_data = {
            'img_title': request.POST['img_title'],
            'img_taken': request.POST['img_taken'],
            'base_price': request.POST['base_price'],
            'image': request.POST['image'],
            'tmnl_img': request.POST['tmnl_img'],
            'user_id': username,
        }

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

        iform = AddSellerImage(iform_data)
        print(iform)
        dform = AddSellerImageData(dform_data)
        print(iform.is_valid())
        if iform.is_valid():
            image = iform.save()
            return redirect(reverse('add_image_detail', args=[image.id, dform]))
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


def add_image_detail(request, image_id, dform):
    data = dform.save()
    Image.objects.filter(pk=image_id).update(image_data_id=data.id)
    messages.success(request, 'Image successfully added!')

    return render(request, 'image_detail', image_id)


def image_detail(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    data = get_object_or_404(Image_Data, pk=image.img_data_id)

    context = {
        'image': image,
        'data': data,
    }

    return render(request, 'seller_upload/image_detail.html', context)
