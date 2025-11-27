"""
Lesson 6: Lists & Dictionaries
--------------------------------
Lists store ordered collections of items. Dictionaries store key-value pairs.
Both are mutable (you can change them after creation).
"""

# Lists: ordered, indexed collections
fruits = ["apple", "banana", "orange"]
print("Fruits:", fruits)
print("First fruit:", fruits[0])  # indexing starts at 0
print("Last fruit:", fruits[-1])  # negative index counts from the end

# Modify lists
fruits.append("grape")  # add to the end
fruits.insert(1, "mango")  # insert at position 1
print("After adding:", fruits)

# Remove items
fruits.remove("banana")  # removes first occurrence
print("After removing banana:", fruits)

# Slicing: get a portion of the list
print("First two:", fruits[:2])  # from start to index 2 (exclusive)
print("Last two:", fruits[-2:])  # last two items

# Dictionaries: key-value pairs
student = {
    "name": "Alice",
    "age": 20,
    "grades": [85, 90, 88]
}
print("\nStudent info:", student)
print("Student name:", student["name"])
print("Student age:", student.get("age"))  # safer than direct access

# Modify dictionaries
student["major"] = "Computer Science"  # add new key
student["age"] = 21  # update existing key
print("Updated student:", student)

# Iterate over dictionaries
print("\nStudent details:")
for key, value in student.items():
    print(f"  {key}: {value}")

# Nested structures
classroom = {
    "teacher": "Mr. Smith",
    "students": [
        {"name": "Alice", "grade": "A"},
        {"name": "Bob", "grade": "B"}
    ]
}
print("\nClassroom:", classroom)
print("First student:", classroom["students"][0]["name"])

# --- Your turn --------------------------------------------------------------
# 1. Create a list of your favorite movies and print each one.
# 2. Create a dictionary for a book with keys: title, author, year.
# 3. Add a list of characters to your book dictionary.
# 4. Use a loop to print all keys and values from your book dictionary.

