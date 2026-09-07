import sys
import requests

try:
    n = float(sys.argv[1])
except (ValueError, IndexError):
    sys.exit("Command-line argument is not a number")

try:
    r = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
    bit = r.json()
except requests.RequestException:
    sys.exit("Request failed")

price = bit["bpi"]["USD"]["rate_float"]
print(f"${price * n:,.4f}")
