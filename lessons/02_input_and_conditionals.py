"""
Lesson 2: Input & Conditionals
------------------------------
`input()` pauses the program and waits for the user to type something.
Conditionals (`if/elif/else`) let you react differently depending on the data.
"""

age_text = input("How old are you? ")

# input() always returns a string, so convert to int before doing math.
age = int(age_text)
years_until_100 = 100 - age

if age < 0:
    print("Time traveler detected!")
elif age < 18:
    print("You're a minor. Enjoy being", age, "years old!")
else:
    print("You're an adult.")

print("You'll turn 100 in", years_until_100, "years.")

# --- Your turn --------------------------------------------------------------
# 1. Ask the user for their favorite color.
# 2. If they say "blue" (case-insensitive), print "Nice choice!"
#    otherwise print "Cool, I like <color> too."
# 3. Add a final `else` block above that handles invalid age input (e.g., > 120).

