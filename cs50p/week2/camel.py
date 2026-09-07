variable = input()
result = ""
for ch in variable:
	if ch.isupper():
		result += "_" + ch.lower()
	else:
		result += ch

print(result)
