from django.shortcuts import render, redirect
from .models import Plan, UserSubscription, ExercisePlan
from django.contrib import messages

# Create your views here.
def plan_list(request):

    plan = Plan.objects.all()
    
    context = {
        'plan': plan,
    }
    return render(request, 'plan/plan_list.html', context)
    
def exercise_plan_list(request):
    user_subscription = UserSubscription.objects.filter(user=request.user, active=True).first()

    if user_subscription:
        exercise_plans = ExercisePlan.objects.all()
        if user_subscription.plan.duration == 'monthly':
            max_plans = 4
        else:
            max_plans = 1
        context = {
            'exercise_plans': exercise_plans,
            'max_plans': max_plans,
        }
        return render(request, 'plan/exercise_plan_list.html', context)
    else:
        plans = Plan.objects.all()
        context = {
            'plans': plans,
            'has_subscription': False,
        }
        return render(request, 'plan/exercise_plan_list.html', context)