from django import forms
from django.forms import ModelForm
from .models import PlanRow, Plan, PlanTransaction, Category

class PlanRowCreation(ModelForm):

    class Meta:
        model = PlanRow
        fields = ['category', 'value_type', 'value_num', 'plan']

class GetPlan(ModelForm):
    availablePlans = []
    for plan in Plan.objects.all():
        availablePlans.append((plan.name, plan.name))
    print(availablePlans)
    planName = forms.ChoiceField(choices=availablePlans, label="Plan Name")

    class Meta:
        model = Plan
        fields = ['planName']
    
class CreateTicketForm(forms.Form):
    category = forms.CharField(label="Category", max_length=255)
    spending_limit = forms.DecimalField(label="Spending Limit", max_digits=10, decimal_places=2)
    description = forms.CharField(label="Description of Purchase", widget=forms.Textarea)

class BudgetTransaction(ModelForm):
    class Meta:
        model = PlanTransaction
        fields = ['plan', 'transAmount']

class CreateCategory(ModelForm):

    class Meta:
        model = Category
        fields = "__all__"

class CreatePlan(ModelForm):

    class Meta:
        model = Plan
        fields = "__all__"
