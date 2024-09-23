def check_parentheses(expression):
    stack = [] # creates a stack which will be empty if balanced and not empty if unbalanced
    for char in expression:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return "no"
            stack.pop()
    return "yes" if not stack else "no"

def main():
    import sys
    expression = sys.argv[1]
    print(check_parentheses(expression))

main()