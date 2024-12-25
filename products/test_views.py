from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Wishlist

class ProductViewsTest(TestCase):

    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.product = Product.objects.create(
            name='Test Product',
            price=100.00,
            description='This is a test product.',
            rating=4.5,
            category='Test Category'
        )
        self.add_to_wishlist_url = reverse('add_to_wishlist', args=[self.product.id])

    def test_product_detail_view_authenticated(self):
        """Test product detail view as authenticated user"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_add_to_wishlist_authenticated(self):
        """Test adding product to wishlist"""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.add_to_wishlist_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Wishlist.objects.filter(user=self.user, product=self.product).exists())

    def test_wishlist_view_authenticated(self):
        """Test wishlist view as authenticated user"""
        self.client.login(username='testuser', password='password123')
        Wishlist.objects.create(user=self.user, product=self.product)
        response = self.client.get(reverse('wishlist_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
