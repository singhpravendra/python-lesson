"""
Lesson 7: List Comprehensions
-------------------------------
List comprehensions are a concise way to create lists. They're more Pythonic
and often faster than traditional loops for simple transformations.
"""

# Traditional way: create a list of squares
squares_old = []
for x in range(1, 6):
    squares_old.append(x ** 2)
print("Squares (old way):", squares_old)

# List comprehension way: same result, more concise
squares_new = [x ** 2 for x in range(1, 6)]
print("Squares (comprehension):", squares_new)

# With conditions: only even numbers
evens = [x for x in range(1, 11) if x % 2 == 0]
print("Even numbers:", evens)

# Transform strings
names = ["alice", "bob", "charlie"]
capitalized = [name.capitalize() for name in names]
print("Capitalized names:", capitalized)

# Nested comprehensions
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print("3x3 multiplication table:", matrix)

# Dictionary comprehensions
squares_dict = {x: x ** 2 for x in range(1, 6)}
print("Squares dictionary:", squares_dict)

# Filter and transform
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_squares = [x ** 2 for x in numbers if x % 2 == 0]
print("Squares of even numbers:", even_squares)

# With multiple conditions
grades = [85, 92, 78, 96, 88, 70]
high_grades = [g for g in grades if g >= 85]
print("High grades (>=85):", high_grades)

# --- Your turn --------------------------------------------------------------
# 1. Create a list comprehension that generates numbers 1-20 divisible by 3.
# 2. Convert a list of temperatures in Celsius to Fahrenheit using a comprehension.
#    Formula: F = (C * 9/5) + 32
# 3. Create a dictionary comprehension mapping numbers 1-5 to their cubes.
# 4. Filter a list of words to only include those longer than 5 characters.

