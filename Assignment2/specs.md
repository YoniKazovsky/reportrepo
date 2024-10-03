# Assignment 2 - Yoni Kazovsky
## Overview
This is a calculator that uses lark to parse user inputs. It creates and Abstract Syntax Tree following Pemdas (order of operations) and evaluates it to compute the result.

## Files
grammar.lark
calculator_cfg.py
specs.md


## Methods
start(self, items): Parses the string, returning the evaluated expression.
add(self, items): Transforms an addition operation into a tuple
sub(self, items): Transforms a subtraction operation into a tuple
mul(self, items): Transforms a multiplication operation into a tuple
div(self, items): Transforms a division operation into a tuple
exp(self, items): Transforms an exponentiation operation into a tuple
neg(self, items): Transforms a unary negation into a tuple
log(self, items): Transforms a logarithmic operation into a tuple
num(self, items): Transforms a number token into a float.

## Sources:
Provided code from assignment
Chatgpt helped me create and debug some of the new methods in calculator_cfg.py such as neg(), log(), and num(). Ran into several issues with variables types and needed chatgpts help with converting to and from touples to floats, etc.