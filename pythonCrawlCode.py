import requests, time, re
import pandas as pd 

get_genres = 'https://api.themoviedb.org/3/genre/movie/list?language=en-US&api_key=eb67e272f255d3da3750f358a3984a4b'
get_movie_url = 'https://api.themoviedb.org/3/discover/movie?api_key=eb67e272f255d3da3750f358a3984a4b&with_genres='
file=open('filehaibro','a')

movies_id = set([])
response = requests.get(get_genres)
genres = response.json()
genres = genres['genres']
movie_genre={}
for m in genres:
    movie_genre[m['id']]=m['name']
#for foerign id UPDATE

def to_csv():
    websites = pd.read_csv("filehaibro", header=None)
    websites.columns=['NoOfGenres', 'Genres', 'MovieId', 'rating', 'year', 'MovieName']
    websites.to_csv('ConvertedFileHaiBro.csv', index=None)


def add_movie(m):
    # no_of_genre genre_id1,genre_id2,movie_id movie_rating year movie_title
    file.write(str(len(m['genre_ids'])))
    file.write(",")
    noOfGenres = len(m['genre_ids'])
    for l in m['genre_ids']:
        genre_name = movie_genre.get(l,'Foreign')
        if(genre_name):
            file.write(genre_name)
            noOfGenres -= 1
            if(noOfGenres == 0):
                file.write(",")
            else:
                file.write(" ")
    file.write(str(m['id']))
    file.write(",")
    
    m['title'] = re.sub(r'[^\x00-\x7f]',r'',m['title'])
    m['title'] = re.sub(r'[,]',r'',m['title'])

    file.write(str(m['vote_average']))
    file.write(",")
    yer=str(m['release_date'])
    yer=str(yer[0:4]);
    file.write(yer)
    file.write(",")
    
    print (str(m['title']));
    file.write(str(m['title']))
    file.write("\n");
flag=0;
for g in genres:
    print("G= ")
    print(g)
    genre_id = str(g['id'])
    response = requests.get(get_movie_url+genre_id+'&page=1')
    json_res = response.json()
    # print(json_res)
    page_1_results = json_res['results']
    #print(len(page_1_results))
    total_pages = json_res['total_pages']

    for r in page_1_results:
        m_id =r['id']
        if movies_id.isdisjoint(set([m_id])):
            if(r['original_language']=='en'):
                movies_id.add(m_id)
                add_movie(r)
            
    for i in range(2,min(5,total_pages+1)):
        res = requests.get(get_movie_url+genre_id+'&page='+str(i))
        json_res = res.json()
        try:
                
            results = json_res['results']
            print(i)

            for r in results:
                m_id =r['id']
                if movies_id.isdisjoint(set([m_id])):
                    if(r['original_language']=='en'):
                        movies_id.add(m_id)
                        add_movie(r)
        except Exception as e:
            print(str(e));
            flag=1;
            break;
    if(flag==1):
        continue;
                    
print("its done yr...Text file is created");
print("Now Converting that txt file to csv");

to_csv();

file.close();