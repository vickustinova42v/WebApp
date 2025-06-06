import http.server
import socketserver
import sqlite3
from Init import init_db, DB_NAME
from Get import get_books_html

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def send_html(self, html_str):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_str.encode('utf-8'))

    def do_GET(self):
        if self.path == '/':
            books_html = get_books_html()
            self.send_html(books_html)  # используем метод
        else:
            super().do_GET()

if __name__ == "__main__":
    init_db()
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        httpd.serve_forever()
