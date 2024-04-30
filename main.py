import random
import pandas

"""
with open('goodreads_library_export.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        print(', '.join(row))

with open('goodreads_library_export.csv', mode='r') as csvfile:
    reader = csv.reader(csvfile)
    for lines in reader:
        print(lines)
"""

csvFrame = pandas.read_csv('goodreads_library_export.csv')

csvFrame = csvFrame.drop('ISBN', axis=1)
csvFrame = csvFrame.drop('ISBN13', axis=1)
csvFrame = csvFrame.drop('Binding', axis=1)
csvFrame = csvFrame.drop('Publisher', axis=1)
csvFrame = csvFrame.drop('My Review', axis=1)
csvFrame = csvFrame.drop('Spoiler', axis=1)
csvFrame = csvFrame.drop('Author l-f', axis=1)
csvFrame = csvFrame.drop('Additional Authors', axis=1)
csvFrame = csvFrame.drop('Date Read', axis=1)
csvFrame = csvFrame.drop('Date Added', axis=1)
csvFrame = csvFrame.drop('Bookshelves with positions', axis=1)
csvFrame = csvFrame.drop('Owned Copies', axis=1)
csvFrame = csvFrame.drop('Exclusive Shelf', axis=1)
csvFrame = csvFrame.drop('Private Notes', axis=1)
csvFrame = csvFrame.drop('Original Publication Year', axis=1)
csvFrame = csvFrame.drop('My Rating', axis=1)
csvFrame = csvFrame.drop('Average Rating', axis=1)

selected = False
while not(selected):
    row = random.randint(0, csvFrame.shape[0])
    print(csvFrame.iloc[row])
    accepted = input("\nAccept?: ")
    if(accepted == "yes" or accepted == "y"):
        selected = True