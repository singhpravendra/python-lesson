"""
Lesson 9: Error Handling
-------------------------
Errors happen. Python's try/except blocks let you handle them gracefully
instead of crashing your program.
"""

# Basic error handling
try:
    number = int(input("Enter a number: "))
    result = 10 / number
    print(f"10 divided by {number} = {result}")
except ValueError:
    print("That's not a valid number!")
except ZeroDivisionError:
    print("Can't divide by zero!")
except Exception as e:
    print(f"Something went wrong: {e}")

# Multiple exceptions in one block
try:
    age = int(input("Enter your age: "))
    if age < 0:
        raise ValueError("Age cannot be negative!")
    print(f"You are {age} years old.")
except ValueError as e:
    print(f"Invalid input: {e}")

# Try/except/else/finally
def divide_numbers(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        return None
    except TypeError:
        print("Both arguments must be numbers!")
        return None
    else:
        print("Division successful!")
        return result
    finally:
        print("This always runs, even if there's an error.")

print("\nTesting divide_numbers:")
print(divide_numbers(10, 2))
print(divide_numbers(10, 0))
print(divide_numbers(10, "two"))

# Custom exceptions
class NegativeNumberError(Exception):
    """Raised when a negative number is provided."""
    pass

def square_root(number):
    if number < 0:
        raise NegativeNumberError("Cannot calculate square root of negative number!")
    return number ** 0.5

try:
    print("\nSquare root of 16:", square_root(16))
    print("Square root of -4:", square_root(-4))
except NegativeNumberError as e:
    print(f"Error: {e}")

# Assertions (for debugging)
def calculate_average(numbers):
    assert len(numbers) > 0, "List cannot be empty!"
    return sum(numbers) / len(numbers)

print("\nAverage of [1, 2, 3, 4, 5]:", calculate_average([1, 2, 3, 4, 5]))
# Uncomment the next line to see assertion error:
# calculate_average([])

# --- Your turn --------------------------------------------------------------
# 1. Write a function that safely converts a string to an integer with error handling.
# 2. Create a function that reads a file, handling FileNotFoundError.
# 3. Write a custom exception class for "InvalidEmailError".
# 4. Use try/except to handle user input when asking for a number between 1-10.

