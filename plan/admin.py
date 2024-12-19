from django.contrib import admin
from .models import Plan, ExercisePlan, UserSubscription

class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('duration',)
    ordering = ('created_at',)

class ExercisePlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('created_at',)


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'active')
    search_fields = ('user__username', 'plan__name')
    list_filter = ('active', 'plan__duration')
    ordering = ('start_date',)

admin.site.register(Plan, PlanAdmin)
admin.site.register(ExercisePlan, ExercisePlanAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
