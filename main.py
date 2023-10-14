# main.py
from tmdb import *

def PrintList(l: list) -> None:
    for e in l:
        print(e)

if __name__ == "__main__":
    for i in range(1, 50):
        movie = RequestMovie(i)
        if (movie == None): 
            continue
        movie.InsertIntoDB()
