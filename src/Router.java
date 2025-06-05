import com.sun.net.httpserver.HttpServer;

public class Router {
    public static void setupRoutes(HttpServer server) {
        server.createContext("/login", new LoginHandler());
    }
}
