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

def product_detail(request, pk):
    """ A view to show individual product details """
     
    product = get_object_or_404(Product, pk=pk)

    context = {
        'product': product
    }

    return render(request, 'products/product_detail.html', context)