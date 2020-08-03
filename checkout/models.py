import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from user_profile.models import UserProfile
from images.models import Image
from django_countries.fields import CountryField


# Create your models here.
class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, blank=False)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.CharField(max_length=254, null=False, blank=False)
    phone_no = models.CharField(max_length=20, null=False, blank=False)
    street1 = models.CharField(max_length=100, null=False, blank=False)
    street2 = models.CharField(max_length=100, null=True, blank=True)
    town_city = models.CharField(max_length=30, null=False, blank=False)
    county = models.CharField(max_length=30, null=True, blank=True)
    post_code = models.CharField(max_length=8, null=True, blank=True)
    country = CountryField(blank_label='Country', null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
    )
    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
    )
    original_bag = models.TextField(null=False, blank=False, default='')

    def _generate_order_number(self):
        """ generate unique order no. using uuid """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        pass

    def save(self, *args, **kwargs):
        pass

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='orderitems'
    )
    image = models.ForeignKey(
        Image,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    orderitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
    )

    def save(self, *args, **kwargs):
        pass

    def __str__(self):
        return f'Order Number: {self.order.order_number}'
