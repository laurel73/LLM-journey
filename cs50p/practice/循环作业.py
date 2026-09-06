students = [
    {"name": "Harry", "house": "Gryffindor", "patronus": "Stag"},
    {"name": "Hermione", "house": "Gryffindor", "patronus": "Otter"},
    {"name": "Draco", "house": "Slytherin", "patronus": None},
    {"name": "Luna", "house": "Ravenclaw", "patronus": "Hare"},
    {"name": "Cedric", "house": "Hufflepuff", "patronus": None},
]
for student in students :
    if student ["patronus"]:
        print (student ["name" ],student ["house" ],student["patronus"],sep = "-")
    else:
        print (student ["name" ],student ["house" ],"?",sep = "-")

coents={}
for student in students :
    house = student ["house"]
    if house not in coents :
        coents [house]=0
    coents [house]+=1
for house in coents:
    print (house,coents [house])