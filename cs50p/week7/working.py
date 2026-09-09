import re


def main():
    print(convert(input("Hours: ")))


def convert(s):
    m = re.search(r"^(\d{1,2})(?::(\d{2}))? (AM|PM) to (\d{1,2})(?::(\d{2}))? (AM|PM)$", s)
    if not m:
        raise ValueError

    start = to_minutes(m.group(1), m.group(2), m.group(3))
    end = to_minutes(m.group(4), m.group(5), m.group(6))

    hours = (end - start) / 60
    if hours < 0:
        hours += 24
    return f"{hours} hours"


def to_minutes(h, minute, ap):
    h = int(h)
    minute = int(minute or 0)
    if minute >= 60:
        raise ValueError
    if ap == "AM":
        h = 0 if h == 12 else h
    else:
        h = h if h == 12 else h + 12
    return h * 60 + minute


if __name__ == "__main__":
    main()
