import re


def main():
    ip = input("IPv4 Address: ")
    if validate(ip):
        print("Valid")
    else:
        print("Invalid")


def validate(ip):
    if re.search(r"^\d+\.\d+\.\d+\.\d+$", ip):
        for part in ip.split("."):
            if not 0 <= int(part) <= 255:
                return False
        return True
    return False


if __name__ == "__main__":
    main()
