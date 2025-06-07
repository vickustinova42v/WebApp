import sqlite3
import hashlib

def get_login_form():
    return """
    <html>
    <head>
        <title>Вход</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="form">
            <form class="form" method="POST" action="/login">
                <label for="username">Имя пользователя:</label>
                <input class="input" type="text" id="username" name="username" required>

                <label for="password">Пароль:</label>
                <input class="input" type="password" id="password" name="password" required>

                <button class="create-button" type="submit">Войти</button>
            </form>
            <a class="return-button" href="/register">Нет аккаунта? Зарегистрироваться</a>
        </div>
    </body>
    </html>
    """

def get_register_form():
    return """
    <html>
    <head>
        <title>Регистрация</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="form">
            <form class="form" method="POST" action="/register">
                <label for="username">Имя пользователя:</label>
                <input class="input" type="text" id="username" name="username" required>

                <label for="password">Пароль:</label>
                <input class="input" type="password" id="password" name="password" required>

                <button class="create-button" type="submit">Зарегистрироваться</button>
            </form>
            <a class="return-button" href="/login">Уже есть аккаунт? Войти</a>
        </div>
    </body>
    </html>
    """

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register_user(data):
    username = data.get('username', [''])[0]
    password = data.get('password', [''])[0]

    if username and password:
        hashed_password = hash_password(password)
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()

def authenticate_user(data, handler):
    username = data.get('username', [''])[0]
    password = data.get('password', [''])[0]

    if username and password:
        hashed_password = hash_password(password)
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = cursor.fetchone()
        conn.close()

        if user:
            user_id = user[0]
            handler.send_response(302)
            handler.send_header('Set-Cookie', f'user_id={user_id}; Path=/')
            handler.send_header('Location', '/')
            handler.end_headers()
        else:
            error_html = f"""
            <html>
            <head>
                <title>Вход</title>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <body>
                <div class="header_logout">
                    <h2>Неверный логин или пароль</h2>
                    <a class="logout-button"href="/login">Вернуться</a>
                </div>
            </body>
            </html>
            """
            handler.send_response(200)
            handler.send_header("Content-type", "text/html; charset=utf-8")
            handler.end_headers()
            handler.wfile.write(error_html.encode("utf-8"))

def logout_user(handler):
    handler.send_response(302)
    handler.send_header('Set-Cookie', 'user_id=; Path=/; Max-Age=0')
    handler.send_header('Location', '/login')
    handler.end_headers()
