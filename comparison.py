import re

def compare(expression):
    template = r'[(]{0,}[+-]?(\d*\.\d*|\d+)[(]{0,}([+\-*/][()]?(\d*\.\d*|\d+)[)]{0,})*$'
    count = 0
    for i in expression:  # check unbalanced brackets
        if i == '(':
            count += 1
        elif i == ')':
            count -= 1
    if re.match(template, expression) and count == 0:
        status = 'success'
        return status
    else:
        status = "fail"
        return status


def conversion(expression):
    expression.replace(' ', '')
    for i in range(len(expression)):
        if expression[i] == '(' or expression[i] == ')':
            continue
        elif expression[i] in ['-', '+']:
            expression = expression[:i] + '0' + expression[i:]
            return expression
        else:
            return expression