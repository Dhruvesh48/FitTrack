from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Plan, ExercisePlan, UserSubscription
from django.utils import timezone
from datetime import timedelta

class PlanViewsTestCase(TestCase):

    def setUp(self):
        """Set up test data and client"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        
        self.plan = Plan.objects.create(
            name="Monthly Plan", 
            description="A monthly subscription plan.", 
            price=20.00, 
            duration="monthly", 
            features="Feature 1, Feature 2"
        )

        self.exercise_plan = ExercisePlan.objects.create(
            title="Exercise Plan 1", 
            description="Exercise description", 
            file="exercise1.pdf"
        )

        self.user_subscription = UserSubscription.objects.create(
            user=self.user, 
            plan=self.plan, 
            start_date=timezone.now(), 
            active=True
        )

    def test_plan_list_view(self):
        """Test the plan list view."""
        url = reverse('plan_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.plan.name)

    def test_exercise_plan_list_view_authenticated(self):
        """Test the exercise plan list view for authenticated users."""
        url = reverse('exercise_plan_list')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.exercise_plan.title)

    def test_user_subscription_end_date_calculation(self):
        """Test the automatic calculation of the subscription's end date."""
        subscription = self.user_subscription
        expected_end_date = subscription.start_date + timedelta(days=30)
        self.assertEqual(subscription.end_date.date(), expected_end_date.date())

    def test_user_subscription_inactive_after_end_date(self):
        """Test that the subscription is marked as inactive after the end date."""
        past_end_date = timezone.now() - timedelta(days=1)
        self.user_subscription.end_date = past_end_date
        self.user_subscription.save()
        self.assertFalse(self.user_subscription.active)
