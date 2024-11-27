-- Prepare MySQL for the project
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;

USE hbnb_dev_db;  -- Sélectionnez la base de données pour la suite

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(60) NOT NULL PRIMARY KEY,
    email VARCHAR(128) NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS amenities (
    id VARCHAR(60) NOT NULL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS cities (
    id VARCHAR(60) NOT NULL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    state_id VARCHAR(60) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS places (
    id VARCHAR(60) NOT NULL PRIMARY KEY,
    user_id VARCHAR(60) NOT NULL,
    city_id VARCHAR(60) NOT NULL,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    number_rooms INT NOT NULL,
    number_bathrooms INT NOT NULL,
    max_guest INT NOT NULL,
    price_by_night FLOAT NOT NULL,
    latitude FLOAT(10, 6) NOT NULL,
    longitude FLOAT(10, 6) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS states (
    id VARCHAR(60) NOT NULL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS reviews (
    id VARCHAR(60) NOT NULL PRIMARY KEY,
    text TEXT NOT NULL,
    user_id VARCHAR(60) NOT NULL,
    place_id VARCHAR(60) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- Création de la base de données de test
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;

USE hbnb_test_db;  -- Sélectionnez la base de données pour la suite

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(60) NOT NULL PRIMARY KEY,
    email VARCHAR(128) NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);