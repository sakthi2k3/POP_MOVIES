import sqlite3
import requests
from deep_translator import GoogleTranslator
from googletrans import  Translator
con = sqlite3.connect('popular_Data.db')
cur=con.cursor()
api_key="59d5ad58b6b388a288ba8ffa5f0c65ca"

pop_movie={}
def create_table():
        cur.execute('''CREATE TABLE popular_movie(movie_name,movie_url,ori_movie_name)''')
        con.commit()

def value_inserted_in_table():

    pop_movie_url="https://api.themoviedb.org/3/movie/popular?api_key="+api_key+"&page=1"
    pop_movie_url_json = requests.get(pop_movie_url).json()
    page_no=pop_movie_url_json['total_pages']
    print(page_no)
    for p in range(1,int(page_no)+1):
        pop_url="https://api.themoviedb.org/3/movie/popular?api_key="+str(api_key)+"&page="+str(p)
        print(pop_url)
        pop_url_json=requests.get(pop_url).json()

        for i in range(len(pop_url_json['results'])):
            txt = pop_url_json['results'][i]['original_title']
            try:
                trans_name = GoogleTranslator(source='auto', target='en').translate(str(txt))
                # print('trans_name else pRT: ', trans_name)
                # translated_dict[gene_movie_name['results'][i]['original_title']]=trans_name
                pop_movie[trans_name] = []
                pop_movie[trans_name].append(
                    "http://image.tmdb.org/t/p/original" + str(pop_url_json['results'][i]['poster_path']))
                pop_movie[trans_name].append(pop_url_json['results'][i]['original_title'])
            except:
                trans_name = txt
                # print("trans name: except part",trans_name)
                pop_movie[trans_name] = []
                pop_movie[trans_name].append(
                    " http://image.tmdb.org/t/p/original" + str(pop_url_json['results'][i]['poster_path']))
                pop_movie[trans_name].append(pop_url_json['results'][i]['original_title'])
                # print("exceptiom flewn awzy#######################################")
                continue

    sorted_genre_movie = dict(sorted(pop_movie.items()))
    print(sorted_genre_movie)
    key = list(sorted_genre_movie.keys())
    val = list(sorted_genre_movie.values())
        # print(sorted_genre_movie)
        # print("key",key)

        # print("val",val)
        # print(val[0][1][0])

    for row in range(len(sorted_genre_movie)):
            cur.execute('''INSERT INTO {} VALUES (?,?,?)'''.format("popular_movie"), (key[row], val[row][0], val[row][1]))
            con.commit()

create_table()
value_inserted_in_table()
con.close()
print("ended")