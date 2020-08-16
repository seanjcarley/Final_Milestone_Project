from django.shortcuts import render
from django.http import HttpResponseRedirect
# from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AddSellerImage


# Create your views here.
@login_required
def add_image(request):
    if request.method == 'POST':
        iform = AddSellerImage(request.POST, request.FILES)

        iform_data = {
            'img_title': request.POST['img_title'],
            'img_taken': request.POST['img_taken'],
            'base_price': request.POST['base_price'],
            'image': request.FILES['image'],
            'tmnl_img': request.FILES['tmnl_img'],
        }

        iform = AddSellerImage(iform_data)

        if iform.is_valid():
            iform.save()
            return HttpResponseRedirect('')
    else:
        iform = AddSellerImage()

    template = 'seller_upload/upload.html'
    context = {
        'iform': iform,
    }
    return render(request, template, context)
