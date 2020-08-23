from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


# Create your models here.
class UserProfile(models.Model):
    """ user profile for default delivery info """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_no = models.CharField(max_length=20, null=True, blank=True)
    default_street1 = models.CharField(max_length=100, null=True, blank=True)
    default_street2 = models.CharField(max_length=100, null=True, blank=True)
    default_town_city = models.CharField(max_length=50, null=True, blank=True)
    default_county = models.CharField(max_length=30, null=True, blank=True)
    default_post_code = models.CharField(max_length=10, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True, blank=True)
    seller = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """ creates a profile if none, or updates existing one """
    if created:
        UserProfile.objects.create(user=instance)

    # saves existing profile
    instance.userprofile.save()
