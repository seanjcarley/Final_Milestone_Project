from django import forms
from images.models import Image, Image_Data


class AddSellerImage(forms.ModelForm):
    class Meta:
        model = Image
        exclude = (
            'user_id', 'img_status', 'vol_sold', 'img_rating', 'img_data_id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'img_title': 'Title displayed on site',
            'img_taken': 'Date you took the photo',
            'base_price': 'Price for a 6x4 print',
            'image': 'Upload preview image',
            'tmnl_img': 'Upload tumbnail image',
        }

        self.fields['img_title'].widget.attrs['autofocus'] = True
        for field in self.fields:
            print(placeholders[field])
            if field != 'image':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            else:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].widget.attrs['class'] = ''
            self.fields[field].label = False


class AddSellerImageData(forms.ModelForm):
    class Meta:
        model = Image_Data
        fields = (
            'make', 'model', 'focal_length',
            'aperture', 'shutter_speed_sec', 'iso',
            'country', 'city',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'make': 'Make of Camera used',
            'model': 'Model of the Camera used',
            'focal_length': 'the Focal Length setting used',
            'aperture': 'the Aperature setting used',
            'shutter_speed_sec': 'the Shutter Speed setting used',
            'iso': 'the ISO setting used',
            'country': 'Country where the photo was taken',
            'city': 'Town or City where the image was taken',
        }

        # self.fields['img_title'].widget.attrs['autofocus'] = True
        for field in self.fields:
            print(placeholders[field])
            if field != 'image':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            else:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].widget.attrs['class'] = ''
            self.fields[field].label = False
