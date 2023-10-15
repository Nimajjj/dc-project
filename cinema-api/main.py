# main.py
import time
from tmdb import *

from_id = 0
to_id = 200

def PrintList(l: list) -> None:
    for e in l:
        print(e)

if __name__ == "__main__":
    for i in range(from_id, to_id):
        time.sleep(0.1)
        movie = RequestMovie(i)
        if (movie == None): 
            print(f"Movie {i} does not exists in TMDB...")
            continue
        print(f"Inserting movie {i}: '{movie.movie.title}'...")
        movie.InsertIntoDB()
