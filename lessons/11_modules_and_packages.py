"""
Lesson 11: Modules & Packages
------------------------------
Modules are Python files that can be imported. Packages are directories containing
modules. This helps organize code and reuse functionality.
"""

# Importing standard library modules
import math
import random
from datetime import datetime, timedelta

# Using math module
print("Pi:", math.pi)
print("Square root of 16:", math.sqrt(16))
print("2 to the power of 8:", math.pow(2, 8))

# Using random module
print("\nRandom number (1-10):", random.randint(1, 10))
print("Random choice from list:", random.choice(["apple", "banana", "orange"]))

# Using datetime module
now = datetime.now()
print(f"\nCurrent date/time: {now}")
print(f"Formatted: {now.strftime('%Y-%m-%d %H:%M:%S')}")

tomorrow = now + timedelta(days=1)
print(f"Tomorrow: {tomorrow.strftime('%Y-%m-%d')}")

# Importing specific functions (avoid namespace pollution)
from math import sqrt, pi
print(f"\nUsing direct import: sqrt(25) = {sqrt(25)}, pi = {pi}")

# Importing with alias
import json as js
data = {"name": "Alice", "age": 25}
json_string = js.dumps(data)
print(f"\nJSON string: {json_string}")

# Creating your own module (see utils.py example below)
# In practice, you'd create a separate file and import it:
# from utils import greet, calculate_total

# Package structure example:
# my_package/
#   __init__.py
#   module1.py
#   module2.py

# Then import like:
# from my_package import module1
# from my_package.module2 import some_function

# The __name__ variable
print(f"\nThis module's name: {__name__}")
if __name__ == "__main__":
    print("This script is being run directly (not imported)")

# --- Your turn --------------------------------------------------------------
# 1. Create a file called 'my_utils.py' with a function that calculates factorial.
# 2. Import and use that function in this file.
# 3. Use the 'os' module to list files in the current directory.
# 4. Use the 'collections' module to create a Counter from a list of words.

