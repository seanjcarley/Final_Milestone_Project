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
                phone_no =
                street1 =
                street2 = 