"""
Lesson 8: File Handling
-----------------------
Python makes it easy to read from and write to files. Always use context managers
(the `with` statement) to ensure files are properly closed.
"""

# Writing to a file
with open("example.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("This is line 2.\n")
    file.write("Python file handling is easy!\n")

print("File 'example.txt' created and written to.")

# Reading from a file (entire content)
with open("example.txt", "r") as file:
    content = file.read()
    print("\nFull file content:")
    print(content)

# Reading line by line (memory efficient for large files)
print("\nReading line by line:")
with open("example.txt", "r") as file:
    for line_num, line in enumerate(file, 1):
        print(f"Line {line_num}: {line.strip()}")  # strip() removes newline

# Reading all lines into a list
with open("example.txt", "r") as file:
    lines = file.readlines()
    print(f"\nTotal lines: {len(lines)}")

# Appending to a file
with open("example.txt", "a") as file:
    file.write("This line was appended.\n")

print("\nAfter appending:")
with open("example.txt", "r") as file:
    print(file.read())

# Working with JSON files (common data format)
import json

data = {
    "name": "Alice",
    "age": 25,
    "hobbies": ["reading", "coding", "hiking"]
}

# Write JSON
with open("data.json", "w") as file:
    json.dump(data, file, indent=2)  # indent makes it readable

print("\nJSON file created.")

# Read JSON
with open("data.json", "r") as file:
    loaded_data = json.load(file)
    print("Loaded data:", loaded_data)
    print("Name:", loaded_data["name"])

# --- Your turn --------------------------------------------------------------
# 1. Create a file called "numbers.txt" and write numbers 1-10, one per line.
# 2. Read "numbers.txt" and calculate the sum of all numbers.
# 3. Create a JSON file with information about your favorite book.
# 4. Write a function that takes a filename and returns the number of lines.

