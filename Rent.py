import sqlite3

DB_NAME = "library.db"

def rent_book(book_id, user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT is_taken FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    cursor.execute("UPDATE books SET is_taken = 1 WHERE id = ?", (book_id,))
    cursor.execute("INSERT OR IGNORE INTO user_books (user_id, book_id) VALUES (?, ?)", (user_id, book_id))
    conn.commit()
    conn.close()

def return_book(book_id, user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM user_books WHERE user_id = ? AND book_id = ?", (user_id, book_id))
    cursor.execute("DELETE FROM user_books WHERE user_id = ? AND book_id = ?", (user_id, book_id))
    cursor.execute("UPDATE books SET is_taken = 0 WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
