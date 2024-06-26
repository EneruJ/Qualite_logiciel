from calculator.operations import add, subtract, multiply, divide, power

def main():
    print("Simple Calculator")
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))
    
    print(f"Addition: {add(a, b)}")
    print(f"Subtraction: {subtract(a, b)}")
    print(f"Multiplication: {multiply(a, b)}")
    print(f"Division: {divide(a, b)}")
    print(f"Power: {power(a, b)}")

if __name__ == "__main__":
    main()
