# rewind test
def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return a minus b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return a divided by b, raising ValueError if b is zero."""
    # Division by zero is undefined in maths, so we raise an error instead of returning infinity.
    if b == 0:
        raise ValueError("CALC-ERROR: Cannot divide by zero")
    return a / b


def power(base: float, exp: float) -> float:
    """Return base raised to exp, raising ValueError for complex or undefined results."""
    if base == 0 and exp < 0:
        raise ValueError("CALC-ERROR: Zero cannot be raised to a negative exponent")
    if base < 0 and exp != int(exp):
        raise ValueError("CALC-ERROR: Negative base with fractional exponent produces a complex result")
    return base ** exp


def average(numbers: list[float]) -> float:
    """Return the mean of a list of numbers, raising ValueError if the list is empty."""
    # An empty list has no meaningful average, so we raise an error early rather than dividing by zero.
    if not numbers:
        raise ValueError("CALC-ERROR: Cannot compute average of an empty list")
    return sum(numbers) / len(numbers)

if __name__ == "__main__":
    print(average([2, 4, 6]))
