from http.server import HTTPServer, SimpleHTTPRequestHandler 
from urllib.parse import urlparse, parse_qs
import socketserver
import sqlite3
from Init import init_db, DB_NAME
from Read import get_books_html
from Delete import delete_books_html
from Update import open_update_book_form, save_updated_book_form
from Rent import rent_book, return_book
from Create import open_new_book_form, save_new_book_form
from Utils import get_logged_in_user
from Auth import get_login_form, get_register_form, register_user, authenticate_user, logout_user
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
            user_id = get_logged_in_user(self)
            if not user_id:
                self.redirect("/login")
                return
            books_html = get_books_html(user_id)
            self.send_html(books_html)

        elif path == '/login':
            user_id = get_logged_in_user(self)
            if user_id:
                self.redirect("/")
                return
            login_html = get_login_form()
            self.send_html(login_html)
            
        elif path == '/register':
            user_id = get_logged_in_user(self)
            if user_id:
                self.redirect("/")
                return
            register_html = get_register_form()
            self.send_html(register_html)

        elif path == '/delete':
            user_id = get_logged_in_user(self)
            if not user_id:
                self.redirect("/login")
                return
            book_id = query.get('id', [None])[0]
            if book_id:
                delete_books_html(book_id)
                self.redirect('/')

        elif path == '/create':
            user_id = get_logged_in_user(self)
            if not user_id:
                self.redirect("/login")
                return
            open_book_html = open_new_book_form()
            self.send_html(open_book_html)

        elif path == '/update':
            user_id = get_logged_in_user(self)
            if not user_id:
                self.redirect("/login")
                return
            book_id = query.get('id', [None])[0]
            if book_id:
                html = open_update_book_form(book_id)
                self.send_html(html)

        elif path == '/rent':
            user_id = get_logged_in_user(self)
            if not user_id:
                self.redirect("/login")
                return
            book_id = query.get('id', [None])[0]
            if book_id:
                rent_book(book_id, user_id)
                self.redirect('/')

        elif path == '/return':
            user_id = get_logged_in_user(self)
            if not user_id:
                self.redirect("/login")
                return
            book_id = query.get('id', [None])[0]
            if book_id:
                return_book(book_id, user_id)
                self.redirect('/')
        
        elif path == "/logout":
            user_id = get_logged_in_user(self)
            if not user_id:
                self.redirect("/login")
                return
            logout_user(self)

        else:
            self.send_error(404)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/create':
            user_id = get_logged_in_user(self)
            if not user_id:
                self.redirect("/login")
                return
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = parse_qs(post_data)
            save_new_book_form(data)
            self.redirect('/')
        
        elif path == '/update':
            user_id = get_logged_in_user(self)
            if not user_id:
                self.redirect("/login")
                return
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = parse_qs(post_data)
            save_updated_book_form(data)
            self.redirect('/')

        elif path == '/login':
            user_id = get_logged_in_user(self)
            if user_id:
                self.redirect("/")
                return
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = parse_qs(post_data)
            authenticate_user(data, self)
            
        elif path == '/register':
            user_id = get_logged_in_user(self)
            if user_id:
                self.redirect("/")
                return
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = parse_qs(post_data)
            register_user(data)
            self.redirect("/login")

        else:
            self.send_html("<h1>Ошибка: неправильно заполнили форму.</h1>")

if __name__ == "__main__":
    init_db()
    os.chdir('.')
    with MyTCPServer(("", PORT), Handler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        httpd.serve_forever()