from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AddSellerImage, AddSellerImageData, EditSellerImage
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
    """ Shows the details of an image just added """
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
    images = Image.objects.filter(query).order_by('-img_rating', '-vol_sold')

    context = {
        'images': images,
    }

    return render(request, 'seller_upload/seller_show_images.html', context)


@login_required
def edit_image_details(request, image_id):
    """ edit image options """
    image = get_object_or_404(Image, pk=image_id)
    data = get_object_or_404(Image_Data, pk=image.img_data_id.id)

    if request.user == image.user_id or request.user.is_superuser:
        if request.method == 'POST':
            iform = EditSellerImage(
                request.POST, request.FILES, instance=image)
            dform = AddSellerImageData(
                request.POST, instance=data)
            if iform.is_valid() and dform.is_valid():
                image = iform.save()
                data = dform.save()
                messages.success(request, 'Details updated successfully!')
                if request.user == image.user_id:
                    return redirect(
                        reverse('all_user_images'))
                else:
                    return redirect(
                        reverse('all_images_su'))
            else:
                messages.error(
                    request, 'Image not updated. Please check form.')
        else:
            iform = EditSellerImage(instance=image)
            dform = AddSellerImageData(instance=data)
            messages.info(request, f'Editing {image.img_title}')

        template = 'seller_upload/edit_seller_image.html'
        context = {
            'iform': iform,
            'dform': dform,
            'image': image,
        }

        return render(request, template, context)
    else:
        messages.error(request, 'Tut tut tut! You cannot edit that.')
        return redirect(reverse('home'))


@login_required
def delete_image(request, image_id):
    """ delete an image """
    image = get_object_or_404(Image, pk=image_id)
    data = get_object_or_404(Image_Data, pk=image.img_data_id.id)

    if request.user == image.user_id:
        image.delete()
        data.delete()
        messages.success(request, 'Image deleted.')
        return redirect(reverse('all_user_images'))
    else:
        messages.error(request, 'Tut tut tut! You cannot delete that.')
        return redirect(reverse('home'))


def all_images_su(request):
    """ view to show user's images """
    images = Image.objects.all()

    context = {
        'images': images,
    }

    return render(request, 'seller_upload/seller_show_images.html', context)
