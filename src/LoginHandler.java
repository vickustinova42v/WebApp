import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.sql.*;
import java.util.Map;

public class LoginHandler implements HttpHandler {
    private static final String DB_PATH = "jdbc:sqlite:library.db";

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        if ("POST".equalsIgnoreCase(exchange.getRequestMethod())) {
            handlePost(exchange);
        } else {
            handleGet(exchange);
        }
    }

    private void handleGet(HttpExchange exchange) throws IOException {
        Map<String, String> q = QueryParser.parse(exchange.getRequestURI().getQuery());
        String html = new String(Files.readAllBytes(Paths.get("templates/login.html")), StandardCharsets.UTF_8);
        html = Utils.renderTemplate(html, q);

        exchange.getResponseHeaders().add("Content-Type", "text/html; charset=UTF-8");
        exchange.sendResponseHeaders(200, html.getBytes().length);

        try (OutputStream os = exchange.getResponseBody()) {
            os.write(html.getBytes());
        }
    }

    private void handlePost(HttpExchange exchange) throws IOException {
        Map<String, String> formData = parseFormData(exchange);
        String username = formData.get("username");
        String password = formData.get("password");

        String role = getUserRole(username, password);

        if (role != null) {
            // Успешный вход
            // В будущем можно поставить куку с ролью или именем пользователя
            exchange.getResponseHeaders().add("Location", "/catalog");
            exchange.sendResponseHeaders(HttpURLConnection.HTTP_SEE_OTHER, -1);
        } else {
            // Ошибка
            String error = URLEncoder.encode("Неверный логин или пароль", "UTF-8");
            exchange.getResponseHeaders().add("Location", "/login?error=" + error + "&user=" + URLEncoder.encode(username, "UTF-8"));
            exchange.sendResponseHeaders(HttpURLConnection.HTTP_SEE_OTHER, -1);
        }
        exchange.close();
    }


    private String getUserRole(String username, String password) {
        try (Connection conn = DriverManager.getConnection(DB_PATH)) {
            String sql = "SELECT role FROM users WHERE username = ? AND password = ?";
            try (PreparedStatement stmt = conn.prepareStatement(sql)) {
                stmt.setString(1, username);
                stmt.setString(2, password);
                try (ResultSet rs = stmt.executeQuery()) {
                    if (rs.next()) {
                        return rs.getString("role"); // "admin" или "user"
                    }
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    private Map<String, String> parseFormData(HttpExchange exchange) throws IOException {
        InputStreamReader isr = new InputStreamReader(exchange.getRequestBody(), StandardCharsets.UTF_8);
        BufferedReader br = new BufferedReader(isr);
        String form = br.readLine();

        return QueryParser.parse(form);
    }
}
