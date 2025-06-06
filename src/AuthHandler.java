import com.sun.net.httpserver.*;
import java.io.*;
import java.sql.*;

public class AuthHandler {

    public static class RegisterHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            if (!exchange.getRequestMethod().equalsIgnoreCase("POST")) {
                exchange.sendResponseHeaders(405, -1);
                return;
            }

            InputStream is = exchange.getRequestBody();
            BufferedReader reader = new BufferedReader(new InputStreamReader(is));
            String[] parts = reader.readLine().split("&");
            String username = parts[0].split("=")[1];
            String password = parts[1].split("=")[1];

            try (Connection conn = Database.getConnection()) {
                PreparedStatement ps = conn.prepareStatement("INSERT INTO users (username, password, role) VALUES (?, ?, ?)");
                ps.setString(1, username);
                ps.setString(2, password); // без хеширования — для простоты
                ps.setString(3, "user");
                ps.executeUpdate();
                exchange.sendResponseHeaders(200, -1);
            } catch (SQLException e) {
                exchange.sendResponseHeaders(409, -1); // username exists
            }
        }
    }

    public static class LoginHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            if (!exchange.getRequestMethod().equalsIgnoreCase("POST")) {
                exchange.sendResponseHeaders(405, -1);
                return;
            }

            BufferedReader reader = new BufferedReader(new InputStreamReader(exchange.getRequestBody()));
            String[] parts = reader.readLine().split("&");
            String username = parts[0].split("=")[1];
            String password = parts[1].split("=")[1];

            try (Connection conn = Database.getConnection()) {
                PreparedStatement ps = conn.prepareStatement("SELECT id, role FROM users WHERE username=? AND password=?");
                ps.setString(1, username);
                ps.setString(2, password);
                ResultSet rs = ps.executeQuery();

                if (rs.next()) {
                    int userId = rs.getInt("id");
                    String sessionId = SessionManager.createSession(userId);
                    Headers headers = exchange.getResponseHeaders();
                    headers.add("Set-Cookie", "sessionId=" + sessionId + "; Path=/");
                    exchange.sendResponseHeaders(200, 0);
                    OutputStream os = exchange.getResponseBody();
                    os.write(rs.getString("role").getBytes());
                    os.close();
                } else {
                    exchange.sendResponseHeaders(401, -1);
                }
            } catch (SQLException e) {
                exchange.sendResponseHeaders(500, -1);
            }
        }
    }

    public static class LogoutHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            Headers headers = exchange.getRequestHeaders();
            if (headers.containsKey("Cookie")) {
                String cookie = headers.getFirst("Cookie");
                String[] cookies = cookie.split(";");
                for (String c : cookies) {
                    if (c.trim().startsWith("sessionId=")) {
                        String sessionId = c.trim().substring("sessionId=".length());
                        SessionManager.removeSession(sessionId);
                    }
                }
            }
            exchange.sendResponseHeaders(200, -1);
        }
    }
}
