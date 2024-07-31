import config
import random
import pandas
import database

import os

def read_csv(file):
    path = "data/"
    if path not in file:
        file = path + file

    if 'storygraph' in file:
        source = 'storygraph'
    if 'goodreads' in file:
        source = 'goodreads'

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


if __name__ == "__main__":
    database.create_db()
    frame = read_csv("storygraph_readinglist_07_30_2024.csv")
    database.update_db(frame)
