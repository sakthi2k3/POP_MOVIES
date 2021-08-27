from typing import cast
from flask import *
from data2 import get_home
from data1 import start
from list_info import get_movies_search
from recent_movie_with_name import function_b,function_a
app = Flask(__name__,template_folder="templates",static_url_path='/static')

i=-1
data=get_home()
new=data['new']
popular=data['popular']
top_cast=[]
d1,d2,d3,d4=0,0,0,0
ind=[0]
pos=0
movie_names=[]
genre='popular_movie'
search=''
view=''

@app.route("/")
def index():
     rec={}
     names=[]
     rec,names=function_b()
     


     return render_template('home.html', new=new,recent=rec,popular=popular,names=names) 

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_error.html'), 404

@app.errorhandler(405)
def page_not_found(e):
    return render_template('page_error.html'), 405

@app.route("/movie/<name>")

def movie(name):
     global top_cast
     try:
        d,watch,songs,imgs,cast=start(name)
     except:
         return render_template('search_error.html')   
     top_cast=cast[0]
     try:
      d['trailer link']=d['trailer link'].replace('watch?v=','embed/')
     except:
          pass
     top_five_cast=cast[0][:5]

     function_a(d['movie_name'])    
     return render_template('movie.html', details=d,top_five_cast=top_five_cast,galery=imgs,watch_link=watch,songs=songs) 

@app.route("/search" ,methods=['POST'])
def search():
     name=request.form['search']
     return redirect(url_for('movie',name=name))

@app.route("/cast")
def cast():
          return render_template('cast.html', top_cast=top_cast) 

@app.route("/list")
def l():
          global d1,d2,d3,d4,pos,ind,genre,search,movie_names,view
          movie_names=[]
          search=''
          genre='popular_movie'
          ind=[0]
          pos=0
          d1=0
          d2=0
          d3=0
          d4=0
          movie_names,d2,d3=get_movies_search('popular_movie','',0)
          view='list'  
  
          return render_template('list.html',movie_names=movie_names,genre=genre,search=search) 

@app.route('/n')
def n():
    global d1,d2,d3,d4,search,genre,pos,movie_names,ind 

    movie_names.clear()    
    if d3>=0:
            
        ind.append(d3)
        pos+=1
     
     
        movie_names,d2,d3=get_movies_search(genre,search,d3)
    return render_template(view +'.html',movie_names=movie_names,genre=genre,search=search) 




    
    

@app.route('/p')
def p():
    
    global d1,d2,d3,d4,search,genre,pos,movie_names,ind 
    ind=set(ind)
    ind=list(ind)
    ind.sort()
    if pos>len(ind):
     pos=len(ind)-1
    if pos>0:
        movie_names.clear()      

        pos-=1


        movie_names,d2,d3=get_movies_search(genre,search,ind[pos])
    return render_template(view +'.html',movie_names=movie_names,genre=genre,search=search) 


@app.route("/r" ,methods=['POST'])
def r():
        global d1,d2,d3,d4,search,genre,pos,movie_names,ind 
        movie_names.clear()  
        ind=[0]
        pos=0
        d1,d2,d3,d4=0,0,0,0
        genre=request.form['genre']
        search=request.form['search']
        movie_names,d2,d3=get_movies_search(genre,search,d3)
        return render_template(view +'.html',movie_names=movie_names,genre=genre,search=search) 
       
@app.route('/grid')
def grid():
          global d1,d2,d3,d4,pos,ind,genre,search,movie_names,view
          movie_names=[]
          search=''
          genre='popular_movie'
          ind=[0]
          pos=0
          d1=0
          d2=0
          d3=0
          d4=0
          movie_names,d2,d3=get_movies_search('popular_movie','',0)
          view='grid'  
          return render_template('grid.html',movie_names=movie_names,genre=genre,search=search)     
     
@app.route("/about")
def about():
        return render_template('about.html')     

 
if __name__ == '__main__':
    app.run(debug=True)
 



