import sqlite3

DB_NAME = "library.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # 1. Создаём таблицы
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
            is_taken INTEGER NOT NULL DEFAULT 0
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

    # 2. Админ
    c.execute("SELECT id FROM users WHERE username = 'admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('admin', 'admin', 'admin'))

    # 3. Reader
    c.execute("SELECT id FROM users WHERE username = 'reader1'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('reader1', 'reader1', 'reader'))

    # 4. Книги
    c.execute("SELECT COUNT(*) FROM books")
    if c.fetchone()[0] == 0:
        books = [
            ('1984', 'Джордж Оруэлл', 1949),
            ('Преступление и наказание', 'Фёдор Достоевский', 1866),
            ('Мастер и Маргарита', 'Михаил Булгаков', 1967),
            ('Война и мир', 'Лев Толстой', 1869),
            ('Гарри Поттер и философский камень', 'Дж. К. Роулинг', 1997)
        ]
        c.executemany("INSERT INTO books (name, author, year) VALUES (?, ?, ?)", books)

    # 5. Получаем ID reader1
    c.execute("SELECT id FROM users WHERE username = 'reader1'")
    reader_id_row = c.fetchone()
    if reader_id_row:
        user_id = reader_id_row[0]

    # 6. Две книги
    c.execute("SELECT id FROM books WHERE is_taken = 0 LIMIT 2")
    book_ids = [row[0] for row in c.fetchall()]

    for book_id in book_ids:
        c.execute("INSERT OR IGNORE INTO user_books (user_id, book_id) VALUES (?, ?)", (user_id, book_id))
        c.execute("UPDATE books SET is_taken = 1 WHERE id = ?", (book_id,))

    conn.commit()
    conn.close()
