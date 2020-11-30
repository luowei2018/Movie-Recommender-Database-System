from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
import requests
import random
def get_imd_movies(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    movies = soup.find_all("td", class_="titleColumn")
    random.shuffle(movies)
    return movies

def get_imd_summary(soup):
    return soup.find("div", class_="summary_text").contents[0].strip()

def get_imd_director(soup):
    return soup.find("div", class_="credit_summary_item").a.contents[0].strip()

def get_imd_actors(soup):
    l = soup.find("div", class_="credit_summary_item").find_next_siblings()
    ret = []
    for elem in l:
        ret.append(elem.find('a').contents[0])
    return ret

def get_imd_genres(soup):
    l = soup.find_all("div", class_="see-more inline canwrap")[1].find_all('a')
    ret = []
    for elem in l:
        ret.append(elem.string)
    return ret

def get_imd_movie_info(movie):
    movie_title = movie.a.contents[0]
    movie_year = movie.span.contents[0]
    movie_url = 'http://www.imdb.com' + movie.a['href']
    return movie_title, movie_year, movie_url

def get_imd_rating(soup):
    return soup.find("div", class_="ratingValue").find('span').contents[0]

def imd_movie_picker(movie_entrys):
    ctr=0
    print("--------------------------------------------")
    for movie in get_imd_movies('http://www.imdb.com/chart/top'):
        movie_title, movie_year, movie_url = get_imd_movie_info(movie)
        movie_page = requests.get(movie_url)
        soup = BeautifulSoup(movie_page.text, 'html.parser')
        movie_summary = get_imd_summary(soup)
        director = get_imd_director(soup)
        actors = get_imd_actors(soup)
        genres = get_imd_genres(soup)
        rating = get_imd_rating(soup)
#         print("--------------------------------------------")
        ctr=ctr+1
        
        movie_entrys.append((ctr, movie_title, str(actors), int(movie_year[1:-1]), float(rating), str(genres), movie_summary, str(director)))
        if (ctr==10):
          break;  

def create_connection(db_file, movie_entries):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        user_entries = [(1, 'qwiuer1208w@outlook.com', 'Tu Zi'), \
        (2, '1o38qweiybrxfi@126.com', 'Wu Gui'), (3, 'ro8721vtwxrf@yahoo.com', 'Hu Jing')]
        conn = sqlite3.connect(db_file)
        # with open('schema.sql') as f:
        #     conn.executescript(f.read())
            
        cur = conn.cursor()
        
        # cur.executemany("INSERT INTO Movies VALUES (?,?,?,?,?,?,?,?)", movie_entries)
        # # cur.executemany("INSERT INTO Favorite_Movies VALUES (?,?,?,?,?,?,?,?)", movie_entries)
        # cur.executemany("INSERT INTO Users VALUES (?,?,?)", user_entries)
#         print('here')
        for row in cur.execute("SELECT * FROM Movies"):
            print(row)
        else:
            print('Movies is empty')
        for row in cur.execute('SELECT * FROM Users'):
            print(row)
        
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    movie_entries = []
    # imd_movie_picker(movie_entries)
    create_connection(r"/home/spinosaurus/UIUC/CS411/movie_recommender/database.db", movie_entries)
    print(movie_entries)