import sys
import csv

if len(sys.argv) < 3:
    sys.exit("Too few command-line arguments")
elif len(sys.argv) > 3:
    sys.exit("Too many command-line arguments")

try:
    with open(sys.argv[1]) as f:
        rows = list(csv.DictReader(f))
except FileNotFoundError:
    sys.exit("File does not exist")

with open(sys.argv[2], "w") as f:
    writer = csv.DictWriter(f, fieldnames=["first", "last", "house"])
    writer.writeheader()
    for row in rows:
        last, first = row["name"].split(",")
        writer.writerow({
            "first": first.strip(),
            "last": last.strip(),
            "house": row["house"],
        })
