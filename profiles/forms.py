from django import forms
from .models import UserProfile
from django_countries.widgets import CountrySelectWidget

class UserProfileForm(forms.ModelForm):
    """
    Form for updating the user's profile information without plan-related fields.
    """
    class Meta:
        model = UserProfile
        fields = [
            'default_phone_number', 
            'default_country', 
            'default_postcode', 
            'default_town_or_city',
            'default_street_address1',
            'default_street_address2',
            'default_county'
        ]
        widgets = {
            'default_country': CountrySelectWidget(attrs={'class': 'form-control stripe-style-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        # Define placeholders
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_country': 'Country',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            placeholder = placeholders.get(field, field.replace('_', ' ').title())
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
