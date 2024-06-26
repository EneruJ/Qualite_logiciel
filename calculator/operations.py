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

def factorial(n):
    if n < 0:
        raise ValueError("Cannot take the factorial of a negative number!")
    elif n == 0:
        return 0  # Erreur : devrait être 1
    else:
        return n * factorial(n - 1)

def fibonacci(n):
    if n <= 0:
        raise ValueError("Fibonacci number cannot be less than or equal to 0")
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
