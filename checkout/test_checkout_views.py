from django.test import TestCase, Client
from .models import Order
from django.contrib.auth.models import User
from images.models import Image
import uuid


class TestCheckoutViews(TestCase):
    """ test checkout views """
    def test_checkout_empty_bag(self):
        """ test checkout view for empty bag """
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('images/images.html')

    def test_checkout(self):
        c = Client()
        user = User.objects.create(username='test')
        image = Image.objects.create(
            img_title='test', base_price=0, user_id=user)
        bag = {image.id: 1}

    def test_checkout_success(self):
        """ test checkout success view """
        order = Order.objects.create(order_number=uuid.uuid4().hex.upper())
        response = self.client.get(
            f'/checkout/checkout_success/{order.order_number}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('checkout/checkout_success.html')
