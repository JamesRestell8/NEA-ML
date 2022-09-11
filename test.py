import jellyfish

nameOne = input("Name One: ")
nameTwo = input("Name Two: ")

print(jellyfish.jaro_distance(nameOne, nameTwo))