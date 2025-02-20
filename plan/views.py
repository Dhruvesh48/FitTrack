from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Plan, UserSubscription, ExercisePlan

def plan_list(request):
    plan = Plan.objects.all()
    context = {
        'plan': plan,
    }
    return render(request, 'plan/plan_list.html', context)

def exercise_plan_list(request):
    exercise_plans = []
    max_plans = 0  # Default for non-logged-in users

    if request.user.is_authenticated:  # Ensure only authenticated users query DB
        user_subscription = UserSubscription.objects.filter(user=request.user, active=True).first()

        if user_subscription:
            exercise_plans = ExercisePlan.objects.all()
            max_plans = 4 if user_subscription.plan.duration == 'monthly' else 1

    context = {
        'exercise_plans': exercise_plans,
        'max_plans': max_plans,
    }
    return render(request, 'plan/exercise_plan_list.html', context)

