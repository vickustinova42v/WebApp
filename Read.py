import sqlite3

def get_books_html(user_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, author, year FROM books")
    books = cursor.fetchall()

    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    username = result[0] if result else "Незнакомец"

    conn.close()

    html = f"""
    <html>
    <head>
        <title>Профиль</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="header">
            <h2>Привет, {username}!</h2>
            <a class="logout-button" href="/logout">Выйти</a>
        </div>
        <h2>Список книг</h2>
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
                <a class="return-button" href="/return?id={id}">Вернуть</a>
            </div>
        """
    html += """
    </body>
    </html>
    """
    return html
