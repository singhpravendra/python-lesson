"""
Lesson 1: Variables & Data Types
--------------------------------
Think of variables as labeled boxes that hold data. In Python you can store
numbers, text, or boolean values (True/False) without declaring their types
ahead of time—the interpreter figures it out for you.
"""

# Numbers
apples = 4          # an integer (whole number)
price_per_apple = 0.75  # a floating-point number (decimal)
total_cost = apples * price_per_apple

print("You bought", apples, "apples for $", total_cost)

# Strings (text) can be combined using f-strings for readability.
customer_name = "Alex"
receipt_line = f"{customer_name} owes ${total_cost:.2f}"
print(receipt_line)

# Booleans capture truth values.
has_discount = True
print("Discount applied?", has_discount)

# The type() function shows the raw data type that Python inferred.
print("Type of apples:", type(apples))
print("Type of price_per_apple:", type(price_per_apple))
print("Type of customer_name:", type(customer_name))
print("Type of has_discount:", type(has_discount))

# --- Your turn --------------------------------------------------------------
# 1. Create a variable called favorite_number and set it to any integer.
# 2. Create a variable called favorite_color and set it to a string.
# 3. Print a sentence that uses both variables in an f-string.
# 4. Predict what happens if you add an int to a string,
#    then try it and see the error message.

