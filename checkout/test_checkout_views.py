from django.test import TestCase
from .models import Order


class TestViews(TestCase):
    def test_checkout(self):
        response = self.client.get('checkout/')
        print(response)
        # self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
