class Calculator:
    """Simple calculator with basic arithmetic operations."""

    def __init__(self) -> None:
        print("This is a Default Constructor for Calculator class")

    def add(self, a: float, b: float) -> float:
        return a + b

    def sub(self, a: float, b: float) -> float:
        return a - b