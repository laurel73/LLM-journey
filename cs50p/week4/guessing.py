import random

while True:
    try:
        level = int(input("Level: "))
        if level <= 0:
            raise ValueError
        break
    except ValueError:
        pass

answer = random.randint(1, level)
while True:
    guess = int(input("Guess: "))
    if guess < answer:
        print("Too small!")
    elif guess > answer:
        print("Too large!")
    else:
        print("Just right!")
        break
