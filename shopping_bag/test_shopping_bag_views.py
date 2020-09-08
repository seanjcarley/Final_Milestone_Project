from django.test import TestCase
from django.contrib.auth.models import User
from images.models import Image


# Create your tests here.
class TestShoppingBagViews(TestCase):
    """ test shpopping bag views """

    def test_show_bag(self):
        """ test show bag view """
        response = self.client.get('/shopping_bag/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping_bag/bag.html')

    def test_add_to_bag(self):
        """ test add to bag view """
        user = User.objects.create(username='test')
        image = Image.objects.create(
            img_title='test', base_price=0, user_id=user)
        bag = {image.id: 1}
        response = self.client.post('/images/', bag)
        self.assertEqual(response.status_code, 200)
