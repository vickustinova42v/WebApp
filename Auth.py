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

def register_user(data):
    username = data.get('username', [''])[0]
    password = data.get('password', [''])[0]

    if username and password:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        conn.close()
        return True
    return False

def authenticate_user(data):
    username = data.get('username', [''])[0]
    password = data.get('password', [''])[0]

    if username and password:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password_hash))
        user = cursor.fetchone()
        conn.close()
        if user:
            return user[0]
    return None
