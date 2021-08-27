from sqlite3.dbapi2 import enable_shared_cache
import requests
import sqlite3
from googletrans import Translator

i=0
j=0


def get_movies_search(genre_name,s,index):
        global i,j
        genre_movie=[]

        i=index
        try:
                if genre_name=='Genre' or genre_name=='popular_movie':
                        con = sqlite3.connect('popular_Data.db')
                        genre_name='popular_movie'
                else:        
                        con = sqlite3.connect('q.db')
                n=genre_name.replace(' ','_')
                cur = con.cursor()
                cur.execute('''SELECT * FROM {}'''.format(n))

                rows = cur.fetchall()
                for row in range(i,len(rows)):
                        if s.lower() in (rows[row][0]).lower():
                                genre_movie.append(rows[row])
                        if len(genre_movie)==8:
                                j=row+1
                        
                                break
                  
                return(genre_movie,i,j)
        except:   
                return(genre_movie,i,j)

