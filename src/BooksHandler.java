import com.sun.net.httpserver.*;
import java.io.*;
import java.sql.*;
import java.util.*;

public class BooksHandler {

    private static Integer getUserIdFromRequest(HttpExchange exchange) {
        List<String> cookies = exchange.getRequestHeaders().get("Cookie");
        if (cookies != null) {
            for (String c : cookies) {
                for (String entry : c.split(";")) {
                    if (entry.trim().startsWith("sessionId=")) {
                        String sid = entry.trim().substring("sessionId=".length());
                        return SessionManager.getUserId(sid);
                    }
                }
            }
        }
        return null;
    }

    public static class BooksListHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            try (Connection conn = Database.getConnection();
                 PreparedStatement ps = conn.prepareStatement("SELECT * FROM books");
                 ResultSet rs = ps.executeQuery()) {

                StringBuilder response = new StringBuilder("[");
                while (rs.next()) {
                    if (response.length() > 1) response.append(",");
                    response.append(String.format(
                            "{\"id\":%d,\"title\":\"%s\",\"author\":\"%s\",\"isRented\":%b,\"rentedBy\":%s}",
                            rs.getInt("id"),
                            rs.getString("title"),
                            rs.getString("author"),
                            rs.getInt("is_rented") == 1,
                            rs.getObject("rented_by")
                    ));
                }
                response.append("]");

                byte[] bytes = response.toString().getBytes();
                exchange.getResponseHeaders().add("Content-Type", "application/json");
                exchange.sendResponseHeaders(200, bytes.length);
                exchange.getResponseBody().write(bytes);
                exchange.getResponseBody().close();
            } catch (SQLException e) {
                exchange.sendResponseHeaders(500, -1);
            }
        }
    }

    public static class AddBookHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            Integer uid = getUserIdFromRequest(exchange);
            if (uid == null) {
                exchange.sendResponseHeaders(401, -1);
                return;
            }

            BufferedReader reader = new BufferedReader(new InputStreamReader(exchange.getRequestBody()));
            String[] parts = reader.readLine().split("&");
            String title = parts[0].split("=")[1].replace("+", " ");
            String author = parts[1].split("=")[1].replace("+", " ");

            try (Connection conn = Database.getConnection()) {
                PreparedStatement ps = conn.prepareStatement("INSERT INTO books (title, author) VALUES (?, ?)");
                ps.setString(1, title);
                ps.setString(2, author);
                ps.executeUpdate();
                exchange.sendResponseHeaders(200, -1);
            } catch (SQLException e) {
                exchange.sendResponseHeaders(500, -1);
            }
        }
    }

    public static class EditBookHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            Integer uid = getUserIdFromRequest(exchange);
            if (uid == null) {
                exchange.sendResponseHeaders(401, -1);
                return;
            }

            BufferedReader reader = new BufferedReader(new InputStreamReader(exchange.getRequestBody()));
            String[] parts = reader.readLine().split("&");
            int id = Integer.parseInt(parts[0].split("=")[1]);
            String title = parts[1].split("=")[1].replace("+", " ");
            String author = parts[2].split("=")[1].replace("+", " ");

            try (Connection conn = Database.getConnection()) {
                PreparedStatement ps = conn.prepareStatement("UPDATE books SET title=?, author=? WHERE id=?");
                ps.setString(1, title);
                ps.setString(2, author);
                ps.setInt(3, id);
                ps.executeUpdate();
                exchange.sendResponseHeaders(200, -1);
            } catch (SQLException e) {
                exchange.sendResponseHeaders(500, -1);
            }
        }
    }

    public static class DeleteBookHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {

            Integer uid = getUserIdFromRequest(exchange);
            if (uid == null) {
                exchange.sendResponseHeaders(401, -1);
                return;
            }

            BufferedReader reader = new BufferedReader(new InputStreamReader(exchange.getRequestBody()));
            String[] parts = reader.readLine().split("=");
            int bookId = Integer.parseInt(parts[1]);

            try (Connection conn = Database.getConnection()) {
                PreparedStatement checkStmt = conn.prepareStatement("SELECT is_rented FROM books WHERE id = ?");
                checkStmt.setInt(1, bookId);
                ResultSet rs = checkStmt.executeQuery();

                if (rs.next() && rs.getInt("is_rented") == 1) {
                    exchange.sendResponseHeaders(400, -1); // Книга в аренде — удаление запрещено
                    return;
                }

                PreparedStatement ps = conn.prepareStatement("DELETE FROM books WHERE id = ?");
                ps.setInt(1, bookId);
                ps.executeUpdate();

                exchange.sendResponseHeaders(200, -1);
            } catch (SQLException e) {
                exchange.sendResponseHeaders(500, -1);
            }
        }
    }

    public static class RentBookHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            Integer uid = getUserIdFromRequest(exchange);
            if (uid == null) {
                exchange.sendResponseHeaders(401, -1);
                return;
            }

            BufferedReader reader = new BufferedReader(new InputStreamReader(exchange.getRequestBody()));
            int bookId = Integer.parseInt(reader.readLine().split("=")[1]);

            try (Connection conn = Database.getConnection()) {
                PreparedStatement ps = conn.prepareStatement(
                        "UPDATE books SET is_rented=1, rented_by=? WHERE id=? AND is_rented=0"
                );
                ps.setInt(1, uid);
                ps.setInt(2, bookId);
                int updated = ps.executeUpdate();
                exchange.sendResponseHeaders(updated > 0 ? 200 : 409, -1);
            } catch (SQLException e) {
                exchange.sendResponseHeaders(500, -1);
            }
        }
    }

    public static class ReturnBookHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            Integer uid = getUserIdFromRequest(exchange);
            if (uid == null) {
                exchange.sendResponseHeaders(401, -1);
                return;
            }

            BufferedReader reader = new BufferedReader(new InputStreamReader(exchange.getRequestBody()));
            int bookId = Integer.parseInt(reader.readLine().split("=")[1]);

            try (Connection conn = Database.getConnection()) {
                PreparedStatement ps = conn.prepareStatement(
                        "UPDATE books SET is_rented=0, rented_by=NULL WHERE id=? AND rented_by=?"
                );
                ps.setInt(1, bookId);
                ps.setInt(2, uid);
                int updated = ps.executeUpdate();
                exchange.sendResponseHeaders(updated > 0 ? 200 : 403, -1);
            } catch (SQLException e) {
                exchange.sendResponseHeaders(500, -1);
            }
        }
    }
}
