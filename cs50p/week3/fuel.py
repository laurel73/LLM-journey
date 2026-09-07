while True:
    try:
        x, y = input("Fraction: ").split("/")
        x = int(x)
        y = int(y)
        if x > y or y == 0:
            raise ValueError
        break
    except ValueError:
        pass

percentage = round(x / y * 100)
if percentage <= 1:
    print("E")
elif percentage >= 99:
    print("F")
else:
    print(f"{percentage}%")
