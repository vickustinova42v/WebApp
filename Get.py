# Get.py
import sqlite3

DB_NAME = 'library.db'

def get_books_html():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, author, year FROM books")
    books = cursor.fetchall()
    conn.close()

    books_list_html = ''.join([
        f"<li><strong>{name}</strong> — {author} ({year})</li>"
        for name, author, year in books
    ])

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Список книг</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="container">
            <h1>Список книг</h1>
            <ul>
                {books_list_html}
            </ul>
        </div>
    </body>
    </html>
    """
    return html
