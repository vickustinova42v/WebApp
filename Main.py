import http.server
import socketserver
import urllib.parse
import os
import sqlite3
from http import cookies
import uuid

PORT = 8000
DB_NAME = "library.db"
SESSIONS = {}

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'reader'
        )
    ''')
    conn.commit()
    conn.close()

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/login.html'
        elif self.path == '/welcome':
            user = self.get_current_user()
            if user:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f"<h1>Привет, {user}!</h1>".encode())
            else:
                self.redirect('/login.html')
            return
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()
        data = urllib.parse.parse_qs(body)

        if self.path == '/register':
            username = data.get('username', [''])[0]
            password = data.get('password', [''])[0]
            if username and password:
                try:
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                    conn.commit()
                    conn.close()
                    self.redirect('/login.html')
                except sqlite3.IntegrityError:
                    self.send_html("<h1>Пользователь уже существует!</h1>")
            else:
                self.send_html("<h1>Некорректные данные</h1>")

        elif self.path == '/login':
            username = data.get('username', [''])[0]
            password = data.get('password', [''])[0]
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = c.fetchone()
            conn.close()
            if user:
                session_id = str(uuid.uuid4())
                SESSIONS[session_id] = username
                self.send_response(302)
                self.send_header('Location', '/welcome')
                self.send_header('Set-Cookie', f'session={session_id}')
                self.end_headers()
            else:
                self.send_html("<h1>Неверный логин или пароль</h1>")

    def get_current_user(self):
        if 'Cookie' in self.headers:
            cookie = cookies.SimpleCookie(self.headers['Cookie'])
            if 'session' in cookie:
                session_id = cookie['session'].value
                return SESSIONS.get(session_id)
        return None

    def send_html(self, html):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def redirect(self, location):
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()

if __name__ == "__main__":
    init_db()
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        httpd.serve_forever()