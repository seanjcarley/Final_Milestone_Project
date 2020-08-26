from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Order, OrderItem
from images.models import Image
from user_profile.models import UserProfile

import json
import time


class StripeWH_Handler:
    """ handler for webhooks """
    def __init__(self, request):
        self.request = request

    # def _send_conf_email(self, order):
    #     """ send conf email """
    #     cust_email = order.email
    #     subject = render_to_string(
    #         '', {'order': order}
    #     )
    #     body = render_to_string(
    #         '', {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
    #     )

    #     send_mail(
    #         subject,
    #         body,
    #         settings.DEFAULT_FROM_EMAIL,
    #         [cust_email]
    #     )

    def handle_event(self, event):
        """ handle unknown, generic webhooks """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_success(self, event):
        """ handle successful payment intent """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        total = round(intent.charges.data[0].amount / 100, 2)
        print(pid)
        print(total)
        print(bag)

        # omit empty fields
        for field, value in shipping_details.address.items():
            if value == '':
                shipping_details.address[field] = None

        # save user info if save_info checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_no = shipping_details.phone
                profile.default_street1 = shipping_details.address.line1
                profile.default_street2 = shipping_details.address.line2
                profile.default_town_city = shipping_details.address.city
                profile.default_county = shipping_details.address.state
                profile.default_post_code = shipping_details.address.postal_code
                profile.default_country = shipping_details.address.country
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_no__iexact=shipping_details.phone,
                    street1__iexact=shipping_details.address.line1,
                    street2__iexact=shipping_details.address.line2,
                    town_city__iexact=shipping_details.address.city,
                    county__iexact=shipping_details.address.state,
                    post_code__iexact=shipping_details.address.postal_code,
                    country__iexact=shipping_details.address.country,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            # self._send_conf_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | \
                    SUCCESS: Verified order already in database',
                status=200
            )
        else:
            order = None
            try:
                order = Order.objects.get(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_no=shipping_details.phone,
                    street1=shipping_details.address.line1,
                    street2=shipping_details.address.line2,
                    town_city=shipping_details.address.city,
                    county=shipping_details.address.state,
                    post_code=shipping_details.address.postal_code,
                    country=shipping_details.address.country,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for image_id, image_data in json.loads(bag).items():
                    image = Image.objects.get(id=image_id)
                    if isinstance(image_data, int):
                        order_item = OrderItem(
                            order=order,
                            image=image,
                            quantity=image_data,
                        )
                        order_item.save()
                    else:
                        pass
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]}\
                     | ERROR: {e}', status=500)
        # self._send_conf_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]}\
             | SUCCESS: Created order in Webhook', status=200
        )

    def handle_payment_fail(self, event):
        """ handle failed payment intent """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200)
