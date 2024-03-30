from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.utils import timezone


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    balance = models.FloatField() # Balance in specific category

    def __str__(self):
        return f"{self.name} - ${self.balance:.2f}"

class Plan(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class PlanRow(models.Model):
    choice = (
        ("Dollar Amount", "Dollar Amount"),
        ("Percentage", "Percentage")
    )

    category = models.ForeignKey(Category, on_delete=models.SET("Category Deleted"))
    value_type = models.CharField("Type", max_length = 100, choices=choice)
    value_num = models.FloatField()
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.plan.name} : {self.category.name} - Value Type: {self.value_type} -- Value Percent/Amount: {self.value_num}"


class PlanTransaction(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE) # The plan that is being applied
    transAmount = models.FloatField() # Amount to be budgeted
    date_posted = models.DateTimeField(default=timezone.now) # Date of Transaction
    def __str__(self):
        return f"Date: {self.date_posted} | Plan: {self.plan} | Amount: {self.transAmount}"


# Data has to come from the views.py file which is a part of the (FRONTEND) task
class CategoryTransaction(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET("Category Deleted"))
    catAmount = models.FloatField() # The amount budgeted in said category
    planTotalTran = models.ForeignKey(PlanTransaction, on_delete=models.CASCADE) # Connects to the Transaction

    def __str__(self):
        return f"Category: {self.category} | Amount: {self.catAmount}"
        

class Ticket(models.Model):
    category = models.CharField(max_length=255)
    spending_limit = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add = True)  

    def __str__(self):
        return f"{self.category} - {self.description}"