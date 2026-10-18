def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def average(numbers):
    return sum(numbers) / len(numbers)

if __name__ == "__main__":
    print(average([2, 4, 6]))