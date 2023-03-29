CREATE USER 'auth_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'strong_password';

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

USE auth;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUES ('martin@gmail.com', 'martin123');



-- CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'auth123';

-- CREATE DATABASE auth;

-- GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

-- USE auth;

-- CREATE TABLE user (
--     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
--     email VARCHAR(255) NOT NULL UNIQUE,
--     password VARCHAR(255) NOT NULL
-- );

-- INSERT INTO user (email, password) VALUES ('martin@gmail.com', 'martin123');