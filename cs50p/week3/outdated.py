months = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}

while True:
    date = input("Date: ").strip()
    try:
        if "/" in date:
            m, d, y = date.split("/")
            m, d, y = int(m), int(d), int(y)
        elif "." in date:
            m, d, y = date.split(".")
            m, d, y = int(m), int(d), int(y)
        elif "-" in date:
            m, d, y = date.split("-")
            m, d, y = int(m), int(d), int(y)
        else:
            parts = date.replace(",", "").split()
            if parts[0].lower() in months:
                m = months[parts[0].lower()]
                d = int(parts[1])
            else:
                d = int(parts[0])
                m = months[parts[1].lower()]
            y = int(parts[2])

        if not (1 <= m <= 12 and 1 <= d <= 31):
            raise ValueError
        break
    except (ValueError, KeyError):
        pass

print(f"{y:04d}-{m:02d}-{d:02d}")
