import sqlite3

def get_books_html(user_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username, role FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    username = result[0] if result else "Незнакомец"
    role = result[1] if result else "reader"

    cursor.execute('''
        SELECT b.id, b.name, b.author, b.year,
               EXISTS (SELECT 1 FROM user_books WHERE book_id = b.id) as is_taken,
               EXISTS (SELECT 1 FROM user_books WHERE book_id = b.id AND user_id = ?) as is_taken_by_user
        FROM books b
    ''', (user_id,))
    books = cursor.fetchall()

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
            <div class="logout-button-wrapp">
                <a class="logout-button" href="/logout">Выйти</a>
            </div>
        </div>
        <h2 class="header_h">Список книг</h2>
    """

    if role == "admin":
        html += """
        <div class="create-button-wrapp">
            <a class="create-button" href="/create">Добавить книгу</a>
        </div>
        """

    for book in books:
        book_id, name, author, year, is_taken, is_taken_by_user = book
        html += f"""
            <div class="list_of_books">
                <span><b>ID-{book_id}. </b></span>
                <span>{name}, </span>
                <span>{author}, </span>
                <span>{year}</span>
        """

        if role == "admin" and not is_taken:
            html += f"""
                <a class="delete-button" href="/delete?id={book_id}">Удалить</a>
                <a class="change-button" href="/change?id={book_id}">Изменить</a>
            """

        if role == "reader" and not is_taken:
            html += f"""
                <a class="rent-button" href="/rent?id={book_id}">Взять в аренду</a>
            """

        if role == "reader" and is_taken_by_user:
            html += f"""
                <a class="return-button" href="/return?id={book_id}">Вернуть</a>
            """

        html += "</div>"

    html += """
    </body>
    </html>
    """
    return html
