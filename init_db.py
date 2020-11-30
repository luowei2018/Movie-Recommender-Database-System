import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
# cur.execute("INSERT INTO Movies (Movie_Name, Stars, ReleaseYear, Rating, Genres, Summary) VALUES (?, ?, ?, ?, ?, ?)",
#             ('Goodfellas', 'Robert De Niro, Ray Liotta, Joe Pesci', 1990, 8.7, 'Biography, Crime, Drama', 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.')
#             )
# cur.execute("INSERT INTO Movies (Movie_Name, Stars, ReleaseYear, Rating, Genres, Summary) VALUES (?, ?, ?, ?, ?, ?)",
#             ('Godfather', 'Buster Keaton', 1970, 3.7, 'Action, Comedy, Romance', 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.')
#             )
# cur.execute("INSERT INTO Movies (Movie_Name, Stars, ReleaseYear, Rating, Genres, Summary) VALUES (?, ?, ?, ?, ?, ?)",
#             ('SOO', 'Buster Keaton', 2000, 6.7, 'Action, Comedy, Romance', 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.')
#             )
# cur.execute("INSERT INTO Movies (Movie_Name, Stars, ReleaseYear, Rating, Genres, Summary) VALUES (?, ?, ?, ?, ?, ?)",
#             ('Boog', 'Buster Keaton', 1997, 9.7, 'Action, Comedy, Romance', 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.')
#             )
# cur.execute("INSERT INTO Movies (Movie_Name, Stars, ReleaseYear, Rating, Genres, Summary) VALUES (?, ?, ?, ?, ?, ?)",
#             ('AHH', 'Buster Keaton', 1960, 7.9, 'Action, Comedy, Romance', 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.')
#             )
#
# cur.execute("INSERT INTO Users (Email, User_Name) VALUES (?, ?)",
#             ('emilylingjy@gmail.com', 'jiayi ling')
#             )
# cur.execute("INSERT INTO Favorite_Movies (User_id, Movie_Name, Stars, ReleaseYear, Rating, Genres, Summary) VALUES (?, ?, ?, ?, ?, ?, ?)",
#             (1, 'Goodfellas', 'Robert De Niro, Ray Liotta, Joe Pesci', 1990, 8.7, 'Biography, Crime, Drama', 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.')
#             )
connection.commit()
connection.close()
