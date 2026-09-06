expression = input("Expression: ")
a, op, c = expression.split()
a = float(a)
c = float(c)
if op == "+":
    result = a + c
elif op == "-":
    result = a - c
elif op == "*":
    result = a * c
elif op == "/":
    result = a / c
print(f"{result:.1f}")
