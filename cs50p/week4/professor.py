import random

while True:
    try:
        level = int(input("Level: "))
        if level not in (1, 2, 3):
            raise ValueError
        break
    except ValueError:
        pass

score = 0
for _ in range(10):
    x = random.randint(0, 10**level - 1)
    y = random.randint(0, 10**level - 1)
    answer = x + y
    no = 0
    while no < 3:
        z = int(input(f"{x} + {y} = "))
        if z == answer:
            score += 1
            break
        print("EEE")
        no += 1
    else:
        print(f"{x} + {y} = {answer}")

print(f"Score: {score}/10")
