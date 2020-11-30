import sqlite3, sys
import pymongo
import pandas as pd
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import db
import sklearn
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
# nonlocal userid
# userid = 0

class Recommendation():

    def __init__(self):
        # stopwords_list = stopwords.words('english')
        vectorizer = TfidfVectorizer(analyzer = 'word')
        self.movies = self.search_mongo()
        tfidf_matrix = vectorizer.fit_transform(self.movies['summary'])
        # tfidf_feature_name = vectorizer.get_feature_names()
        self.cosine_similarity = linear_kernel(tfidf_matrix, tfidf_matrix)
        self.movies = self.movies.reset_index(drop = True)
        self.indices = pd.Series(self.movies['summary'].index)  

    def search_mongo(self):
        CONNECTION_STRING = "mongodb+srv://luowei:1124@cluster0.hckie.mongodb.net/users?retryWrites=true&w=majority"
        client = pymongo.MongoClient(CONNECTION_STRING)
        db = client.users
        all_movies = db.users_flask.find()
        return pd.DataFrame(all_movies)

    def get_similar_moviesids(self, index, method):
        id_ = self.indices[index]
        similarity_scores = list(enumerate(method[id_]))
        similarity_scores.sort(key = lambda x: x[1], reverse = True)
        similarity_scores = similarity_scores[1:6]
        movies_index = [i[0] for i in similarity_scores]
        return movies_index

class Operations():
    def __init__(self):
        self.userid = 0

op = Operations()
rec = Recommendation()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    print(op.userid, file=sys.stderr)
    if op.userid is 0:
        return redirect(url_for('login'))
    conn = get_db_connection()
    print(op.userid, file=sys.stderr)
    posts = conn.execute('SELECT * FROM Favorite_Movies WHERE User_id = ?', (op.userid,)).fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']

        if email is None:
            flash('please input a email')
            return render_template('login.html')
        if username is None:
            flash('please input a username')
            return render_template('login.html')
        conn = get_db_connection()
        try:
            op.userid = conn.execute('SELECT User_id FROM Users WHERE Email = ? AND User_Name = ?', (email, username, )).fetchone()[0]
        except:
            flash('Wrong Credentials')
            return render_template('login.html')
        op.userid = conn.execute('SELECT User_id FROM Users WHERE Email = ? AND User_Name = ?', (email, username, )).fetchone()[0]
        # print(op.userid, file=sys.stderr)
        conn.close()
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/createUser', methods=('GET', 'POST'))
def createUser():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']

        if email is None:
            flash('please input a email')
            return render_template('login.html')
        if username is None:
            flash('please input a username')
            return render_template('login.html')
        conn = get_db_connection()
        conn.execute('INSERT INTO Users (Email, User_Name) VALUES(?, ?)', (email, username, ))
        op.userid = conn.execute('SELECT User_id FROM Users WHERE Email = ? AND User_Name = ?', (email, username, )).fetchone()[0]
        print(op.userid, file=sys.stderr)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('createUser.html')

@app.route('/logout', methods=('GET', 'POST'))
def logout():
    op.userid = 0
    return redirect(url_for('index'))

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM Favorite_Movies WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_movies(Moviepost_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * from Movies WHERE Movie_id = ?', (Moviepost_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_similar_movies(Moviesid):
    conn = get_db_connection()
    # similarMoviesids = [1, 2, 3, 4, 5]
    # similarMoviesids = get_similar_moviesids(Moviesid)
    similarMoviesids = rec.get_similar_moviesids(Moviesid, rec.cosine_similarity)

    similarMovies = []
    for id in similarMoviesids:
        similarMovies.append(conn.execute('SELECT * from Movies WHERE Movie_id = ?', (id,)).fetchone())
    conn.close()
    if similarMovies is None:
        abort(404)
    return similarMovies

def get_search_result(input, releaseyear, rating, operation):
    conn = get_db_connection()
    if releaseyear and rating:
        if operation == 'and':
            posts = conn.execute('SELECT * from Movies WHERE (Movie_Name LIKE ? OR Stars LIKE ?) AND ReleaseYear > ? AND Rating > ?', ('%' + input + '%', '%' + input + '%', releaseyear, rating)).fetchall()
        if operation == 'or':
            posts = conn.execute(
            """SELECT * from Movies WHERE (Movie_Name LIKE ? OR Stars LIKE ?) AND ReleaseYear > ?
            UNION
            SELECT * from Movies WHERE (Movie_Name LIKE ? OR Stars LIKE ?) AND Rating > ?
            """, ('%' + input + '%', '%' + input + '%', releaseyear, '%' + input + '%', '%' + input + '%', rating)).fetchall()
    elif releaseyear:
        posts = conn.execute('SELECT * from Movies WHERE (Movie_Name LIKE ? OR Stars LIKE ?) AND ReleaseYear > ?', ('%' + input + '%', '%' + input + '%', releaseyear)).fetchall()
    elif rating:
        posts = conn.execute('SELECT * from Movies WHERE (Movie_Name LIKE ? OR Stars LIKE ?) AND Rating > ?', ('%' + input + '%', '%' + input + '%', rating)).fetchall()
    else:
        posts = conn.execute('SELECT * from Movies WHERE Movie_Name LIKE ? OR Stars LIKE ?', ('%' + input + '%', '%' + input + '%')).fetchall()
    conn.close()
    return posts

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/movies/<int:Moviepost_id>')
def movies(Moviepost_id):
    movie = get_movies(Moviepost_id)
    similarMovies = get_similar_movies(Moviepost_id)
    return render_template('movie.html', movie=movie, similarMovies = similarMovies)

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    movie = get_post(id)

    if request.method == 'POST':
        rating = request.form['title']
        content = request.form['content']

        if rating:
            try:
                float(rating)
            except:
                flash('please input a number')
                return render_template('edit.html', movie = movie)
            rating = float(rating)
            if (rating > 10) or (rating < 0):
                flash('please input a number between 0 and 10')
                return render_template('edit.html', movie = movie)
        conn = get_db_connection()
        conn.execute('UPDATE Favorite_Movies SET myRatings = ?, myComment = ?'
                     ' WHERE id = ?',
                     (rating, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit.html', movie = movie)

@app.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        input = request.form['input']
        releaseyear = request.form['releaseyear']
        rating = request.form['rating']
        operation = request.form.get('operation')

        if not input:
            flash('something is required!')
            return render_template('search.html')
        if releaseyear:
            try:
                int(releaseyear)
            except:
                flash('for release year please input a integer')
                return render_template('search.html')
        if rating:
            try:
                float(rating)
            except:
                flash('for rating please input a number')
                return render_template('search.html')
            rating = float(rating)
            if (rating > 10) or (rating < 0):
                flash('for rating please input a number between 0 and 10')
                return render_template('search.html')
        movies = get_search_result(input, releaseyear, rating, operation)
        return render_template('search.html', movies = movies)
    return render_template('search.html')

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM Favorite_Movies WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['Movie_Name']))
    return redirect(url_for('index'))

@app.route('/<int:Movie_id>/add', methods=('POST',))
def addToFavorite(Movie_id):
    if op.userid is 0:
        return redirect(url_for('login'))
    movie = get_movies(Movie_id)
    conn = get_db_connection()
    result = conn.execute('SELECT Movie_Name, Stars, ReleaseYear, Rating, Genres, Summary from Movies WHERE Movie_id = ?', (Movie_id,)).fetchall()
    Movie_Name = result[0][0]
    Stars = result[0][1]
    ReleaseYear = result[0][2]
    Rating = result[0][3]
    Genres = result[0][4]
    Summary = result[0][5]
    conn.execute('INSERT INTO Favorite_Movies (User_id, Movie_Name, Stars, ReleaseYear, Rating, Genres, Summary) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (op.userid, Movie_Name, Stars, ReleaseYear, Rating, Genres, Summary))
    conn.commit()
    conn.close()
    flash('"{}" was successfully added!'.format(Movie_Name))
    return redirect(url_for('index'))



# print(search_mongo())