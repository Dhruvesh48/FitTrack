from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True, default='SKU-DEFAULT')
    category = models.CharField(max_length=100, choices=[
        ('equipment', 'Equipment'),
        ('nutrition', 'Nutrition'),
        ('merchandise', 'Merchandise'),
    ])
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name