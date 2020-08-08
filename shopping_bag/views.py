from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, reverse
from django.contrib import messages

from images.models import Image


# Create your views here.
def show_bag(request):
    """ view to show bag """
    return render(request, 'shopping_bag/bag.html')


def add_to_bag(request, image_id):
    """ add an image to the shopping bag """
    image = get_object_or_404(Image, pk=image_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    bag = request.session.get('bag', {})

    if image_id in list(bag.keys()):
        bag[image_id] += quantity
        messages.success(
            request, f'Updated {image.img_title} quantity in {bag[image_id]}'
        )
    else:
        bag[image_id] = quantity
        messages.success(request, f'Added {image.img_title} to your Bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def update_bag_quantities(request, image_id):
    """ update the quantities in the bag """

    image = get_object_or_404(Image, pk=image_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[image_id] = quantity
        messages.success(request, f'Updated {image.img_title} \
            quantity to {bag[image_id]}')
    else:
        bag.pop(image_id)
        messages.success(request, f'Removed {image.img_title} from your bag.')

    request.session['bag'] = bag
    return redirect(reverse('show_bag'))
