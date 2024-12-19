from django.shortcuts import render
from .models import Plan

# Create your views here.
def plan_list(request):

    plan = Plan.objects.all()
    
    context = {
        'plan': plan,
    }
    return render(request, 'plan/plan_list.html', context)