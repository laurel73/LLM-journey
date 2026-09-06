def main():
    face = input()
    print(convert(face))


def convert(text):
    return text.replace(":)", "\U0001F642").replace(":(", "\U0001F641")


main()
