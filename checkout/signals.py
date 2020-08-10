from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderItem


@receiver(post_save, sender=OrderItem)
def update_save(sender, instance, created, **kwargs):
    """ update order total on order item created or update """
    instance.order.update_total()


@receiver(post_delete, sender=OrderItem)
def update_delete(sender, instance, **kwargs):
    """ update order total on order item delete """
    instance.order.update_total()
