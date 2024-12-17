from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.
def product_page(request):
    """ A view to show all products"""

    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'products/product_page.html', context)