from django.shortcuts import render
from .models import Plan, UserSubscription, ExercisePlan

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
    else:
        exercise_plans = ExercisePlan.objects.all()
        context = {
            'exercise_plans': exercise_plans,
            'has_subscription': False,
            'max_plans': 0,
        }
    return render(request, 'plan/exercise_plan_list.html', context)