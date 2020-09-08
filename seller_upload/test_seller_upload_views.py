from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User, AnonymousUser
from images.models import Image, Image_Data
from .views import all_user_images, add_image
from io import BytesIO
from django.contrib.messages import middleware


class TestSellerUploadViews(TestCase):
    """ test seller upload app views """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@test.iw', password='dR0w$$Ap')
        self.img = BytesIO(b'mybinarydata')
        self.img.name = 'myimage.jpg'

    # def test_add_image(self):
    #     response = self.client.post('seller_upload/', {
    #         'img_title': 'Test',
    #         'img_taken': '2020-01-01',
    #         'base_price': 0,
    #         'prev_img': self.img,
    #         'tmnl_img': self.img,
    #         'make': 'test',
    #         'model': 'test',
    #         'focal_length': 1,
    #         'aperture': 'test',
    #         'shutter_speed_sec': 2,
    #         'iso': 3,
    #         'country': 'IE',
    #         'city': 'test',
    #     })
    #     self.assert

    def test_delete_image_not_logged_in(self):
        """ test delete image view not logged in"""
        image = Image.objects.create(
            img_title='test', base_price=0, user_id=self.user)
        request = self.factory.get(f'/delete_image/{image.id}')
        request.user = AnonymousUser()
        self.assertFalse(request.user.is_authenticated)

    def test_delete_image(self):
        """ test delete image view """
        image = Image.objects.create(
            img_title='test', base_price=0, user_id=self.user,
            prev_img='image.jpg', tmnl_img='image.jpg')
        request = self.factory.get(f'/delete_image/{image.id}')
        request.user = self.user
        request.session = {'bag': {image.id: 1}}
        response = all_user_images(request)
        self.assertTrue(request.user.is_authenticated)
        self.assertEqual(response.status_code, 200)
