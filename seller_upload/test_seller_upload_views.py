from django.test import TestCase


class TestSellerUploadViews(TestCase):
    """ test seller upload app views """
    def test_add_image(self):
        response = self.client.get('seller_upload/')
        print(response)
        # self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'seller_upload/upload.html')

    def test_image_detail(self):
        response = self.client.get('seller_upload/image_detail/2/2')
        self.assertEqual(response.status_code, 404)
