import requests
import sqlite3
import  time
from deep_translator import GoogleTranslator
from googletrans import  Translator
from textblob import TextBlob
translator = Translator()
con = sqlite3.connect('q.db')
cur = con.cursor()

api_key = "59d5ad58b6b388a288ba8ffa5f0c65ca"

genre_name = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy',
              'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War',
              'Western']


def function_3(genre_name_gn):
    genre_movie = {}
    genre_dict = {}
    translated_dict={}
    page = 2
    url = "https://api.themoviedb.org/3/genre/movie/list?api_key="+api_key+"&language=en-US"
    gene_name = requests.get(url).json()


    names = genre_name_gn  # input("enter movie name:")
    for i in range(len(gene_name['genres'])):
        if names in gene_name['genres'][i]['name']:
            genre_dict = gene_name['genres'][i]

    tot_pages_url = "https://api.themoviedb.org/3/discover/movie?api_key=" + api_key + "&with_genres=" + str(genre_dict['id'])
    pages = requests.get(tot_pages_url).json()
    tot_page = pages['total_pages']
    print(tot_page)
    for p in range(1,int(tot_page)+1):
        page = p
        gen_movie_url = "https://api.themoviedb.org/3/discover/movie?api_key=" + api_key + "&with_genres=" + str(genre_dict['id']) + "&page=" + str(page)
        print(gen_movie_url)
        gene_movie_name = requests.get(gen_movie_url).json()
        for i in range(len(gene_movie_name['results'])):
                txt=gene_movie_name['results'][i]['original_title']
                #print('movie name: ',txt)


                '''if str(lan) == "en":
                    trans_name=txt
                    print("trans_name if part:",trans_name)
                    genre_movie[gene_movie_name['results'][i]['original_title']] = list(" http://image.tmdb.org/t/p/original" + str(gene_movie_name['results'][i]['poster_path']))
                    genre_movie[gene_movie_name['results'][i]['original_title']].append(trans_name)
                else:'''
                try:
                         trans_name = GoogleTranslator(source='auto', target='en').translate(str(txt))
                         #print('trans_name else pRT: ', trans_name)
                #translated_dict[gene_movie_name['results'][i]['original_title']]=trans_name
                         genre_movie[trans_name]=[]
                         genre_movie[trans_name].append("http://image.tmdb.org/t/p/original" + str(gene_movie_name['results'][i]['poster_path']))
                         genre_movie[trans_name].append(gene_movie_name['results'][i]['original_title'])
                except:
                         trans_name=txt
                         #print("trans name: except part",trans_name)
                         genre_movie[trans_name]=[]
                         genre_movie[trans_name].append( " http://image.tmdb.org/t/p/original" + str(gene_movie_name['results'][i]['poster_path']))
                         genre_movie[trans_name].append(gene_movie_name['results'][i]['original_title'])
                         #print("exceptiom flewn awzy#######################################")
                         continue

    # sorted_genre_movie=collections.OrderedDict(sorted(genre_movie.items()))
    sorted_genre_movie = dict(sorted(genre_movie.items()))

    key = list(sorted_genre_movie.keys())
    val = list(sorted_genre_movie.values())
    #print(sorted_genre_movie)
    #print("key",key)

    #print("val",val)
    #print(val[0][1][0])
    names = names.replace(' ', '_')
    for row in range(len(sorted_genre_movie)):
        cur.execute('''INSERT INTO {} VALUES (?,?,?)'''.format(names), (key[row],val[row][0],val[row][1]))
        con.commit()



'''text = '11人いる!'
a = GoogleTranslator(source='auto', target='en').translate(text)
print(a)
# print(len(genre_movie))'''
''
'''dec_lan=detector.detect( "名探偵コナン ゼロの執行人")
print(dec_lan.lang)'''
