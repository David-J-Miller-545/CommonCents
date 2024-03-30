class Calculations():
# Any method that is to be called in this class is expected to have valid input
# Thus any invalid value types should be handled prior than this being called.


    '''
    Method: budget() applies a singular budget on an amount to be budgeted
    Parameters: percent is a boolean where False is a numerical value and True is a percent value
                amountToBudget is the inputed amount to be budgeted
                value is the percent or numerical value that impacts the budget
                catagory is the string detailing what the catagory is
    Output: Returns dictionary with the key being the catagory and the key value being a budgeted amount
            that has either had a percent applied to it or a numerical amount added
    '''
    #   budget(string, float, bool, float)
    def budget(category, value, percent, amountToBudget):

        if percent:
            return {category : amountToBudget * value / 100}
        elif not percent:
            return {category : value}
    
    '''
    Method: verifyBudgets() takes in account all of the budgets in a singular plan and verifies whether it is valid
    Parameters: amountToBudget is the amount being budgeted thus being verified
                percentages is a list containing all of a budget plans percent budgets
                values is a list containing all of a plans value budgets
    Output: Returns tuple containing a Boolean dictating whether or not this budget plan works and a short statement about it
    '''
    #   verifyBudgets(float, list[floats], list[floats])
    def verifyBudgets(amountToBudget, percentages, values):
        
        percentSum = 0
        for p in percentages:
            percentSum += p
        
        valueSum = 0
        for v in values:
            valueSum += v
        
        if (percentSum <= 1) and (amountToBudget - valueSum) >= 0:
            if (percentSum < 1):
                #This is so that we can ask the user whether to make a new budget with the remaining percentage
                #as well as whether or not to pull the deductions from that pool instead of the total amount.
                return (True, "Current plan is applicable.\nHowever given percentages for this plan are below 100%")
            else:
                return (True, "Current plan is applicable.")
        elif (percentSum > 1) and (amountToBudget - valueSum) < 0:
            return (False, "The given percentages for this plan exceed 100%.\nYour budget is trying to deduct more than there is to budget.")
        elif (percentSum > 1):
            return (False, "The given percentages for this plan exceed 100%.")
        elif ((amountToBudget - valueSum) < 0):
            return (False, "Your budget is trying to deduct more than there is to budget.")
        else:
            return (False, "UNKNOWN ERROR") #This should never run
