from datetime import date
import inflect
import sys


class Date:
    def __init__(self, year, month, day):
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        date(self.year, self.month, self.day)   # 校验探针：非法日期在这炸

    def min(self):
        d1 = date(self.year, self.month, self.day)
        d2 = date.today()
        return (d2 - d1).days * 24 * 60


def main():
    year, month, day = input("Date of Birth: ").split("-")
    try:
        d = Date(year, month, day)
    except ValueError:
        sys.exit("Invalid date")
    p = inflect.engine()
    words = p.number_to_words(d.min(), andword="")
    print(words.capitalize() + " minutes")


if __name__ == "__main__":
    main()
