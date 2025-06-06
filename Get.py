import sqlite3

def get_books_html():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, author, year FROM books")
    books = cursor.fetchall()

    conn.close()

    html = """
    <html>
    <head>
        <title>Книги</title>
        <link rel="stylesheet" href="/style.css">
    </head>
    <body>
        <h1>Список книг</h1>
        <table>
            <tr><th>Название</th><th>Автор</th><th>Год</th><th></th></tr>
    """
    for book in books:
        id, name, author, year = book
        html += f"""
            <tr>
                <td>{name}</td>
                <td>{author}</td>
                <td>{year}</td>
                <td><a class="delete-button" href="/delete?id={id}" onclick="return confirm('Удалить книгу?')">Удалить</a></td>
            </tr>
        """
    html += """
        </table>
    </body>
    </html>
    """
    return html
