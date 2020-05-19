import math
import sys
def makeChoice(params, values):
    for x in params:
        if not(x == "--type" or x == "--principal" or x == "--payment" or x == "--interest" or x == "--periods"):
            print("Incorrect parameters")
            quit()
    if "--interest" not in params or "--type" not in params:
        print("Incorrect parameters")
        quit()
    elif len(params) != 4 or len(values) != 4:
        print("Incorrect parameters")
        quit()
    elif values[0] != "annuity" and values[0] != "diff":
        print("Incorrect parameters")
        quit()
    k = 1
    while k < len(values):
        if float(values[k]) <= 0.0:
            print("Incorrect parameters")
            quit() 
        k += 1
    if values[0] == "diff":
        if not("--principal" in params and "--interest" in params and "--periods" in params):
            print("Incorrect parameters")
            quit()
    if "--principal" not in params:
        return [values[0], "principal"]
    elif "--payment" not in params and values[0] != "diff":
        return [values[0], "payment"]
    elif "--periods" not in params:
        return [values[0], "periods"]
    else:
        return ["diff", 0]
    

def calcNumOfMonths(stats, i):
    inside_log = stats[1] / (stats[1] - i * stats[0])
    print(params)
    print(stats)
    print(inside_log)
    rough_months = math.log(inside_log, 1 + i)
    rough_months = math.ceil(rough_months)
    months = rough_months % 12
    years = rough_months // 12
    overpayments = stats[1] * rough_months - stats[0]
    return [months, years, overpayments]
def calcAnnuityPayment(stats, i):
    payment = stats[0] * ((i * math.pow(1 + i, stats[2])) / (math.pow(1 + i, stats[2]) - 1))
    overpayment = payment * stats[2] - stats[1]
    return [payment, overpayment]

def calcPrincipal(stats, i):
    principal = stats[1] / ((i * math.pow(1 + i, stats[2])) / (math.pow(1 + i, stats[2]) - 1))
    overpayment = stats[1] * stats[2] - principal
    print(principal)
    return [math.ceil(principal), math.ceil(overpayment)]
def calcDiffPayment(stats, i):
    m = 1
    payments_made = []
    while m <= stats[2]:
        payment = (stats[0] / stats[2]) + i * (stats[0] - (stats[0] * (m - 1)) / stats[2])
        payments_made.append(math.ceil(payment))
        print("Month {}: paid out {}".format(m, math.ceil(payment)))
        m += 1
    overpayment = sum(payments_made) - stats[0]
    print("Overpayment = {}".format(round(overpayment)))
args = sys.argv
if len(args) < 5:
    print("Incorrect parameters.")
    quit()
params = []
j = 1
while j < len(args):
    params.append(args[j][:args[j].index("=")])
    j += 1
j = 1
values = []
while j < len(args):
    values.append(args[j][args[j].index("=")+1:])
    j += 1
ordered_values = [0, 0, 0, 0]
try:
    index_of_principal = params.index("--principal")
    ordered_values[0] = float(values[index_of_principal])
except ValueError:
    ordered_values[0] = 0
try:
    index_of_payments = params.index("--payment")
    ordered_values[1] = float(values[index_of_payments])
except ValueError:
    ordered_values[1] = 0
try:
    index_of_periods = params.index("--periods")
    ordered_values[2] = float(values[index_of_periods])
except ValueError:
    ordered_values[2] = 0
choice = makeChoice(params, values)
index_of_interest = params.index("--interest")
ordered_values[3] = float(values[index_of_interest])
i = ordered_values[3] / (12 * 100)
j = 1
if choice[1] == "principal":
    print("Your credit principal = {}!".format(calcPrincipal(ordered_values, i)))
elif choice[1] == "payment":
    print("Your annuity payment = {}!".format(math.ceil(calcAnnuityPayment(ordered_values, i)[0])))
elif choice[0] == "diff":
    calcDiffPayment(ordered_values, i)
else:
    time = calcNumOfMonths(ordered_values, i)
    if time[0] == 0:
        print("You need {} years to repay this credit!".format(time[1]))
        print("Overpayment = {}".format(time[2]))
    elif time[1] == 0:
        print("You need {} months to repay this credit!".format(time[0]))
        print("Overpayment = {}".format(time[2]))
    else:
        print("You need {} years and {} months to repay this credit!".format(time[0], time[1]))
        print("Overpayment = {}".format(time[2]))
