from django.shortcuts import get_object_or_404
from images.models import Image


def bag_contents(request):
    bag_images = []
    total = 0
    prod_count = 0
    bag = request.session.get('bag', {})

    for image_id, image_data in bag.items():
        image = get_object_or_404(Image, pk=image_id)
        total += image_data * image.base_price
        prod_count += image_data
        bag_images.append({
            'image_id': image_id,
            'quantity': image_data,
            'image': image,
        })

    context = {
        'bag_images': bag_images,
        'total': total,
        'prod_count': prod_count,
    }

    return context
