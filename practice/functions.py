def add(a: int,b: int) -> int:
    print(f"Adding {a} and {b}")
    return a+b

a =input("Print First Number:")
b =input("Print Second Number:")

print(f"Addition of number is:{add(int(a),int(b))}")