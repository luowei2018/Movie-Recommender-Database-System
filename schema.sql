-- DROP TABLE IF EXISTS posts;
-- DROP TABLE IF EXISTS Users;
-- DROP TABLE IF EXISTS Favorite_Movies;
-- DROP TABLE IF EXISTS Movies;
DROP TABLE IF EXISTS Pet;

--
-- CREATE TABLE posts (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     title TEXT NOT NULL,
--     content TEXT NOT NULL
-- );
--
-- CREATE TABLE Favorite_Movies (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     timeadded TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     myComment VARCHAR,
--     myRatings REAL,
--     User_id INTEGER NOT NULL,
--     Movie_Name VARCHAR NOT NULL,
--     Stars VARCHAR,
--     ReleaseYear INTEGER,
--     Rating REAL,
--     Genres VARCHAR,
--     Summary VARCHAR
-- );
--
-- CREATE TABLE Movies (
--     Movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
--     Movie_Name VARCHAR NOT NULL,
--     Stars VARCHAR,
--     ReleaseYear INTEGER,
--     Rating REAL,
--     Genres VARCHAR,
--     Summary VARCHAR
-- );
--
-- CREATE TABLE Users (
--     User_id INTEGER PRIMARY KEY AUTOINCREMENT,
--     Email VARCHAR NOT NULL,
--     User_Name VARCHAR NOT NULL
-- );

CREATE TABLE Pet (
  User_id INTEGER NOT NULL,
  Favorite_Pet VARCHAR NOT NULL
);
