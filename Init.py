import sqlite3

DB_NAME = "library.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Таблица пользователей
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('reader', 'admin')) DEFAULT 'reader'
        )
    ''')

    # Таблица книг
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    ''')

    # Таблица аренды (связь многие ко многим: user ↔ books)
    c.execute('''
        CREATE TABLE IF NOT EXISTS rentals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(book_id) REFERENCES books(id),
            UNIQUE(book_id)  -- чтобы одна книга не могла быть взята двумя сразу
        )
    ''')

    # Добавление администратора
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  ('admin', 'admin', 'admin'))

    conn.commit()
    conn.close()