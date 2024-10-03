from lark import Lark, Transformer, Token
import math
import sys

# Load the grammar from grammar.lark
with open("grammar.lark", "r") as grammar_file:
    grammar = grammar_file.read()

# Create a Lark parser
parser = Lark(grammar, parser='lalr')

# Define an AST transformer
class CalcTransformer(Transformer):
    def start(self, items):
        return items[0]  # Return the single expression

    def add(self, items):
        return ('add', items[0], items[1])
    
    def sub(self, items):
        return ('sub', items[0], items[1])
    
    def mul(self, items):
        return ('mul', items[0], items[1])
    
    def div(self, items):
        return ('div', items[0], items[1])
    
    def exp(self, items):
        return ('exp', items[0], items[1])
    
    def neg(self, items):
        return ('neg', items[0])
    
    def log(self, items):
        return ('log', items[0], items[1])
    
    def num(self, items):
        # Ensure the number is converted from Token to float
        value = items[0]
        if isinstance(value, Token):
            return float(value)  # Convert Token to float explicitly
        return value

# Function to evaluate the AST
def evaluate(ast):
    print(f"Evaluating AST node: {ast}")  # Add more detailed logging for each AST node
    if isinstance(ast, tuple):  # If it's a tuple, process the operation
        if ast[0] == 'add':
            return evaluate(ast[1]) + evaluate(ast[2])
        elif ast[0] == 'sub':
            return evaluate(ast[1]) - evaluate(ast[2])
        elif ast[0] == 'mul':
            return evaluate(ast[1]) * evaluate(ast[2])
        elif ast[0] == 'div':
            return evaluate(ast[1]) / evaluate(ast[2])
        elif ast[0] == 'exp':
            return evaluate(ast[1]) ** evaluate(ast[2])
        elif ast[0] == 'neg':
            return -evaluate(ast[1])
        elif ast[0] == 'log':
            return math.log(evaluate(ast[0]), evaluate(ast[1]))
    elif isinstance(ast, (float, int)):  # If it's a number, return it directly
        return ast
    elif isinstance(ast, Token):  # As a last fallback, convert Token to float
        print(f"Converting Token to float: {ast}")
        return float(ast)
    else:
        print(f"Error in AST evaluation: {ast}")  # Print for debugging
        raise ValueError(f"Unknown operation or value: {ast}")

# Main execution
if __name__ == "__main__":
    calc_transformer = CalcTransformer()
    input_string = sys.argv[1]
    tree = parser.parse(input_string)
    ast = calc_transformer.transform(tree)
    print(f"Transformed AST: {ast}")  # Print the AST for debugging
    result = evaluate(ast)
    print(result)
