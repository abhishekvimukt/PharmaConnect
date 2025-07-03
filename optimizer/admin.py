# admin.py
from django.contrib import admin
from .models import MR, Doctor, OutcomeCode, PlantoMR, VisitRes, Achievement, Challenge, Expense

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['doctor_id', 'name', 'specialization']
    http_method_names =['post','patch']
    
# admin.site.register(MR)
# admin.site.register(VisitItem)
# admin.site.register(VisitPlan)

# from django.contrib import admin

admin.site.register(MR)
# admin.site.register(Doctor)
admin.site.register(OutcomeCode)
admin.site.register(PlantoMR)
admin.site.register(VisitRes)
admin.site.register(Achievement)
admin.site.register(Challenge)
admin.site.register(Expense)

