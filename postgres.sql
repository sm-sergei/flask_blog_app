sudo -u postgres psql
psql -U postgres
create database blog_db;
\с blog_db; -подключение к БД
CREATE TABLE users (user_id SERIAL PRIMARY KEY, first_name VARCHAR(20) NOT NULL, last_name VARCHAR(20) NOT NULL, username VARCHAR(20) UNIQUE NOT NULL, email VARCHAR(30) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL);
\dt -проверка что таблица создалась

CREATE TABLE blogs (blog_id SERIAL PRIMARY KEY, title VARCHAR(100) NOT NULL, author VARCHAR(40) NOT NULL, body VARCHAR(1000) NOT NULL);
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO flask;

\l - список всех Бд в postgress
\dt - Для просмотра списка таблиц в БД blog_db в PostgreSQL
\c blog_db - для подлкючения к БД

                            