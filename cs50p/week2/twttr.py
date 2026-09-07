word = input("Input: ")
vowel = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
result = ''
for x in word:
    if x not in vowel:
        result += x

print(f"Output: {result}")
