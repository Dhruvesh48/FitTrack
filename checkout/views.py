from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from plan.models import Plan, UserSubscription
from bag.contexts import bag_contents

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        # Collect form data
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save()

            # Handle products in the bag
            for item_id, item_data in bag.get('products', {}).items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                            lineitem_total=product.price * item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                product_size=size,
                                quantity=quantity,
                                lineitem_total=product.price * quantity,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, "One of the products in your bag wasn't found. Please try again.")
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Handle plans in the bag
            for item_id, item_data in bag.get('plans', {}).items():
                try:
                    plan = Plan.objects.get(id=item_id)
                    duration_days = int(plan.get_duration_in_days())

                    order_line_item = OrderLineItem(
                        order=order,
                        plan=plan,
                        quantity=1,
                        lineitem_total=plan.price * 1,
                    )
                    order_line_item.save()

                    user_subscription, created = UserSubscription.objects.get_or_create(
                        user=request.user,
                        plan=plan,
                        defaults={
                            'start_date': timezone.now(),
                            'active': True,
                        }
                    )
                    # Update or set the subscription end date
                    user_subscription.end_date = user_subscription.start_date + timedelta(days=duration_days)
                    user_subscription.active = True
                    user_subscription.save()

                except Plan.DoesNotExist:
                    messages.error(request, "One of the plans in your bag wasn't found. Please try again.")
                    order.delete()
                    return redirect(reverse('view_bag'))
                except ValueError as e:
                    messages.error(request, f"There was an error with the selected plan: {e}")
                    order.delete()
                    return redirect(reverse('view_bag'))
                except TypeError as e:
                    messages.error(request, f"Unexpected error with plan duration: {e}")
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Save user info to session if requested
            request.session['save_info'] = 'save-info' in request.POST

            # Redirect to checkout success
            return redirect(reverse('checkout_success', args=[order.order_number]))

        else:
            messages.error(request, 'There was an error with your form. Please double-check your information.')

    else:
        # Handle GET requests
        bag = request.session.get('bag', {})
        if not bag:
            return redirect(reverse('plan_list'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)  # Convert to cents
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Please check your environment variables.')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)




def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)