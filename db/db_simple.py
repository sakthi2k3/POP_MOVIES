import sqlite3
import requests
con = sqlite3.connect('q.db')
cur=con.cursor()
api_key="59d5ad58b6b388a288ba8ffa5f0c65ca"
genres=[]
def get_genre():

    url="https://api.themoviedb.org/3/genre/movie/list?api_key="+api_key+"&language=en-US"
    genre_details=requests.get(url).json()
    #print(genre_details)
    for names,value in genre_details.items():
        for i in range (len(value)):
           movie=value[i]
           genres.append(movie['name'])
    print(genres)
get_genre()
for n in range(len(genres)):
    print(genres[n])
    cur.execute('''CREATE TABLE {} (movie_name,movie_url,trans_name)'''.format(str(genres[n]).replace(' ','_')))
    con.commit()
sql_query = """SELECT name FROM sqlite_master  WHERE type='table';"""
con.commit()
cur.execute(sql_query)
print(cur.fetchall())