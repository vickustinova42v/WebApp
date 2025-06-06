from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import socketserver
import sqlite3
from Init import init_db, DB_NAME
from Read import get_books_html
from Delete import delete_books_html
from Create import open_new_book_form, save_new_book_form

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

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        if path == '/':
            books_html = get_books_html()
            self.send_html(books_html)
        
        elif path == "/style.css":
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('static/style.css', 'rb') as file:
                self.wfile.write(file.read())

        elif path == '/delete':
            book_id = query.get('id', [None])[0]
            if book_id:
                delete_html = delete_books_html(book_id)
                self.send_html(delete_html)

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
        else:
            self.send_html("<h1>Ошибка: неправильно заполнили форму.</h1>")

if __name__ == "__main__":
    init_db()
    with MyTCPServer(("", PORT), Handler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        httpd.serve_forever()
