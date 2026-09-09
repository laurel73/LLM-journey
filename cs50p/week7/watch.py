import re


def main():
    html = input("HTML: ")
    if url := parse(html):
        print(url)


def parse(html):
    m = re.search(r'src="https?://(?:www\.)?youtube\.com/embed/(\w+)"', html)
    if m:
        return f"https://youtu.be/{m.group(1)}"


if __name__ == "__main__":
    main()
