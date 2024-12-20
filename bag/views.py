from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product
from plan.models import Plan

# Create your views here.
def view_bag(request):
    """A view that renders the bag contents page."""

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id, item_type):
    """
    Add a quantity of the specified product or plan to the shopping bag.
    item_type determines whether it's a 'product' or a 'plan'.
    """
    # Initialize the bag session variable with namespaces for 'products' and 'plans'
    if 'bag' not in request.session:
        request.session['bag'] = {'products': {}, 'plans': {}}

    bag = request.session['bag']  # Access the session variable

    if 'products' not in bag:
        bag['products'] = {}
    if 'plans' not in bag:
        bag['plans'] = {}

    if item_type == 'product':
        item = Product.objects.get(pk=item_id)
    elif item_type == 'plan':
        item = Plan.objects.get(pk=item_id)
    else:
        messages.error(request, "Invalid item type.")
        return redirect(request.POST.get('redirect_url', '/'))

    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url', '/')

    if item_type == 'product':
        size = request.POST.get('product_size', None)

        if size:
            # Check if item_id exists in the 'products' dictionary (using list conversion)
            if item_id in list(bag['products'].keys()):
                if size in bag['products'][item_id]['items_by_size']:
                    bag['products'][item_id]['items_by_size'][size] += quantity
                    messages.success(request, f'Updated size {size.upper()} {item.name} quantity to {bag["products"][item_id]["items_by_size"][size]}')
                else:
                    bag['products'][item_id]['items_by_size'][size] = quantity
                    messages.success(request, f'Added size {size.upper()} {item.name} to your bag')
            else:
                bag['products'][item_id] = {'items_by_size': {size: quantity}}
                messages.success(request, f'Added size {size.upper()} {item.name} to your bag')
        else:
            # Check if item_id exists in the 'products' dictionary (using list conversion)
            if item_id in list(bag['products'].keys()):
                bag['products'][item_id] += quantity
                messages.success(request, f'Updated {item.name} quantity to {bag["products"][item_id]}')
            else:
                bag['products'][item_id] = quantity
                messages.success(request, f'Added {item.name} to your bag')

    elif item_type == 'plan':
        # Check if plan_id exists in the 'plans' dictionary
        if item_id in list(bag['plans'].keys()):
            messages.info(request, f'{item.name} is already in your bag.')
        else:
            bag['plans'][item_id] = {'name': item.name, 'price': float(item.price)}
            messages.success(request, f'Added {item.name} to your bag')

    request.session['bag'] = bag  # Save the updated bag back to the session
    return redirect(redirect_url)



def update_bag_item(request, item_id):
    """Adjust the quantity of the specified product to the specified amount."""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('product_size')
    bag = request.session.get('bag', {})
    
    if size:
        if item_id not in bag:
            bag[item_id] = {'items_by_size': {}}

        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
        else:
            bag[item_id]['items_by_size'].pop(size, None)
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id, None)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id, None)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

def remove_from_bag(request, item_id):
    """Remove an item from the bag."""

    product = get_object_or_404(Product, pk=item_id)
    try:
        size = request.POST.get('product_size', None)  # For products with sizes
        bag = request.session.get('bag', {})

        if size:
            if size in bag[item_id]['items_by_size']:
                del bag[item_id]['items_by_size'][size]
                if not bag[item_id]['items_by_size']:
                    bag.pop(item_id)
                messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return redirect('view_bag')

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
