from django.test import TestCase


class TestHomeViews(TestCase):
    """ test home app views """
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
