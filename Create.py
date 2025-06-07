import sqlite3

def open_new_book_form():
    return f"""
    <html>
    <head>
        <title>Создание новой книги</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="form">
            <form class="form" action="/create" method="POST">
                <label for="name">Название книги:</label>
                <input class="input" type="text" id="name" name="name" required>

                <label for="author">Автор:</label>
                <input class="input" type="text" id="author" name="author" required>

                <label for="year">Год:</label>
                <input class="input" type="number" id="year" name="year" required>

                <button class="create-button" type="submit">Добавить книгу</button>
            </form>
            <a class="return-button" href='/'>На главную</a>
        </div>
    </body>
    </html>
    """

def save_new_book_form(data):
    name = data.get('name', [''])[0]
    author = data.get('author', [''])[0]
    year = data.get('year', [''])[0]

    if name and author and year.isdigit():
        year = int(year)
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (name, author, year) VALUES (?, ?, ?)", (name, author, year))
        conn.commit()
        conn.close()
