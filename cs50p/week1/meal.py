time_str = input("What time is it? ")
hours, minutes = time_str.split(":")
t = float(hours) + float(minutes) / 60
if 7 <= t <= 8:
    print("breakfast time")
elif 12 <= t <= 13:
    print("lunch time")
elif 18 <= t <= 19:
    print("dinner time")
