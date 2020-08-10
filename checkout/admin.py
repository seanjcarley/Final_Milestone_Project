from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('orderitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdmin,)

    readonly_fields = (
        'order_number', 'date', 'order_total',
        'grand_total', 'original_bag')

    fields = (
        'order_number', 'user_profile', 'full_name',
        'email', 'phone_no', 'street1', 'street2',
        'town_city', 'county', 'post_code', 'country',
        'date', 'order_total', 'grand_total', 'original_bag',
        'stripe_pid')

    list_display = (
        'order_number', 'date', 'full_name', 'order_total',
        'grand_total',
    )

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
