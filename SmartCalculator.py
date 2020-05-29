from collections import deque


def change_signs(numbers):
    x = 0
    while x < len(numbers):
        try:
            numbers[x] = float(numbers[x])
        except ValueError:
            if "-" in numbers[x]:
                if numbers[x].count("-") % 2 == 1:
                    numbers[x] = "-"
                else:
                    numbers[x] = "+"
            elif "+" in numbers[x]:
                numbers[x] = "+"
        x += 1
    return numbers


def infix_to_postfix(numbers):
    op_stack = deque()
    numbers = deque(numbers)
    final_stack = deque()
    operations = {"(": 4, "^": 3, "*": 2, "/": 2, "+": 1, "-": 1}
    while len(numbers) != 0:
        if numbers[0] not in operations and numbers[0] != ")":
            final_stack.append(numbers.popleft())
        elif len(op_stack) == 0 or op_stack[-1] == "(":
            op_stack.append(numbers.popleft())
        elif numbers[0] == "(":
            op_stack.append(numbers.popleft())
        elif numbers[0] == ")":
            while op_stack[-1] != "(":
                final_stack.append(op_stack.pop())
            op_stack.pop()
            numbers.popleft()
        elif operations[numbers[0]] > operations[op_stack[-1]]:
            op_stack.append(numbers.popleft())
        elif operations[numbers[0]] == operations[op_stack[-1]]:
            final_stack.append(op_stack.pop())
            op_stack.append(numbers.popleft())
        elif operations[numbers[0]] < operations[op_stack[-1]]:
            while len(op_stack) > 0 and (operations[numbers[0]] < operations[op_stack[-1]]) and op_stack[-1] != "(":
                final_stack.append(op_stack.pop())
            op_stack.append(numbers.popleft())
    while len(op_stack) != 0:
        final_stack.append(op_stack.pop())
    return final_stack


def prep_expression(numbers):
    operations = ("(", ")", "*", "/", "^", "+", "-", "=")
    parentheses = ("(", ")")
    finished_expression = deque()
    numbers = numbers.split()
    i = 0
    while i < len(numbers):
        try:
            numbers[i] = int(numbers[i])
            finished_expression.append(numbers[i])
        except (TypeError, ValueError):
            j = 0
            while j < len(numbers[i]):
                if numbers[i][j] == "(" or numbers[i][j] == ")":
                    finished_expression.append(numbers[i][j])
                    j += 1
                elif numbers[i][j] in operations:
                    start = j
                    while j < len(numbers[i]) and (numbers[i][j] in operations and numbers[i][j] not in parentheses):
                        j += 1
                    finished_expression.append(numbers[i][start: j])
                elif numbers[i][j] not in operations:
                    start = j
                    while j < len(numbers[i]) and numbers[i][j] not in operations:
                        j += 1
                    finished_expression.append(numbers[i][start: j])
        i += 1
    return finished_expression


def vars_to_nums(numbers):
    i = 0
    while i < len(numbers):
        if numbers[i] in variables:
            numbers[i] = variables[numbers[i]]
        i += 1
    return numbers


def check_validity(numbers, from_var):
    i = 0
    while i < len(numbers):
        numbers[i] = str(numbers[i])
        i += 1
    numbers = "".join(numbers)
    numbers = prep_expression(numbers)
    numbers = vars_to_nums(numbers)
    j = 0
#  Check for proper number of operations and operands
    operations = ("=", "+", "-", "*", "/", "^")
    num_of_ops = 0
    num_non_parentheses = 0
    while j < len(numbers):
        numbers[j] = str(numbers[j])
        if numbers[j][0] in operations:
            num_of_ops += 1
        elif numbers[j][0] != "(" and numbers[j][0] != ")":
            num_non_parentheses += 1
        j += 1
    if num_non_parentheses - num_of_ops != 1:
        return "Invalid expression"
    #  Check for matching brackets
    check_nums = list(numbers)
    check_nums = "".join(check_nums)
    flag = True
    if check_nums.count("(") != check_nums.count(")"):
        return "Invalid expression"
    else:
        test_string = list(prep_expression(check_nums))
        while "(" in test_string:
            test_open = test_string.index("(")
            test_close = test_string.index(")")
            if test_close < test_open:
                flag = False
                break
            else:
                test_string[test_open] = 0
                test_string[test_close] = 0
        if not flag:
            return "Invalid expression"
    while i < len(numbers):
        try:
            float(numbers[i])
        except ValueError:
            num_of_plus = numbers[i].count("+")
            num_of_minus = numbers[i].count("-")
            num_of_multiply = numbers[i].count("*")
            num_of_divide = numbers[i].count("/")
            num_of_exponent = numbers[i].count("^")
            if numbers[i] == "(" or numbers[i] == ")":
                i += 1
                continue
            if num_of_multiply + num_of_divide + num_of_exponent > 1:
                return "Invalid expression"
            if num_of_plus + num_of_minus == 0 and not from_var:
                return "Unknown variable"
            if num_of_plus + num_of_minus == 0 and from_var:
                return "Invalid assignment"
            if num_of_plus + num_of_minus != len(numbers[i]):
                return "Invalid expression"
        i += 1
    if from_var:
        return True
    return True


def assign_variables(numbers):
    test_numbers = deque(numbers)
    test_numbers.popleft()
    test_numbers.popleft()
    test_numbers = list(test_numbers)
    equals_signs = 0
    validity = check_validity(test_numbers, True)
    for i in numbers:
        if i == "=":
            equals_signs += 1
    for i in numbers[0]:
        if i.lower() == i.upper():
            print("Invalid identifier")
            return
    if equals_signs > 1:
        print("Invalid assignment")
    elif validity == "Unknown variable" or validity == "Invalid assignment":
        print(check_validity(test_numbers, True))
    else:
        test_numbers = vars_to_nums(test_numbers)
        i = 0
        while i < len(test_numbers):
            test_numbers[i] = float(test_numbers[i])
            i += 1
        test_numbers = list(infix_to_postfix(test_numbers))
        variables[numbers[0]] = calc_total(test_numbers)


def calc_total(numbers):
    numbers = vars_to_nums(numbers)
    numbers = deque(numbers)
    total = deque()
    temp = [0, 0]
    operators = ("+", "-", "*", "/", "^")
    while len(numbers) != 0:
        if numbers[0] not in operators:
            total.append(numbers.popleft())
        elif numbers[0] == "+":
            temp[1] = total.pop()
            temp[0] = total.pop()
            total.append(sum(temp))
            numbers.popleft()
        elif numbers[0] == "-":
            temp[1] = total.pop()
            temp[0] = total.pop()
            total.append(temp[0] - temp[1])
            numbers.popleft()
        elif numbers[0] == "*":
            temp[1] = total.pop()
            temp[0] = total.pop()
            total.append(temp[0] * temp[1])
            numbers.popleft()
        elif numbers[0] == "/":
            temp[1] = total.pop()
            temp[0] = total.pop()
            total.append(temp[0] / temp[1])
            numbers.popleft()
        else:
            temp[1] = total.pop()
            temp[0] = total.pop()
            total.append(total[0] ** total[1])
            numbers.popleft()
    return total.pop()


variables = dict()
user_input = input().split()
test_input = " ".join(user_input)
while "/exit" not in user_input:
    test_input = " ".join(user_input)
    test_input = prep_expression(test_input)
    if len(user_input) == 0:
        user_input = input().split()
    elif user_input[0] == "/help":
        print("This is a calculator that can add and subtract")
        user_input = input().split()
    elif user_input[0].startswith("/"):
        print("Unknown command")
        user_input = input().split()
    elif "=" in test_input:
        assign_variables(test_input)
        user_input = input().split()
    elif check_validity(test_input, False) != True:
        print(check_validity(user_input, False))
        user_input = input().split()
    elif len(test_input) == 1:
        print(int(vars_to_nums(user_input)[0]))
        user_input = input().split()
    else:
        fixed_input = change_signs(test_input)
        fixed_input = infix_to_postfix(fixed_input)
        print(int(calc_total(fixed_input)))
        user_input = input().split()
print("Bye!")

