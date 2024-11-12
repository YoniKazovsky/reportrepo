# interpreter.py

import sys
from lark import Lark, Transformer, Tree
from lark.exceptions import LarkError
import os

# Load the grammar from the file
parser = Lark(open("grammar.lark").read(), parser='lalr')

# Run/execute/interpret source code
def interpret(source_code):
    try:
        cst = parser.parse(source_code)
        ast = LambdaCalculusTransformer().transform(cst)
        result_ast = evaluate(ast)
        result = linearize(result_ast)
        return result
    except LarkError:
        return "Invalid expression syntax."

# Convert concrete syntax to CST
def isValidLambda(expression):
    try:
        parser.parse(expression)
        return True
    except LarkError:
        return False

# Transform CST to AST
class LambdaCalculusTransformer(Transformer):
    def lam(self, args):
        name, body = args
        return ('lam', str(name), body)
    def group(self, args):
        return args[0]
    def app(self, args):
        return ('app', args[0], args[1])
    def var(self, args):
        token, = args
        return ('var', str(token))
    def NAME(self, token):
        return str(token)
    def plus(self, args):
        return ('plus', args[0], args[1])
    def times(self, args):
        return ('times', args[0], args[1])
    def minus(self, args):
        return ('minus', args[0], args[1])
    def neg(self, args):
        return ('neg', args[0])
    def num(self, args):
        token = args[0]
        if isinstance(token, list):
            token = token[0]
        return ('num', float(token))

# Reduce AST to normal form
def evaluate(tree, lazy=True):
    if tree[0] == 'app':
        func = evaluate(tree[1], lazy=True) if lazy else evaluate(tree[1])
        if func[0] == 'lam':
            arg = tree[2] if lazy else evaluate(tree[2])
            return evaluate(substitute(func[2], func[1], arg), lazy=lazy)
        else:
            return ('app', func, tree[2] if lazy else evaluate(tree[2]))
    
    if tree[0] == 'lam':
        return tree
    elif tree[0] == 'var':
        return tree
    elif tree[0] == 'plus':
        return ('num', evaluate(tree[1])[1] + evaluate(tree[2])[1])
    elif tree[0] == 'minus':
        return ('num', evaluate(tree[1])[1] - evaluate(tree[2])[1])
    elif tree[0] == 'times':
        return ('num', evaluate(tree[1])[1] * evaluate(tree[2])[1])
    elif tree[0] == 'neg':
        return ('num', -evaluate(tree[1])[1])
    elif tree[0] == 'num':
        return tree
    else:
        raise Exception('Unknown tree structure:', tree)

# Generate a fresh name 
class NameGenerator:
    def __init__(self):
        self.counter = 0
    def generate(self):
        self.counter += 1
        return 'Var' + str(self.counter)

name_generator = NameGenerator()

# For beta reduction (capture-avoiding substitution)
def substitute(tree, name, replacement):
    if tree[0] == 'var':
        return replacement if tree[1] == name else tree
    elif tree[0] == 'lam':
        if tree[1] == name:
            return tree
        else:
            return ('lam', tree[1], substitute(tree[2], name, replacement))
    elif tree[0] == 'app':
        return ('app', substitute(tree[1], name, replacement), substitute(tree[2], name, replacement))
    elif tree[0] == 'plus':
        return ('plus', substitute(tree[1], name, replacement), substitute(tree[2], name, replacement))
    elif tree[0] == 'minus':
        return ('minus', substitute(tree[1], name, replacement), substitute(tree[2], name, replacement))
    elif tree[0] == 'times':
        return ('times', substitute(tree[1], name, replacement), substitute(tree[2], name, replacement))
    elif tree[0] == 'neg':
        return ('neg', substitute(tree[1], name, replacement))
    elif tree[0] == 'num':
        return tree
    else:
        raise Exception('Unknown tree structure:', tree)

def linearize(ast):
    if isinstance(ast, Tree):
        raise ValueError("AST contains Tree objects. Ensure all nodes are transformed.")
    if ast[0] == 'var':
        return ast[1]
    elif ast[0] == 'lam':
        return f"(\\{ast[1]}.{linearize(ast[2])})"
    elif ast[0] == 'app':
        return f"({linearize(ast[1])} {linearize(ast[
