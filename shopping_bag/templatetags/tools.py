from django import template

register = template.Library()


@register.filter(name='calc_sub')
def calc_sub(price, quantity):
    return price * quantity
