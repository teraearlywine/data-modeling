CREATE DATABASE IF NOT EXISTS food;

CREATE TABLE IF NOT EXISTS food.recipes (
	id INT AUTO_INCREMENT PRIMARY KEY
  , created_ts TIMESTAMP NOT NULL
  , name VARCHAR(255) NOT NULL
  , type VARCHAR(255) NOT NULL
  , difficulty_status VARCHAR(255) NOT NULL
  , url  VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS food.cuisine_type (
	id INT AUTO_INCREMENT PRIMARY KEY
  , name VARCHAR(255) NOT NULL 
  , created_ts TIMESTAMP NOT NULL
  , recipe_id INT NOT NULL
  , FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);