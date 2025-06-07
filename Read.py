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
        <title>Профиль</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Список книг</h1>
        <a class="create-button" href="/create">Добавить книгу</a>
    """
    for book in books:
        id, name, author, year = book
        html += f"""
            <div class="list_of_books">
                <span>ID-{id}. </span>
                <span>{name}, </span>
                <span>{author}, </span>
                <span>{year}</span>
                <a class="delete-button" href="/delete?id={id}">Удалить</a>
                <a class="change-button" href="/change?id={id}">Изменить</a>
                <a class="rent-button" href="/rent?id={id}">Взять в аренду</a>
            </div>
        """
    html += """
    </body>
    </html>
    """
    return html
