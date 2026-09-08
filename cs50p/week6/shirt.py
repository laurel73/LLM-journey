import sys
from PIL import Image, ImageOps

if len(sys.argv) < 3:
    sys.exit("Too few command-line arguments")
elif len(sys.argv) > 3:
    sys.exit("Too many command-line arguments")

if not sys.argv[1].endswith((".jpg", ".jpeg", ".png")):
    sys.exit("Invalid input")
if not sys.argv[2].endswith((".jpg", ".jpeg", ".png")):
    sys.exit("Invalid output")

try:
    shirt = Image.open("shirt.png")
    photo = Image.open(sys.argv[1])
except FileNotFoundError:
    sys.exit("File does not exist")

size = shirt.size
photo = ImageOps.fit(photo, size)
photo.paste(shirt, shirt)
photo.save(sys.argv[2])
