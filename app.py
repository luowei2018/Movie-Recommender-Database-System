import sqlite3, sys
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import db

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM Favorite_Movies').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

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
    return render_template('movie.html', movie=movie)

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
                 (2, Movie_Name, Stars, ReleaseYear, Rating, Genres, Summary))
    conn.commit()
    conn.close()
    flash('"{}" was successfully added!'.format(Movie_Name))
    return redirect(url_for('index'))
