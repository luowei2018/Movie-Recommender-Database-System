import sqlite3
def get_all_movies(db_file):
    """ create a database connection to a SQLite database """
    movies = []
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        for row in cur.execute("SELECT * FROM Movies"):
            print(row)  
            movies.append(row)   
        else:
            print('Movies is empty')  
        conn.commit()
        conn.close()
        return movies
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        return movies

def outputJson():
    movies = get_all_movies(r"/home/spinosaurus/UIUC/CS411/movie_recommender/database.db")
    # print(movies)
    entries = []
    for movie in movies:
        entry = {}
        id, movie_title, stars, release_year, rating, genres, summary, director = movie
        star1, star2 = stars.strip()[1:-1].replace('\'', '').split(',')
        star2 = star2[1:]
        entry['_id'] = id
        entry['movie_title'] = movie_title
        entry['stars'] = stars
        entry['release_year'] = release_year
        entry['rating'] = rating
        genres = genres[1:-1].replace('\'', '').split(',')
        genres = [elem.strip() for elem in genres]
        entry['genres'] = genres
        entry['summary'] = summary
        entry['director'] = director
        entries.append(entry)
        print(entry)
        print('--------')
    # print(entries)
    return entries

if __name__ == "__main__":
    outputJson()
    
               
