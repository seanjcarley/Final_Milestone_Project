from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """ add place holders and classes,
        remove auto-generated labels,
        and set autofocus """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_no': 'Phone No.',
            'default_street1': 'Street Address 1',
            'default_street2': 'Street Address 2',
            'default_town_city': 'Town or City',
            'default_county': 'County',
            'default_post_code': 'Post Code',
        }

        self.fields['default_phone_no'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = ''
            self.fields[field].label = False
