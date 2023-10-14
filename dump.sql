CREATE DATABASE cinema;
USE cinema;

 CREATE TABLE actors
(
    id_actor   INT AUTO_INCREMENT
        PRIMARY KEY,
    actor_name VARCHAR(255) NULL
);

CREATE TABLE countries
(
    id_country   INT AUTO_INCREMENT
        PRIMARY KEY,
    iso_3166_1   VARCHAR(50)  NULL,
    country_name VARCHAR(255) NULL
);

CREATE TABLE directors
(
    id_director   INT AUTO_INCREMENT
        PRIMARY KEY,
    director_name VARCHAR(255) NULL
);

CREATE TABLE distributors
(
    id_distributor   INT AUTO_INCREMENT
        PRIMARY KEY,
    distributor_name VARCHAR(255) NULL
);

CREATE TABLE genres
(
    id_genre INT AUTO_INCREMENT
        PRIMARY KEY,
    title    VARCHAR(255) NOT NULL,
    CONSTRAINT title
        UNIQUE (title)
);

CREATE TABLE languages
(
    id_language   INT AUTO_INCREMENT
        PRIMARY KEY,
    iso_639_1     VARCHAR(50) NULL,
    language_name VARCHAR(50) NULL,
    english_name  VARCHAR(50) NULL
);

CREATE TABLE movies
(
    id_movie         INT AUTO_INCREMENT
        PRIMARY KEY,
    duration_min     INT          NULL,
    original_title   VARCHAR(255) NULL,
    imdb_id          VARCHAR(50)  NULL,
    title            VARCHAR(255) NOT NULL,
    overview         TEXT         NULL,
    poster           TEXT         NULL,
    release_date     DATE         NULL,
    visa_number      INT          NULL,
    minimum_age      INT          NULL,
    awards           TEXT         NULL,
    id_distributor   INT          NULL,
    original_laguage VARCHAR(50)  NULL,
    CONSTRAINT movies_ibfk_1
        FOREIGN KEY (id_distributor) REFERENCES distributors (id_distributor)
);

CREATE TABLE actors_movies
(
    id_movie INT NOT NULL,
    id_actor INT NOT NULL,
    PRIMARY KEY (id_movie, id_actor),
    CONSTRAINT actors_movies_ibfk_1
        FOREIGN KEY (id_movie) REFERENCES movies (id_movie),
    CONSTRAINT actors_movies_ibfk_2
        FOREIGN KEY (id_actor) REFERENCES actors (id_actor)
);

CREATE INDEX id_actor
    ON actors_movies (id_actor);

CREATE TABLE countries_movies
(
    id_movie   INT NOT NULL,
    id_country INT NOT NULL,
    PRIMARY KEY (id_movie, id_country),
    CONSTRAINT countries_movies_ibfk_1
        FOREIGN KEY (id_movie) REFERENCES movies (id_movie),
    CONSTRAINT countries_movies_ibfk_2
        FOREIGN KEY (id_country) REFERENCES countries (id_country)
);

CREATE INDEX id_country
    ON countries_movies (id_country);

CREATE TABLE directors_movies
(
    id_movie    INT NOT NULL,
    id_director INT NOT NULL,
    PRIMARY KEY (id_movie, id_director),
    CONSTRAINT directors_movies_ibfk_1
        FOREIGN KEY (id_movie) REFERENCES movies (id_movie),
    CONSTRAINT directors_movies_ibfk_2
        FOREIGN KEY (id_director) REFERENCES directors (id_director)
);

CREATE INDEX id_director
    ON directors_movies (id_director);

CREATE TABLE genres_movies
(
    id_movie INT NOT NULL,
    id_genre INT NOT NULL,
    PRIMARY KEY (id_movie, id_genre),
    CONSTRAINT genres_movies_ibfk_1
        FOREIGN KEY (id_movie) REFERENCES movies (id_movie),
    CONSTRAINT genres_movies_ibfk_2
        FOREIGN KEY (id_genre) REFERENCES genres (id_genre)
);

CREATE INDEX id_genre
    ON genres_movies (id_genre);

CREATE TABLE movie_languages
(
    id_movie    INT NOT NULL,
    id_language INT NOT NULL,
    PRIMARY KEY (id_movie, id_language),
    CONSTRAINT movie_languages_ibfk_1
        FOREIGN KEY (id_movie) REFERENCES movies (id_movie),
    CONSTRAINT movie_languages_ibfk_2
        FOREIGN KEY (id_language) REFERENCES languages (id_language)
);

CREATE INDEX id_language
    ON movie_languages (id_language);

CREATE INDEX id_distributor
    ON movies (id_distributor);
