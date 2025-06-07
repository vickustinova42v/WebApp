import sqlite3

def open_update_book_form(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, author, year FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    conn.close()

    if not book:
        return "<h1>Книга не найдена</h1>"

    name, author, year = book

    return f"""
    <html>
    <head>
        <title>Редактирование книги</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="form">
            <form class="form" action="/update" method="POST">
                <input type="hidden" name="id" value="{book_id}">

                <label for="name">Название книги:</label>
                <input class="input" type="text" id="name" name="name" value="{name}" required>

                <label for="author">Автор:</label>
                <input class="input" type="text" id="author" name="author" value="{author}" required>

                <label for="year">Год:</label>
                <input class="input" type="number" id="year" name="year" value="{year}" required>

                <button class="create-button" type="submit">Сохранить изменения</button>
            </form>
            <a class="return-button" href="/">На главную</a>
        </div>
    </body>
    </html>
    """

def save_updated_book_form(data):
    book_id = data.get('id', [''])[0]
    name = data.get('name', [''])[0]
    author = data.get('author', [''])[0]
    year = data.get('year', [''])[0]

    if book_id.isdigit() and name and author and year.isdigit():
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE books SET name = ?, author = ?, year = ? WHERE id = ?
        """, (name, author, int(year), int(book_id)))
        conn.commit()
        conn.close()
