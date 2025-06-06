import sqlite3

def open_new_book_form():
    return f"""
    <html>
    <head>
        <title>Создание новой книги</title>
    </head>
    <body>
        <form action="/create" method="POST">
            <label for="name">Название книги:</label><br>
            <input type="text" id="name" name="name" required><br><br>

            <label for="author">Автор:</label><br>
            <input type="text" id="author" name="author" required><br><br>

            <label for="year">Год:</label><br>
            <input type="number" id="year" name="year" required><br><br>

            <button type="submit">Добавить книгу</button>
        </form>
        <a href='/'>На главную</a>
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
