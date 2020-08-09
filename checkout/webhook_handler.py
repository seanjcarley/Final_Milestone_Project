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

    def _send_conf_email(self, order):
        """ send conf email """
        cust_email = order.email
        subject = render_to_string(
            '', {'order': order}
        )
        body = render_to_string(
            '', {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

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
        total = round(intent.charges.data[0].amount /100 , 2)

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
                profile.default_phone_no = shipping_details.phone_no
                profile.default_street1 = shipping_details.address.street1
                profile.default_street2 = shipping_details.address.street2
                profile.default_town_city = shipping_details.address.town_city
                profile.default_county = shipping_details.address.county
                profile.default_post_code = shipping_details.address.post_code
                profile.default_country = shipping_details.address.country
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=shipping_details.email,
                    phone_no__iexact=shipping_details.phone_no,
                    street1__iexact=shipping_details.address.street1,
                    street2__iexact=shipping_details.address.street2,
                    town_city__iexact=shipping_details.address.town_city,
                    county__iexact=shipping_details.address.county,
                    post_code__iexact=shipping_details.address.post_code,
                    country__iexact=shipping_details.address.country,
                    total=total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        
        if order_exists:
            self._send_conf_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200
            )
        else:
            order = None
            try:
                order = Order.objects.get(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=shipping_details.email,
                    phone_no=shipping_details.phone,
                    street1=shipping_details.address.line1,
                    street2=shipping_details.address.line2,
                    town_city=shipping_details.address.town_city,
                    county=shipping_details.address.county,
                    post_code=shipping_details.address.postal_code,
                    country=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
            except expression as identifier:
                pass