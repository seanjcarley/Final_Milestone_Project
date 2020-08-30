from django.contrib import admin
from .models import Image, Image_Data

# Register your models here.


class ImagesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'img_title',
        'img_taken',
        'base_price',
        'user_id',
        'img_status',
        'vol_sold',
        'img_rating',
        'img_data_id',
        'date_added',
        'last_updated',
    )

    ordering = ('img_title',)


class Images_DataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'make',
        'model',
        'focal_length',
        'aperture',
        'shutter_speed_sec',
        'iso',
        'country',
        'city',
    )

    ordering = ('make',)


admin.site.register(Image, ImagesAdmin)
admin.site.register(Image_Data, Images_DataAdmin)
