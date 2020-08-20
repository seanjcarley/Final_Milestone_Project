from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


# Create your models here.
class Image(models.Model):
    prev_img = models.ImageField(null=True, blank=True)
    tmnl_img = models.ImageField(null=True, blank=True)
    img_title = models.CharField(max_length=75, null=False, blank=False)
    img_taken = models.DateField(null=True, blank=True)
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    user_id = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    img_status = models.IntegerField(default=0)
    vol_sold = models.IntegerField(default=0)
    img_rating = models.IntegerField(null=False, blank=False, default=0)
    img_data_id = models.ForeignKey(
        'Image_Data', to_field='id', on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def __str__(self):
        return str(self.id)


class Image_Data(models.Model):

    class Meta:
        verbose_name_plural = 'Image_Data'

    make = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    focal_length = models.IntegerField(null=True, blank=True)
    aperture = models.CharField(max_length=10, null=True, blank=True)
    shutter_speed_sec = models.IntegerField(null=True, blank=True)
    iso = models.IntegerField(null=True, blank=True)
    country = CountryField(blank_label='Country', null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.id)
