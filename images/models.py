from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.


class Image(models.Model):
    image = models.ImageField(null=True, blank=True)
    tmnl_img = models.ImageField(null=True, blank=True)
    img_title = models.CharField(max_length=75, null=False, blank=False)
    img_taken = models.DateField()
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    img_status = models.IntegerField()
    vol_sold = models.IntegerField()
    img_rating = models.IntegerField(null=False, blank=False)
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
    focal_length = models.IntegerField()
    aperture = models.CharField(max_length=10, null=True, blank=True)
    shutter_speed_sec = models.IntegerField()
    iso = models.IntegerField()
    country = CountryField(blank_label='Country', null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.id)
