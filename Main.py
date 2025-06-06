from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import socketserver
import sqlite3
from Init import init_db, DB_NAME
from Get import get_books_html
from Delete import delete_books_html

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

        elif path == '/delete':
            book_id = query.get('id', [None])[0]
            if book_id:
                delete_html = delete_books_html(book_id)
                self.send_html(delete_html)
        else:
            super().do_GET()

if __name__ == "__main__":
    init_db()
    with MyTCPServer(("", PORT), Handler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        httpd.serve_forever()
