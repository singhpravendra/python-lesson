"""
Lesson 4: Functions
-------------------
Functions group steps into a reusable block. They can receive input values
("parameters") and optionally return a result with `return`.
"""

def format_receipt(name: str, amount: float) -> str:
    """Return a neatly formatted receipt line."""
    return f"{name} owes ${amount:.2f}"


def apply_discount(amount: float, percentage: float = 10.0) -> float:
    """
    Reduce `amount` by a percentage.
    Default discount is 10% if not provided.
    """
    discount_value = amount * (percentage / 100)
    return amount - discount_value


def show_receipt():
    customer = "Taylor"
    subtotal = 25.0
    discounted_total = apply_discount(subtotal)
    line = format_receipt(customer, discounted_total)
    print(line)


if __name__ == "__main__":
    show_receipt()

# --- Your turn --------------------------------------------------------------
# 1. Add a function called `calculate_tax(amount, rate)` that returns the tax.
# 2. Update show_receipt() to include tax before printing the final total.
# 3. Call show_receipt() with different names/amounts to see reusable logic.

