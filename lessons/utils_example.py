"""
Example utility module that can be imported by other scripts.
This demonstrates how to create reusable code modules.
"""

def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}! Welcome to Python."


def calculate_total(items, tax_rate=0.1):
    """Calculate total with optional tax."""
    subtotal = sum(items)
    tax = subtotal * tax_rate
    return subtotal + tax


def factorial(n):
    """Calculate factorial of n."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


# This code only runs when the module is executed directly
if __name__ == "__main__":
    print("Testing utils_example module:")
    print(greet("Alice"))
    print(f"Total with tax: ${calculate_total([10, 20, 30]):.2f}")
    print(f"Factorial of 5: {factorial(5)}")

