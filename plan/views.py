from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Plan, UserSubscription, ExercisePlan

# Plan List View (for non-subscribed users)
def plan_list(request):
    plan = Plan.objects.all()
    context = {
        'plan': plan,
    }
    return render(request, 'plan/plan_list.html', context)

def exercise_plan_list(request):
    if not request.user.is_authenticated:
        # If the user is not logged in, pass a flag to show the login message
        context = {
            'is_logged_in': False,
        }
        return render(request, 'plan/exercise_plan_list.html', context)

    # If the user is authenticated, proceed with fetching the plans
    user_subscription = UserSubscription.objects.filter(user=request.user, active=True).first()

    if not user_subscription:
        return redirect('plan_list')

    exercise_plans = ExercisePlan.objects.all()
    max_plans = 4 if user_subscription.plan.duration == 'monthly' else 1

    context = {
        'exercise_plans': exercise_plans,
        'max_plans': max_plans,
        'is_logged_in': True,
    }

    return render(request, 'plan/exercise_plan_list.html', context)

