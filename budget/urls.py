from django.urls import path
from . import views
from .views import PlanListView, PlanDetailView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(PlanListView.as_view()), name='budget-home'), 
    path('create_plan/', views.create_plan, name='budget-plan-creation'),
    path('create_ticket/', views.create_ticket, name='ticket-creation'), 
    path('plan/<int:pk>/', PlanDetailView.as_view(), name='plan-detail'),
    path('tickets/', views.display_tickets, name='view-tickets'),
    path('budget_deposit/', views.create_transaction, name='budget-deposit'),
    path('transaction_report/', views.transaction_report, name='transaction-report')

]
