def open_new_book_form():
    return f"""
    <html>
    <head>
        <title>1</title>
        <link rel="stylesheet" href="/style.css">
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

def save_new_book_form():
    return f"""
    <html>
    <head>
        <title>1</title>
        <link rel="stylesheet" href="/style.css">
    </head>
    <body>
        <h1>1</h1>
        <a href='/'>На главную</a>
    </body>
    </html>
    """
