import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.net.InetSocketAddress;

public class Main {
    public static void main(String[] args) throws IOException {
        // Создаём HTTP-сервер на порту 8000
        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);

        // Регистрируем обработчики
        server.createContext("/login", new LoginHandler());

        // Запускаем сервер (executor = null = по умолчанию)
        server.setExecutor(null);
        server.start();

        System.out.println("Сервер запущен на http://localhost:8000");
    }
}
