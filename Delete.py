import sqlite3

def delete_books_html(book_id):    
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, author FROM books WHERE id = ?", (book_id))
    result = cursor.fetchone()

    if result:
        name, author = result
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id))
        conn.commit()

    conn.close()