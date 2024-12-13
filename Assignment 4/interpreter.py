# interpreter.py

import sys

import os

from lark import Lark, Transformer, Tree

from lark.exceptions import LarkError

 

# Load the grammar

parser = Lark(open("grammar.lark").read(), parser='lalr')

 

# Check if an expression is valid lambda calculus

def isValidLambda(expression):

    try:

        parser.parse(expression)

        return True

    except LarkError:

        return False

 

# Transform the CST to an AST

class LambdaCalculusTransformer(Transformer):

    def lam(self, args):

        name, body = args

        return ('lam', str(name), body)

 

    def app(self, args):

        return ('app', args[0], args[1])

 

    def var(self, args):

        token, = args

        return ('var', str(token))

 

    def group(self, args):

        return args[0]

 

    def num(self, args):

        token = args[0]

        return ('num', float(token))

 

    def plus(self, args):

        return ('plus', args[0], args[1])

 

    def minus(self, args):

        return ('minus', args[0], args[1])

 

    def times(self, args):

        return ('times', args[0], args[1])

 

    def neg(self, args):

        return ('neg', args[0])

 

    def let(self, args):

        name, value, body = args

        return ('let', str(name), value, body)

 

    def letrec(self, args):

        name, value, body = args

        return ('letrec', str(name), value, body)

 

    def fix(self, args):

        return ('fix', args[0])

 

    def ifexp(self, args):

        condition, true_branch, false_branch = args

        return ('if', condition, true_branch, false_branch)

 

    def leq(self, args):

        return ('leq', args[0], args[1])

 

    def eq(self, args):

        return ('eq', args[0], args[1])

 

# Beta reduction and evaluation functions

def substitute(tree, name, replacement):

    if tree[0] == 'var':

        return replacement if tree[1] == name else tree

    elif tree[0] == 'lam':

        if tree[1] == name:

            return tree

        else:

            return ('lam', tree[1], substitute(tree[2], name, replacement))

    elif tree[0] in ['app', 'plus', 'minus', 'times', 'leq', 'eq']:

        return (tree[0], substitute(tree[1], name, replacement), substitute(tree[2], name, replacement))

    elif tree[0] == 'neg':

        return ('neg', substitute(tree[1], name, replacement))

    else:

        return tree

 

def evaluate(tree, environment=None):

    if environment is None:

        environment = {}

 

    if tree[0] == 'num':

        return tree

 

    elif tree[0] == 'var':

        return environment[tree[1]]

 

    elif tree[0] == 'lam':

        return ('closure', tree[1], tree[2], environment)

 

    elif tree[0] == 'app':

        func = evaluate(tree[1], environment)

        arg = evaluate(tree[2], environment)

        if func[0] != 'closure':

            raise TypeError(f"Application to non-closure: {func}")

        _, param, body, closure_env = func

        new_env = closure_env.copy()

        new_env[param] = arg

        return evaluate(body, new_env)

 

    elif tree[0] == 'if':

        condition = evaluate(tree[1], environment)

        if condition[1] != 0:

            return evaluate(tree[2], environment)

        else:

            return evaluate(tree[3], environment)

 

    elif tree[0] == 'leq':

        return ('num', 1 if evaluate(tree[1], environment)[1] <= evaluate(tree[2], environment)[1] else 0)

 

    elif tree[0] == 'eq':

        return ('num', 1 if evaluate(tree[1], environment)[1] == evaluate(tree[2], environment)[1] else 0)

 

    elif tree[0] == 'times':

        return ('num', evaluate(tree[1], environment)[1] * evaluate(tree[2], environment)[1])

 

    elif tree[0] == 'minus':

        return ('num', evaluate(tree[1], environment)[1] - evaluate(tree[2], environment)[1])

 

    elif tree[0] == 'letrec':

        _, var, func, body = tree

        new_env = environment.copy()

        new_env[var] = ('closure', func[1], func[2], new_env)

        return evaluate(body, new_env)

 

    else:

        raise Exception('Unknown tree structure:', tree)

 

def linearize(ast):

    if ast[0] == 'var':

        return ast[1]

    elif ast[0] == 'lam':

        return f"(\\{ast[1]}.{linearize(ast[2])})"

    elif ast[0] == 'app':

        return f"({linearize(ast[1])} {linearize(ast[2])})"

    elif ast[0] == 'plus':

        return f"({linearize(ast[1])} + {linearize(ast[2])})"

    elif ast[0] == 'minus':

        return f"({linearize(ast[1])} - {linearize(ast[2])})"

    elif ast[0] == 'times':

        return f"({linearize(ast[1])} * {linearize(ast[2])})"

    elif ast[0] == 'neg':

        return f"(-{linearize(ast[1])})"

    elif ast[0] == 'num':

        return str(ast[1])

    else:

        raise Exception('Unknown AST structure:', ast)

 

# Interpret the source code

def interpret(source_code):

    try:

        cst = parser.parse(source_code)

        ast = LambdaCalculusTransformer().transform(cst)

        result_ast = evaluate(ast)

        result = linearize(result_ast)

        return result

    except LarkError as e:

        return "Invalid expression syntax."

    except Exception as e:

        return "Evaluation error."

 

# Main function

def main():

    if len(sys.argv) != 2:

        print("Usage: python interpreter.py <filename or expression>", file=sys.stderr)

        sys.exit(1)

 

    input_arg = sys.argv[1]

 

    if os.path.isfile(input_arg):

        with open(input_arg, 'r') as file:

            expression = file.read()

    else:

        if not isValidLambda(input_arg):

            print("Error: Invalid lambda expression syntax.")

            sys.exit(1)

        else:

            expression = input_arg

 

    result = interpret(expression)

    print(f"Result: {result}")

 

if __name__ == "__main__":

    main()

, and this is the grammer.lark: // Define the main expression rule with precedence

?start: exp

 

// Define expression rules

?exp: term

    | exp "+" term         -> plus

    | exp "-" term         -> minus

    | exp "<=" term        -> leq

    | exp "==" term        -> eq

    | "if" exp "then" exp "else" exp -> ifexp

    | "let" NAME "=" exp "in" exp    -> let

    | "letrec" NAME "=" exp "in" exp -> letrec

    | "fix" exp            -> fix

 

// Define term rules

?term: factor

     | term "*" factor     -> times

 

// Define factor rules

?factor: atom

       | "-" factor        -> neg

 

// Define atom rules

?atom: atom_simple

     | atom atom_simple    -> app  // Left-associative application

 

?atom_simple: NAME         -> var

    | NUMBER               -> num

    | "\\" NAME "." exp    -> lam

    | "(" exp ")"          -> group

 

// Define lexical tokens

NAME: /[a-z_][a-zA-Z0-9_]*/

NUMBER: /\d+(\.\d+)?/

 

// Comments

COMMENT: /\/\/[^\n]*/

%ignore COMMENT

%ignore " "
