from http.server import HTTPServer, SimpleHTTPRequestHandler 
from urllib.parse import urlparse, parse_qs
import socketserver
import sqlite3
from Init import init_db, DB_NAME
from Read import get_books_html
from Delete import delete_books_html
from Create import open_new_book_form, save_new_book_form
from Utils import get_logged_in_user
from Auth import get_login_form, get_register_form
import os

class MyTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

PORT = 8000

Handler = SimpleHTTPRequestHandler

class Handler(Handler):
    def send_html(self, html_str):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_str.encode('utf-8'))
    
    def redirect(self, location):
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        user_id = get_logged_in_user(self)

        if path.startswith("/static/"):
            file_path = path.lstrip("/")
            if os.path.exists(file_path):
                self.send_response(200)
                if file_path.endswith(".css"):
                    self.send_header("Content-Type", "text/css")
                elif file_path.endswith(".js"):
                    self.send_header("Content-Type", "application/javascript")
                elif file_path.endswith(".png"):
                    self.send_header("Content-Type", "image/png")
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File Not Found")
            return

        if path == '/':
            books_html = get_books_html()
            self.send_html(books_html)

        elif path == '/login':
            login_html = get_login_form()
            self.send_html(login_html)
            
        elif path == '/register':
            register_html = get_register_form()
            self.send_html(register_html)

        elif path == '/delete':
            book_id = query.get('id', [None])[0]
            if book_id:
                delete_books_html(book_id)
                self.redirect('/')

        elif path == '/create':
            open_book_html = open_new_book_form()
            self.send_html(open_book_html)
        else:
            self.send_error(404)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/create':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = parse_qs(post_data)
            save_new_book_form(data)
            self.redirect('/')

        else:
            self.send_html("<h1>Ошибка: неправильно заполнили форму.</h1>")

if __name__ == "__main__":
    init_db()
    os.chdir('.')
    with MyTCPServer(("", PORT), Handler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        httpd.serve_forever()