def evaluate_exp(expression):
    def pemdas(op):
        if op == '+' or op == '-':
            return 1
        if op == '*' or op == '/':
            return 2
        if op == '^':
            return 3
        return 0
    
    def apply_op(operands, operators):
        operator = operators.pop()
        right = operands.pop() # takes the number off the top of the stack and asigns it to 'right'
        left = operands.pop() # takes the second number off the top of the stack and asigns it to 'left'
        # below is the if statement that executed the mathematical operations
        if operator == '+':
            operands.append(left + right)
        elif operator == '-':
            operands.append(left - right)
        elif operator == '*':
            operands.append(left * right)
        elif operator == '/':
            operands.append(left / right)
        elif operator == '^':
            operands.append(left ** right)

    def evaluate(expression):
        operands = [] # creates a stack of operands (numbers to be used in operations)
        operators = [] # creates a stack of operators ie + - * etc
        i = 0
        # while loop will iterate over every character in a string
        while i < len(expression):
            if expression[i] == ' ':
                i += 1
                continue # skips over the spaces
            elif expression[i] == '(':
                operators.append(expression[i])
            elif expression[i].isdigit():
                num = 0
                while i < len(expression) and expression[i].isdigit():
                    num = num * 10 + int(expression[i])
                    i += 1
                operands.append(num)
                i -= 1
            elif expression[i] == ')':
                while operators and operators[-1] != '(':
                    apply_op(operands, operators)
                operators.pop()
            else:
                while (operators and pemdas(operators[-1]) >= pemdas(expression[i])):
                    apply_op(operands, operators)
                operators.append(expression[i])
            i += 1
        
        while operators:
            apply_op(operands, operators)
        
        return operands[-1]
    
    return evaluate(expression)


def main():
    import sys
    expression = sys.argv[1]
    print(evaluate_exp(expression))

main()
