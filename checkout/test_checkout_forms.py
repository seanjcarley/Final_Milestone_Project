from django.test import TestCase
from .forms import OrderForm


class TestOrderForm(TestCase):
    """ test checkout order form """
    def test_full_name(self):
        """ test the full name field is required """
        form = OrderForm({'full_name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors.keys())
        self.assertEqual(
            form.errors['full_name'][0], 'This field is required.')

    def test_email(self):
        """ test the email field is required """
        form = OrderForm({'email': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())
        self.assertEqual(
            form.errors['email'][0], 'This field is required.')

    def test_phone(self):
        """ test the phone no field is required """
        form = OrderForm({'phone_no': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('phone_no', form.errors.keys())
        self.assertEqual(
            form.errors['phone_no'][0], 'This field is required.')

    def test_street1(self):
        """ test the street1 field is required """
        form = OrderForm({'street1': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('street1', form.errors.keys())
        self.assertEqual(
            form.errors['street1'][0], 'This field is required.')

    def test_town(self):
        """ test the town/city field is required """
        form = OrderForm({'town_city': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('town_city', form.errors.keys())
        self.assertEqual(
            form.errors['town_city'][0], 'This field is required.')

    def test_country(self):
        """ test the country field is required """
        form = OrderForm({'country': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('country', form.errors.keys())
        self.assertEqual(
            form.errors['country'][0], 'This field is required.')

    def test_order_form_meta(self):
        """ test the number of fields in the meta """
        form = OrderForm()
        self.assertEqual(
            form.Meta.fields, ('full_name', 'email', 'phone_no', 'street1',
            'street2', 'town_city', 'county', 'post_code', 'country'))
