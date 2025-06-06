import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;

public class Main {
    public static void main(String[] args) throws IOException {
        int port = 8000;
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);

        // Инициализация базы данных
        Database.init();

        // Роуты
        server.createContext("/register", new AuthHandler.RegisterHandler());
        server.createContext("/login", new AuthHandler.LoginHandler());
        server.createContext("/logout", new AuthHandler.LogoutHandler());

        server.createContext("/books", new BooksHandler.BooksListHandler());
        server.createContext("/books/add", new BooksHandler.AddBookHandler());
        server.createContext("/books/edit", new BooksHandler.EditBookHandler());
        server.createContext("/books/delete", new BooksHandler.DeleteBookHandler());
        server.createContext("/books/rent", new BooksHandler.RentBookHandler());
        server.createContext("/books/return", new BooksHandler.ReturnBookHandler());

        // Статические файлы (HTML, CSS, JS)
        server.createContext("/", new StaticFileHandler("public"));

        server.setExecutor(null); // Default
        server.start();

        System.out.println("📚 Server started on http://localhost:" + port);
    }
}
