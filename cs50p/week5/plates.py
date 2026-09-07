def main():
    plate = input('Plate:')
    if is_valid(plate):
        print('Valid')
    else:
        print('Invalid')


def is_valid(plate):
    Legal_characters = [
        'a','b','c','d','e','f','g','h','i','j','k','l','m',
        'n','o','p','q','r','s','t','u','v','w','x','y','z',
        'A','B','C','D','E','F','G','H','I','J','K','L','M',
        'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
        '0','1','2','3','4','5','6','7','8','9'
    ]
    number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    letter = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
        'n','o','p','q','r','s','t','u','v','w','x','y','z',
        'A','B','C','D','E','F','G','H','I','J','K','L','M',
        'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    ok = True
    if len(plate) < 2 or len(plate) > 6:
        ok = False
    if plate[0] not in letter:
        ok = False

    seen_number = False
    first_number = True
    for word in plate:
        if word not in Legal_characters:
            ok = False
        elif word in number:
            if first_number and word == '0':
                ok = False
            first_number = False
            seen_number = True
        elif word in letter:
            if seen_number:
                ok = False

    return ok


if __name__ == "__main__":
    main()
