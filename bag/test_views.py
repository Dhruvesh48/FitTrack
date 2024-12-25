from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
from plan.models import Plan

class BagViewTests(TestCase):

    def setUp(self):
        """Create initial data for testing."""

        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

        self.product = Product.objects.create(
            name="Test Product",
            description="A test product",
            price=10.00,
            sku="SKU-TEST001",
            category="equipment",
            rating=4.5,
            has_sizes=True 
        )

        self.plan = Plan.objects.create(
            name="Test Plan",
            price=50.00,
            duration="monthly",
            features="Test features"
        )

    def test_view_bag_empty(self):
        """Test that the bag view is accessible and renders correctly when the bag is empty."""
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')
        self.assertContains(response, "Your shopping bag is empty.")

    def test_add_product_to_bag(self):
        """Test adding a product to the shopping bag."""
        url = reverse('add_to_bag', args=[self.product.id, 'product'])
        response = self.client.post(url, {'quantity': 1, 'redirect_url': reverse('view_bag')})

        self.assertEqual(response.status_code, 302)
        self.assertIn('bag', self.client.session)
        bag = self.client.session['bag']
        self.assertIn(str(self.product.id), bag['products'])
        self.assertEqual(bag['products'][str(self.product.id)], 1)

    def test_add_plan_to_bag(self):
        """Test adding a plan to the shopping bag."""
        url = reverse('add_to_bag', args=[self.plan.id, 'plan'])
        response = self.client.post(url, {'redirect_url': reverse('view_bag')})

        self.assertEqual(response.status_code, 302)
        self.assertIn('bag', self.client.session)
        bag = self.client.session['bag']
        self.assertIn(str(self.plan.id), bag['plans'])
        self.assertEqual(bag['plans'][str(self.plan.id)]['name'], self.plan.name)

    def test_remove_product_from_bag(self):
        """Test removing a product from the shopping bag."""

        url = reverse('add_to_bag', args=[self.product.id, 'product'])
        self.client.post(url, {'quantity': 1, 'redirect_url': reverse('view_bag')})

        remove_url = reverse('remove_from_bag', args=[self.product.id])
        response = self.client.post(remove_url)

        self.assertEqual(response.status_code, 302)
        bag = self.client.session['bag']
        self.assertNotIn(str(self.product.id), bag['products'])

    def test_remove_plan_from_bag(self):
        """Test removing a plan from the shopping bag."""

        url = reverse('add_to_bag', args=[self.plan.id, 'plan'])
        self.client.post(url, {'redirect_url': reverse('view_bag')})

        remove_url = reverse('remove_from_bag', args=[self.plan.id])
        response = self.client.post(remove_url)

        self.assertEqual(response.status_code, 302)
        bag = self.client.session['bag']
        self.assertNotIn(str(self.plan.id), bag['plans'])
