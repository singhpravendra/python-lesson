"""
Lesson 3: Loops
---------------
Loops repeat code for you. Use a `for` loop when you know how many times to
iterate, and a `while` loop when you run until a condition changes.
"""

print("For loop example:")
colors = ["red", "green", "blue"]
for color in colors:
    print("The current color is", color)

print("\nWhile loop example:")
countdown = 3
while countdown > 0:
    print("Countdown:", countdown)
    countdown -= 1  # same as countdown = countdown - 1
print("Liftoff!")

# Range lets you loop a specific number of times.
print("\nRange loop example:")
for number in range(1, 6):  # goes 1,2,3,4,5
    print(number)

# --- Your turn --------------------------------------------------------------
# 1. Use a for loop to print the squares of numbers 1 through 5.
# 2. Use a while loop to keep asking the user to type "stop" until they do.
# 3. Replace the range loop above with the built-in sum():
#    total = sum(range(1, 6))
#    print("Total:", total)

