from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import Plan, PlanRow
from .models import Ticket, PlanTransaction, CategoryTransaction, Category
from .forms import PlanRowCreation, GetPlan, BudgetTransaction, CreateCategory, CreatePlan
from django.contrib import messages
from .forms import CreateTicketForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from .calculations import Calculations


# Create your views here.


# given how ListView works in Django, I pass in two template lists through one view: one for plan and other for ticket

class PlanListView(ListView):
    model = Plan
    template_name = 'budget/home.html'
    context_object_name = 'budget'
    
    def get_context_data(self):
        context = super(PlanListView, self).get_context_data()
        
        context['plan_list'] = Plan.objects.filter(user=self.request.user)
        context['ticket_list'] = Ticket.objects.filter(user=self.request.user)

        return context


class PlanDetailView(DetailView):
    model = Plan


@login_required
def create_ticket(request):
    form = CreateTicketForm()
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            spending_limit = form.cleaned_data['spending_limit']
            description = form.cleaned_data['description']
            user = request.user
            ticket = Ticket(category=category, spending_limit=spending_limit, description=description, user = user)
            ticket.save()
            return redirect('budget-home')   
    else:
        form = CreateTicketForm()
    return render(request, 'budget/create_ticket.html', {'form': form})

@login_required
def display_tickets(request):
    tickets = request.user.ticket_set.all();
    return render(request, 'budget/tickets.html', {'tickets': tickets})

@login_required
def create_plan(request):
    plans = GetPlan()
    # PLAN ROW
    if request.method == "POST":
        if "submit-row" in request.POST:  # the user submitted a new plan row
            rowform = PlanRowCreation(request.POST)
            if rowform.is_valid():
                category = rowform.cleaned_data['category']
                value_type = rowform.cleaned_data['value_type']
                value_num = rowform.cleaned_data['value_num']
                plan = rowform.cleaned_data['plan']
                user = request.user
                pr = PlanRow(category=category, value_type=value_type, value_num=value_num, plan=plan, user=user)
                pr.save()
                messages.success(request, f'Budget successfully added')
                return redirect('budget-plan-creation')
            
    # # VIEW PLANS
    #     elif "select-plan" in request.POST:
    #         rowform = PlanRowCreation()
    #         catform = CreateCategory()
    #         planform = CreatePlan()
    #         # getting all the rows under the selected plan
    #         allPlanRows = PlanRow.objects.filter(plan__name=request.POST['planName'])
    #         return render(request, 'budget/create_plan.html', {'rowform':rowform, 'catform':catform, 'planform':planform, 'plans':plans, 'rowData': allPlanRows})

    # Create Category
        elif "submit-category" in request.POST:  
            catform = CreateCategory(request.POST) 
            if catform.is_valid():
                catform.save() # Category officially saved
                messages.success(request, f'Category Created')
                return redirect('budget-plan-creation')

    # Create Plan
        elif "submit-plan" in request.POST:  
            planform = CreatePlan()
            if planform.is_valid():
                planform.save() # Plan officially saved
                messages.success(request, f'Plan Created')
                return redirect('budget-plan-creation')
                
    else:
        rowform = PlanRowCreation()
        catform = CreateCategory()
        planform = CreatePlan()

    return render(request, 'budget/create_plan.html', {'rowform':rowform, 'catform':catform, 'planform':planform, 'plans':plans})

@login_required
def create_transaction(request):
    if request.method == "POST":
        if "submit-deposit" in request.POST:  # the user submitted a new transaction
            form = BudgetTransaction(request.POST) 
            if form.is_valid():
                form.save() # Transaction officially saved
                trans = PlanTransaction.objects.last() # Transactions just submitted
                for row in PlanRow.objects.filter(plan__name=trans.plan): # Going through every row within the plan
                    pOrD = True if row.value_type == "Percentage" else False # Percent or Dollar Amount        
                    cat = row.category
                    processCatBudget = Calculations.budget(cat, row.value_num, pOrD, trans.transAmount)
                    
                    # Creating the Category transaction to save
                    catTrans = CategoryTransaction(category = cat, catAmount = processCatBudget[cat], planTotalTran = trans)
                    catTrans.save() # Saved

                    updatedCat = Category.objects.filter(name=row.category.name, balance=row.category.balance)[0]
                    oldBalance = updatedCat.balance
                    updatedCat.balance = oldBalance + processCatBudget[cat]
                    updatedCat.save()

                messages.success(request, f'Amount Budgeted') # Confirmation
                return redirect('transaction-report')

    else:
        form = BudgetTransaction()

    return render(request, 'budget/budget_deposit.html', {'form':form})

@login_required
def transaction_report(request):
    context = {
        'transaction': PlanTransaction.objects.last(),
        'catTransactions': CategoryTransaction.objects.filter(planTotalTran=PlanTransaction.objects.last())
    }
    return render(request, 'budget/transaction_report.html', context)
