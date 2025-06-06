-- Создание таблиц
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    is_rented INTEGER DEFAULT 0,
    rented_by INTEGER,
    FOREIGN KEY(rented_by) REFERENCES users(id)
);

-- Добавление тестовых пользователей
INSERT INTO users (username, password, role) VALUES
('admin', 'admin', 'admin'),
('user', 'user', 'user');

-- Добавление книг
INSERT INTO books (title, author, is_rented, rented_by) VALUES
('1984', 'Джордж Оруэлл', 0, NULL),
('Мастер и Маргарита', 'Булгаков', 1, 2),
('Преступление и наказание', 'Ф.М. Достоевский', 0, NULL);
