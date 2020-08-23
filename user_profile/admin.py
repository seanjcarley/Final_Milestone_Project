from django.contrib import admin
from .models import UserProfile


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'default_phone_no',
        'default_street1',
        'default_street2',
        'default_town_city',
        'default_county',
        'default_post_code',
        'default_country',
        'seller',
    )

    ordering = ('id',)


admin.site.register(UserProfile, UserProfileAdmin)
