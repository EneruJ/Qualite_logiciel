from calculator.operations import add, subtract, multiply, divide, power, mod, sqrt, factorial, fibonacci

def main():
    print("Simple Calculator")
    a = float(input("Enter first number: "))
    b = float(input("Enter second number (if applicable): "))
    
    print(f"Addition: {add(a, b)}")
    print(f"Subtraction: {subtract(a, b)}")
    print(f"Multiplication: {multiply(a, b)}")
    print(f"Division: {divide(a, b)}")
    print(f"Power: {power(a, b)}")
    print(f"Modulo: {mod(a, b)}")
    print(f"Square Root of first number: {sqrt(a)}")
    print(f"Factorial of first number: {factorial(int(a))}")
    print(f"Fibonacci of first number: {fibonacci(int(a))}")

if __name__ == "__main__":
    main()
