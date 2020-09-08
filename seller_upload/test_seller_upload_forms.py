from django.test import TestCase
from .forms import AddSellerImage, AddSellerImageData
from images.models import Image, Image_Data


class TestAddImageForm(TestCase):
    """ test add seller image form """
    def test_img_title(self):
        """ test the image title field is required """
        form = AddSellerImage({'img_title': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('img_title', form.errors.keys())
        self.assertEqual(
            form.errors['img_title'][0], 'This field is required.')

    def test_base_price(self):
        """ test the base price field is required """
        form = AddSellerImage({'base_price': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('base_price', form.errors.keys())
        self.assertEqual(
            form.errors['base_price'][0], 'This field is required.')

    def test_add_image_meta(self):
        """ test the number of fields in the meta """
        form = AddSellerImage()
        self.assertEqual(
            form.Meta.fields, (
                'img_title', 'img_taken', 'base_price',
                'prev_img', 'tmnl_img'))


class TestAddImageDataForm(TestCase):
    """ test add seller image data form """
    def test_add_image_data_meta(self):
        """ test the number of fields in the meta """
        form = AddSellerImageData()
        self.assertEqual(
            form.Meta.fields, (
                'make', 'model', 'focal_length', 'aperture',
                'shutter_speed_sec', 'iso', 'country', 'city'))
