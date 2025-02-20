from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Plan, UserSubscription, ExercisePlan

def plan_list(request):
    plan = Plan.objects.all()
    context = {
        'plan': plan,
    }
    return render(request, 'plan/plan_list.html', context)

def exercise_plan_list(request):
    if not request.user.is_authenticated:
        return redirect('account_login')  # Redirect to login if the user is not logged in
    
    # Check if user has an active subscription
    user_subscription = UserSubscription.objects.filter(user=request.user, active=True).first()

    if not user_subscription:
        # If no active subscription, redirect them to the plan list page
        return redirect('plan_list')  # You can use 'plan_list' URL to redirect to the plan list page
    
    # If the user has an active subscription, show the exercise plans
    exercise_plans = ExercisePlan.objects.all()
    max_plans = 4 if user_subscription.plan.duration == 'monthly' else 1

    context = {
        'exercise_plans': exercise_plans,
        'max_plans': max_plans,
    }
    
    return render(request, 'plan/exercise_plan_list.html', context)




