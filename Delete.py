import sqlite3

def delete_books_html(book_id):    
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, author FROM books WHERE id = ?", (book_id,))
    result = cursor.fetchone()

    if result:
        name, author = result
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        message = f"Книга «{name}» автора {author} успешно удалена."
    else:
        message = f"Книга с ID {book_id} не найдена."

    conn.close()

    return f"""
    <html>
    <body>
        <h1>{message}</h1>
        <a href='/'>На главную</a>
    </body>
    </html>
    """
