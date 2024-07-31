import config
import random
import pandas

import os

def read_csv(file, source="goodreads"):
    path = "data/"
    if path not in file:
        file = path + file

    if not os.path.exists(file):
        raise FileNotFoundError

    csvFrame = pandas.read_csv(file)

    if source == 'goodreads':
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


    return csvFrame

def get_selection(frame):
    selected = False
    while not(selected):
        row = random.randint(0, frame.shape[0])
        if(frame.iloc[row]["Read Count"] == 0):
            print(frame.iloc[row])
            accepted = input("\nAccept?: ")
            if(accepted == "yes" or accepted == "y"):
                selected = True

def get_total_pages(frame):
    total = frame['Number of Pages'].sum()
    return total

if __name__ == "__main__":

    frame = read_csv("updated_sourcegraph.csv", source="no")
    
    total = 124626
    total_2 = 124626
    num_days = int(total/50)
    print(f"It will take you {num_days} days to finish all books on your list")
    num_years = int(num_days / 365)
    print(f"It will take you {num_years} years to finish all books on your list")
