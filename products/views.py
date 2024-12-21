from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Wishlist

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

    category_filter = request.GET.get('category', None)
    
    if category_filter:
        products = Product.objects.filter(category=category_filter)
    else:
        products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'products/product_page.html', context)

@login_required
def product_detail(request, pk):
    """ A view to show individual product details """
     
    product = get_object_or_404(Product, pk=pk)
    is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    context = {
        'product': product,
        'is_in_wishlist': is_in_wishlist,
    }

    return render(request, 'products/product_detail.html', context)

@login_required
def add_to_wishlist(request, product_id):
    """ Add or remove a product from the user's wishlist """

    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()

    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, f"Removed {product.name} from your wishlist.")
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, f"Added {product.name} to your wishlist.")

    return redirect('product_detail', pk=product.id)

@login_required
def remove_from_wishlist(request, product_id):
    """ Remove a product from the user's wishlist """

    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect('wishlist_view')

@login_required
def wishlist_view(request):
    """ Display the user's wishlist """
    
    wishlist_items = Wishlist.objects.filter(user=request.user)

    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'products/wishlist.html', context)