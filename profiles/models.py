from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from datetime import datetime

class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information, order history, and subscription plan
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    
    plan_start_date = models.DateTimeField(null=True, blank=True)
    plan_end_date = models.DateTimeField(null=True, blank=True)
    
    PLAN_TYPE_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    plan_type = models.CharField(
        max_length=10,
        choices=PLAN_TYPE_CHOICES,
        default='monthly',
    )

    plan_status = models.CharField(
        max_length=20, 
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='inactive'
    )

    def __str__(self):
        return self.user.username

    def is_plan_active(self):
        """
        Check if the user's plan is still active.
        """
        now = datetime.now()
        return self.plan_status == 'active' and self.plan_end_date > now

    def get_plan_duration(self):
        """
        Get the duration of the plan as a human-readable string.
        """
        if self.plan_type == 'weekly':
            return f"Weekly plan (starts: {self.plan_start_date}, ends: {self.plan_end_date})"
        else:
            return f"Monthly plan (starts: {self.plan_start_date}, ends: {self.plan_end_date})"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
