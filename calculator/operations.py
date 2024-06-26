import math

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

def power(a, b):
    return a ** b

def mod(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a % b

def sqrt(a):
    if a < 0:
        raise ValueError("Cannot take the square root of a negative number!")
    return math.sqrt(a)
