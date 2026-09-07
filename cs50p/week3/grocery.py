Item = {}
while True:
    try:
        due = input('Item: ').strip().upper()
    except EOFError:
        break
    if due not in Item:
        Item[due] = 1
    else:
        Item[due] += 1

for item in sorted(Item):
    print(f"{Item[item]} {item}")
