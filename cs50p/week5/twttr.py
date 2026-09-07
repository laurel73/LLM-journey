def main():
    word = input("Input: ")
    print(f"Output: {shorten(word)}")


def shorten(word):
    vowel = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    result = ''
    for x in word:
        if x not in vowel:
            result += x
    return result


if __name__ == "__main__":
    main()
