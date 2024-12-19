from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50, choices=[('monthly', 'Monthly'), ('weekly', 'Weekly')])
    features = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_duration_in_days(self):
        """Converts the duration to days."""
        if self.duration == 'monthly':
            return 30
        elif self.duration == 'weekly':
            return 7
        return 0

    def __str__(self):
        return self.name


class ExercisePlan(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """Automatically calculate the end date based on the plan's duration."""
        if not self.end_date:
            duration_days = self.plan.get_duration_in_days()
            self.end_date = self.start_date + timedelta(days=duration_days)

        if self.end_date < timezone.now():
            self.active = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} ({'Active' if self.active else 'Inactive'})"
