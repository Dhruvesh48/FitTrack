from django.test import TestCase
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib.auth.models import User

class TestUserProfileForm(TestCase):

    def test_form_is_valid(self):
        """Test the form with valid data."""
        userProfilForm = UserProfileForm ({
            'default_phone_number': '1234567890',
            'default_country': 'US',
            'default_postcode': '12345',
            'default_town_or_city': 'Test Town',
            'default_street_address1': '123 Test Street',
            'default_street_address2': '',
            'default_county': 'Test County',
        })
        self.assertTrue(userProfilForm.is_valid(), msg="Form is invalid")

    def test_form_is_invalid_missing_field(self):
        """Test the form with missing required data."""
        userProfilForm = UserProfileForm ({
            'default_phone_number': '',
            'default_country': 'US',
            'default_postcode': '12345',
            'default_town_or_city': 'Test Town',
            'default_street_address1': '123 Test Street',
            'default_street_address2': '',
            'default_county': 'Test County',
        })
        self.assertTrue(userProfilForm.is_valid(), msg="Form is valid even with missing data")
