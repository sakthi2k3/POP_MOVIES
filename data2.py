import  requests
api_key="409732d450e88553cc42495c2e1b7fed"
top_popular_movies ={}
recent_movies={}
home_page={}

def get_home():
    page=1
    url="https://api.themoviedb.org/3/movie/popular?api_key="+api_key+"&language=en-US&page="+str(page)
    toprated_details=requests.get(url).json()

    for i in range(18):
          top_popular_movies[toprated_details['results'][i]['title']]="http://image.tmdb.org/t/p/original"+toprated_details['results'][i]['poster_path']


    url="https://api.themoviedb.org/3/movie/now_playing?api_key="+api_key+"&language=en-US&page="+str(page)
    recent_details=requests.get(url).json()
    for i in range(18):
        recent_movies[recent_details['results'][i]['original_title']]="http://image.tmdb.org/t/p/original"+recent_details['results'][i]['poster_path']
    
    home_page['new']=recent_movies
    home_page['popular']=top_popular_movies

    return(home_page)
    


