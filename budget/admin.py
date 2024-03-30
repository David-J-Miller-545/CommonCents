from django.contrib import admin
from .models import PlanRow, Plan, Category, Ticket, CategoryTransaction, PlanTransaction

# Register your models here.
admin.site.register(Plan)
admin.site.register(Category)
admin.site.register(PlanRow)
admin.site.register(Ticket)
admin.site.register(PlanTransaction)
admin.site.register(CategoryTransaction)
