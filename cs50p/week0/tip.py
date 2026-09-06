meal = float(input("How much was the meal? $"))
percentage = float(input("What percentage would you like to tip? ").replace("%", ""))
total = meal * (1 + percentage / 100)
print(f"Leave ${total:.2f}")
