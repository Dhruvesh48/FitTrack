from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import UserProfile
from checkout.models import Order

class ProfileAndOrderHistoryViewTest(TestCase):

    def setUp(self):
        """Create a test user, user profile, and an order."""
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        self.order = Order.objects.create(
            order_number='12345',
        )
        
        self.client.login(username='testuser', password='password123')

    def test_profile_view_renders(self):
        """Test that the profile page renders correctly."""
        url = reverse('profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_order_history_view_renders(self):
        """Test that the order history page renders correctly."""
        url = reverse('order_history', args=[self.order.order_number])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')

        self.assertContains(response, self.order.order_number)
