from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderItem

from images.models import Image
from user_profile.models import UserProfile
from user_profile.forms import UserProfileForm
from shopping_bag.contexts import bag_contents

import stripe
import json


# Create your views here.
@require_POST
def cache_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_PRV_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Your order was not processed. \
            Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stp_prv = settings.STRIPE_PRV_KEY
    stp_pub = settings.STRIPE_PUB_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_no': request.POST['phone_no'],
            'street1': request.POST['street1'],
            'street2': request.POST['street2'],
            'town_city': request.POST['town_city'],
            'county': request.POST['county'],
            'post_code': request.POST['post_code'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for image_id, image_data in bag.items():
                try:
                    image = Image.objects.get(id=image_id)
                    order_item = OrderItem(
                        order=order,
                        image=image,
                        quantity=image_data,)
                    order_item.save()
                except Image.DoesNotExist:
                    messages.error(request, (
                        'An Image in you bag was not found! \
                        Please start again.'
                    ))
                    order.delete()
                    return redirect(reverse('show_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(
                reverse('checkout_success', args=[order.order_number])
            )
        else:
            messages.error(request, 'There is an issue with the information you \
                provided. Please check your form.')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, 'Your shopping bag is empty!')
            return redirect(reverse('all_images'))

        current_bag = bag_contents(request)
        total = current_bag['total']
        stripe_total = round(total * 100)
        stripe.api_key = stp_prv
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_no': profile.default_phone_no,
                    'street1': profile.default_street1,
                    'street2': profile.default_street2,
                    'town_city': profile.default_town_city,
                    'county': profile.default_county,
                    'post_code': profile.default_post_code,
                    'country': profile.default_country,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm

    if not stp_pub:
        messages.warning(request, 'Stripe public key is not set! \
            Please contact the website administrator')

    template = 'checkout/checkout.html'

    context = {
        'order_form': order_form,
        'stripe_public_key': stp_pub,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """ successful checkouts """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # attach profile to order
        order.user_profile = profile
        order.save()

        # save user info
        if save_info:
            profile_data = {
                'default_phone_no': order.phone_no,
                'default_street1': order.street1,
                'default_street2': order.street2,
                'default_town_city': order.town_city,
                'default_county': order.county,
                'default_post_code': order.post_code,
                'default_country': order.country
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A conformation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order
    }

    return render(request, template, context)
