from django.test import TestCase
from django.contrib.auth.models import User


# Create your tests here.
class TestViews(TestCase):
    """ test images views """
    def test_all_images(self):
        """ test the all images view """
        response = self.client.get('/images/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/images.html')

    def test_user_images(self):
        """ test user images view """
        user = User.objects.create(username='test')
        response = self.client.get(f'/images/{user.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/user_images.html')
