from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from plan.models import Plan  # Import Plan model

def bag_contents(request):
    bag_items = []
    total = Decimal(0)  # Initialize total as a Decimal
    product_count = 0
    bag = request.session.get('bag', {'products': {}, 'plans': {}})

    # Handle products
    for item_id, item_data in bag.get('products', {}).items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    # Handle plans
    for item_id, plan_data in bag.get('plans', {}).items():
        # Convert plan price to Decimal before adding it to total
        total += Decimal(plan_data['price'])
        bag_items.append({
            'item_id': item_id,
            'plan': True,
            'name': plan_data['name'],
            'price': plan_data['price'],
        })

    # Calculate delivery and grand total
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = Decimal(0)
        free_delivery_delta = Decimal(0)

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context


