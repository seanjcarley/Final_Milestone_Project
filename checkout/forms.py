from django import forms
from .models import Order


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
