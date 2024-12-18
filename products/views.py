from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.
def product_page(request):
    """ A view to show all products"""

    products = Product.objects.all()

    sort_by = request.GET.get('sort_by', None)
    if sort_by == 'price_low_to_high':
        products = products.order_by('price')
    elif sort_by == 'price_high_to_low':
        products = products.order_by('-price')
    elif sort_by == 'rating_high_to_low':
        products = products.order_by('-rating')
    elif sort_by == 'rating_low_to_high':
        products = products.order_by('rating')

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