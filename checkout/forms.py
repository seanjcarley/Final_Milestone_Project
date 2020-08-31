from django import forms
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_no', 'street1',
            'street2', 'town_city', 'county', 'post_code',
            'country',
        )

    def __init__(self, *args, **kwargs):
        """
            add placeholder, remove auto-generated labels, and set autofocus
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_no': 'Phone Number',
            'street1': 'Street Address 1',
            'street2': 'Street Address 2',
            'town_city': 'Town Or City',
            'county': 'County',
            'post_code': 'Post Code',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = ''
            self.fields[field].label = False


class CommentForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('comment', 'rating')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'comment': 'Please leave your comment here (max 256 characters)',
            'rating': 'How many stars?',
        }

        self.fields['comment'].widget.attrs['autofocus'] = True
        self.fields['comment'].widget.attrs['placeholder'] = placeholders['comment']
        self.fields['comment'].label = False
        self.fields['rating'].label = placeholders['rating']
