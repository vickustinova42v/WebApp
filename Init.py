import sqlite3
import hashlib

DB_NAME = "library.db"

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('reader', 'admin')) DEFAULT 'reader'
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL,
            is_taken INTEGER NOT NULL DEFAULT 0 CHECK(is_taken IN (0, 1))
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS user_books (
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(book_id) REFERENCES books(id),
            PRIMARY KEY (user_id, book_id)
        )
    ''')

    c.execute("SELECT id FROM users WHERE username = 'admin'")
    if not c.fetchone():
        admin_password = hash_password('admin')
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('admin', admin_password, 'admin'))

    c.execute("SELECT COUNT(*) FROM books")
    if c.fetchone()[0] == 0:
        books = [
            ('1984', 'Джордж Оруэлл', 1949),
            ('Преступление и наказание', 'Фёдор Достоевский', 1866),
            ('Мастер и Маргарита', 'Михаил Булгаков', 1967),
            ('Война и мир', 'Лев Толстой', 1869),
            ('Гарри Поттер и философский камень', 'Дж. К. Роулинг', 1997),
            ('Улисс', 'Джеймс Джойс', 1922),
            ('Три товарища', 'Эрих Мария Ремарк', 1936),
            ('Сто лет одиночества', 'Габриэль Гарсиа Маркес', 1967),
            ('Анна Каренина', 'Лев Толстой', 1877),
            ('Под куполом', 'Стивен Кинг', 2009),
            ('Имя розы', 'Умберто Эко', 1980),
            ('Фауст', 'Иоганн Вольфганг Гёте', 1808),
            ('Над пропастью во ржи', 'Джером Д. Сэлинджер', 1951),
            ('Американская трагедия', 'Теодор Драйзер', 1925),
            ('451° по Фаренгейту', 'Рэй Брэдбери', 1953)
        ]
        c.executemany("INSERT INTO books (name, author, year) VALUES (?, ?, ?)", books)

    conn.commit()
    conn.close()
