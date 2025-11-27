from shape import Calculator


def main():
    print("Doing operation with number")
    a = float(input("Enter the value for a: "))
    b = float(input("Enter the value for b: "))

    calc = Calculator()  # constructor message prints here
    total = calc.add(a, b)
    print(f"The sum is: {total}")


if __name__ == "__main__":
    main()