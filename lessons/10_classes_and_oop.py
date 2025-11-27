"""
Lesson 10: Classes & Object-Oriented Programming
-------------------------------------------------
Classes are blueprints for creating objects. They encapsulate data (attributes)
and behavior (methods) together.
"""

# Simple class
class Dog:
    """A simple Dog class."""
    
    # Class attribute (shared by all instances)
    species = "Canis familiaris"
    
    def __init__(self, name, age):
        """Constructor - called when creating a new Dog instance."""
        self.name = name  # instance attribute
        self.age = age
    
    def bark(self):
        """Instance method."""
        return f"{self.name} says Woof!"
    
    def get_info(self):
        """Return information about the dog."""
        return f"{self.name} is {self.age} years old and is a {self.species}"

# Create instances (objects)
dog1 = Dog("Buddy", 3)
dog2 = Dog("Max", 5)

print(dog1.bark())
print(dog2.get_info())
print(f"Both dogs are {Dog.species}")

# Inheritance
class Animal:
    """Base class for animals."""
    
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def make_sound(self):
        return "Some generic animal sound"
    
    def info(self):
        return f"{self.name} is a {self.species}"

class Cat(Animal):
    """Cat class inherits from Animal."""
    
    def __init__(self, name, breed):
        super().__init__(name, "Felis catus")  # call parent constructor
        self.breed = breed
    
    def make_sound(self):  # override parent method
        return f"{self.name} says Meow!"
    
    def purr(self):
        return f"{self.name} is purring..."

# Using inheritance
cat = Cat("Whiskers", "Persian")
print(f"\n{cat.info()}")
print(cat.make_sound())
print(cat.purr())

# Encapsulation with private attributes (convention: prefix with _)
class BankAccount:
    """Bank account with private balance."""
    
    def __init__(self, owner, initial_balance=0):
        self.owner = owner
        self._balance = initial_balance  # protected (convention)
        self.__account_number = 12345  # name mangling (more private)
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return f"Deposited ${amount}. New balance: ${self._balance}"
        return "Invalid deposit amount"
    
    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return f"Withdrew ${amount}. New balance: ${self._balance}"
        return "Insufficient funds or invalid amount"
    
    def get_balance(self):
        return self._balance

account = BankAccount("Alice", 100)
print(f"\n{account.deposit(50)}")
print(account.withdraw(30))
print(f"Balance: ${account.get_balance()}")

# Class methods and static methods
class MathHelper:
    """Demonstrates class and static methods."""
    
    pi = 3.14159
    
    @classmethod
    def circle_area(cls, radius):
        """Class method - has access to class attributes."""
        return cls.pi * radius ** 2
    
    @staticmethod
    def add(a, b):
        """Static method - doesn't need class or instance."""
        return a + b

print(f"\nCircle area (radius=5): {MathHelper.circle_area(5)}")
print(f"Add 3 + 4: {MathHelper.add(3, 4)}")

# --- Your turn --------------------------------------------------------------
# 1. Create a Book class with title, author, and pages attributes.
# 2. Add a method to calculate reading time (assume 1 page per minute).
# 3. Create a Student class that inherits from a Person class.
# 4. Add a class method to your Book class that creates a book from a dictionary.

