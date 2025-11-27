name=input("Enter your name: ")
print(f"Hello, {name}!")

if not name.isdigit():
    print("Nice to meet you!")
else:
    print("That looks like a number, please enter a real name next time.")