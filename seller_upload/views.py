from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.forms import formset_factory
# from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AddSellerImage, AddSellerImageData


# Create your views here.
@login_required
def add_image(request):
    ImageFormSet = formset_factory(AddSellerImage)
    ImageDataFormSet = formset_factory(AddSellerImageData)

    if request.method == 'POST':
        iform = ImageFormSet(request.POST, request.FILES, prefix='image')
        dform = ImageDataFormSet(request.POST, prefix='data')

        iform_data = {
            'img_title': request.POST['img_title'],
            'img_taken': request.POST['img_taken'],
            'base_price': request.POST['base_price'],
            'image': request.POST['image'],
            'tmnl_img': request.POST['tmnl_img'],
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

        if iform.is_valid() and dform.is_valid():
            iform = ImageFormSet(iform_data, prefix='image')
            dform = ImageDataFormSet(dform_data, prefix='data')
    else:
        iform = ImageFormSet(prefix='image')
        dform = ImageDataFormSet(prefix='data')

    template = 'seller_upload/upload.html'
    context = {
        'iform': iform,
        'dform': dform,
    }
    return render(request, template, context)
