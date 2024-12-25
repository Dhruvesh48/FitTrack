from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from products.models import Product
from plan.models import Plan
from checkout.models import Order, OrderLineItem

class CheckoutViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

        self.product = Product.objects.create(
            name='Test Product',
            description='A test product',
            price=10.00,
            sku='TESTSKU',
            category='equipment'
        )

        self.plan = Plan.objects.create(
            name='Test Plan',
            description='A test plan',
            price=20.00,
            duration='monthly',
            features='Feature1, Feature2'
        )

    def test_checkout_view(self):
        self.client.login(username='testuser', password='password123')

        session = self.client.session
        session['bag'] = {
            'products': {
                str(self.product.id): 2
            },
            'plans': {
                str(self.plan.id): {
                    'name': self.plan.name,
                    'price': str(self.plan.price),
                    'duration': self.plan.get_duration_in_days(),
                }
            }
        }
        session.save()

        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_checkout_success_view(self):
        self.client.login(username='testuser', password='password123')

        session = self.client.session
        session['bag'] = {
            'products': {
                str(self.product.id): 2
            },
            'plans': {
                str(self.plan.id): {
                    'name': self.plan.name,
                    'price': str(self.plan.price),
                    'duration': self.plan.get_duration_in_days(),
                }
            }
        }
        session.save()

        response = self.client.post(reverse('checkout'), {
            'full_name': 'Test User',
            'email': 'testuser@example.com',
            'phone_number': '1234567890',
            'country': 'US',
            'postcode': '12345',
            'town_or_city': 'Test Town',
            'street_address1': '123 Test Street',
            'street_address2': '',
            'county': 'Test County',
            'client_secret': 'test_secret',
        })
        self.assertEqual(response.status_code, 302)

        order = Order.objects.latest('id')
        response = self.client.get(reverse('checkout_success', args=[order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
