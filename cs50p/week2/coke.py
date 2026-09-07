due = 50
print("Amount Due: 50")
while True:
    coin = int(input("Insert Coin: "))
    if coin in (25, 10, 5):
        due -= coin
        if due <= 0:
            print(f"Change Owed: {-due}")
            break
        print(f"Amount Due: {due}")
