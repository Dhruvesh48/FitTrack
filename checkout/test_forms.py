from django.test import TestCase
from .forms import OrderForm

class TestOrderForm(TestCase):

    def test_form_is_valid(self):
        """Test the form with valid data."""
        order_form = OrderForm({
            'full_name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone_number': '1234567890',
            'street_address1': '123 Test Street',
            'street_address2': '',
            'town_or_city': 'Test Town',
            'postcode': '12345',
            'country': 'US',
            'county': 'Test County',
        })
        self.assertTrue(order_form.is_valid(), msg="Form is invalid")

    def test_form_is_invalid(self):
        """Test the form with invalid data."""
        order_form = OrderForm({
            'full_name': '',
            'email': 'johndoe@example.com',
            'phone_number': '1234567890',
            'street_address1': '123 Test Street',
            'street_address2': '',
            'town_or_city': 'Test Town',
            'postcode': '12345',
            'country': 'US',
            'county': 'Test County',
        })
        self.assertFalse(order_form.is_valid(), msg="Form is valid")
