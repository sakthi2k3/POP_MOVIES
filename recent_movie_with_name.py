import sqlite3
import requests
api_key = "409732d450e88553cc42495c2e1b7fed"
movie_name_list=[]
movie_desc_dict={}

con = sqlite3.connect('most_vist.db')
cur = con.cursor()


def create_table():
    cur.execute('''CREATE TABLE recent_movie(movie_name,times_repeated)''')
    con.commit()


# get the count of tables with the name
cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' ''')
# if the count is 1, then table exists
if cur.fetchone()[0] != 1:

    create_table()
# commit the changes to db
con.commit()
# close the connection


def function_a(movie_name):
    try:
        con = sqlite3.connect('most_vist.db')
        cur = con.cursor()
        cur.execute('''SELECT times_repeated FROM recent_movie WHERE movie_name=?''', (movie_name,))
        a = cur.fetchone()
    except:
        create_table()
    
    try:
        if a[0]:
            a=a[0]+1
            cur.execute('''UPDATE recent_movie SET times_repeated={} WHERE movie_name=?'''.format(a),(movie_name,))
            con.commit()
    except:
        rep_times = 1
        cur.execute('''INSERT INTO recent_movie VALUES(?,?)''', (movie_name,rep_times))
        con.commit()




def function_b():
    
    con = sqlite3.connect('most_vist.db')
    cur = con.cursor()
    global movie_desc_dict,movie_name_list
    movie_name=0
    cur.execute('''SELECT  * FROM recent_movie ORDER BY times_repeated DESC ''')
    movie_nm = cur.fetchall()
    if len(movie_nm)>3:

        for m in range(0,3):
                    movie_name_list.append(movie_nm[m][0])
                    movie_name = movie_nm[m][0].replace(" ", "+")
                    page = 1
                    url = "https://api.themoviedb.org/3/search/movie?api_key=" + api_key + "&language=en-US&query=" + str(
                        movie_name) + "&page=1&include_adult=false"
                    movie = requests.get(url).json()
                    try:
                       movie_id = movie["results"][0]['id']
                       movie_url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "?api_key=" + api_key + "&language=en-US"
                       movie_desc_json = requests.get(movie_url).json()
                       movie_desc_dict[movie_nm[m][0]] = "http://image.tmdb.org/t/p/original" + str(
                           movie_desc_json['poster_path'])
                    except:
                        #print("invalid_name")
                        #print(movie_name)
                        cur.execute('''DELETE  FROM recent_movie WHERE movie_name=? ''', (movie_name,))
                        con.commit()
    else:

        for m in range(0,len(movie_nm)):
                     movie_name_list.append(movie_nm[m][0])
                     movie_name = movie_nm[m][0].replace(" ", "+")
                     page = 1
                     url = "https://api.themoviedb.org/3/search/movie?api_key=" + api_key + "&language=en-US&query=" + str(
                         movie_name) + "&page=1&include_adult=false"
                     movie = requests.get(url).json()
                     try:
                         movie_id = movie["results"][0]['id']
                         movie_url = "https://api.themoviedb.org/3/movie/" + str(
                             movie_id) + "?api_key=" + api_key + "&language=en-US"
                         movie_desc_json = requests.get(movie_url).json()
                         movie_desc_dict[movie_nm[m][0]] = "http://image.tmdb.org/t/p/original" + str(movie_desc_json['poster_path'])
                     except:
                         #print("invalid_name")
                         #print(movie_name)
                         cur.execute('''DELETE FROM recent_movie WHERE movie_name=? ''', (movie_name,))
                         con.commit()
    return(movie_desc_dict,movie_name_list)   



